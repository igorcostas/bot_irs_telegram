# 🇵🇹 Bot IRS Portugal - Marinete

> **Assistente virtual inteligente especializada em IRS (Imposto sobre o Rendimento das Pessoas Singulares) em Portugal**

Bot Telegram com IA que simula IRS, calcula reembolsos/pagamentos e orienta sobre deduções fiscais usando Groq API + Moonshot AI (Kimi K2).

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg?logo=telegram)](https://telegram.org/)
[![Groq API](https://img.shields.io/badge/Groq-API-green.svg)](https://groq.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🤖 Sobre a Marinete

**Marinete** é uma técnica administrativa e contábil sênior virtual com 15 anos de experiência em escritórios contábeis portugueses. Especializada em IRS Portugal, ela ajuda cidadãos portugueses a:

- 🧮 Simular e calcular IRS 2025
- 💰 Estimar reembolsos ou pagamentos
- 📊 Comparar tributação individual vs conjunta
- 💡 Otimizar deduções fiscais legalmente
- 📝 Esclarecer dúvidas sobre declaração

---

## ✨ Funcionalidades

### 🎯 Principais

- **Simulação Completa de IRS** - Questionário interativo de 20 perguntas com análise detalhada
- **Cálculo Rápido** - Estimativa instantânea com comando simples
- **Guia de Deduções** - Informações completas sobre todas as deduções fiscais
- **Conversa Natural** - IA especializada responde qualquer dúvida sobre IRS
- **Análise Personalizada** - Sugestões específicas para sua situação fiscal

### 🛠️ Comandos

```
/start      - Boas-vindas e menu principal
/simular    - Simulação completa (20 perguntas)
/calcular   - Cálculo rápido de IRS
/deducoes   - Ver deduções fiscais disponíveis
/ajuda      - Ajuda completa
/reset      - Limpar dados e recomeçar
/cancel     - Cancelar operação atual
```

### 💬 Exemplos de Uso

```
/calcular 30000
/calcular 35000 saude:500 educacao:300
/simular
"Quanto pago de IRS com 40.000€?"
"Compensa fazer IRS em conjunto?"
```

---

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.12 ou superior
- Conta Telegram
- API Key da Groq (gratuita)
- Token do BotFather do Telegram

### Instalação Rápida

```bash
# 1. Clonar repositório
git clone https://github.com/seu-usuario/irs_telegram_bot.git
cd irs_telegram_bot

# 2. Instalar dependências (com uv - recomendado)
uv sync

# OU com pip
pip install -r requirements.txt

# 3. Configurar API keys em config.py
# Edite config.py e adicione:
# - TELEGRAM_BOT_TOKEN = "seu_token"
# - GROQ_API_KEY = "sua_key"

# 4. Executar bot
uv run main.py

# OU
python main.py
```

### Obter API Keys

**Groq API (gratuito):**
1. Acesse https://console.groq.com/
2. Crie conta gratuita
3. Gere API key em https://console.groq.com/keys

**Telegram Bot Token:**
1. No Telegram, fale com @BotFather
2. Envie `/newbot` e siga instruções
3. Copie o token fornecido

---

## 📊 Tecnologias

| Tecnologia | Versão | Função |
|------------|--------|--------|
| Python | 3.12.11 | Linguagem base |
| python-telegram-bot | 21.11.1 | Framework do bot |
| Groq API | 0.32.0 | Provider de IA |
| Moonshot AI (Kimi K2) | - | Modelo de IA (128k contexto) |
| httpx | 0.28.1 | Cliente HTTP |
| uv | latest | Gerenciador de pacotes |

---

## 📁 Estrutura do Projeto

```
irs_telegram_bot/
├── main.py                    # Ponto de entrada
├── conversation_handler.py    # Lógica do bot
├── prompts.py                 # Prompts e perguntas IRS
├── config.py                  # Configurações
├── llm_handler/
│   ├── __init__.py
│   └── groq_handler.py        # Handler Groq API
├── test_groq_api.py           # Testes
├── validar_migracao.sh        # Validação
├── pyproject.toml             # Dependências (uv)
├── requirements.txt           # Dependências (pip)
└── docs/                      # Documentação adicional
```

---

## 🧪 Testes

```bash
# Testar API Groq
uv run test_groq_api.py

# Validar instalação completa
./validar_migracao.sh

# Testar bot no Telegram
uv run main.py
# No Telegram: envie /start
```

---

## 📖 Documentação Adicional

- [COMECE_AQUI.txt](COMECE_AQUI.txt) - Guia visual de início rápido
- [COMANDOS_TELEGRAM.txt](COMANDOS_TELEGRAM.txt) - Lista completa de comandos
- [MIGRACAO_GROQ.md](MIGRACAO_GROQ.md) - História da migração xAI→Groq
- [SOLUCAO_PYTHON313.md](SOLUCAO_PYTHON313.md) - Solução bug Python 3.13

---

## ⚙️ Configuração Avançada

### Variáveis de Ambiente (Produção)

Para ambiente de produção, use `.env`:

```bash
# Criar arquivo .env
echo "GROQ_API_KEY=sua_key" >> .env
echo "TELEGRAM_BOT_TOKEN=seu_token" >> .env

# Adicionar ao .gitignore
echo ".env" >> .gitignore
```

### Personalização da IA

Edite `prompts.py` para ajustar:
- Personalidade da Marinete
- Perguntas do questionário
- Escalões e deduções IRS

---

## 💡 Exemplos de Conversas

### Simulação Completa
```
Você: /simular
Bot: Olá! Sou a Marinete. Vou fazer 20 perguntas...
     Pergunta 1/20: Qual é o teu estado civil?
Você: Casado(a)
[... 18 perguntas ...]
Bot: ✅ Análise completa:
     - IRS estimado: 4.500€
     - Reembolso previsto: 800€
     - Sugestões: PPR, mais deduções em saúde...
```

### Cálculo Rápido
```
Você: /calcular 35000 saude:600
Bot: ⚡ Cálculo Rápido:
     Rendimento: 35.000€
     Escalão: 4º (26%)
     IRS: ~5.200€
```

### Conversa Natural
```
Você: Posso deduzir despesas de ginásio?
Bot: Ah! Ótima pergunta! Sim, despesas de ginásio 
     entram em "Despesas Gerais Familiares" com 
     taxa de dedução de 35% (máx. 250€)...
```

---

## ⚠️ Notas Importantes

- ⚠️ Este bot é **informativo e orientativo**
- ⚠️ Não substitui aconselhamento de contabilista certificado
- ⚠️ Cálculos são estimativas - confirme no Portal das Finanças
- ✅ Dados atualizados para IRS 2025 Portugal
- ✅ Escalões e deduções conforme legislação vigente

---

## 🔒 Segurança

- API keys devem estar em `.env` (produção)
- Nunca commite `config.py` com keys expostas
- Use `.gitignore` para proteger informações sensíveis
- Bot não armazena dados pessoais permanentemente

---

## 📈 Rate Limits (Groq Tier Gratuito)

- **30 requisições/minuto**
- **10.000 tokens/minuto**

Suficiente para uso pessoal ou escritório pequeno.

---

## 🤝 Contribuir

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📝 Changelog

### v2.0.0 - Groq Edition (2025-01-04)
- ✅ Migração de xAI Grok para Groq API
- ✅ Implementação da Marinete (IA especializada)
- ✅ Sistema de 20 perguntas interativas
- ✅ Cálculo rápido com comando
- ✅ Conversa natural com IA
- ✅ Suporte Python 3.12
- ✅ Limpeza e otimização do código

### v1.0.0 - Versão Inicial
- Estrutura básica do bot

---

## 🆘 Suporte

- **Issues:** [GitHub Issues](https://github.com/seu-usuario/irs_telegram_bot/issues)
- **Portal das Finanças:** https://www.portaldasfinancas.gov.pt
- **e-fatura:** https://faturas.portaldasfinancas.gov.pt
- **Groq Console:** https://console.groq.com/

---

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Bot IRS Portugal - Marinete**
- Desenvolvido com ❤️ para ajudar portugueses com IRS
- Powered by Groq + Moonshot AI (Kimi K2)

---

## 🌟 Agradecimentos

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Framework do bot
- [Groq](https://groq.com/) - API de IA ultra-rápida
- [Moonshot AI](https://www.moonshot.cn/) - Modelo Kimi K2

---

**⭐ Se este projeto te ajudou, dá uma estrela no GitHub!**

---

<div align="center">

**🇵🇹 Feito em Portugal | 🤖 Powered by AI | ⚡ Ultra-rápido com Groq**

[Reportar Bug](https://github.com/seu-usuario/irs_telegram_bot/issues) · [Solicitar Feature](https://github.com/seu-usuario/irs_telegram_bot/issues) · [Documentação](docs/)

</div>