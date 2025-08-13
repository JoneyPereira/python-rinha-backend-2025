#!/usr/bin/env python3
"""
Script para subir imagens da implementação Python da Rinha de Backend 2025 para o Docker Hub
"""

import subprocess
import os
import sys
import time

def run_command(command: str, cwd: str = None) -> bool:
    """Executa um comando e retorna True se bem-sucedido"""
    try:
        print(f"🔄 Executando: {command}")
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if result.returncode == 0:
            print(f"✅ Comando executado com sucesso")
            return True
        else:
            print(f"❌ Comando falhou (código: {result.returncode})")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def get_docker_hub_username():
    """Solicita o username do Docker Hub"""
    print("🐳 Configuração do Docker Hub")
    print("=" * 40)
    
    username = input("Digite seu username do Docker Hub: ").strip()
    if not username:
        print("❌ Username é obrigatório!")
        return None
    
    return username

def login_docker_hub():
    """Faz login no Docker Hub"""
    print("🔐 Fazendo login no Docker Hub...")
    print("💡 Digite suas credenciais quando solicitado")
    
    if run_command("docker login"):
        print("✅ Login realizado com sucesso!")
        return True
    else:
        print("❌ Falha no login. Verifique suas credenciais.")
        return False

def build_and_tag_images(username: str):
    """Constrói e faz tag das imagens"""
    print("🏗️  Construindo e fazendo tag das imagens...")
    
    # Tag para a aplicação principal
    app_tag = f"{username}/rinha-backend-2025-python:latest"
    
    # Construir imagem da aplicação
    if run_command(f"docker build -t {app_tag} ."):
        print(f"✅ Imagem construída: {app_tag}")
        return app_tag
    else:
        print("❌ Falha ao construir imagem")
        return None

def push_images(tag: str):
    """Faz push das imagens para o Docker Hub"""
    print("📤 Fazendo push das imagens...")
    
    if run_command(f"docker push {tag}"):
        print(f"✅ Imagem enviada com sucesso: {tag}")
        return True
    else:
        print("❌ Falha ao fazer push da imagem")
        return False

def create_docker_compose_public(username: str):
    """Cria docker-compose.yml para uso público"""
    print("📝 Criando docker-compose.yml para uso público...")
    
    compose_content = f"""version: '3.8'

services:
  # Aplicação principal - 2 instâncias para load balancing
  app1:
    image: {username}/rinha-backend-2025-python:latest
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
          cpus: "0.4"
          memory: "80MB"
    networks:
      - rinha-network
      - payment-processor

  app2:
    image: {username}/rinha-backend-2025-python:latest
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
          cpus: "0.4"
          memory: "80MB"
    networks:
      - rinha-network
      - payment-processor

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
          memory: "40MB"
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
          memory: "80MB"
    networks:
      - rinha-network
      - payment-processor

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
          memory: "40MB"
    networks:
      - rinha-network
      - payment-processor

networks:
  rinha-network:
    driver: bridge
  payment-processor:
    external: true

volumes:
  postgres_data:
  redis_data:
"""
    
    with open("docker-compose.public.yml", "w") as f:
        f.write(compose_content)
    
    print("✅ docker-compose.public.yml criado!")
    return True

def main():
    """Função principal"""
    print("🐳 Push para Docker Hub - Rinha de Backend 2025 Python")
    print("=" * 60)
    
    # Verificar se Docker está disponível
    if not run_command("docker --version"):
        print("❌ Docker não encontrado. Instale o Docker primeiro.")
        return
    
    # Obter username do Docker Hub
    username = get_docker_hub_username()
    if not username:
        return
    
    # Fazer login no Docker Hub
    if not login_docker_hub():
        return
    
    # Construir e fazer tag das imagens
    tag = build_and_tag_images(username)
    if not tag:
        return
    
    # Fazer push das imagens
    if not push_images(tag):
        return
    
    # Criar docker-compose público
    create_docker_compose_public(username)
    
    print("\n🎉 Push concluído com sucesso!")
    print("=" * 60)
    print("📝 Informações importantes:")
    print(f"   🐳 Imagem: {tag}")
    print(f"   📄 docker-compose.public.yml criado")
    print("=" * 60)
    print("💡 Para usar a imagem publicada:")
    print("   docker pull {tag}")
    print("   docker-compose -f docker-compose.public.yml up -d")
    print("=" * 60)

if __name__ == "__main__":
    main() 