"""
Módulo de monitoramento para a aplicação Python da Rinha de Backend 2025
"""

import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from fastapi.responses import PlainTextResponse

# Métricas Prometheus
PAYMENT_REQUESTS = Counter(
    'payment_requests_total',
    'Total number of payment requests',
    ['processor', 'status']
)

PAYMENT_DURATION = Histogram(
    'payment_duration_seconds',
    'Payment processing duration in seconds',
    ['processor']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)

HEALTH_CHECK_FAILURES = Counter(
    'health_check_failures_total',
    'Total number of health check failures',
    ['processor']
)

class MetricsMiddleware:
    """Middleware para coletar métricas"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            
            # Incrementar conexões ativas
            ACTIVE_CONNECTIONS.inc()
            
            # Processar request
            await self.app(scope, receive, send)
            
            # Decrementar conexões ativas
            ACTIVE_CONNECTIONS.dec()
            
            # Registrar duração se for endpoint de pagamento
            if scope["path"] == "/payments" and scope["method"] == "POST":
                duration = time.time() - start_time
                # Nota: processor seria extraído do response, mas aqui simplificamos
                PAYMENT_DURATION.labels(processor="unknown").observe(duration)

def get_metrics():
    """Retorna métricas no formato Prometheus"""
    return generate_latest()

def record_payment_request(processor: str, status: str):
    """Registra uma requisição de pagamento"""
    PAYMENT_REQUESTS.labels(processor=processor, status=status).inc()

def record_payment_duration(processor: str, duration: float):
    """Registra duração de processamento de pagamento"""
    PAYMENT_DURATION.labels(processor=processor).observe(duration)

def record_health_check_failure(processor: str):
    """Registra falha em health check"""
    HEALTH_CHECK_FAILURES.labels(processor=processor).inc()

# Endpoint para métricas Prometheus
async def metrics_endpoint():
    """Endpoint para métricas Prometheus"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    ) 