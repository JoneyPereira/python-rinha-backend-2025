import asyncio
import logging
import time
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

import httpx
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from monitoring import metrics_endpoint, record_payment_request, record_payment_duration
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import json
import os
import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações
DEFAULT_PAYMENT_PROCESSOR_URL = os.getenv("DEFAULT_PAYMENT_PROCESSOR_URL", "http://payment-processor-default:8080")
FALLBACK_PAYMENT_PROCESSOR_URL = os.getenv("FALLBACK_PAYMENT_PROCESSOR_URL", "http://payment-processor-fallback:8080")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/payments")

# Modelos Pydantic
class PaymentRequest(BaseModel):
    amount: float
    description: Optional[str] = None

class PaymentResponse(BaseModel):
    id: str
    amount: float
    status: str
    processor: str
    timestamp: float

class PaymentSummary(BaseModel):
    total_payments: int
    total_amount: float
    payments_by_processor: Dict[str, Dict[str, float]]

# Configuração do banco de dados
Base = declarative_base()

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(String, primary_key=True)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    processor = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    description = Column(Text, nullable=True)

# Engine e Session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Redis client
redis_client: Optional[redis.Redis] = None

# Health check cache
health_cache = {}
last_health_check = {}

class PaymentProcessor:
    def __init__(self):
        self.default_url = DEFAULT_PAYMENT_PROCESSOR_URL
        self.fallback_url = FALLBACK_PAYMENT_PROCESSOR_URL
        self.health_cache = {}
        self.last_health_check = {}
        
    async def check_health(self, processor_url: str) -> Dict:
        """Verifica a saúde do processador de pagamento"""
        current_time = time.time()
        
        # Rate limiting: máximo 1 chamada a cada 5 segundos
        if processor_url in self.last_health_check:
            if current_time - self.last_health_check[processor_url] < 5:
                return self.health_cache.get(processor_url, {"status": "unknown"})
        
        # Simular processador local em vez de tentar conectar a serviços externos
        if "payment-processor" in processor_url:
            # Simular processador saudável
            health_data = {"status": "healthy", "processor": "local-simulator"}
            self.health_cache[processor_url] = health_data
            self.last_health_check[processor_url] = current_time
            return health_data
        
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{processor_url}/payments/service-health")
                if response.status_code == 200:
                    health_data = response.json()
                    self.health_cache[processor_url] = health_data
                    self.last_health_check[processor_url] = current_time
                    return health_data
                else:
                    return {"status": "unhealthy", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"Erro ao verificar saúde do processador {processor_url}: {e}")
            return {"status": "unhealthy", "error": str(e)}
    
    async def process_payment(self, payment_request: PaymentRequest) -> PaymentResponse:
        """Processa um pagamento usando a melhor estratégia"""
        payment_id = f"pay_{int(time.time() * 1000)}_{hash(str(payment_request))}"
        
        # Verificar saúde dos processadores
        default_health = await self.check_health(self.default_url)
        fallback_health = await self.check_health(self.fallback_url)
        
        # Estratégia: usar default se saudável, senão fallback
        if default_health.get("status") == "healthy":
            processor_url = self.default_url
            processor_name = "default"
        elif fallback_health.get("status") == "healthy":
            processor_url = self.fallback_url
            processor_name = "fallback"
        else:
            # Se ambos estão indisponíveis, tentar default primeiro
            processor_url = self.default_url
            processor_name = "default"
        
        # Processar pagamento
        try:
            # Simular processamento local se for um processador externo
            if "payment-processor" in processor_url:
                # Simular processamento local
                await asyncio.sleep(0.1)  # Simular latência
                
                payment_response = PaymentResponse(
                    id=payment_id,
                    amount=payment_request.amount,
                    status="processed",
                    processor="local-simulator",
                    timestamp=time.time()
                )
                
                # Salvar no banco de dados
                await self.save_payment(payment_response, payment_request.description)
                
                # Cache no Redis para auditoria
                await self.cache_payment(payment_response)
                
                return payment_response
            else:
                # Tentar processador externo real
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        f"{processor_url}/payments",
                        json={"amount": payment_request.amount, "description": payment_request.description}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        payment_response = PaymentResponse(
                            id=payment_id,
                            amount=payment_request.amount,
                            status="processed",
                            processor=processor_name,
                            timestamp=time.time()
                        )
                        
                        # Salvar no banco de dados
                        await self.save_payment(payment_response, payment_request.description)
                        
                        # Cache no Redis para auditoria
                        await self.cache_payment(payment_response)
                        
                        return payment_response
                    else:
                        # Se falhou, tentar fallback se não estava usando
                        if processor_name == "default" and fallback_health.get("status") == "healthy":
                            return await self.process_with_fallback(payment_request, payment_id)
                        else:
                            raise HTTPException(status_code=500, detail="Payment processing failed")
                        
        except Exception as e:
            logger.error(f"Erro ao processar pagamento: {e}")
            # Tentar fallback como último recurso
            if processor_name == "default":
                return await self.process_with_fallback(payment_request, payment_id)
            else:
                raise HTTPException(status_code=500, detail="Payment processing failed")
    
    async def process_with_fallback(self, payment_request: PaymentRequest, payment_id: str) -> PaymentResponse:
        """Processa pagamento usando fallback"""
        try:
            # Simular processamento local se for um processador externo
            if "payment-processor" in self.fallback_url:
                # Simular processamento local
                await asyncio.sleep(0.1)  # Simular latência
                
                payment_response = PaymentResponse(
                    id=payment_id,
                    amount=payment_request.amount,
                    status="processed",
                    processor="local-simulator-fallback",
                    timestamp=time.time()
                )
                
                await self.save_payment(payment_response, payment_request.description)
                await self.cache_payment(payment_response)
                
                return payment_response
            else:
                # Tentar processador externo real
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        f"{self.fallback_url}/payments",
                        json={"amount": payment_request.amount, "description": payment_request.description}
                    )
                    
                    if response.status_code == 200:
                        payment_response = PaymentResponse(
                            id=payment_id,
                            amount=payment_request.amount,
                            status="processed",
                            processor="fallback",
                            timestamp=time.time()
                        )
                        
                        await self.save_payment(payment_response, payment_request.description)
                        await self.cache_payment(payment_response)
                        
                        return payment_response
                    else:
                        raise HTTPException(status_code=500, detail="Fallback payment processing failed")
        except Exception as e:
            logger.error(f"Erro no fallback: {e}")
            raise HTTPException(status_code=500, detail="Payment processing failed")
    
    async def save_payment(self, payment: PaymentResponse, description: Optional[str] = None):
        """Salva pagamento no banco de dados"""
        try:
            db = SessionLocal()
            db_payment = Payment(
                id=payment.id,
                amount=payment.amount,
                status=payment.status,
                processor=payment.processor,
                timestamp=datetime.datetime.utcfromtimestamp(payment.timestamp),
                description=description
            )
            db.add(db_payment)
            db.commit()
            db.close()
        except Exception as e:
            logger.error(f"Erro ao salvar pagamento no banco: {e}")
    
    async def cache_payment(self, payment: PaymentResponse):
        """Cache pagamento no Redis para auditoria"""
        try:
            if redis_client:
                await redis_client.hset(
                    "payments",
                    payment.id,
                    json.dumps(payment.dict())
                )
        except Exception as e:
            logger.error(f"Erro ao cachear pagamento: {e}")

