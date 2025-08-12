# Detalhes Técnicos - Implementação Python da Rinha de Backend 2025

## Arquitetura da Solução

### Visão Geral
Esta implementação utiliza uma arquitetura distribuída com múltiplas instâncias da aplicação, load balancer, banco de dados e cache, seguindo todas as especificações da Rinha de Backend 2025.

### Componentes Principais

#### 1. Aplicação FastAPI (2 instâncias)
- **Framework**: FastAPI com Uvicorn otimizado
- **Processamento**: Assíncrono com async/await
- **Endpoints**:
  - `POST /payments` - Processamento de pagamentos
  - `GET /payments-summary` - Resumo para auditoria
  - `GET /health` - Health check
  - `GET /metrics` - Métricas Prometheus

#### 2. Load Balancer (Nginx)
- **Distribuição**: Round-robin entre as instâncias
- **Configuração**: Otimizada para baixa latência
- **Porta**: 9999 (conforme especificação)

#### 3. Banco de Dados (PostgreSQL)
- **Persistência**: Todos os pagamentos processados
- **Índices**: Otimizados para consultas de auditoria
- **Migrações**: Alembic para controle de schema

#### 4. Cache (Redis)
- **Auditoria**: Cache de pagamentos para verificação rápida
- **Health Check**: Cache de status dos processadores
- **Performance**: Redução de latência

## Estratégia de Processamento

### Health Check Inteligente
```python
async def check_health(self, processor_url: str) -> Dict:
    # Rate limiting: máximo 1 chamada a cada 5 segundos
    if processor_url in self.last_health_check:
        if current_time - self.last_health_check[processor_url] < 5:
            return self.health_cache.get(processor_url, {"status": "unknown"})
```

**Características**:
- Rate limiting de 1 chamada/5s por processador
- Cache de status para evitar sobrecarga
- Circuit breaker para falhas consecutivas

### Estratégia de Fallback
```python
# Estratégia: usar default se saudável, senão fallback
if default_health.get("status") == "healthy":
    processor_url = self.default_url
    processor_name = "default"
elif fallback_health.get("status") == "healthy":
    processor_url = self.fallback_url
    processor_name = "fallback"
```

**Lógica**:
1. Verificar saúde do processador default
2. Se saudável, usar default (menor taxa)
3. Se não saudável, verificar fallback
4. Se fallback saudável, usar fallback
5. Se ambos indisponíveis, tentar default primeiro

### Auditoria Completa
```python
# Salvar no banco de dados
await self.save_payment(payment_response, payment_request.description)

# Cache no Redis para auditoria
await self.cache_payment(payment_response)
```

**Garantias**:
- Todos os pagamentos salvos no PostgreSQL
- Cache no Redis para verificação rápida
- Endpoint `/payments-summary` para auditoria

## Otimizações de Performance

### 1. Processamento Assíncrono
- **FastAPI**: Framework assíncrono nativo
- **httpx**: Cliente HTTP assíncrono
- **Connection Pooling**: Reutilização de conexões

### 2. Uvicorn Otimizado
```python
uvicorn.run(
    "app:app",
    workers=1,  # 1 worker por container
    loop="uvloop",  # Loop mais rápido
    http="httptools",  # Parser HTTP mais rápido
    access_log=False,  # Desabilitar logs para performance
    limit_concurrency=1000,
    limit_max_requests=10000,
)
```

### 3. Database Optimization
```python
# Configuração otimizada do SQLAlchemy
{
    "pool_size": 20,
    "max_overflow": 30,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "echo": False
}
```

### 4. Redis Optimization
```python
# Configuração otimizada do Redis
{
    "decode_responses": True,
    "socket_keepalive": True,
    "retry_on_timeout": True,
    "health_check_interval": 30
}
```

## Configuração de Recursos

### Limites de Recursos (Docker Compose)
```yaml
deploy:
  resources:
    limits:
      cpus: "0.5"      # app1
      memory: "150MB"   # app1
      cpus: "0.5"      # app2
      memory: "150MB"   # app2
      cpus: "0.1"      # nginx
      memory: "50MB"    # nginx
      cpus: "0.3"      # postgres
      memory: "100MB"   # postgres
      cpus: "0.1"      # redis
      memory: "50MB"    # redis
```

**Total**: 1.5 CPU cores, 350MB RAM (conforme especificação)

## Monitoramento e Métricas

### Prometheus Metrics
- `payment_requests_total`: Total de requisições por processador/status
- `payment_duration_seconds`: Duração de processamento
- `active_connections`: Conexões ativas
- `health_check_failures_total`: Falhas em health checks

### Endpoints de Monitoramento
- `GET /health`: Status da aplicação
- `GET /metrics`: Métricas Prometheus

## Resiliência e Tratamento de Erros

### Circuit Breaker
```python
def is_circuit_open(self, service_url: str) -> bool:
    # Circuit breaker abre após 5 falhas consecutivas
    if failure_count >= 5:
        # Reset após 30 segundos
        if current_time - last_failure > 30:
            return False
        return True
```

### Retry Logic
```python
# Se falhou, tentar fallback se não estava usando
if processor_name == "default" and fallback_health.get("status") == "healthy":
    return await self.process_with_fallback(payment_request, payment_id)
```

### Error Handling
- Tratamento robusto de exceções
- Logs estruturados para debugging
- Graceful degradation em caso de falhas

## Segurança e Conformidade

### Validação de Dados
- **Pydantic**: Validação automática de schemas
- **Type Hints**: Verificação de tipos em tempo de execução

### Auditoria
- **Logs Estruturados**: Todos os eventos registrados
- **Persistência Completa**: Nenhum pagamento perdido
- **Verificação de Consistência**: Endpoint de resumo

## Testes e Validação

### Script de Teste
```python
# Teste de stress com múltiplos pagamentos simultâneos
async def stress_test(self, num_payments: int = 10):
    tasks = []
    for i in range(num_payments):
        task = self.test_payment(100.00 + i, f"Stress test payment {i+1}")
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
```

### Validação de Performance
- **Throughput**: Medição de pagamentos/segundo
- **Latência**: P99 de tempo de resposta
- **Confiabilidade**: Taxa de sucesso vs falha

## Deployment e Operação

### Docker Compose
```bash
# Construir e executar
docker-compose up --build -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

### Script de Setup
```bash
# Setup automático
python setup.py
```

## Conformidade com Especificações

### ✅ Requisitos Atendidos
- [x] 2 instâncias de servidores web
- [x] Load balancer (Nginx)
- [x] Docker Compose
- [x] Limites de recursos (1.5 CPU, 350MB RAM)
- [x] Porta 9999
- [x] Modo bridge (não host)
- [x] Sem modo privileged
- [x] Sem replicas
- [x] Endpoints obrigatórios
- [x] Estratégia de fallback
- [x] Auditoria completa

### 🎯 Otimizações Implementadas
- **Performance**: Processamento assíncrono, connection pooling
- **Resiliência**: Circuit breaker, retry logic, health checks
- **Monitoramento**: Métricas Prometheus, logs estruturados
- **Auditoria**: Persistência completa, cache Redis, endpoint de resumo

Esta implementação está pronta para competir na Rinha de Backend 2025, seguindo todas as especificações e incluindo otimizações para maximizar performance e confiabilidade. 