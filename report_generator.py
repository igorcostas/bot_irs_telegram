"""
Report Generator - Gera relatórios personalizados baseados no perfil da empresa
"""

import json
import datetime
from typing import Dict, List, Any
from data_processor import EmpresaProfile, DataProcessor


class ReportGenerator:
    def __init__(self):
        self.templates = {
            "diagnostico": self._template_diagnostico,
            "plano_acao": self._template_plano_acao,
            "relatorio_executivo": self._template_executivo,
            "proposta_automacao": self._template_proposta,
        }

    def gerar_relatorio_completo(self, profile: EmpresaProfile, insights: Dict) -> str:
        """Gera relatório completo para o Telegram"""
        relatorio = f"""🏢 **DIAGNÓSTICO EMPRESARIAL COMPLETO**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **DADOS DA EMPRESA**
• Nome: {profile.nome}
• Regime Tributário: {profile.regime_tributario}
• Faturamento Mensal: R$ {profile.faturamento_mensal:,.2f}
• Funcionários: {profile.funcionarios}
• Atividade: {profile.atividade_principal}
• Score Organização: {profile.score_organizacao}/10 {"🟢" if profile.score_organizacao >= 7 else "🟡" if profile.score_organizacao >= 5 else "🔴"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 **PROBLEMAS IDENTIFICADOS**
"""

        if profile.problemas_identificados:
            for i, problema in enumerate(profile.problemas_identificados, 1):
                relatorio += f"{i}. ❌ {problema}\n"
        else:
            relatorio += "✅ Nenhum problema crítico identificado\n"

        relatorio += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ **URGÊNCIAS** (Ação Imediata)
"""

        if profile.urgencias:
            for i, urgencia in enumerate(profile.urgencias, 1):
                relatorio += f"{i}. 🔥 {urgencia}\n"
        else:
            relatorio += "✅ Nenhuma urgência identificada\n"

        relatorio += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 **AUTOMAÇÕES RECOMENDADAS**
"""

        if profile.automacoes_sugeridas:
            for i, automacao in enumerate(profile.automacoes_sugeridas, 1):
                relatorio += f"{i}. ⚙️ {automacao}\n"
        else:
            relatorio += "ℹ️ Nenhuma automação prioritária identificada\n"

        # Adicionar insights de economia
        if insights["economia_estimada"] > 0:
            relatorio += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 **IMPACTO FINANCEIRO ESTIMADO**
• Economia mensal: R$ {insights["economia_estimada"]:,.2f}
• Tempo economizado: {insights["tempo_economizado"]}h/mês
• ROI estimado: {self._calcular_roi(insights["economia_estimada"])}

