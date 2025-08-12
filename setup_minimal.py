#!/usr/bin/env python3
"""
Script de setup minimalista para a implementação Python da Rinha de Backend 2025
Versão que evita problemas de codificação
"""

import os
import sys
import subprocess
import time

def run_command_simple(command: str, cwd: str = None) -> bool:
    """Executa um comando de forma simples"""
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

def check_docker():
    """Verifica se o Docker está instalado"""
    print("🔍 Verificando Docker...")
    return run_command_simple("docker --version")

def check_docker_compose():
    """Verifica se o Docker Compose está instalado"""
    print("🔍 Verificando Docker Compose...")
    return run_command_simple("docker-compose --version")

def build_and_start():
    """Constrói e inicia os containers"""
    print("🚀 Construindo e iniciando containers...")
    
    # Parar containers existentes
    print("🛑 Parando containers existentes...")
    run_command_simple("docker-compose down")
    
    # Construir e iniciar
    if run_command_simple("docker-compose up --build -d"):
        print("✅ Containers iniciados com sucesso!")
        return True
    else:
        print("❌ Erro ao iniciar containers")
        return False

def wait_for_services():
    """Aguarda os serviços ficarem prontos"""
    print("⏳ Aguardando serviços ficarem prontos...")
    print("⏰ Aguardando 60 segundos para inicialização completa...")
    
    for i in range(60, 0, -1):
        if i % 10 == 0:
            print(f"⏳ Aguardando... {i}s restantes")
        time.sleep(1)
    
    print("✅ Tempo de espera concluído!")
    return True

def show_status():
    """Mostra o status dos containers"""
    print("📊 Status dos containers:")
    run_command_simple("docker-compose ps")

def main():
    """Função principal"""
    print("🐍 Setup Minimalista - Rinha de Backend 2025")
    print("=" * 50)
    
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
        print("💡 Tente executar manualmente:")
        print("   docker-compose up --build -d")
        return
    
    # Aguardar serviços
    if not wait_for_services():
        print("❌ Serviços não ficaram prontos")
        return
    
    print("\n🎉 Setup concluído!")
    print("=" * 50)
    print("📝 Comandos úteis:")
    print("   docker-compose ps          - Ver status")
    print("   docker-compose logs        - Ver logs")
    print("   docker-compose down        - Parar")
    print("=" * 50)
    print("🧪 Para testar:")
    print("   curl http://localhost:9999/health")
    print("   curl http://localhost:9999/payments-summary")
    print("=" * 50)

if __name__ == "__main__":
    main() 