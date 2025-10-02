# 4. MAIN INTEGRATION - Integra todo o fluxo após as 20 perguntas
main_integration_code = '''"""
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
        
    async def processar_respostas_completas(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Processa todas as respostas quando as 20 perguntas terminam"""
        
        user_id = update.effective_user.id
        
        # Recuperar respostas armazenadas (assumindo que estão em context.user_data)
        respostas = context.user_data.get('respostas_questionario', {})
        
        if len(respostas) < 20:
            await update.message.reply_text(
                "⚠️ Questionário incompleto! Faltam algumas respostas.\\n"
                "Digite /reset para recomeçar."
            )
            return
        
        # Mostrar loading
        loading_msg = await update.message.reply_text(
            "🤖 **Analisando suas respostas...**\\n"
            "⏳ Processando dados empresariais...\\n" 
            "📊 Gerando diagnóstico...\\n"
            "📋 Criando plano de ação..."
        )
        
        try:
            # 1. Processar dados
            profile = self.data_processor.processar_respostas(respostas)
            insights = self.data_processor.gerar_insights(profile)
            
            # 2. Salvar perfil para uso futuro
            context.user_data['empresa_profile'] = profile.__dict__
            context.user_data['insights'] = insights
            
            # 3. Deletar mensagem de loading
            await loading_msg.delete()
            
            # 4. Enviar relatório completo
            relatorio_completo = self.report_generator.gerar_relatorio_completo(profile, insights)
            
            # Dividir relatório se for muito longo (Telegram tem limite)
            if len(relatorio_completo) > 4000:
                partes = self._dividir_texto(relatorio_completo, 3800)
                for i, parte in enumerate(partes):
                    await update.message.reply_text(
                        parte, 
                        parse_mode='Markdown',
                        disable_web_page_preview=True
                    )
                    if i < len(partes) - 1:  # Não esperar na última parte
                        import asyncio
                        await asyncio.sleep(1)  # Evitar rate limit
            else:
                await update.message.reply_text(
                    relatorio_completo,
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                )
            
            # 5. Mostrar menu de opções
            await self._mostrar_menu_pos_analise(update, context)
            
        except Exception as e:
            await loading_msg.delete()
            await update.message.reply_text(
                "❌ Erro ao processar dados. Tente novamente.\\n"
                f"Erro técnico: {str(e)}"
            )
            logging.error(f"Erro no processamento: {e}")
    
    async def _mostrar_menu_pos_analise(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mostra menu com opções após análise"""
        
        keyboard = [
            [
                InlineKeyboardButton("📋 Ver Plano de Ação", callback_data="plano_acao"),
                InlineKeyboardButton("📊 Relatório Executivo", callback_data="relatorio_exec")
            ],
            [
                InlineKeyboardButton("🤖 Cronograma de Automações", callback_data="cronograma"),
                InlineKeyboardButton("💰 Análise Financeira", callback_data="analise_financeira")
            ],
            [
                InlineKeyboardButton("🚀 Implementar Automação", callback_data="implementar"),
                InlineKeyboardButton("📞 Falar com Especialista", callback_data="contato")
            ],
            [
                InlineKeyboardButton("🔄 Refazer Diagnóstico", callback_data="reset"),
                InlineKeyboardButton("💾 Salvar Relatório", callback_data="salvar")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎯 **O que você gostaria de fazer agora?**\\n\\n"
            "Escolha uma opção abaixo para continuar:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para callbacks dos botões"""
        
        query = update.callback_query
        await query.answer()
        
        profile_data = context.user_data.get('empresa_profile')
        insights = context.user_data.get('insights')
        
        if not profile_data or not insights:
            await query.message.reply_text(
                "❌ Dados não encontrados. Execute o diagnóstico novamente.\\n"
                "Digite /start para começar."
            )
            return
        
        # Reconstruir objetos
        profile = EmpresaProfile(**profile_data)
        
        if query.data == "plano_acao":
            await self._enviar_plano_acao(query, profile, insights)
            
        elif query.data == "relatorio_exec":
            await self._enviar_relatorio_executivo(query, profile, insights)
            
        elif query.data == "cronograma":
            await self._enviar_cronograma(query, profile, insights)
            
        elif query.data == "analise_financeira":
            await self._enviar_analise_financeira(query, profile, insights)
            
        elif query.data == "implementar":
            await self._iniciar_implementacao(query, context, profile)
            
        elif query.data == "contato":
            await self._mostrar_contato(query)
            
        elif query.data == "reset":
            await self._reset_questionario(query, context)
            
        elif query.data == "salvar":
            await self._salvar_relatorio(query, context, profile, insights)
    
    async def _enviar_plano_acao(self, query, profile, insights):
        """Envia plano de ação detalhado"""
        plano = self.report_generator.gerar_plano_acao(profile, insights)
        
        # Dividir se necessário
        if len(plano) > 4000:
            partes = self._dividir_texto(plano, 3800)
            for parte in partes:
                await query.message.reply_text(parte, parse_mode='Markdown')
        else:
            await query.message.reply_text(plano, parse_mode='Markdown')
    
    async def _enviar_relatorio_executivo(self, query, profile, insights):
        """Envia relatório executivo"""
        relatorio = self.report_generator.gerar_relatorio_executivo(profile, insights)
        await query.message.reply_text(relatorio, parse_mode='Markdown')
    
    async def _enviar_cronograma(self, query, profile, insights):
        """Envia cronograma de automações"""
        tasks = self.automation_manager.criar_roadmap_automacao(profile)
        cronograma = self.automation_manager.gerar_cronograma_telegram(tasks)
        
        if len(cronograma) > 4000:
            partes = self._dividir_texto(cronograma, 3800)
            for parte in partes:
                await query.message.reply_text(parte, parse_mode='Markdown')
        else:
            await query.message.reply_text(cronograma, parse_mode='Markdown')
    
    async def _enviar_analise_financeira(self, query, profile, insights):
        """Envia análise financeira detalhada"""
        analise = f"""
💰 **ANÁLISE FINANCEIRA DETALHADA**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **SITUAÇÃO ATUAL - {profile.nome}**
• Faturamento mensal: R$ {profile.faturamento_mensal:,.2f}
• Regime tributário: {profile.regime_tributario}
• Funcionários: {profile.funcionarios}
• Score organização: {profile.score_organizacao}/10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 **OPORTUNIDADES IDENTIFICADAS**
• Economia mensal potencial: R$ {insights['economia_estimada']:,.2f}
• Tempo economizado: {insights['tempo_economizado']}h/mês
• Investimento necessário: R$ {self._calcular_investimento_total(profile):,.2f}

📈 **PROJEÇÃO DE RESULTADOS**
• Payback: {self._calcular_payback(insights['economia_estimada'], profile)} meses
• ROI anual: {int((insights['economia_estimada'] * 12 / self._calcular_investimento_total(profile)) * 100)}%
• Economia anual: R$ {insights['economia_estimada'] * 12:,.2f}

🎯 **RECOMENDAÇÃO**
Com base na análise, recomendamos implementar as automações em {len(profile.automacoes_sugeridas)} fases para maximizar o retorno.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        await query.message.reply_text(analise, parse_mode='Markdown')
    
    def _dividir_texto(self, texto: str, max_length: int) -> list:
        """Divide texto em partes menores respeitando linhas"""
        if len(texto) <= max_length:
            return [texto]
        
        partes = []
        linhas = texto.split('\\n')
        parte_atual = ""
        
        for linha in linhas:
            if len(parte_atual + linha + '\\n') > max_length:
                if parte_atual:
                    partes.append(parte_atual)
                    parte_atual = linha + '\\n'
                else:
                    # Linha muito longa, forçar quebra
                    partes.append(linha[:max_length])
                    parte_atual = linha[max_length:] + '\\n'
            else:
                parte_atual += linha + '\\n'
        
        if parte_atual:
            partes.append(parte_atual)
        
        return partes
    
    def _calcular_investimento_total(self, profile):
        """Calcula investimento total estimado"""
        base = 5000
        if profile.funcionarios > 20:
            base *= 1.5
        if profile.faturamento_mensal > 200000:
            base *= 1.3
        return base
    
    def _calcular_payback(self, economia_mensal, profile):
        """Calcula payback em meses"""
        investimento = self._calcular_investimento_total(profile)
        if economia_mensal > 0:
            return max(1, int(investimento / economia_mensal))
        return 12

# EXEMPLO DE INTEGRAÇÃO COM SEU CÓDIGO EXISTENTE
"""
No seu conversation_handler.py, adicione:

from main_integration import PostAnalysisHandler

class ConversationHandler:
    def __init__(self):
        # ... seu código existente
        self.post_analysis = PostAnalysisHandler()
    
    async def finalizar_questionario(self, update, context):
        '''Chama quando termina as 20 perguntas'''
        await self.post_analysis.processar_respostas_completas(update, context)
    
    # Registrar o callback handler
    application.add_handler(CallbackQueryHandler(self.post_analysis.callback_handler))
"""

print("✅ Main Integration criado!")
print("Integra todos os módulos após as 20 perguntas")
'''

# Salvar arquivo
with open('main_integration.py', 'w', encoding='utf-8') as f:
    f.write(main_integration_code)

print("✅ main_integration.py criado com sucesso!")
print("Contém:")
print("- Integração completa com seu bot existente") 
print("- Menu interativo pós-análise")
print("- Handlers para todos os relatórios")
print("- Sistema de callbacks para botões")
print("- Divisão automática de mensagens longas")