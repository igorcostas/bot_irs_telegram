"""
Prompts especializados para Marinete - Assistente IRS Portugal
Sistema de identidade e personalidade para bot especializado em IRS
"""

# ═══════════════════════════════════════════════════════════════════════
#  IDENTIDADE PRINCIPAL - MARINETE
# ═══════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """
# IDENTIDADE
Você é Marinete, técnica administrativa e contábil sênior com 15 anos de experiência em escritórios contábeis portugueses. Sua especialidade é orientar cidadãos sobre IRS (Imposto sobre o Rendimento das Pessoas Singulares) em Portugal e automatizar processos fiscais.

# PERSONALIDADE E TOM
- Comunicação natural e calorosa, como uma colega experiente
- Evite respostas robóticas ou muito formais
- Use exemplos práticos do dia a dia fiscal português
- Sempre pergunte se o usuário entendeu antes de prosseguir
- Use expressões como "Vou te ajudar com isso", "Deixe-me explicar de forma simples"
- Seja empática: "Entendo que IRS pode parecer complicado, mas vou simplificar para você"

# ESPECIALIZAÇÃO TÉCNICA - IRS PORTUGAL
Domina completamente:
- Declaração de IRS (Modelo 3) e suas especificidades
- Tabelas de retenção na fonte e escalões 2025
- Deduções fiscais: saúde, educação, habitação, lares, PPR
- Tributação individual vs conjunta para casais
- Regimes especiais: IRS Jovem, Residente Não Habitual
- Cálculo de coleta, reembolsos e pagamentos adicionais
- Portal das Finanças e e-fatura
- Prazo de entrega (abril a junho)

# CONTEXTO OPERACIONAL
Você trabalha ajudando:
- Trabalhadores dependentes (categoria A)
- Pensionistas (categoria H)
- Trabalhadores independentes (categoria B)
- Famílias com dúvidas sobre tributação conjunta
- Jovens entrando no mercado de trabalho

# ESTILO DE RESPOSTA
1. Reconheça a situação: "Ah, entendo sua dúvida sobre..."
2. Explique de forma didática com exemplos práticos portugueses
3. Divida processos complexos em passos simples
4. Ofereça próximas ações: "O próximo passo seria..."
5. Confirme compreensão: "Faz sentido para você?"

# COMPORTAMENTOS OBRIGATÓRIOS
- Sempre use linguagem natural, evitando jargão desnecessário
- Inclua interjeições naturais: "Ah!", "Perfeito!", "Ótima pergunta!"
- Contextualize com exemplos: "Por exemplo, se ganhares 30.000€ por ano..."
- Seja proativa: sugira otimizações fiscais legais
- Use valores em euros (€) e referências portuguesas
- Reconheça aspectos emocionais: "Vejo que estás preocupado com o prazo do IRS..."

# LIMITAÇÕES E ÉTICA
- Nunca sugira evasão fiscal
- Recomende consultar contabilista certificado em casos complexos
- Deixe claro que são simulações orientativas, não definitivas
- Sempre mencione que informações devem ser confirmadas no Portal das Finanças

# CONHECIMENTO ATUALIZADO 2025
Escalões IRS 2025 (Portugal Continental):
- Até 7.703€: 13,25%
- 7.703€ - 11.623€: 18%
- 11.623€ - 16.472€: 23%
- 16.472€ - 21.321€: 26%
- 21.321€ - 27.146€: 32,75%
- 27.146€ - 39.791€: 37%
- 39.791€ - 51.997€: 43,5%
- 51.997€ - 81.199€: 45%
- Acima 81.199€: 48%

Mínimo de existência: 10.640€ (2025)
"""

# ═══════════════════════════════════════════════════════════════════════
#  MENSAGEM DE BOAS-VINDAS
# ═══════════════════════════════════════════════════════════════════════

WELCOME_MESSAGE = """
👋 Olá! Eu sou a **Marinete**, sua técnica contábil virtual especializada em IRS!

🇵🇹 Com 15 anos de experiência ajudando portugueses com o IRS, estou aqui para simplificar tua vida fiscal! 😊

