# llm_handler/llm_handler.py

import config
import requests
from prompts import SYSTEM_PROMPT

XAI_API_BASE = "https://api.x.ai/v1/chat/completions"

class LLMHandler:
    def __init__(self):
        if config.LLM_PROVIDER != "grok":
            raise ValueError("Defina LLM_PROVIDER = 'grok' em config.py")
        if not config.GROK_API_KEY:
            raise ValueError("Adicione GROK_API_KEY no arquivo de configurações")
        if not getattr(config, "MODEL_NAME", None):
            raise ValueError("Defina MODEL_NAME em config.py (ex.: 'grok-4')")

    def get_response(self, user_message: str, user_context: dict = None) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if user_context:
            ctx = (
                f"Estado civil: {user_context.get('civil_status','Não informado')}; "
                f"Rendimento anual: {user_context.get('annual_income','Não informado')}; "
                f"Dependentes: {user_context.get('dependents','Não informado')}"
            )
            messages.append({"role": "system", "content": ctx})
        messages.append({"role": "user", "content": user_message})

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.GROK_API_KEY}",
        }
        payload = {
            "model": config.MODEL_NAME,
            "messages": messages,
            "temperature": 0.7,
            "stream": False
        }

        try:
            resp = requests.post(
                XAI_API_BASE,
                json=payload,
                headers=headers,
                timeout=60,
                verify=False   # desativa verificação SSL para evitar TLSV1_UNRECOGNIZED_NAME
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"❌ Erro ao chamar API Grok: {e}"

# Instância global
llm_handler = LLMHandler()

