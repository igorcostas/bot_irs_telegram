"""
Configurações do Bot IRS Portugal
IMPORTANTE: Use variáveis de ambiente em produção!
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# ⚠️ SEGURANÇA: API Keys devem estar em arquivo .env (não commitado)
# Para desenvolvimento: copie .env.example para .env e preencha
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN not found in environment variables. Please set it in .env file"
    )
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in environment variables. Please set it in .env file"
    )

# Configurações do Bot
BOT_NAME = "IRS Portugal Assistant - Marinete"
BOT_VERSION = "2.0.0"
MAX_MESSAGE_LENGTH = 4000

# Configurações LLM
LLM_PROVIDER = "groq"
MODEL_NAME = os.getenv("MODEL_NAME", "moonshotai/kimi-k2-instruct-0905")

# Configurações IRS Portugal 2025
IRS_YEAR = 2025
TAX_BRACKETS = {
    "escalao_1": {"min": 0, "max": 7703, "rate": 0.145},
    "escalao_2": {"min": 7703, "max": 11623, "rate": 0.23},
    "escalao_3": {"min": 11623, "max": 16472, "rate": 0.285},
    "escalao_4": {"min": 16472, "max": 21321, "rate": 0.353},
    "escalao_5": {"min": 21321, "max": 27146, "rate": 0.403},
    "escalao_6": {"min": 27146, "max": 39791, "rate": 0.45},
    "escalao_7": {"min": 39791, "max": 51997, "rate": 0.485},
    "escalao_8": {"min": 51997, "max": None, "rate": 0.485},
}

# Deduções principais
DEDUCTIONS = {
    "minimo_existencia": 4104,
    "despesas_saude": {"max": 1000, "rate": 0.15},
    "despesas_educacao": {"max": 800, "rate": 0.30},
    "encargos_habitacao": {"max": 296, "rate": 0.15},
    "lares": {"max": 403.75, "rate": 0.25},
}