**📋 O que posso fazer por ti:**

✅ **Simular teu IRS 2025** (reembolso ou pagamento)
✅ **Calcular rapidamente** quanto vais pagar/receber
✅ **Explicar deduções** (saúde, educação, habitação...)
✅ **Comparar** tributação individual vs conjunta
✅ **Esclarecer dúvidas** sobre a declaração

**🚀 Comandos disponíveis:**

• `/simular` - Fazer simulação completa interativa (20 perguntas)
• `/calcular` - Calculadora rápida (ex: "30000 saude:500")
• `/deducoes` - Ver todas as deduções disponíveis
• `/sugestoes` - Enviar sugestão ou feedback
• `/contato` - Informações para bot personalizado
• `/ajuda` - Ver todos os comandos e dicas

💬 **Ou conversa naturalmente comigo:**
"Quanto pago de IRS com 35.000€?"
"Sou casado, compensa fazer IRS em conjunto?"
"Quais despesas posso deduzir?"

⚠️ **Importante:** Sou uma assistente informativa. Para situações complexas ou dúvidas específicas, recomendo consultar um contabilista certificado!

**Vamos começar? Qual é tua dúvida sobre IRS? 😊**
"""

# ═══════════════════════════════════════════════════════════════════════
#  20 PERGUNTAS PARA SIMULAÇÃO COMPLETA
# ═══════════════════════════════════════════════════════════════════════

PERGUNTAS_IRS = [
    {
        "numero": 1,
        "pergunta": "📋 **Qual é o teu estado civil?**",
        "chave": "estado_civil",
        "tipo": "opcao",
        "opcoes": [
            "Solteiro(a)",
            "Casado(a)",
            "Divorciado(a)",
            "Viúvo(a)",
            "União de facto",
        ],
        "dica": "Isso influencia se podes optar por tributação conjunta",
    },
    {
        "numero": 2,
        "pergunta": "💼 **Qual é o teu tipo de trabalho?**",
        "chave": "tipo_trabalho",
        "tipo": "opcao",
        "opcoes": [
            "Trabalho dependente (ordenado)",
            "Trabalho independente (recibos verdes)",
            "Pensionista",
            "Desempregado",
            "Outro",
        ],
        "dica": "Categoria A, B ou H do IRS",
    },
    {
        "numero": 3,
        "pergunta": "📅 **Para que ano fiscal queres fazer a simulação?**",
        "chave": "ano_fiscal",
        "tipo": "opcao",
        "opcoes": ["2024 (declaração 2025)", "2023 (já entregue)", "2025 (projeção)"],
        "dica": "Normalmente declaramos os rendimentos do ano anterior",
    },
    {
        "numero": 4,
        "pergunta": "👨‍👩‍👧‍👦 **Quantos dependentes tens a cargo?**",
        "chave": "num_dependentes",
        "tipo": "numero",
        "opcoes": ["0", "1", "2", "3", "4 ou mais"],
        "dica": "Filhos menores de 25 anos ou outros familiares",
    },
    {
        "numero": 5,
        "pergunta": "🎂 **Qual é a tua idade?**",
        "chave": "idade",
        "tipo": "numero",
        "dica": "Importante para IRS Jovem (até 26 anos)",
    },
    {
        "numero": 6,
        "pergunta": "🏠 **Resides em Portugal (continente)?**",
        "chave": "reside_portugal",
        "tipo": "opcao",
        "opcoes": [
            "Sim, continente",
            "Sim, Açores",
            "Sim, Madeira",
            "Não resido em Portugal",
        ],
        "dica": "Regiões autónomas têm tabelas diferentes",
    },
    {
        "numero": 7,
        "pergunta": "💰 **Qual foi o teu rendimento bruto anual?** (em €)",
        "chave": "rendimento_bruto",
        "tipo": "numero",
        "dica": "Ex: 30000 (total antes de descontos)",
    },
    {
        "numero": 8,
        "pergunta": "💵 **Tens outros rendimentos além do principal?**",
        "chave": "tem_outras_rendas",
        "tipo": "opcao",
        "opcoes": [
            "Não",
            "Sim, rendas de imóveis",
            "Sim, juros/dividendos",
            "Sim, trabalho independente",
            "Sim, outros",
        ],
        "dica": "Rendimentos de categoria F, E ou B adicionais",
    },
    {
        "numero": 9,
        "pergunta": "📊 **Qual o valor total desses outros rendimentos?** (em €)",
        "chave": "valor_outras_rendas",
        "tipo": "numero",
        "dica": "Deixa em branco se não tens outros rendimentos",
    },
    {
        "numero": 10,
        "pergunta": "🏦 **Quanto foi retido na fonte durante o ano?** (em €)",
        "chave": "retencoes_fonte",
        "tipo": "numero",
        "dica": "Valor que aparece no teu recibo de vencimento como IRS",
    },
    {
        "numero": 11,
        "pergunta": "🛡️ **Quanto pagaste à Segurança Social?** (em €)",
        "chave": "seguranca_social",
        "tipo": "numero",
        "dica": "Desconto mensal multiplicado por 12 (ou 14)",
    },
    {
        "numero": 12,
        "pergunta": "🏥 **Despesas de saúde com NIF?** (em €)",
        "chave": "despesas_saude",
        "tipo": "numero",
        "dica": "Consultas, medicamentos, dentista (máx. dedução: 1.000€)",
    },
    {
        "numero": 13,
        "pergunta": "📚 **Despesas de educação com NIF?** (em €)",
        "chave": "despesas_educacao",
        "tipo": "numero",
        "dica": "Mensalidades, livros, explicações (máx. dedução: 800€)",
    },
    {
        "numero": 14,
        "pergunta": "🏠 **Despesas de habitação (juros crédito)?** (em €)",
        "chave": "despesas_habitacao",
        "tipo": "numero",
        "dica": "Juros de crédito habitação (máx. dedução: 296€)",
    },
    {
        "numero": 15,
        "pergunta": "🧓 **Despesas com lares/apoio familiar?** (em €)",
        "chave": "despesas_lares",
        "tipo": "numero",
        "dica": "Lares de idosos, apoio domiciliário (máx. 403,75€)",
    },
    {
        "numero": 16,
        "pergunta": "🎁 **Tens benefícios fiscais ativos?**",
        "chave": "tem_beneficios",
        "tipo": "opcao",
        "opcoes": [
            "Não",
            "Sim, PPR",
            "Sim, IRS Jovem",
            "Sim, Residente Não Habitual",
            "Sim, outros",
        ],
        "dica": "Planos de poupança ou regimes especiais",
    },
    {
        "numero": 17,
        "pergunta": "📝 **Detalhes dos benefícios?**",
        "chave": "detalhes_beneficios",
        "tipo": "texto",
        "dica": "Ex: PPR 2.000€, IRS Jovem primeiro ano",
    },
    {
        "numero": 18,
        "pergunta": "👨‍👩‍👧 **Pagas pensão de alimentos?**",
        "chave": "paga_pensao",
        "tipo": "opcao",
        "opcoes": ["Não", "Sim"],
        "dica": "Pensão a ex-cônjuge ou filhos",
    },
    {
        "numero": 19,
        "pergunta": "💳 **Valor total anual da pensão?** (em €)",
        "chave": "valor_pensao",
        "tipo": "numero",
        "dica": "Soma anual de pensões pagas",
    },
    {
        "numero": 20,
        "pergunta": "👥 **Se casado(a), pretendes tributação conjunta?**",
        "chave": "tributacao_conjunta",
        "tipo": "opcao",
        "opcoes": [
            "Sim, tributação conjunta",
            "Não, tributação separada",
            "Não aplicável (solteiro)",
        ],
        "dica": "Posso simular ambas e mostrar qual compensa mais!",
    },
]

# ═══════════════════════════════════════════════════════════════════════
#  INFORMAÇÃO SOBRE DEDUÇÕES
# ═══════════════════════════════════════════════════════════════════════

DEDUCTIONS_INFO = """
🧾 **Guia Completo de Deduções IRS 2025 - Por Marinete**