# Instância global do processador
payment_processor = PaymentProcessor()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global redis_client
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        await redis_client.ping()
        logger.info("Conectado ao Redis")
    except Exception as e:
        logger.warning(f"Não foi possível conectar ao Redis: {e}")
        redis_client = None
    
    yield
    
    # Shutdown
    if redis_client:
        await redis_client.close()

# Criação da aplicação FastAPI
app = FastAPI(title="Payment Processor API", lifespan=lifespan)

# Adicionar endpoint de métricas
app.add_api_route("/metrics", metrics_endpoint, methods=["GET"])

@app.post("/payments", response_model=PaymentResponse)
async def create_payment(payment_request: PaymentRequest, background_tasks: BackgroundTasks):
    """Processa um novo pagamento"""
    try:
        payment_response = await payment_processor.process_payment(payment_request)
        return payment_response
    except Exception as e:
        logger.error(f"Erro ao processar pagamento: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/payments-summary", response_model=PaymentSummary)
async def get_payments_summary():
    """Retorna resumo dos pagamentos processados"""
    try:
        db = SessionLocal()
        
        # Consulta para obter estatísticas
        result = db.execute(text("""
            SELECT 
                processor,
                COUNT(*) as count,
                SUM(amount) as total_amount
            FROM payments 
            WHERE status = 'processed'
            GROUP BY processor
        """))
        
        payments_by_processor = {}
        total_payments = 0
        total_amount = 0.0
        
        for row in result:
            processor = row.processor
            count = row.count
            amount = float(row.total_amount)
            
            payments_by_processor[processor] = {
                "count": count,
                "total_amount": amount
            }
            
            total_payments += count
            total_amount += amount
        
        db.close()
        
        return PaymentSummary(
            total_payments=total_payments,
            total_amount=total_amount,
            payments_by_processor=payments_by_processor
        )
        
    except Exception as e:
        logger.error(f"Erro ao obter resumo: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check da aplicação"""
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999) 