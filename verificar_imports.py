"""
VERIFICAÇÃO DE IMPORTS - Checklist completo para o projeto
Execute este arquivo para verificar se todos os imports estão funcionando
"""

print("🔍 VERIFICANDO IMPORTS DO PROJETO...")
print("=" * 60)

# Lista de verificações
verificacoes = []

print("\n1️⃣ VERIFICANDO IMPORTS BÁSICOS...")
try:
    import json
    import logging
    import datetime
    from typing import Dict, List, Any
    from dataclasses import dataclass
    print("✅ Imports básicos do Python: OK")
    verificacoes.append("✅ Imports básicos")
except ImportError as e:
    print(f"❌ Erro em imports básicos: {e}")
    verificacoes.append("❌ Imports básicos")

print("\n2️⃣ VERIFICANDO TELEGRAM BOT...")
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
    from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, CallbackQueryHandler, filters
    print("✅ python-telegram-bot: OK")
    verificacoes.append("✅ Telegram Bot")
except ImportError as e:
    print(f"❌ Erro telegram bot: {e}")
    print("💡 Solução: pip install python-telegram-bot")
    verificacoes.append("❌ Telegram Bot")

print("\n3️⃣ VERIFICANDO OPENAI (PARA GROK)...")
try:
    from openai import OpenAI
    print("✅ OpenAI (compatível com Grok): OK")
    verificacoes.append("✅ OpenAI")
except ImportError as e:
    print(f"❌ Erro OpenAI: {e}")
    print("💡 Solução: pip install openai")
    verificacoes.append("❌ OpenAI")

print("\n4️⃣ VERIFICANDO PYTHON-DOTENV...")
try:
    from dotenv import load_dotenv
    import os
    print("✅ python-dotenv: OK")
    verificacoes.append("✅ python-dotenv")
except ImportError as e:
    print(f"❌ Erro python-dotenv: {e}")
    print("💡 Solução: pip install python-dotenv")
    verificacoes.append("❌ python-dotenv")

print("\n5️⃣ VERIFICANDO MÓDULOS DO SEU PROJETO...")

# Verificar módulos existentes do projeto
modulos_projeto = [
    ("config", "Configurações do bot"),
    ("prompts", "Prompts do sistema"),  
]

for modulo, descricao in modulos_projeto:
    try:
        __import__(modulo)
        print(f"✅ {modulo}.py ({descricao}): OK")
        verificacoes.append(f"✅ {modulo}.py")
    except ImportError as e:
        print(f"❌ {modulo}.py não encontrado: {e}")
        verificacoes.append(f"❌ {modulo}.py")

print("\n6️⃣ VERIFICANDO MÓDULOS LLM...")
try:
    # Tentar importar handler do Grok (estrutura do usuário)
    from llm_handler.grok_handler import GrokHandler
    print("✅ llm_handler/grok_handler.py: OK")
    verificacoes.append("✅ GrokHandler")
except ImportError as e:
    print(f"❌ llm_handler/grok_handler.py: {e}")
    print("💡 Verifique se o arquivo existe na pasta llm_handler/")
    verificacoes.append("❌ GrokHandler")

print("\n7️⃣ VERIFICANDO NOVOS MÓDULOS CRIADOS...")
novos_modulos = [
    ("data_processor", "DataProcessor, EmpresaProfile"),
    ("report_generator", "ReportGenerator"), 
    ("automation_manager", "AutomationManager"),
    ("main_integration", "PostAnalysisHandler")
]

for modulo, classes in novos_modulos:
    try:
        mod = __import__(modulo)
        print(f"✅ {modulo}.py ({classes}): OK")
        verificacoes.append(f"✅ {modulo}.py")
    except ImportError as e:
        print(f"❌ {modulo}.py não encontrado: {e}")
        print(f"💡 Copie o arquivo {modulo}.py para a pasta do projeto")
        verificacoes.append(f"❌ {modulo}.py")

print("\n" + "=" * 60)
print("📊 RESUMO DA VERIFICAÇÃO:")
print("=" * 60)

sucessos = len([v for v in verificacoes if "✅" in v])
erros = len([v for v in verificacoes if "❌" in v])

for verificacao in verificacoes:
    print(verificacao)

print(f"\n🎯 RESULTADO: {sucessos} OK | {erros} PROBLEMAS")

if erros == 0:
    print("\n🎉 PARABÉNS! Todos os imports estão funcionando!")
    print("✅ Seu projeto está pronto para executar!")
else:
    print(f"\n⚠️ Encontrados {erros} problemas que precisam ser resolvidos.")
    print("📋 Siga as soluções indicadas acima.")

print("\n" + "=" * 60)
