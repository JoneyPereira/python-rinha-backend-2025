# 🚀 Início Rápido - Rinha de Backend 2025 Python

## Pré-requisitos
- Docker e Docker Compose instalados
- Python 3.8+ (opcional, para scripts de setup)

## ⚡ Execução Rápida

### 1. Setup Automatizado (Mais Fácil)
```bash
# Navegar para o diretório
cd python-rinha-backend-2025

# Executar setup automatizado (recomendado)
python setup_minimal.py

# Ou versão com mais detalhes
python setup_simple.py
```

### 2. Docker Compose Manual
```bash
# Navegar para o diretório
cd python-rinha-backend-2025

# Construir e executar
docker-compose up --build -d

# Aguardar 45 segundos para inicialização
```

## 🧪 Testes Rápidos

### Health Check
```bash
curl http://localhost:9999/health
```

### Resumo de Pagamentos
```bash
curl http://localhost:9999/payments-summary
```

### Processar Pagamento
```bash
curl -X POST http://localhost:9999/payments \
  -H "Content-Type: application/json" \
  -d '{"amount": 100.00, "description": "Teste"}'
```

## 📊 Monitoramento

### Status dos Containers
```bash
docker-compose ps
```

### Logs
```bash
docker-compose logs -f
```

### Métricas
```bash
curl http://localhost:9999/metrics
```

## 🛑 Parar Serviços
```bash
docker-compose down
```

## 🔧 Solução de Problemas

### Se o setup falhar:
1. Verificar se Docker está rodando
2. Verificar se a porta 9999 está livre
3. Executar `docker-compose logs` para ver erros

### Se health check falhar:
1. Aguardar mais tempo (pode levar até 60s)
2. Verificar logs: `docker-compose logs app1 app2`

### Se pagamentos falharem:
1. Verificar se os payment processors estão disponíveis
2. Verificar logs: `docker-compose logs app1 app2`

## 📝 Comandos Úteis

```bash
# Ver status
docker-compose ps

# Ver logs de um serviço específico
docker-compose logs app1

# Reiniciar um serviço
docker-compose restart app1

# Reconstruir e reiniciar
docker-compose up --build -d

# Parar tudo
docker-compose down

# Limpar volumes (cuidado: apaga dados)
docker-compose down -v
```

## 🎯 Próximos Passos

1. **Teste os endpoints** usando os comandos curl acima
2. **Monitore os logs** para ver o processamento
3. **Verifique as métricas** em `/metrics`
4. **Teste diferentes cenários** de pagamento
5. **Analise a performance** com múltiplas requisições

## 📚 Documentação Completa

- [README.md](README.md) - Documentação principal
- [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md) - Detalhes técnicos
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Resumo da implementação

---

**🎉 Sua implementação Python da Rinha de Backend 2025 está pronta para uso!** 