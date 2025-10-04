"""
Main entry point for IRS Telegram Bot
Bot com sistema de análise completa usando Groq API (Moonshot AI - Kimi K2)

Versão 2.0.0 - Compatível com Python 3.13
"""

import sys
import logging
from conversation_handler import create_application

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("bot_contabil.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def main():
    """Função principal para iniciar o bot"""
    try:
        # Criar aplicação
        logger.info("🚀 Iniciando Bot Técnico Contábil Virtual...")
        app = create_application()

        print("=" * 70)
        print("🤖 Bot Técnico Contábil Virtual iniciado!")
        print("📊 Sistema de análise completa ativo")
        print("🔥 API: Groq (Moonshot AI - Kimi K2)")
        print("=" * 70)
        print("\n✅ Bot está rodando... Pressione Ctrl+C para parar.\n")

        # Iniciar polling
        # Workaround para Python 3.13: usar run_polling() diretamente
        app.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True,
            poll_interval=1.0,
            timeout=10,
        )

    except KeyboardInterrupt:
        logger.info("🛑 Bot parado pelo usuário (Ctrl+C)")
        print("\n\n🛑 Bot parado. Até logo!")
        sys.exit(0)

    except Exception as e:
        logger.error(f"❌ Erro crítico ao iniciar bot: {e}", exc_info=True)
        print(f"\n❌ ERRO: {e}")
        print("\n💡 Dicas:")
        print("  1. Verifique se a API key está correta em config.py")
        print("  2. Verifique sua conexão com a internet")
        print("  3. Execute: python3 test_groq_api.py")
        print("  4. Veja os logs em: bot_contabil.log")
        sys.exit(1)


if __name__ == "__main__":
    main()