"""

        # Prioridades
        relatorio += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **PRÓXIMOS PASSOS PRIORITÁRIOS**
"""

        for i, prioridade in enumerate(insights["prioridades"], 1):
            relatorio += f"{i}. 📌 {prioridade}\n"

        # Recomendações
        if insights["recomendacoes"]:
            relatorio += f"""
💡 **RECOMENDAÇÕES ESTRATÉGICAS**
"""
            for i, rec in enumerate(insights["recomendacoes"], 1):
                relatorio += f"{i}. 💭 {rec}\n"

        relatorio += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Relatório gerado em: {datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")}
🤖 Assistente: Maria - Técnica Contábil Virtual

➡️ **QUER IMPLEMENTAR ALGUMA AUTOMAÇÃO?**
Digite /plano para ver o plano de ação detalhado!
"""

        return relatorio

    def gerar_plano_acao(self, profile: EmpresaProfile, insights: Dict) -> str:
        """Gera plano de ação específico"""

        plano = f"""📋 **PLANO DE AÇÃO - {profile.nome}**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **OBJETIVO**: Automatizar processos e otimizar operações

📊 **SITUAÇÃO ATUAL**
• Score Organização: {profile.score_organizacao}/10
• Problemas ativos: {len(profile.problemas_identificados)}
• Urgências: {len(profile.urgencias)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 **CRONOGRAMA DE IMPLEMENTAÇÃO**

**🔥 FASE 1 - URGÊNCIAS (0-15 dias)**
"""

        if profile.urgencias:
            for i, urgencia in enumerate(profile.urgencias, 1):
                prazo, acao = self._definir_acao_urgencia(urgencia)
                plano += f"""
{i}. {urgencia}
   ⏰ Prazo: {prazo}
   📝 Ação: {acao}
"""
        else:
            plano += "✅ Nenhuma urgência identificada\n"

        plano += f"""
**⚡ FASE 2 - AUTOMAÇÕES RÁPIDAS (15-45 dias)**
"""

        automacoes_rapidas = [
            auto
            for auto in profile.automacoes_sugeridas
            if "relatório" in auto or "conciliação" in auto
        ][:2]

        for i, auto in enumerate(automacoes_rapidas, 1):
            prazo, custo, beneficio = self._definir_detalhes_automacao(auto)
            plano += f"""
{i}. {auto}
   ⏰ Prazo: {prazo}
   💰 Custo estimado: {custo}
   📈 Benefício: {beneficio}
"""

        plano += f"""
**🏗️ FASE 3 - AUTOMAÇÕES COMPLEXAS (45-90 dias)**
"""

        automacoes_complexas = [
            auto
            for auto in profile.automacoes_sugeridas
            if auto not in automacoes_rapidas
        ]

        for i, auto in enumerate(automacoes_complexas, 1):
            prazo, custo, beneficio = self._definir_detalhes_automacao(auto)
            plano += f"""
{i}. {auto}
   ⏰ Prazo: {prazo}
   💰 Custo estimado: {custo}
   📈 Benefício: {beneficio}
"""

        # Resumo financeiro
        plano += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 **RESUMO FINANCEIRO**
• Investimento total: R$ {self._calcular_investimento_total(profile):,.2f}
• Economia mensal: R$ {insights["economia_estimada"]:,.2f}
• Retorno em: {self._calcular_payback(insights["economia_estimada"], profile)} meses
• Tempo economizado: {insights["tempo_economizado"]}h/mês

🎯 **METAS DE RESULTADO**
• Reduzir processos manuais em 80%
• Aumentar produtividade em 60%
• Eliminar atrasos fiscais em 100%
• Score organização target: 9/10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Plano criado em: {datetime.datetime.now().strftime("%d/%m/%Y")}

➡️ **PRÓXIMO PASSO**: Digite /implementar para começar!
"""

        return plano

    def gerar_relatorio_executivo(self, profile: EmpresaProfile, insights: Dict) -> str:
        """Gera relatório executivo resumido"""

        return f"""👔 **RELATÓRIO EXECUTIVO**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **DIAGNÓSTICO**: {profile.nome}

**🎯 OPORTUNIDADE IDENTIFICADA**
Implementação de automações pode economizar R$ {insights["economia_estimada"]:,.2f}/mês e {insights["tempo_economizado"]}h de trabalho.

**📈 POTENCIAL DE MELHORIA**
• Atual: {profile.score_organizacao}/10
• Target: 9/10
• Melhoria: {9 - profile.score_organizacao} pontos

**💡 RECOMENDAÇÃO PRINCIPAL**
{insights["prioridades"][0] if insights["prioridades"] else "Manter processos atuais"}

**⚡ AÇÃO IMEDIATA**
{profile.urgencias[0] if profile.urgencias else "Planejar implementação gradual"}

**💰 ROI PROJETADO**
{self._calcular_roi(insights["economia_estimada"])} em {self._calcular_payback(insights["economia_estimada"], profile)} meses

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Para relatório completo: /relatorio
"""

    def _calcular_roi(self, economia_mensal: float) -> str:
        """Calcula ROI estimado"""
        if economia_mensal > 5000:
            return "ROI Alto (>300%)"
        elif economia_mensal > 2000:
            return "ROI Médio (150-300%)"
        else:
            return "ROI Baixo (<150%)"

    def _calcular_payback(self, economia_mensal: float, profile: EmpresaProfile) -> int:
        """Calcula payback em meses"""
        investimento = self._calcular_investimento_total(profile)
        if economia_mensal > 0:
            return max(1, int(investimento / economia_mensal))
        return 12

    def _calcular_investimento_total(self, profile: EmpresaProfile) -> float:
        """Estima investimento total"""
        base = 5000  # Custo base
        if profile.funcionarios > 20:
            base *= 1.5
        if profile.faturamento_mensal > 200000:
            base *= 1.3
        return base

    def _definir_acao_urgencia(self, urgencia: str) -> tuple:
        """Define ação específica para urgência"""
        acoes = {
            "ECF com prazo próximo": (
                "3 dias",
                "Organizar documentos e transmitir ECF",
            ),
            "SPED Fiscal pendente": ("7 dias", "Revisar movimentação e enviar SPED"),
            "Folha de pagamento em atraso": (
                "2 dias",
                "Processar e enviar folha urgentemente",
            ),
        }
        return acoes.get(urgencia, ("7 dias", "Ação corretiva imediata"))

    def _definir_detalhes_automacao(self, automacao: str) -> tuple:
        """Define detalhes de cada automação"""
        detalhes = {
            "Automação de lançamento de NF-e": (
                "30 dias",
                "R$ 2.000",
                "40h/mês economizadas",
            ),
            "Automação da conciliação bancária": (
                "20 dias",
                "R$ 1.500",
                "20h/mês economizadas",
            ),
            "Automação da folha de pagamento": (
                "45 dias",
                "R$ 3.000",
                "30h/mês economizadas",
            ),
            "Geração automática de relatórios": (
                "15 dias",
                "R$ 1.000",
                "15h/mês economizadas",
            ),
        }
        return detalhes.get(automacao, ("30 dias", "R$ 1.500", "10h/mês economizadas"))

    def _template_diagnostico(self):
        pass

    def _template_plano_acao(self):
        pass

    def _template_executivo(self):
        pass

    def _template_proposta(self):
        pass
