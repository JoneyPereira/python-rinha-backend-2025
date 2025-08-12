#!/bin/bash

# Script para subir imagens para Docker Hub - Comandos Manuais
# Uso: ./docker-hub-manual.sh SEU_USERNAME

if [ $# -eq 0 ]; then
    echo "❌ Uso: ./docker-hub-manual.sh SEU_USERNAME"
    echo "Exemplo: ./docker-hub-manual.sh meuusername"
    exit 1
fi

USERNAME=$1
IMAGE_NAME="rinha-backend-2025-python"
FULL_IMAGE_NAME="$USERNAME/$IMAGE_NAME:latest"

echo "🐳 Docker Hub Push - Comandos Manuais"
echo "======================================"
echo "Username: $USERNAME"
echo "Imagem: $FULL_IMAGE_NAME"
echo ""

# 1. Login no Docker Hub
echo "🔐 1. Fazendo login no Docker Hub..."
docker login
if [ $? -ne 0 ]; then
    echo "❌ Falha no login. Verifique suas credenciais."
    exit 1
fi
echo "✅ Login realizado com sucesso!"
echo ""

# 2. Construir imagem
echo "🏗️  2. Construindo imagem..."
docker build -t $FULL_IMAGE_NAME .
if [ $? -ne 0 ]; then
    echo "❌ Falha ao construir imagem."
    exit 1
fi
echo "✅ Imagem construída: $FULL_IMAGE_NAME"
echo ""

# 3. Fazer push
echo "📤 3. Fazendo push da imagem..."
docker push $FULL_IMAGE_NAME
if [ $? -ne 0 ]; then
    echo "❌ Falha ao fazer push da imagem."
    exit 1
fi
echo "✅ Push realizado com sucesso!"
echo ""

# 4. Verificar
echo "🔍 4. Verificando push..."
docker search $USERNAME/$IMAGE_NAME
echo ""

# 5. Criar docker-compose público
echo "📝 5. Criando docker-compose público..."
cat > docker-compose.public.yml << EOF
version: '3.8'

services:
  # Aplicação principal - 2 instâncias para load balancing
  app1:
    image: $FULL_IMAGE_NAME
    container_name: python-rinha-app1
    ports:
      - "9999"
    environment:
      - DEFAULT_PAYMENT_PROCESSOR_URL=http://payment-processor:8080
      - FALLBACK_PAYMENT_PROCESSOR_URL=http://payment-processor-fallback:8080
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://user:password@postgres:5432/payments
    depends_on:
      - postgres
      - redis
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: "150MB"
    networks:
      - rinha-network

  app2:
    image: $FULL_IMAGE_NAME
    container_name: python-rinha-app2
    ports:
      - "9999"
    environment:
      - DEFAULT_PAYMENT_PROCESSOR_URL=http://payment-processor:8080
      - FALLBACK_PAYMENT_PROCESSOR_URL=http://payment-processor-fallback:8080
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://user:password@postgres:5432/payments
    depends_on:
      - postgres
      - redis
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: "150MB"
    networks:
      - rinha-network

  # Load Balancer (Nginx)
  nginx:
    image: nginx:alpine
    container_name: python-rinha-nginx
    ports:
      - "9999:9999"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app1
      - app2
    deploy:
      resources:
        limits:
          cpus: "0.1"
          memory: "50MB"
    networks:
      - rinha-network

  # Banco de dados PostgreSQL
  postgres:
    image: postgres:15-alpine
    container_name: python-rinha-postgres
    environment:
      - POSTGRES_DB=payments
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    deploy:
      resources:
        limits:
          cpus: "0.3"
          memory: "100MB"
    networks:
      - rinha-network

  # Redis para cache
  redis:
    image: redis:7-alpine
    container_name: python-rinha-redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    deploy:
      resources:
        limits:
          cpus: "0.1"
          memory: "50MB"
    networks:
      - rinha-network

networks:
  rinha-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
EOF

echo "✅ docker-compose.public.yml criado!"
echo ""

echo "🎉 Push concluído com sucesso!"
echo "======================================"
echo "📝 Informações importantes:"
echo "   🐳 Imagem: $FULL_IMAGE_NAME"
echo "   📄 docker-compose.public.yml criado"
echo ""
echo "💡 Para usar a imagem publicada:"
echo "   docker pull $FULL_IMAGE_NAME"
echo "   docker-compose -f docker-compose.public.yml up -d"
echo ""
echo "🔍 Para verificar no Docker Hub:"
echo "   Acesse: https://hub.docker.com/r/$USERNAME/$IMAGE_NAME"
echo "======================================" 