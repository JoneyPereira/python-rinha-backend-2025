# Rinha de Backend 2025 - Implementação Python

Esta é uma implementação do desafio da Rinha de Backend 2025 usando Python com FastAPI.

## Tecnologias Utilizadas

- **Linguagem**: Python 3.11
- **Framework Web**: FastAPI
- **Banco de Dados**: PostgreSQL
- **Cache**: Redis
- **Load Balancer**: Nginx
- **Containerização**: Docker & Docker Compose
- **ORM**: SQLAlchemy
- **HTTP Client**: httpx (assíncrono)

## Arquitetura

### Componentes

1. **2 Instâncias da Aplicação** (app1, app2)
   - FastAPI com endpoints `/payments` e `/payments-summary`
   - Processamento assíncrono de pagamentos
   - Estratégia de fallback inteligente

2. **Load Balancer** (nginx)
   - Distribuição de carga entre as instâncias
   - Configuração otimizada para performance

3. **Banco de Dados** (postgres)
   - PostgreSQL para persistência de dados
   - Índices otimizados para consultas

4. **Cache** (redis)
   - Redis para cache de auditoria
   - Melhoria de performance

### Estratégia de Processamento

1. **Health Check Inteligente**
   - Verificação de saúde dos processadores com rate limiting (1 chamada/5s)
   - Cache de status para evitar sobrecarga

2. **Fallback Automático**
   - Uso do processador default quando saudável
   - Fallback automático para processador de backup
   - Retry automático em caso de falha

3. **Auditoria Completa**
   - Registro de todos os pagamentos no banco
   - Cache no Redis para auditoria
   - Endpoint `/payments-summary` para verificação

## Endpoints

### POST /payments
Processa um novo pagamento.

**Request:**
```json
{
  "amount": 100.00,
  "description": "Pagamento teste"
}
```

**Response:**
```json
{
  "id": "pay_1234567890_12345",
  "amount": 100.00,
  "status": "processed",
  "processor": "default",
  "timestamp": 1640995200.0
}
```

### GET /payments-summary
Retorna resumo dos pagamentos processados.

**Response:**
```json
{
  "total_payments": 150,
  "total_amount": 15000.00,
  "payments_by_processor": {
    "default": {
      "count": 120,
      "total_amount": 12000.00
    },
    "fallback": {
      "count": 30,
      "total_amount": 3000.00
    }
  }
}
```

### GET /health
Health check da aplicação.

## Configuração de Recursos

- **Total CPU**: 1.5 cores (0.5 + 0.5 + 0.1 + 0.3 + 0.1)
- **Total Memória**: 350MB (150MB + 150MB + 50MB + 100MB + 50MB)
- **Porta**: 9999 (conforme especificação)

## Execução

### Opção 1: Setup Automatizado (Recomendado)

```bash
# Instalar dependências necessárias (se necessário)
python install_deps.py

# Setup completo automatizado
python setup.py

# Ou versão simplificada (sem dependências extras)
python setup_simple.py
```

### Opção 2: Docker Compose Manual

```bash
# Construir e executar
docker-compose up --build

# Executar em background
docker-compose up -d --build
```

### Opção 3: Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python app.py
```

### Testes

```bash
# Teste de pagamento
curl -X POST http://localhost:9999/payments \
  -H "Content-Type: application/json" \
  -d '{"amount": 100.00, "description": "Teste"}'

# Teste de resumo
curl http://localhost:9999/payments-summary

# Health check
curl http://localhost:9999/health
```

## Características Técnicas

### Performance
- **Processamento Assíncrono**: Uso de async/await para melhor throughput
- **Connection Pooling**: Reutilização de conexões HTTP e banco
- **Cache Inteligente**: Redis para reduzir latência
- **Load Balancing**: Distribuição de carga com Nginx

## 🐳 Docker Hub

Esta implementação está disponível no Docker Hub para uso público:

### Usando a Imagem Publicada
```bash
# Baixar a imagem
docker pull SEU_USERNAME/rinha-backend-2025-python:latest

# Executar com docker-compose público
docker-compose -f docker-compose.public.yml up -d
```

### Para Publicar Sua Própria Imagem
```bash
# Script automatizado (recomendado)
python docker-hub-push.py

# Ou comandos manuais
./docker-hub-manual.sh SEU_USERNAME
```

Veja [DOCKER_HUB_GUIDE.md](DOCKER_HUB_GUIDE.md) para instruções detalhadas.

### Resiliência
- **Health Check**: Monitoramento contínuo dos processadores
- **Fallback Automático**: Troca automática em caso de falha
- **Retry Logic**: Tentativas automáticas de processamento
- **Error Handling**: Tratamento robusto de erros

### Auditoria
- **Logging Estruturado**: Logs detalhados para debugging
- **Persistência Completa**: Todos os pagamentos salvos no banco
- **Cache de Auditoria**: Redis para verificação rápida
- **Endpoint de Resumo**: Estatísticas em tempo real

## Estratégia de Otimização

1. **Minimizar Taxas**: Priorizar processador default (menor taxa)
2. **Maximizar Throughput**: Processamento assíncrono e load balancing
3. **Reduzir Latência**: Cache e connection pooling
4. **Garantir Consistência**: Auditoria completa e logs detalhados

## Monitoramento

- **Logs**: Estruturados com python-json-logger
- **Métricas**: Endpoints de health check
- **Auditoria**: Tabelas de auditoria no banco
- **Cache**: Monitoramento via Redis

Esta implementação segue todas as especificações da Rinha de Backend 2025, incluindo restrições de recursos, arquitetura de múltiplas instâncias e estratégia de processamento de pagamentos.
<p>Repositoria da aplicação [GitHub](https://github.com/JoneyPereira/python-rinha-backend-2025).