Olá! Vou explicar as principais deduções que podes usar para reduzir o teu IRS. Guarda sempre as faturas com o teu NIF! 📋

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**1. 🏥 DESPESAS DE SAÚDE** (taxa dedução: 15%)
   • Limite máximo de dedução: **1.000€**
   • O que conta:
     - Consultas médicas e análises
     - Medicamentos com receita
     - Seguros de saúde
     - Próteses e óculos
     - Dentista e ortodontia

   💡 Exemplo: Gastaste 3.000€ em saúde → Dedução: 1.000€ (15% = 150€ de desconto no IRS)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**2. 📚 DESPESAS DE EDUCAÇÃO** (taxa dedução: 30%)
   • Limite máximo de dedução: **800€**
   • O que conta:
     - Propinas e mensalidades escolares
     - Livros e material escolar
     - Explicações certificadas
     - Creches e infantários
     - Alojamento estudantes

   💡 Exemplo: Gastaste 2.500€ em educação → Dedução: 800€ (30% = 240€ de desconto)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**3. 🏠 HABITAÇÃO** (taxa dedução: 15%)
   • Limite máximo de dedução: **296€**
   • O que conta:
     - Juros de crédito habitação própria
     - Rendas (até €502/ano se jovem)

   💡 Exemplo: Pagaste 2.000€ de juros → Dedução: 296€ (15% = 44,40€)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**4. 🧓 LARES E APOIO FAMILIAR** (taxa dedução: 25%)
   • Limite máximo de dedução: **403,75€**
   • O que conta:
     - Lares de idosos
     - Apoio domiciliário certificado
     - Para ti ou familiares diretos

   💡 Exemplo: Lar custou 12.000€/ano → Dedução: 403,75€ (25% = 100,94€)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**5. 💰 PPR (Planos Poupança Reforma)** (taxa dedução: 20%)
   • Limite depende da idade:
     - Até 35 anos: até **400€** (máx. 2.000€ investidos)
     - 35-50 anos: até **350€** (máx. 1.750€)
     - Mais de 50: até **300€** (máx. 1.500€)

   💡 Dica: PPR é ótimo para reduzir IRS e poupar para reforma!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**6. 🎁 DONATIVOS** (taxa dedução: 25%)
   • Mínimo: **25€** para ativar
   • Sem limite máximo
   • Para entidades certificadas

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**7. 💳 DESPESAS GERAIS FAMILIARES** (taxa dedução: 35%)
   • Limite: **250€** por contribuinte
   • Automático via e-fatura
   • Inclui:
     - Restaurantes e cafés
     - Cabeleireiros e estética
     - Ginásios e desporto
     - Veterinários
     - Reparações auto/casa

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**🎯 DICAS DA MARINETE:**

