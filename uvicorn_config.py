"""
Configuração otimizada do Uvicorn para a aplicação Python da Rinha de Backend 2025
"""

import uvicorn
from app import app

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=9999,
        workers=1,  # Usar 1 worker por container (load balancer distribui)
        loop="uvloop",  # Loop de eventos mais rápido
        http="httptools",  # Parser HTTP mais rápido
        access_log=False,  # Desabilitar logs de acesso para performance
        log_level="info",
        timeout_keep_alive=30,
        timeout_graceful_shutdown=30,
        limit_concurrency=1000,  # Limite de conexões simultâneas
        limit_max_requests=10000,  # Reiniciar worker após N requests
        reload=False,  # Desabilitar reload em produção
    ) 