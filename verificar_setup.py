#!/usr/bin/env python3
import os
import sys

def verificar_arquivos():
    """Verifica arquivos essenciais do projeto"""
    arquivos_essenciais = [
        'main.py',
        'config.py', 
        '.env',
        'requirements.txt',
        'conversation_handler.py',
        'data_processor.py',
        'report_generator.py',
        'pyproject.toml'  # Criado pelo uv
    ]
    
    print("🔍 Verificando estrutura do projeto...")
    
    for arquivo in arquivos_essenciais:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - AUSENTE")

def verificar_imports():
    """Testa imports principais"""
    imports_teste = [
        'telegram',
        'dotenv', 
        'openai',
        'config'
    ]
    
    print("\n🧪 Testando imports...")
    
    for modulo in imports_teste:
        try:
            __import__(modulo)
            print(f"✅ {modulo}")
        except ImportError as e:
            print(f"❌ {modulo} - {e}")

if __name__ == "__main__":
    verificar_arquivos()
    verificar_imports()