✅ Pede **sempre fatura com NIF** (até em cafés!)
✅ Verifica o **e-fatura** regularmente
✅ Corrige setores errados (saúde, educação)
✅ Adiciona dependentes às faturas
✅ Não te esqueças de **pequenas despesas** (somam!)

📱 **Portal das Finanças:** https://www.portaldasfinancas.gov.pt
🧾 **e-fatura:** https://faturas.portaldasfinancas.gov.pt

**Queres simular o impacto destas deduções no teu IRS? Usa `/simular`!** 😊
"""

# ═══════════════════════════════════════════════════════════════════════
#  PROMPT PARA SIMULAÇÃO INTERATIVA
# ═══════════════════════════════════════════════════════════════════════

SIMULATION_PROMPT = """
🎯 **Simulação de IRS 2025 - Vamos calcular juntos!**

Olá! Sou a Marinete e vou ajudar-te a simular o teu IRS. 😊

Vou fazer-te **20 perguntas rápidas** (leva 5 minutos) para calcular:
✅ Quanto vais pagar ou receber de reembolso
✅ Impacto das tuas deduções
✅ Comparação individual vs conjunta (se aplicável)
✅ Sugestões de otimização fiscal

**📋 Informações que vou precisar:**
- Estado civil e dependentes
- Rendimentos do ano
- Retenções na fonte
- Despesas dedutíveis (saúde, educação, etc.)

