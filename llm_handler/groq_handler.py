"""
Groq Handler - Manipula chamadas para API Groq
Usando modelo Moonshot AI (Kimi K2 Instruct)
"""

import logging
from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME


class GroqHandler:
    """Handler para API Groq com modelo Moonshot AI"""

    def __init__(self):
        # Inicializar cliente Groq com API key do config
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = MODEL_NAME

        # Configurações padrão otimizadas para o modelo Kimi
        self.default_params = {
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.9,
        }

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"✅ GroqHandler inicializado com modelo: {self.model}")

    async def generate_response(
        self, user_message: str, system_prompt: str = None
    ) -> str:
        """
        Gera resposta usando Groq API (versão assíncrona)

        Args:
            user_message: Mensagem do usuário
            system_prompt: Prompt de sistema opcional

        Returns:
            str: Resposta gerada pelo modelo
        """
        try:
            messages = []

            # Adicionar system prompt se fornecido
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # Adicionar mensagem do usuário
            messages.append({"role": "user", "content": user_message})

            # Fazer chamada para API Groq
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, **self.default_params
            )

            return response.choices[0].message.content

        except Exception as e:
            self.logger.error(f"Erro na API Groq: {e}")
            return f"Desculpe, tive um problema técnico ao processar sua mensagem. Erro: {str(e)}"

    def generate_response_sync(
        self, user_message: str, system_prompt: str = None
    ) -> str:
        """
        Versão síncrona da geração de resposta

        Args:
            user_message: Mensagem do usuário
            system_prompt: Prompt de sistema opcional

        Returns:
            str: Resposta gerada pelo modelo
        """
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
            self.logger.error(f"Erro na API Groq (sync): {e}")
            return f"Desculpe, tive um problema técnico ao processar sua mensagem. Erro: {str(e)}"

    def set_temperature(self, temperature: float):
        """
        Ajusta temperatura para respostas mais ou menos criativas

        Args:
            temperature: Valor entre 0.0 (determinístico) e 2.0 (criativo)
        """
        self.default_params["temperature"] = max(0.0, min(2.0, temperature))
        self.logger.info(f"Temperature ajustada para: {temperature}")

    def set_max_tokens(self, max_tokens: int):
        """
        Ajusta tamanho máximo da resposta

        Args:
            max_tokens: Número máximo de tokens (1 a 8000 para Kimi)
        """
        self.default_params["max_tokens"] = max(1, min(8000, max_tokens))
        self.logger.info(f"Max tokens ajustado para: {max_tokens}")

    def test_connection(self) -> bool:
        """
        Testa conexão com API Groq

        Returns:
            bool: True se conectado com sucesso, False caso contrário
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Teste de conexão"}],
                max_tokens=10,
            )
            self.logger.info("✅ Teste de conexão com Groq API bem-sucedido!")
            return True
        except Exception as e:
            self.logger.error(f"❌ Erro no teste de conexão com Groq: {e}")
            return False

    def get_model_info(self) -> dict:
        """
        Retorna informações sobre o modelo atual

        Returns:
            dict: Informações do modelo e configurações
        """
        return {
            "provider": "Groq",
            "model": self.model,
            "temperature": self.default_params["temperature"],
            "max_tokens": self.default_params["max_tokens"],
            "top_p": self.default_params["top_p"],
        }


# Exemplo de uso e testes
if __name__ == "__main__":
    # Configurar logging para testes
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("🧪 Testando GroqHandler com Moonshot AI (Kimi K2)")
    print("=" * 60)

    try:
        handler = GroqHandler()

        # Exibir informações do modelo
        info = handler.get_model_info()
        print(f"\n📊 Informações do Modelo:")
        for key, value in info.items():
            print(f"   • {key}: {value}")

        # Teste de conexão
        print(f"\n🔌 Testando conexão com API...")
        if handler.test_connection():
            print("   ✅ Conexão estabelecida com sucesso!")

            # Teste de resposta
            print(f"\n💬 Testando geração de resposta...")
            resposta = handler.generate_response_sync(
                user_message="Olá! Você é um técnico contábil?",
                system_prompt="Você é Maria, uma técnica contábil experiente e prestativa. Responda de forma breve e profissional.",
            )
            print(f"\n🤖 Resposta do modelo:")
            print(f"   {resposta}")

        else:
            print("   ❌ Falha na conexão com API Groq")
            print("   💡 Verifique se a GROQ_API_KEY está correta em config.py")

    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        print("💡 Certifique-se de que:")
        print("   1. A biblioteca 'groq' está instalada: pip install groq")
        print("   2. A API key está configurada corretamente em config.py")
        print("   3. Você tem conexão com a internet")

    print("\n" + "=" * 60)
    print("✅ Testes concluídos!")
