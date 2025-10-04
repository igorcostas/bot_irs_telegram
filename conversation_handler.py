"""
Conversation Handler - Bot IRS Portugal com Marinete
Sistema de simulação de IRS com 20 perguntas interativas
"""

import logging
from typing import Dict, Any
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)

# Importar handler LLM
from llm_handler.groq_handler import GroqHandler

# Importar prompts e perguntas
from prompts import (
    WELCOME_MESSAGE,
    SIMULATION_PROMPT,
    DEDUCTIONS_INFO,
    HELP_MESSAGE,
    PERGUNTAS_IRS,
    SYSTEM_PROMPT,
)

# Estados da conversação (20 perguntas + estados auxiliares)
(
    MENU_PRINCIPAL,
    PERGUNTA_1,
    PERGUNTA_2,
    PERGUNTA_3,
    PERGUNTA_4,
    PERGUNTA_5,
    PERGUNTA_6,
    PERGUNTA_7,
    PERGUNTA_8,
    PERGUNTA_9,
    PERGUNTA_10,
    PERGUNTA_11,
    PERGUNTA_12,
    PERGUNTA_13,
    PERGUNTA_14,
    PERGUNTA_15,
    PERGUNTA_16,
    PERGUNTA_17,
    PERGUNTA_18,
    PERGUNTA_19,
    PERGUNTA_20,
    PROCESSANDO_RESULTADO,
    CALCULO_RAPIDO,
) = range(23)

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("bot_contabil.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class IRSBotHandler:
    """Handler principal para o bot IRS Portugal com Marinete"""

    def __init__(self):
        self.groq = GroqHandler()
        logger.info("✅ IRSBotHandler inicializado com Marinete")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /start - Boas-vindas"""
        user = update.effective_user

        # Limpar dados anteriores
        context.user_data.clear()

        logger.info(f"Usuário {user.id} ({user.first_name}) iniciou o bot")

        await update.message.reply_text(
            WELCOME_MESSAGE,
            parse_mode="Markdown",
        )

        return ConversationHandler.END

    async def simular(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /simular - Inicia simulação completa de IRS"""
        user = update.effective_user

        # Limpar dados anteriores e iniciar novo questionário
        context.user_data.clear()
        context.user_data["respostas_irs"] = {}
        context.user_data["pergunta_atual"] = 0

        logger.info(f"Usuário {user.id} iniciou simulação de IRS")

        await update.message.reply_text(
            SIMULATION_PROMPT,
            parse_mode="Markdown",
        )

        # Enviar primeira pergunta
        return await self._enviar_pergunta(update, context, 0)

    async def _enviar_pergunta(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, numero_pergunta: int
    ) -> int:
        """Envia uma pergunta específica do questionário"""

        if numero_pergunta >= len(PERGUNTAS_IRS):
            # Terminou as perguntas
            return await self.finalizar_questionario(update, context)

        pergunta_data = PERGUNTAS_IRS[numero_pergunta]

        # Criar teclado se houver opções
        reply_markup = None
        if "opcoes" in pergunta_data and pergunta_data["opcoes"]:
            keyboard = [[KeyboardButton(opcao)] for opcao in pergunta_data["opcoes"]]
            reply_markup = ReplyKeyboardMarkup(
                keyboard, one_time_keyboard=True, resize_keyboard=True
            )

        # Montar mensagem
        mensagem = f"**Pergunta {numero_pergunta + 1}/20**\n\n"
        mensagem += pergunta_data["pergunta"]

        if "dica" in pergunta_data:
            mensagem += f"\n\n💡 _Dica: {pergunta_data['dica']}_"

        await update.message.reply_text(
            mensagem,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )

        # Retornar estado correspondente à pergunta
        return PERGUNTA_1 + numero_pergunta

    async def processar_resposta(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Processa cada resposta do questionário"""

        pergunta_atual = context.user_data.get("pergunta_atual", 0)
        resposta = update.message.text

        # Validar e salvar resposta
        pergunta_data = PERGUNTAS_IRS[pergunta_atual]
        chave = pergunta_data["chave"]

        context.user_data["respostas_irs"][chave] = resposta

        logger.info(f"Resposta {pergunta_atual + 1}: {chave} = {resposta}")

        # Avançar para próxima pergunta
        pergunta_atual += 1
        context.user_data["pergunta_atual"] = pergunta_atual

        # Verificar se terminaram as perguntas
        if pergunta_atual >= len(PERGUNTAS_IRS):
            return await self.finalizar_questionario(update, context)

        # Enviar próxima pergunta
        await update.message.reply_text(
            "✅ Resposta registada!",
            reply_markup=ReplyKeyboardRemove(),
        )

        return await self._enviar_pergunta(update, context, pergunta_atual)

    async def finalizar_questionario(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Finaliza questionário e processa cálculo de IRS"""

        await update.message.reply_text(
            "✅ **Questionário concluído!**\n\n"
            "🤖 Agora vou analisar as tuas respostas e calcular o teu IRS...",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="Markdown",
        )

        # Processar com LLM
        respostas = context.user_data.get("respostas_irs", {})

        try:
            # Criar prompt para análise
            prompt_analise = self._criar_prompt_analise(respostas)

            # Gerar análise com Groq
            resultado = self.groq.generate_response_sync(
                user_message=prompt_analise, system_prompt=SYSTEM_PROMPT
            )

            # Enviar resultado
            await update.message.reply_text(
                resultado,
                parse_mode="Markdown",
            )

            # Oferecer opções
            await update.message.reply_text(
                "\n📊 **O que desejas fazer agora?**\n\n"
                "• `/simular` - Nova simulação\n"
                "• `/deducoes` - Ver deduções disponíveis\n"
                "• `/ajuda` - Ver outros comandos\n\n"
                "Ou faz-me outra pergunta! 😊",
                parse_mode="Markdown",
            )

        except Exception as e:
            logger.error(f"Erro ao processar resultado: {e}")
            await update.message.reply_text(
                f"❌ Erro ao processar dados. Tenta novamente.\n"
                f"Erro técnico: {str(e)}\n\n"
                f"Usa `/reset` para recomeçar.",
            )

        return ConversationHandler.END

    def _criar_prompt_analise(self, respostas: Dict[str, Any]) -> str:
        """Cria prompt para análise das respostas"""

        prompt = "Com base nas seguintes informações, calcula e explica o IRS:\n\n"

        for i, pergunta in enumerate(PERGUNTAS_IRS):
            chave = pergunta["chave"]
            resposta = respostas.get(chave, "Não informado")
            prompt += f"{i + 1}. {pergunta['pergunta']}\n   Resposta: {resposta}\n\n"

        prompt += """
Por favor, fornece:

1. **💰 CÁLCULO DETALHADO DO IRS:**
   - Rendimento coletável
   - Escalão aplicável e taxa
   - Valor de IRS a pagar/receber
   - Impacto das deduções

2. **📊 COMPARAÇÃO (se aplicável):**
   - Tributação individual vs conjunta
   - Qual compensa mais e porquê

3. **💡 SUGESTÕES DE OTIMIZAÇÃO:**
   - Como reduzir o IRS legalmente
   - Deduções que pode aproveitar melhor
   - Benefícios fiscais disponíveis

4. **🎯 PRÓXIMOS PASSOS:**
   - Quando e como entregar a declaração
   - Documentos necessários
   - Prazos importantes

Formata de forma clara, com emojis e seções bem definidas. Lembra-te: és a Marinete, fala de forma natural e empática!
"""

        return prompt

    async def calcular_rapido(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Comando /calcular - Cálculo rápido de IRS"""

        texto = update.message.text.replace("/calcular", "").strip()

        if not texto:
            await update.message.reply_text(
                "⚡ **Cálculo Rápido de IRS**\n\n"
                "Usa assim:\n"
                "`/calcular 30000`\n"
                "ou\n"
                "`/calcular 30000 saude:500 educacao:300`\n\n"
                "Valores em euros (€)",
                parse_mode="Markdown",
            )
            return ConversationHandler.END

        try:
            # Processar entrada
            prompt = f"""
Faz um cálculo rápido de IRS para: {texto}

Considera:
- Trabalhador dependente, solteiro, sem dependentes
- Rendimento e deduções fornecidos
- Portugal Continental, 2024

Mostra:
1. Rendimento coletável
2. Escalão e taxa
3. IRS a pagar/receber (estimativa)
4. Breve explicação

Sê breve e direto! Máximo 10 linhas.
"""

            resultado = self.groq.generate_response_sync(
                user_message=prompt, system_prompt=SYSTEM_PROMPT
            )

            await update.message.reply_text(
                f"⚡ **Cálculo Rápido:**\n\n{resultado}\n\n"
                f"💡 Para simulação detalhada, usa `/simular`",
                parse_mode="Markdown",
            )

        except Exception as e:
            logger.error(f"Erro no cálculo rápido: {e}")
            await update.message.reply_text(
                f"❌ Erro no cálculo. Verifica o formato!\nExemplo: `/calcular 30000`"
            )

        return ConversationHandler.END

    async def deducoes(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /deducoes - Mostra informações sobre deduções"""

        await update.message.reply_text(
            DEDUCTIONS_INFO,
            parse_mode="Markdown",
        )

        return ConversationHandler.END

    async def ajuda(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /ajuda - Mostra ajuda"""

        await update.message.reply_text(
            HELP_MESSAGE,
            parse_mode="Markdown",
        )

        return ConversationHandler.END

    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /reset - Reinicia o bot"""

        context.user_data.clear()

        await update.message.reply_text(
            "🔄 Dados limpos!\n\n"
            "Usa `/start` para começar de novo ou `/simular` para nova simulação.",
            reply_markup=ReplyKeyboardRemove(),
        )

        return ConversationHandler.END

    async def cancelar(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /cancel - Cancela operação atual"""

        await update.message.reply_text(
            "❌ Operação cancelada.\n\n"
            "Usa `/start` para ver opções ou `/simular` para nova simulação.",
            reply_markup=ReplyKeyboardRemove(),
        )

        return ConversationHandler.END

    async def mensagem_livre(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Processa mensagens livres (conversação natural)"""

        mensagem = update.message.text

        try:
            # Gerar resposta com contexto
            resposta = await self.groq.generate_response(
                user_message=mensagem, system_prompt=SYSTEM_PROMPT
            )

            await update.message.reply_text(
                resposta,
                parse_mode="Markdown",
            )

        except Exception as e:
            logger.error(f"Erro na mensagem livre: {e}")
            await update.message.reply_text(
                "Desculpa, tive um problema ao processar a tua mensagem. "
                "Podes tentar de novo? 😊"
            )

        return ConversationHandler.END

    def get_conversation_handler(self) -> ConversationHandler:
        """Retorna o ConversationHandler configurado"""

        # Estados para as 20 perguntas
        states = {}

        # Cada pergunta tem seu estado
        for i in range(20):
            states[PERGUNTA_1 + i] = [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.processar_resposta)
            ]

        return ConversationHandler(
            entry_points=[
                CommandHandler("simular", self.simular),
            ],
            states=states,
            fallbacks=[
                CommandHandler("cancel", self.cancelar),
                CommandHandler("reset", self.reset),
            ],
            per_user=True,
            per_chat=True,
        )


def create_application():
    """Cria e configura a aplicação do bot IRS"""
    from config import TELEGRAM_BOT_TOKEN

    # Criar aplicação
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Criar handler principal
    bot = IRSBotHandler()

    # Registrar handlers
    # 1. Comandos principais (fora da conversação)
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("calcular", bot.calcular_rapido))
    application.add_handler(CommandHandler("deducoes", bot.deducoes))
    application.add_handler(CommandHandler("ajuda", bot.ajuda))
    application.add_handler(CommandHandler("reset", bot.reset))

    # 2. Conversation handler para simulação
    application.add_handler(bot.get_conversation_handler())

    # 3. Handler para mensagens livres (deve ser último)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, bot.mensagem_livre)
    )

    logger.info("✅ Bot IRS Portugal configurado com Marinete!")

    return application


if __name__ == "__main__":
    # Teste direto
    app = create_application()
    print("🤖 Bot IRS Portugal - Marinete iniciado!")
    app.run_polling()
