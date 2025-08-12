#!/usr/bin/env python3
"""
Script de setup simplificado para a implementação Python da Rinha de Backend 2025
Versão que não depende de requests
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(command: str, cwd: str = None) -> bool:
    """Executa um comando e retorna True se bem-sucedido"""
    try:
        print(f"🔄 Executando: {command}")
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            print(f"[OK] Comando executado com sucesso")
            if result.stdout and result.stdout.strip():
                print(f"[SAIDA] Saída: {result.stdout.strip()}")
            return True
        else:
            error_msg = result.stderr.strip() if result.stderr else "Erro desconhecido"
            print(f"[ERRO] Erro ao executar comando: {error_msg}")
            return False
    except Exception as e:
        print(f"[ERRO] Erro: {e}")
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
    print("[BUILD] Construindo e iniciando containers...")
    
    # Parar containers existentes
    print("[STOP] Parando containers existentes...")
    run_command("docker-compose down", cwd=".")
    
    # Construir e iniciar
    if run_command("docker-compose up --build -d", cwd="."):
        print("[OK] Containers iniciados com sucesso!")
        return True
    else:
        print("[ERRO] Erro ao iniciar containers")
        return False

def wait_for_services_simple():
    """Aguarda os serviços ficarem prontos (versão simples)"""
    print("[AGUARDAR] Aguardando serviços ficarem prontos...")
    print("[TEMPO] Aguardando 45 segundos para inicialização completa...")
    
    for i in range(45, 0, -1):
        print(f"[AGUARDAR] Aguardando... {i}s restantes")
        time.sleep(1)
    
    print("[OK] Tempo de espera concluído!")
    return True

def show_status():
    """Mostra o status dos containers"""
    print("[STATUS] Status dos containers:")
    run_command("docker-compose ps", cwd=".")

def show_logs():
    """Mostra os logs dos containers"""
    print("[LOGS] Logs dos containers:")
    run_command("docker-compose logs --tail=20", cwd=".")

def test_health_simple():
    """Testa health check usando curl (se disponível)"""
    print("[TESTE] Testando health check...")
    
    # Tentar usar curl se disponível
    if run_command("curl --version"):
        if run_command("curl -s http://localhost:9999/health"):
            print("[OK] Health check bem-sucedido!")
            return True
        else:
            print("[ERRO] Health check falhou")
            return False
    else:
        print("[AVISO] curl não disponível. Pulando teste de health check.")
        return True

def main():
    """Função principal"""
    print("[PYTHON] Setup Simplificado - Rinha de Backend 2025")
    print("=" * 60)
    
    # Verificar pré-requisitos
    if not check_docker():
        print("[ERRO] Docker não encontrado. Instale o Docker primeiro.")
        return
    
    if not check_docker_compose():
        print("[ERRO] Docker Compose não encontrado. Instale o Docker Compose primeiro.")
        return
    
    # Construir e iniciar
    if not build_and_start():
        print("[ERRO] Falha ao iniciar containers")
        return
    
    # Aguardar serviços
    if not wait_for_services_simple():
        print("[ERRO] Serviços não ficaram prontos")
        show_logs()
        return
    
    # Testar health check
    if not test_health_simple():
        print("[AVISO] Health check falhou, mas continuando...")
        show_logs()
    
    print("\n[SUCESSO] Setup concluído!")
    print("=" * 60)
    print("[COMANDOS] Comandos úteis:")
    print("   docker-compose ps          - Ver status dos containers")
    print("   docker-compose logs        - Ver logs")
    print("   docker-compose down        - Parar containers")
    print("   curl http://localhost:9999/health - Health check")
    print("   curl http://localhost:9999/payments-summary - Resumo")
    print("=" * 60)
    print("[TESTE] Para testar pagamentos:")
    print("   curl -X POST http://localhost:9999/payments \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"amount\": 100.00, \"description\": \"Teste\"}'")
    print("=" * 60)

if __name__ == "__main__":
    main() 