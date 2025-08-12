#!/usr/bin/env python3
"""
Script de setup para a implementação Python da Rinha de Backend 2025
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Tentar importar requests, mas não falhar se não estiver disponível
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  requests não está instalado. Algumas funcionalidades podem não funcionar.")

def run_command(command: str, cwd: str = None) -> bool:
    """Executa um comando e retorna True se bem-sucedido"""
    try:
        print(f"🔄 Executando: {command}")
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Comando executado com sucesso")
            return True
        else:
            print(f"❌ Erro ao executar comando: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def check_docker():
    """Verifica se o Docker está instalado"""
    print("🔍 Verificando Docker...")
    return run_command("docker --version")

def check_docker_compose():
    """Verifica se o Docker Compose está instalado"""
    print("🔍 Verificando Docker Compose...")
    return run_command("docker-compose --version")

def build_and_start():
    """Constrói e inicia os containers"""
    print("🚀 Construindo e iniciando containers...")
    
    # Parar containers existentes
    run_command("docker-compose down", cwd=".")
    
    # Construir e iniciar
    if run_command("docker-compose up --build -d", cwd="."):
        print("✅ Containers iniciados com sucesso!")
        return True
    else:
        print("❌ Erro ao iniciar containers")
        return False

def wait_for_services():
    """Aguarda os serviços ficarem prontos"""
    if not REQUESTS_AVAILABLE:
        print("⚠️  requests não disponível. Pulando verificação de serviços.")
        print("⏳ Aguardando 30 segundos para serviços inicializarem...")
        time.sleep(30)
        return True
    
    print("⏳ Aguardando serviços ficarem prontos...")
    
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get("http://localhost:9999/health", timeout=5)
            if response.status_code == 200:
                print("✅ Serviços prontos!")
                return True
        except:
            pass
        
        attempt += 1
        print(f"⏳ Tentativa {attempt}/{max_attempts}...")
        time.sleep(2)
    
    print("❌ Timeout aguardando serviços")
    return False

def run_tests():
    """Executa os testes"""
    print("🧪 Executando testes...")
    
    if run_command("python test_client.py", cwd="."):
        print("✅ Testes executados com sucesso!")
        return True
    else:
        print("❌ Erro nos testes")
        return False

def show_status():
    """Mostra o status dos containers"""
    print("📊 Status dos containers:")
    run_command("docker-compose ps", cwd=".")

def show_logs():
    """Mostra os logs dos containers"""
    print("📋 Logs dos containers:")
    run_command("docker-compose logs --tail=20", cwd=".")

def main():
    """Função principal"""
    print("🐍 Setup da Implementação Python - Rinha de Backend 2025")
    print("=" * 60)
    
    # Verificar pré-requisitos
    if not check_docker():
        print("❌ Docker não encontrado. Instale o Docker primeiro.")
        return
    
    if not check_docker_compose():
        print("❌ Docker Compose não encontrado. Instale o Docker Compose primeiro.")
        return
    
    # Construir e iniciar
    if not build_and_start():
        print("❌ Falha ao iniciar containers")
        return
    
    # Aguardar serviços
    if not wait_for_services():
        print("❌ Serviços não ficaram prontos")
        show_logs()
        return
    
    # Executar testes
    if not run_tests():
        print("❌ Testes falharam")
        show_logs()
        return
    
    print("\n🎉 Setup concluído com sucesso!")
    print("=" * 60)
    print("📝 Comandos úteis:")
    print("   docker-compose ps          - Ver status dos containers")
    print("   docker-compose logs        - Ver logs")
    print("   docker-compose down        - Parar containers")
    print("   python test_client.py      - Executar testes")
    print("   curl http://localhost:9999/health - Health check")
    print("=" * 60)

if __name__ == "__main__":
    main() 