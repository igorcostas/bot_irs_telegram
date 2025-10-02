"""
Grok Handler - Manipula chamadas para API do Grok da xAI
"""

import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Carrega o .env automaticamente


class GrokHandler:
    """Handler para API do Grok da xAI"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")  # Correto, sem indentação extra
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY não encontrada no .env. Configure-a para usar o Grok."
            )

        self.client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        self.model = "grok-4"

        # Configurações padrão
        self.default_params = {
            "temperature": 0.8,
            "max_tokens": 800,
            "presence_penalty": 0.6,
            "frequency_penalty": 0.4,
        }

        self.logger = logging.getLogger(__name__)

    async def generate_response(
        self, user_message: str, system_prompt: str = None
    ) -> str:
        """Gera resposta usando Grok API"""

        try:
            messages = []

            # Adicionar system prompt se fornecido
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # Adicionar mensagem do usuário
            messages.append({"role": "user", "content": user_message})

            # Fazer chamada para API
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, **self.default_params
            )

            return response.choices[0].message.content

        except Exception as e:
            self.logger.error(f"Erro na API Grok: {e}")
            return f"Desculpe, tive um problema técnico. Erro: {str(e)}"

    def generate_response_sync(
        self, user_message: str, system_prompt: str = None
    ) -> str:
        """Versão síncrona da geração de resposta"""

        try:
            messages = []

            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            messages.append({"role": "user", "content": user_message})

            response = self.client.chat.completions.create(
                model=self.model, messages=messages, **self.default_params
            )

            return response.choices[0].message.content

        except Exception as e:
            self.logger.error(f"Erro na API Grok: {e}")
            return f"Desculpe, tive um problema técnico. Erro: {str(e)}"

    def set_temperature(self, temperature: float):
        """Ajusta temperatura para respostas mais ou menos criativas"""
        self.default_params["temperature"] = max(0.0, min(2.0, temperature))

    def set_max_tokens(self, max_tokens: int):
        """Ajusta tamanho máximo da resposta"""
        self.default_params["max_tokens"] = max(1, min(4000, max_tokens))

    def test_connection(self) -> bool:
        """Testa conexão com API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Teste"}],
                max_tokens=10,
            )
            return True
        except Exception as e:
            self.logger.error(f"Erro no teste de conexão: {e}")
            return False


# Exemplo de uso
if __name__ == "__main__":
    handler = GrokHandler()

    # Teste básico
    if handler.test_connection():
        print("✅ Conexão com Grok API funcionando!")

        # Teste de resposta
        resposta = handler.generate_response_sync(
            "Olá, você é um técnico contábil?",
            "Você é Maria, técnica contábil experiente.",
        )
        print(f"Resposta: {resposta}")
    else:
        print("❌ Problema na conexão com Grok API")
        print("Verifique sua XAI_API_KEY no arquivo .env")
