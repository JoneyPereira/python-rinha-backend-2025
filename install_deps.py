#!/usr/bin/env python3
"""
Script para instalar dependências necessárias para o setup da Rinha de Backend 2025
"""

import subprocess
import sys
import os

def install_package(package):
    """Instala um pacote Python"""
    try:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar {package}: {e}")
        return False

def main():
    """Função principal"""
    print("🐍 Instalando dependências para Rinha de Backend 2025")
    print("=" * 50)
    
    # Dependências necessárias para o setup
    dependencies = [
        "requests==2.31.0",
        "httpx==0.25.2"
    ]
    
    success_count = 0
    total_count = len(dependencies)
    
    for package in dependencies:
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Resultado: {success_count}/{total_count} dependências instaladas")
    
    if success_count == total_count:
        print("🎉 Todas as dependências foram instaladas com sucesso!")
        print("Agora você pode executar: python setup.py")
    else:
        print("⚠️  Algumas dependências falharam. Tente instalar manualmente:")
        for package in dependencies:
            print(f"   pip install {package}")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 