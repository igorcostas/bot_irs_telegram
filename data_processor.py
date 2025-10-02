"""
Data Processor - Analisa e processa dados coletados das 20 perguntas
"""
import json
import datetime
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class EmpresaProfile:
    """Perfil completo da empresa baseado nas respostas"""
    nome: str
    regime_tributario: str
    faturamento_mensal: float
    funcionarios: int
    atividade_principal: str
    problemas_identificados: List[str]
    urgencias: List[str]
    automacoes_sugeridas: List[str]
    score_organizacao: int  # 1-10

class DataProcessor:
    def __init__(self):
        self.weights = {
            'faturamento': 0.3,
            'funcionarios': 0.2,
            'organizacao': 0.25,
            'tecnologia': 0.25
        }

    def processar_respostas(self, respostas: Dict[str, Any]) -> EmpresaProfile:
        """Processa as 20 respostas e cria perfil da empresa"""

        # Extrair informações básicas
        nome = respostas.get('nome_empresa', 'Empresa')
        regime = self._identificar_regime(respostas)
        faturamento = self._calcular_faturamento(respostas)
        funcionarios = respostas.get('num_funcionarios', 0)
        atividade = respostas.get('atividade_principal', 'Não informado')

        # Análise de problemas
        problemas = self._identificar_problemas(respostas)
        urgencias = self._identificar_urgencias(respostas)
        automacoes = self._sugerir_automacoes(respostas)
        score = self._calcular_score_organizacao(respostas)

        return EmpresaProfile(
            nome=nome,
            regime_tributario=regime,
            faturamento_mensal=faturamento,
            funcionarios=funcionarios,
            atividade_principal=atividade,
            problemas_identificados=problemas,
            urgencias=urgencias,
            automacoes_sugeridas=automacoes,
            score_organizacao=score
        )

    def _identificar_regime(self, respostas: Dict) -> str:
        """Identifica regime tributário baseado no faturamento"""
        faturamento_anual = respostas.get('faturamento_anual', 0)

        if faturamento_anual <= 4800000:  # 4.8M
            return "Simples Nacional"
        elif faturamento_anual <= 78000000:  # 78M  
            return "Lucro Presumido"
        else:
            return "Lucro Real"

    def _calcular_faturamento(self, respostas: Dict) -> float:
        """Calcula faturamento mensal estimado"""
        if 'faturamento_mensal' in respostas:
            return float(respostas['faturamento_mensal'])
        elif 'faturamento_anual' in respostas:
            return float(respostas['faturamento_anual']) / 12
        else:
            return 0.0

    def _identificar_problemas(self, respostas: Dict) -> List[str]:
        """Identifica problemas principais baseado nas respostas"""
        problemas = []

        # Análise baseada em padrões das respostas
        if respostas.get('atraso_obrigacoes', False):
            problemas.append("Atrasos em obrigações fiscais")

        if respostas.get('controle_manual', False):
            problemas.append("Processos manuais excessivos")

        if respostas.get('dificuldade_conciliacao', False):
            problemas.append("Dificuldades na conciliação bancária")

        if respostas.get('falta_relatorios', False):
            problemas.append("Ausência de relatórios gerenciais")

        if respostas.get('equipe_sobrecarregada', False):
            problemas.append("Equipe sobrecarregada")

        return problemas

    def _identificar_urgencias(self, respostas: Dict) -> List[str]:
        """Identifica urgências que precisam ação imediata"""
        urgencias = []

        # Prazos fiscais próximos
        if respostas.get('prazo_ecf_proximo', False):
            urgencias.append("ECF com prazo próximo")

        if respostas.get('sped_pendente', False):
            urgencias.append("SPED Fiscal pendente")

        if respostas.get('folha_atrasada', False):
            urgencias.append("Folha de pagamento em atraso")

        return urgencias

    def _sugerir_automacoes(self, respostas: Dict) -> List[str]:
        """Sugere automações baseadas no perfil"""
        automacoes = []

        if respostas.get('volume_nfs_alto', False):
            automacoes.append("Automação de lançamento de NF-e")

        if respostas.get('conciliacao_manual', False):
            automacoes.append("Automação da conciliação bancária")

        if respostas.get('folha_complexa', False):
            automacoes.append("Automação da folha de pagamento")

        if respostas.get('relatorios_manuais', False):
            automacoes.append("Geração automática de relatórios")

        return automacoes

    def _calcular_score_organizacao(self, respostas: Dict) -> int:
        """Calcula score de organização de 1-10"""
        pontos = 0
        total_criterios = 0

        # Critérios de organização
        criterios = [
            'usa_sistema_integrado',
            'backups_regulares', 
            'processos_documentados',
            'controles_internos',
            'equipe_treinada'
        ]

        for criterio in criterios:
            total_criterios += 1
            if respostas.get(criterio, False):
                pontos += 1

        # Penalidades
        if respostas.get('atraso_obrigacoes', False):
            pontos -= 1
        if respostas.get('controle_manual', False):
            pontos -= 1

        score = max(1, min(10, int((pontos / max(1, total_criterios)) * 10)))
        return score

    def gerar_insights(self, profile: EmpresaProfile) -> Dict[str, Any]:
        """Gera insights inteligentes baseados no perfil"""
        insights = {
            'prioridades': [],
            'economia_estimada': 0,
            'tempo_economizado': 0,
            'recomendacoes': []
        }

        # Prioridades baseadas em urgências e problemas
        if profile.urgencias:
            insights['prioridades'] = profile.urgencias[:3]
        else:
            insights['prioridades'] = profile.problemas_identificados[:3]

        # Estimativa de economia com automações
        economia_por_automacao = {
            'Automação de lançamento de NF-e': 2000,
            'Automação da conciliação bancária': 1500,
            'Automação da folha de pagamento': 3000,
            'Geração automática de relatórios': 1000
        }

        economia_total = sum(
            economia_por_automacao.get(auto, 500) 
            for auto in profile.automacoes_sugeridas
        )
        insights['economia_estimada'] = economia_total

        # Tempo economizado (horas/mês)
        tempo_por_automacao = {
            'Automação de lançamento de NF-e': 40,
            'Automação da conciliação bancária': 20,
            'Automação da folha de pagamento': 30,
            'Geração automática de relatórios': 15
        }

        tempo_total = sum(
            tempo_por_automacao.get(auto, 10)
            for auto in profile.automacoes_sugeridas
        )
        insights['tempo_economizado'] = tempo_total

        # Recomendações específicas
        if profile.score_organizacao < 5:
            insights['recomendacoes'].append("Implementar controles internos básicos")
        if profile.faturamento_mensal > 100000 and not any('sistema_integrado' in str(profile.__dict__)):
            insights['recomendacoes'].append("Migrar para sistema integrado")
        if len(profile.problemas_identificados) > 3:
            insights['recomendacoes'].append("Reorganizar processos antes das automações")

        return insights

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de dados coletados
    exemplo_respostas = {
        'nome_empresa': 'Exemplo Comércio Ltda',
        'faturamento_anual': 2400000,
        'num_funcionarios': 15,
        'atividade_principal': 'Comércio varejista',
        'atraso_obrigacoes': True,
        'controle_manual': True,
        'volume_nfs_alto': True,
        'usa_sistema_integrado': False,
        'equipe_sobrecarregada': True
    }

    processor = DataProcessor()
    profile = processor.processar_respostas(exemplo_respostas)
    insights = processor.gerar_insights(profile)

    print("PERFIL PROCESSADO:")
    print(f"Empresa: {profile.nome}")
    print(f"Regime: {profile.regime_tributario}")
    print(f"Score Organização: {profile.score_organizacao}/10")
    print(f"Problemas: {len(profile.problemas_identificados)}")
    print(f"Automações sugeridas: {len(profile.automacoes_sugeridas)}")
