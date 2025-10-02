"""
Main Integration - Integra todo o fluxo após coleta das 20 perguntas
Adicione esta integração ao seu conversation_handler.py existente
"""

import json
import logging
from typing import Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Importar os novos módulos
from data_processor import DataProcessor, EmpresaProfile
from report_generator import ReportGenerator
from automation_manager import AutomationManager


class PostAnalysisHandler:
    """Handler para processar dados após as 20 perguntas"""

    def __init__(self):
        self.data_processor = DataProcessor()
        self.report_generator = ReportGenerator()
        self.automation_manager = AutomationManager()

    async def processar_respostas_completas(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Processa todas as respostas quando as 20 perguntas terminam"""

        user_id = update.effective_user.id

        # Recuperar respostas armazenadas (assumindo que estão em context.user_data)
        respostas = context.user_data.get("respostas_questionario", {})

        if len(respostas) < 20:
            await update.message.reply_text(
                "⚠️ Questionário incompleto! Faltam algumas respostas.\n"
                "Digite /reset para recomeçar."
            )
            return

        # Mostrar loading
        loading_msg = await update.message.reply_text(
            "🤖 **Analisando suas respostas...**\n"
            "⏳ Processando dados empresariais...\n"
            "📊 Gerando diagnóstico...\n"
            "📋 Criando plano de ação..."
        )

        try:
            # 1. Processar dados
            profile = self.data_processor.processar_respostas(respostas)
            insights = self.data_processor.gerar_insights(profile)

            # 2. Salvar perfil para uso futuro
            context.user_data["empresa_profile"] = profile.__dict__
            context.user_data["insights"] = insights

            # 3. Deletar mensagem de loading
            await loading_msg.delete()

            # 4. Enviar relatório completo
            relatorio_completo = self.report_generator.gerar_relatorio_completo(
                profile, insights
            )

            # Dividir relatório se for muito longo (Telegram tem limite)
            if len(relatorio_completo) > 4000:
                partes = self._dividir_texto(relatorio_completo, 3800)
                for i, parte in enumerate(partes):
                    await update.message.reply_text(
                        parte, parse_mode="Markdown", disable_web_page_preview=True
                    )
                    if i < len(partes) - 1:  # Não esperar na última parte
                        import asyncio

                        await asyncio.sleep(1)  # Evitar rate limit
            else:
                await update.message.reply_text(
                    relatorio_completo,
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                )

            # 5. Mostrar menu de opções
            await self._mostrar_menu_pos_analise(update, context)

        except Exception as e:
            await loading_msg.delete()
            await update.message.reply_text(
                f"❌ Erro ao processar dados. Tente novamente.\nErro técnico: {str(e)}"
            )
            logging.error(f"Erro no processamento: {e}")

    async def _mostrar_menu_pos_analise(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Mostra menu com opções após análise"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "📋 Ver Plano de Ação", callback_data="plano_acao"
                ),
                InlineKeyboardButton(
                    "📊 Relatório Executivo", callback_data="relatorio_exec"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🤖 Cronograma de Automações", callback_data="cronograma"
                ),
                InlineKeyboardButton(
                    "💰 Análise Financeira", callback_data="analise_financeira"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🚀 Implementar Automação", callback_data="implementar"
                ),
                InlineKeyboardButton(
                    "📞 Falar com Especialista", callback_data="contato"
                ),
            ],
            [
                InlineKeyboardButton("🔄 Refazer Diagnóstico", callback_data="reset"),
                InlineKeyboardButton("💾 Salvar Relatório", callback_data="salvar"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🎯 **O que você gostaria de fazer agora?**\n\n"
            "Escolha uma opção abaixo para continuar:",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )

    def _dividir_texto(self, texto: str, max_length: int) -> list:
        """Divide texto em partes menores respeitando linhas"""
        if len(texto) <= max_length:
            return [texto]

        partes = []
        linhas = texto.split("\n")
        parte_atual = ""

        for linha in linhas:
            if len(parte_atual + linha + "\n") > max_length:
                if parte_atual:
                    partes.append(parte_atual)
                    parte_atual = linha + "\n"
                else:
                    # Linha muito longa, forçar quebra
                    partes.append(linha[:max_length])
                    parte_atual = linha[max_length:] + "\n"
            else:
                parte_atual += linha + "\n"

        if parte_atual:
            partes.append(parte_atual)

        return partes

    async def callback_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handles callback queries from the post-analysis menu"""
        query = update.callback_query
        await query.answer()

        data = query.data
        if data == "plano_acao":
            await query.edit_message_text("Aqui está o Plano de Ação: [detalhes]")
        elif data == "relatorio_exec":
            await query.edit_message_text("Relatório Executivo: [detalhes]")
        elif data == "cronograma":
            await query.edit_message_text("Cronograma de Automações: [detalhes]")
        elif data == "analise_financeira":
            await query.edit_message_text("Análise Financeira: [detalhes]")
        elif data == "implementar":
            await query.edit_message_text("Implementando Automação: [detalhes]")
        elif data == "contato":
            await query.edit_message_text("Contato com Especialista: [detalhes]")
        elif data == "reset":
            await query.edit_message_text("Refazendo Diagnóstico...")
        elif data == "salvar":
            await query.edit_message_text("Salvando Relatório...")
        else:
            await query.edit_message_text("Opção inválida.")


print("✅ Main Integration module criado!")