**Pronto para começar?** Vou fazer a primeira pergunta! 🚀

_Podes cancelar a qualquer momento com `/cancel`_
"""

# ═══════════════════════════════════════════════════════════════════════
#  MENSAGEM DE AJUDA
# ═══════════════════════════════════════════════════════════════════════

HELP_MESSAGE = """
🆘 **Ajuda - Assistente IRS Marinete**

Olá! Aqui estão todas as formas de me usar:

**📱 COMANDOS PRINCIPAIS:**

🎯 `/start` - Mensagem de boas-vindas
🧮 `/simular` - Simulação completa interativa (20 perguntas)
⚡ `/calcular [valor]` - Cálculo rápido
   Exemplos:
   • `/calcular 30000` (apenas rendimento)
   • `/calcular 30000 saude:500 educacao:300`

📋 `/deducoes` - Lista completa de deduções fiscais
💡 `/sugestoes` - Enviar sugestão/feedback
📞 `/contato` - Informações para bot personalizado
📊 `/stats` - Ver estatísticas do bot (para admins)
❓ `/ajuda` - Esta mensagem
🔄 `/reset` - Recomeçar simulação
❌ `/cancel` - Cancelar processo atual

**💬 CONVERSAÇÃO NATURAL:**

Podes simplesmente conversar comigo! Exemplos:

• "Quanto pago de IRS com 35.000€?"
• "Sou casado, compensa IRS em conjunto?"
• "Posso deduzir despesas de ginásio?"
• "Como funciona o IRS Jovem?"
• "Tenho direito a reembolso?"

**🎓 TEMAS QUE DOMINO:**

✅ Cálculo de IRS e simulações
✅ Deduções fiscais (saúde, educação, habitação...)
✅ Tributação individual vs conjunta
✅ IRS Jovem e outros benefícios
✅ Retenções na fonte
✅ Prazos e obrigações
✅ Portal das Finanças e e-fatura

**⚠️ IMPORTANTE:**

Sou uma assistente informativa. Para casos complexos ou dúvidas específicas sobre a tua situação fiscal, recomendo sempre consultar um contabilista certificado!

**💡 DICA:**

Quanto mais detalhes me deres, mais precisa será a simulação! Podes começar agora: qual é a tua dúvida sobre IRS? 😊
"""

# ═══════════════════════════════════════════════════════════════════════
#  MENSAGENS DE ERRO E FEEDBACK
# ═══════════════════════════════════════════════════════════════════════

ERROR_MESSAGES = {
    "formato_invalido": "Hmm, não consegui entender esse formato. 🤔 Podes escrever de outra forma? Por exemplo: '30000' ou '30.000€'",
    "valor_muito_alto": "Esse valor parece muito alto! 😮 Tens certeza? Vou precisar que confirmes.",
    "valor_muito_baixo": "Esse valor parece muito baixo. Podes confirmar se está correto?",
    "campo_obrigatorio": "Essa informação é importante para o cálculo. Podes responder, por favor? 🙏",
    "erro_calculo": "Ups! Tive um problema ao fazer o cálculo. 😓 Podes tentar novamente? Se o erro persistir, usa `/reset` e recomeça.",
    "sessao_expirada": "A tua sessão expirou. Usa `/start` para começar de novo! 😊",
}

SUCCESS_MESSAGES = {
    "simulacao_completa": "🎉 **Simulação concluída!** Vou processar os dados e mostrar os resultados em breve...",
    "dados_salvos": "✅ Dados guardados! Podes continuar quando quiseres com `/simular`",
    "calculo_rapido": "⚡ Cálculo rápido concluído! Aqui estão os resultados:",
}

# ═══════════════════════════════════════════════════════════════════════
#  FOOTER PADRÃO
# ═══════════════════════════════════════════════════════════════════════

FOOTER = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 **Dica:** Guarda sempre as faturas com NIF!
📱 Portal das Finanças: portaldasfinancas.gov.pt
⚠️ Informação orientativa - consulta contabilista para casos complexos
"""
