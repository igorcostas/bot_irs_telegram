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
    filters,
)

# Importar handler LLM
from llm_handler.groq_handler import GroqHandler

# Importar sistemas de monitoramento e sugestões
from monitoring import monitoring
from suggestions import suggestion_manager

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
    AGUARDANDO_SUGESTAO,
) = range(24)

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
        if not user:
            return ConversationHandler.END

        # Registrar usuário e atividade no sistema de monitoramento
        monitoring.register_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
        )
        monitoring.register_activity(user.id, "command", "/start")

        # Limpar dados anteriores e inicializar estrutura
        context.user_data.clear()
        context.user_data["respostas_irs"] = {}
        context.user_data["pergunta_atual"] = 0

        logger.info(f"Usuário {user.id} ({user.first_name}) iniciou o bot")

        await update.message.reply_text(
            WELCOME_MESSAGE,
            parse_mode="Markdown",
        )

        return ConversationHandler.END

    async def simular(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /simular - Inicia simulação completa de IRS"""
        user = update.effective_user
        if not user:
            return ConversationHandler.END

        # Registrar usuário e atividade
        monitoring.register_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
        )
        monitoring.register_activity(user.id, "command", "/simular")

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
        """Processa resposta de uma pergunta e avança para a próxima"""

        # Verificar se o questionário foi iniciado corretamente
        if "respostas_irs" not in context.user_data:
            await update.message.reply_text(
                "⚠️ Por favor, inicie a simulação com o comando /simular primeiro."
            )
            return ConversationHandler.END

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

            # Registrar simulação completada para métricas
            monitoring.register_simulation_completion(update.effective_user.id)

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
        user = update.effective_user
        if not user:
            return ConversationHandler.END

        # Registrar usuário e atividade
        monitoring.register_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
        )
        monitoring.register_activity(user.id, "command", "/calcular")

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
        user = update.effective_user
        if not user:
            return ConversationHandler.END

        # Registrar atividade
        monitoring.register_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
        )
        monitoring.register_activity(user.id, "command", "/deducoes")

        await update.message.reply_text(
            DEDUCTIONS_INFO,
            parse_mode="Markdown",
        )

        return ConversationHandler.END

    async def ajuda(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /ajuda - Mostra ajuda"""
        user = update.effective_user
        if not user:
            return ConversationHandler.END

        # Registrar atividade
        monitoring.register_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
        )
        monitoring.register_activity(user.id, "command", "/ajuda")

        await update.message.reply_text(
            HELP_MESSAGE,
            parse_mode="Markdown",
        )

        return ConversationHandler.END

    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /reset - Reinicia o bot"""
        user = update.effective_user
        if not user:
            return ConversationHandler.END

        # Registrar atividade
        monitoring.register_activity(user.id, "command", "/reset")

        context.user_data.clear()

        await update.message.reply_text(
            "🔄 Dados limpos!\n\n"
            "Usa `/start` para começar de novo ou `/simular` para nova simulação.",
            reply_markup=ReplyKeyboardRemove(),
        )

        return ConversationHandler.END

    async def cancelar(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /cancel - Cancela operação atual"""
        user = update.effective_user
        if not user:
            return ConversationHandler.END

        # Registrar atividade
        monitoring.register_activity(user.id, "command", "/cancel")

        await update.message.reply_text(
            "❌ Operação cancelada.\n\n"
            "Usa `/start` para ver opções ou `/simular` para nova simulação.",
            reply_markup=ReplyKeyboardRemove(),
        )

        return ConversationHandler.END

    async def sugestoes(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Comando /sugestoes - Permite ao usuário enviar sugestão"""
        user = update.effective_user
        if not user:
            return ConversationHandler.END

        # Registrar usuário e atividade
        monitoring.register_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
        )
        monitoring.register_activity(user.id, "command", "/sugestoes")

        # Verificar se pode enviar sugestão (cooldown)
        can_suggest, error_msg = suggestion_manager.can_user_suggest(user.id)

        if not can_suggest:
            await update.message.reply_text(
                f"⏰ **Aguarda um pouco**\n\n{error_msg}",
                parse_mode="Markdown",
            )
            return ConversationHandler.END

        # Pedir sugestão
        await update.message.reply_text(
            "💡 **Envia a tua sugestão!**\n\n"
            "Podes sugerir melhorias, novas funcionalidades, "
            "reportar problemas ou dar feedback geral.\n\n"
            "📝 Escreve a tua sugestão na próxima mensagem:",
            parse_mode="Markdown",
        )

        return AGUARDANDO_SUGESTAO

    async def processar_sugestao(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Processa a sugestão enviada pelo usuário"""
        user = update.effective_user
        if not user or not update.message or not update.message.text:
            return ConversationHandler.END

        suggestion_text = update.message.text

        # Registrar a sugestão
        success, message = suggestion_manager.add_suggestion(
            user_id=user.id,
            suggestion_text=suggestion_text,
            username=user.username or "",
            first_name=user.first_name or "",
        )

        if success:
            await update.message.reply_text(
                f"✅ **Sugestão recebida!**\n\n"
                f"{message}\n\n"
                f"🙏 Obrigado pelo teu feedback! A tua sugestão será analisada.",
                parse_mode="Markdown",
            )
        else:
            await update.message.reply_text(
                f"❌ **Erro ao enviar sugestão**\n\n{message}",
                parse_mode="Markdown",
            )

        return ConversationHandler.END

    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /stats - Mostra estatísticas do bot (admin)"""
        user = update.effective_user
        if not user:
            return ConversationHandler.END

        # Lista de IDs de administradores - Henrick (user ID 1378607128)
        admin_ids = [1378607128]  # Henrick - Admin do bot

        if user.id not in admin_ids:
            await update.message.reply_text("❌ Comando apenas para administradores.")
            return ConversationHandler.END

        # Registrar atividade
        monitoring.register_activity(user.id, "command", "/stats")

        try:
            # Gerar relatório de showcase para clientes
            showcase_report = monitoring.generate_showcase_report()

            # Gerar relatório de sugestões
            suggestions_report = suggestion_manager.generate_suggestions_report()

            # Enviar relatório de showcase (dividido se muito longo)
            if len(showcase_report) > 4000:
                # Dividir em partes
                parts = [
                    showcase_report[i : i + 4000]
                    for i in range(0, len(showcase_report), 4000)
                ]
                for i, part in enumerate(parts):
                    await update.message.reply_text(
                        f"**PARTE {i + 1}/{len(parts)}**\n\n{part}",
                        parse_mode="Markdown",
                    )
            else:
                await update.message.reply_text(
                    showcase_report,
                    parse_mode="Markdown",
                )

            # Enviar relatório de sugestões separadamente
            await update.message.reply_text(
                suggestions_report,
                parse_mode="Markdown",
            )

        except Exception as e:
            logger.error(f"Erro ao gerar estatísticas: {e}")
            await update.message.reply_text(
                "❌ Erro ao gerar relatório de estatísticas.",
            )

        return ConversationHandler.END

    async def showcase_detalhado(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Comando /showcase_detalhado - Relatório técnico completo para clientes (admin apenas)"""
        user = update.effective_user
        if not user:
            return ConversationHandler.END

        # Restrito apenas para Henrick (user ID 1378607128)
        if user.id != 1378607128:
            await update.message.reply_text("❌ Comando apenas para administradores.")
            return ConversationHandler.END

        # Registrar atividade
        monitoring.register_activity(user.id, "command", "/showcase_detalhado")

        try:
            # Gerar relatório técnico completo
            stats_report = monitoring.generate_stats_report()
            showcase_report = monitoring.generate_showcase_report()
            suggestions_report = suggestion_manager.generate_suggestions_report()

            # Cabeçalho do relatório técnico
            technical_header = """🔬 **RELATÓRIO TÉCNICO DETALHADO**
_Análise Completa para Demonstração Técnica_

═══════════════════════════════════════════════

"""

            # Enviar relatório técnico completo
            await update.message.reply_text(
                technical_header,
                parse_mode="Markdown",
            )

            # Enviar showcase report
            if len(showcase_report) > 4000:
                parts = [
                    showcase_report[i : i + 4000]
                    for i in range(0, len(showcase_report), 4000)
                ]
                for i, part in enumerate(parts, 1):
                    await update.message.reply_text(
                        f"**SHOWCASE PART {i}:**\n\n{part}",
                        parse_mode="Markdown",
                    )
            else:
                await update.message.reply_text(showcase_report, parse_mode="Markdown")

            # Separador
            await update.message.reply_text(
                "═══════════════════════════════════════════════"
            )

            # Enviar stats técnicas
            if len(stats_report) > 4000:
                parts = [
                    stats_report[i : i + 4000]
                    for i in range(0, len(stats_report), 4000)
                ]
                for i, part in enumerate(parts, 1):
                    await update.message.reply_text(
                        f"**STATS TÉCNICAS PART {i}:**\n\n{part}",
                        parse_mode="Markdown",
                    )
            else:
                await update.message.reply_text(stats_report, parse_mode="Markdown")

            # Separador
            await update.message.reply_text(
                "═══════════════════════════════════════════════"
            )

            # Enviar relatório de sugestões
            await update.message.reply_text(suggestions_report, parse_mode="Markdown")

            # Footer técnico
            footer = """
═══════════════════════════════════════════════
🎯 **CAPACIDADES TÉCNICAS DEMONSTRADAS:**

✅ Monitoramento em tempo real
✅ Análise de padrões de uso
✅ Sistema de feedback integrado
✅ Métricas de performance
✅ Relatórios automatizados
✅ Escalabilidade comprovada

📊 _Relatório gerado automaticamente pelo sistema de monitoramento_
"""
            await update.message.reply_text(footer, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Erro ao gerar showcase detalhado: {e}")
            await update.message.reply_text(
                "❌ Erro ao gerar relatório técnico detalhado.",
            )

        return ConversationHandler.END

    async def contato(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Comando /contato - Informações para contratar serviços de bot personalizado"""
        user = update.effective_user
        if not user:
            return ConversationHandler.END

        # Registrar usuário e atividade
        monitoring.register_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
        )
        monitoring.register_activity(user.id, "command", "/contato")

        contact_message = """
🤖 **BOT PERSONALIZADO PARA SEU NEGÓCIO**

💼 **VALOR PARA SUA EMPRESA:**
• ✅ **Automatização 24/7** - Atendimento contínuo aos clientes
• ✅ **Redução de custos** - Diminui carga da equipe de suporte
• ✅ **Experiência premium** - Clientes satisfeitos e engajados
• ✅ **Análise inteligente** - Dados e insights em tempo real
• ✅ **Escalabilidade total** - Atende milhares simultaneamente
• ✅ **ROI comprovado** - Retorno rápido do investimento

🎯 **SOLUÇÕES PERSONALIZADAS:**
• 📊 Bots para contabilidade e consultoria fiscal
• 🏥 Assistentes virtuais para clínicas e hospitais
• 🏢 Automação de atendimento empresarial
• 📚 Sistemas educacionais interativos
• 🛍️ E-commerce e vendas automatizadas
• ⚖️ Consultoria jurídica inteligente

🚀 **TECNOLOGIA DE PONTA:**
• 🧠 Inteligência Artificial avançada (Groq/OpenAI)
• 📱 Integração completa com Telegram
• 📊 Sistema de monitoramento e análise
• 🔒 Segurança e privacidade garantidas
• 🛠️ Manutenção e suporte contínuo

💰 **INVESTIMENTO ACESSÍVEL:**
• Preços competitivos
• Pagamento facilitado
• Retorno rápido garantido

📞 **ENTRE EM CONTATO AGORA:**
👨‍💼 **Administrador:** @bgtfx8

💬 **Vamos conversar sobre seu projeto!**
_Análise gratuita das suas necessidades_
_Proposta personalizada sem compromisso_

🎁 **OFERTA ESPECIAL:** Demonstração gratuita do seu bot personalizado!
"""

        await update.message.reply_text(
            contact_message,
            parse_mode="Markdown",
        )

        return ConversationHandler.END

    async def mensagem_livre(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Processa mensagens livres (conversação natural)"""
        user = update.effective_user
        if not user or not update.message or not update.message.text:
            return ConversationHandler.END

        mensagem = update.message.text

        # Registrar usuário e atividade
        monitoring.register_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
        )
        monitoring.register_activity(user.id, "message", mensagem)

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

        # Estado para aguardar sugestão
        states[AGUARDANDO_SUGESTAO] = [
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.processar_sugestao)
        ]

        return ConversationHandler(
            entry_points=[
                CommandHandler("simular", self.simular),
                CommandHandler("sugestoes", self.sugestoes),
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
    application.add_handler(CommandHandler("contato", bot.contato))
    application.add_handler(CommandHandler("ajuda", bot.ajuda))
    application.add_handler(CommandHandler("reset", bot.reset))
    application.add_handler(CommandHandler("stats", bot.stats))
    application.add_handler(
        CommandHandler("showcase_detalhado", bot.showcase_detalhado)
    )

    # 2. Conversation handler para simulação e sugestões
    application.add_handler(bot.get_conversation_handler())

    # 3. Handler para mensagens livres (deve ser último)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, bot.mensagem_livre)
    )

    logger.info(
        "✅ Bot IRS Portugal configurado com Marinete e sistema de monitoramento!"
    )

    return application


if __name__ == "__main__":
    # Teste direto
    app = create_application()
    print("🤖 Bot IRS Portugal - Marinete iniciado!")
    app.run_polling()
