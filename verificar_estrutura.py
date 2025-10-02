#!/usr/bin/env python3
"""
Verificação de Estrutura do Projeto - Identifica o que está faltando
"""
import os

def verificar_estrutura_projeto():
    print("🔍 VERIFICANDO ESTRUTURA DO PROJETO...")
    print("=" * 60)

    # Arquivos essenciais que devem existir
    arquivos_necessarios = {
        'main.py': 'Arquivo principal do bot',
        'config.py': 'Configurações',
        'prompts.py': 'Prompts do sistema',
        '.env': 'Variáveis de ambiente',
        'conversation_handler.py': 'Handler das conversas',

        # Novos arquivos
        'data_processor.py': 'Processador de dados',
        'report_generator.py': 'Gerador de relatórios',
        'automation_manager.py': 'Gerenciador de automações',  
        'main_integration.py': 'Integração principal',

        # Pasta LLM
        'llm_handler/__init__.py': 'Init da pasta LLM',
        'llm_handler/grok_handler.py': 'Handler do Grok'
    }

    print("📁 VERIFICANDO ARQUIVOS:")
    existem = []
    faltam = []

    for arquivo, descricao in arquivos_necessarios.items():
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} - {descricao}")
            existem.append(arquivo)
        else:
            print(f"❌ {arquivo} - {descricao} [FALTANDO]")
            faltam.append(arquivo)

    print("\n" + "=" * 60)
    print(f"📊 RESUMO: {len(existem)} existem | {len(faltam)} faltando")

    if faltam:
        print("\n🚨 ARQUIVOS FALTANDO:")
        for arquivo in faltam:
            print(f"  - {arquivo}")

        print("\n💡 SOLUÇÕES:")
        if 'data_processor.py' in faltam:
            print("  1. Copie data_processor.py para a pasta do projeto")
        if 'report_generator.py' in faltam:
            print("  2. Copie report_generator.py para a pasta do projeto")
        if 'automation_manager.py' in faltam:
            print("  3. Copie automation_manager.py para a pasta do projeto")
        if 'main_integration.py' in faltam:
            print("  4. Copie main_integration.py para a pasta do projeto")
        if 'llm_handler/grok_handler.py' in faltam:
            print("  5. Crie pasta llm_handler/ e copie grok_handler.py")
    else:
        print("\n🎉 TODOS OS ARQUIVOS ESTÃO PRESENTES!")

    return len(faltam) == 0

def verificar_dependencias():
    print("\n🔧 VERIFICANDO DEPENDENCIAS...")
    print("=" * 60)

    dependencias = [
        'telegram',
        'openai', 
        'dotenv',
        'json',
        'logging',
        'datetime',
        'typing'
    ]

    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - pip install {dep}")
            if dep == 'telegram':
                print("   💡 pip install python-telegram-bot")
            elif dep == 'dotenv':
                print("   💡 pip install python-dotenv")

def main():
    estrutura_ok = verificar_estrutura_projeto()
    verificar_dependencias()

    print("\n" + "=" * 60)
    if estrutura_ok:
        print("🎯 PRONTO PARA EXECUTAR: python main.py")
    else:
        print("⚠️ CORRIJA OS PROBLEMAS ACIMA PRIMEIRO")
    print("=" * 60)

if __name__ == "__main__":
    main()
