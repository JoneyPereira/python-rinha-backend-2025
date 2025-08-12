"""
Módulo de otimizações para a aplicação Python da Rinha de Backend 2025
"""

import asyncio
import time
from typing import Dict, Optional
from functools import lru_cache
import httpx

class PerformanceOptimizer:
    """Classe para otimizações de performance"""
    
    def __init__(self):
        self.connection_pool = {}
        self.health_cache = {}
        self.last_health_check = {}
        self.circuit_breaker = {}
    
    async def get_optimized_client(self, base_url: str) -> httpx.AsyncClient:
        """Retorna um cliente HTTP otimizado com connection pooling"""
        if base_url not in self.connection_pool:
            limits = httpx.Limits(
                max_keepalive_connections=20,
                max_connections=100,
                keepalive_expiry=30.0
            )
            
            self.connection_pool[base_url] = httpx.AsyncClient(
                timeout=httpx.Timeout(10.0),
                limits=limits,
                http2=True
            )
        
        return self.connection_pool[base_url]
    
    def is_circuit_open(self, service_url: str) -> bool:
        """Verifica se o circuit breaker está aberto para um serviço"""
        if service_url not in self.circuit_breaker:
            return False
        
        last_failure = self.circuit_breaker[service_url].get('last_failure', 0)
        failure_count = self.circuit_breaker[service_url].get('failure_count', 0)
        current_time = time.time()
        
        # Circuit breaker abre após 5 falhas consecutivas
        if failure_count >= 5:
            # Reset após 30 segundos
            if current_time - last_failure > 30:
                self.circuit_breaker[service_url] = {
                    'last_failure': 0,
                    'failure_count': 0
                }
                return False
            return True
        
        return False
    
    def record_failure(self, service_url: str):
        """Registra uma falha para o circuit breaker"""
        if service_url not in self.circuit_breaker:
            self.circuit_breaker[service_url] = {
                'last_failure': time.time(),
                'failure_count': 1
            }
        else:
            self.circuit_breaker[service_url]['last_failure'] = time.time()
            self.circuit_breaker[service_url]['failure_count'] += 1
    
    def record_success(self, service_url: str):
        """Registra um sucesso para o circuit breaker"""
        if service_url in self.circuit_breaker:
            self.circuit_breaker[service_url]['failure_count'] = 0
    
    @lru_cache(maxsize=128)
    def get_cached_health(self, service_url: str, timestamp: int) -> Dict:
        """Cache para health checks com TTL de 5 segundos"""
        return self.health_cache.get(service_url, {})
    
    async def optimized_health_check(self, service_url: str) -> Dict:
        """Health check otimizado com cache e circuit breaker"""
        current_time = int(time.time())
        
        # Verificar circuit breaker
        if self.is_circuit_open(service_url):
            return {"status": "unhealthy", "reason": "circuit_breaker_open"}
        
        # Verificar cache (TTL de 5 segundos)
        if service_url in self.last_health_check:
            if current_time - self.last_health_check[service_url] < 5:
                return self.get_cached_health(service_url, current_time)
        
        try:
            client = await self.get_optimized_client(service_url)
            response = await client.get(f"{service_url}/payments/service-health")
            
            if response.status_code == 200:
                health_data = response.json()
                self.health_cache[service_url] = health_data
                self.last_health_check[service_url] = current_time
                self.record_success(service_url)
                return health_data
            else:
                self.record_failure(service_url)
                return {"status": "unhealthy", "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            self.record_failure(service_url)
            return {"status": "unhealthy", "error": str(e)}
    
    async def close_connections(self):
        """Fecha todas as conexões HTTP"""
        for client in self.connection_pool.values():
            await client.aclose()

class DatabaseOptimizer:
    """Otimizações para banco de dados"""
    
    @staticmethod
    def get_optimized_engine_config() -> Dict:
        """Retorna configuração otimizada para SQLAlchemy"""
        return {
            "pool_size": 20,
            "max_overflow": 30,
            "pool_pre_ping": True,
            "pool_recycle": 3600,
            "echo": False
        }
    
    @staticmethod
    def get_optimized_session_config() -> Dict:
        """Retorna configuração otimizada para sessões"""
        return {
            "autoflush": False,
            "autocommit": False,
            "expire_on_commit": False
        }

class CacheOptimizer:
    """Otimizações para cache Redis"""
    
    @staticmethod
    def get_redis_config() -> Dict:
        """Retorna configuração otimizada para Redis"""
        return {
            "decode_responses": True,
            "socket_keepalive": True,
            "socket_keepalive_options": {},
            "retry_on_timeout": True,
            "health_check_interval": 30
        }
    
    @staticmethod
    async def batch_cache_operations(redis_client, operations: list):
        """Executa operações de cache em lote"""
        if not operations:
            return
        
        pipe = redis_client.pipeline()
        for operation in operations:
            if operation['type'] == 'hset':
                pipe.hset(operation['key'], operation['field'], operation['value'])
            elif operation['type'] == 'expire':
                pipe.expire(operation['key'], operation['ttl'])
        
        await pipe.execute()

# Instância global do otimizador
performance_optimizer = PerformanceOptimizer() 