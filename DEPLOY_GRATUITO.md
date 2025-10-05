# 🚀 Deploy Gratuito do Bot IRS - Render.com

Este guia mostra como fazer deploy do seu bot Telegram para rodar 24/7 **GRATUITAMENTE** no Render.com.

## ✅ Pré-requisitos

- Conta no GitHub (gratuita)
- Seu código já commitado no repositório
- Token do Telegram Bot
- API Key da Groq

---

## 📋 Passo 1: Preparar os Arquivos

Seu projeto já tem os arquivos necessários:
- ✅ `requirements.txt` - Dependências Python
- ✅ `Procfile` - Comando para iniciar o bot
- ✅ `runtime.txt` - Versão do Python
- ✅ `main.py` - Arquivo principal
- ✅ `config.py` - Configurações (usa variáveis de ambiente)

---

## 🔒 Passo 2: Verificar Segurança

**IMPORTANTE**: Nunca commite suas API keys no GitHub!

Verifique se você tem um arquivo `.env` na raiz do projeto e que ele está no `.gitignore`:

```
.env
.env.local
config.py.local
```

---

## 🌐 Passo 3: Fazer Push para GitHub

```bash
# Se ainda não fez:
git add .
git commit -m "Preparado para deploy no Render"
git push origin main
```

---

## 🎯 Passo 4: Criar Conta no Render

1. Acesse: https://render.com
2. Clique em **"Get Started for Free"**
3. Faça login com sua conta do GitHub
4. Autorize o Render a acessar seus repositórios

---

## 🤖 Passo 5: Criar Web Service

1. No Dashboard do Render, clique em **"New +"**
2. Selecione **"Background Worker"** (NÃO é Web Service!)
3. Conecte seu repositório `irs_telegram_bot`
4. Configure:

### Configurações Básicas:
- **Name**: `irs-telegram-bot` (ou qualquer nome)
- **Region**: `Frankfurt (EU Central)` (mais próximo de Portugal)
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`

### Plan:
- Selecione: **Free** (0$/mês)

---

## 🔐 Passo 6: Adicionar Variáveis de Ambiente

**MUITO IMPORTANTE!** Antes de fazer deploy, configure as variáveis:

1. Na página de configuração do seu serviço, vá até **"Environment"**
2. Clique em **"Add Environment Variable"**
3. Adicione as seguintes variáveis:

| Key | Value |
|-----|-------|
| `TELEGRAM_BOT_TOKEN` | `seu_token_aqui` |
| `GROQ_API_KEY` | `sua_api_key_aqui` |
| `MODEL_NAME` | `moonshotai/kimi-k2-instruct-0905` |

**Como obter as chaves:**
- **TELEGRAM_BOT_TOKEN**: Fale com @BotFather no Telegram
- **GROQ_API_KEY**: https://console.groq.com/keys

---

## 🚀 Passo 7: Deploy!

1. Clique em **"Create Background Worker"**
2. Aguarde o build (leva 2-5 minutos)
3. Verifique os logs para confirmar que está rodando

---

## ✅ Passo 8: Verificar se Está Funcionando

### No Render:
- Vá para a aba **"Logs"**
- Você deve ver:
```
🤖 Bot Técnico Contábil Virtual iniciado!
📊 Sistema de análise completa ativo
🔥 API: Groq (Moonshot AI - Kimi K2)
✅ Bot está rodando...
```

### No Telegram:
1. Abra o Telegram
2. Procure seu bot
3. Envie `/start`
4. O bot deve responder!

---

## 💡 Limitações do Plano Gratuito

### Render Free Tier:
- ✅ **Roda 24/7** sem parar
- ✅ **750 horas/mês** de execução (suficiente para o mês inteiro!)
- ✅ **512MB RAM**
- ✅ **Banda ilimitada**
- ⚠️ **Inatividade**: O serviço pode ser pausado se não houver atividade por 15 minutos
  - **Solução**: Use um serviço de ping gratuito (veja abaixo)

---

## 🔄 Como Manter o Bot Sempre Ativo

### Opção 1: Cron-Job.org (Recomendado)
1. Acesse: https://cron-job.org
2. Crie conta gratuita
3. Adicione um job que faz ping no bot a cada 10 minutos

### Opção 2: UptimeRobot
1. Acesse: https://uptimerobot.com
2. Crie conta gratuita
3. Configure monitor HTTP para o endpoint do Render

**OBS**: Para Background Workers, isso não é necessário! Ele roda continuamente.

---

## 🔧 Troubleshooting

### Bot não responde no Telegram
1. Verifique os logs no Render
2. Confirme que as variáveis de ambiente estão corretas
3. Teste a API Key da Groq: `python test_groq_api.py`

### Erro de build
- Verifique se `requirements.txt` está correto
- Verifique se `runtime.txt` tem a versão Python correta
- Se Python 3.13 der problema, mude para `python-3.11.0`

### Bot para após alguns minutos
- Verifique se você criou um **Background Worker** (não Web Service)
- Verifique os logs para ver erros

### "Module not found"
- Adicione o módulo em `requirements.txt`
- Faça commit e push
- O Render fará redeploy automático

---

## 🆓 Outras Opções Gratuitas

### 1. **Railway.app**
- ✅ $5 crédito gratuito/mês
- ✅ Fácil de usar
- ⚠️ Requer cartão de crédito

### 2. **Fly.io**
- ✅ 3 VMs gratuitas
- ✅ Boa para bots
- ⚠️ Configuração mais complexa

### 3. **Heroku** (Recomendação antiga)
- ❌ Não tem mais plano gratuito desde 2022

### 4. **PythonAnywhere**
- ✅ Plano gratuito
- ⚠️ Limitado a 100 segundos de CPU/dia
- ❌ Não recomendado para bots Telegram

---

## 🔄 Atualizar o Bot

Sempre que fizer alterações:

```bash
git add .
git commit -m "Suas alterações"
git push origin main
```

O Render detecta automaticamente e faz o redeploy! 🎉

---

## 📊 Monitoramento

### Ver Logs em Tempo Real:
1. Acesse o Dashboard do Render
2. Clique no seu serviço
3. Vá para a aba **"Logs"**

### Ver Uso de Recursos:
1. Aba **"Metrics"**
2. Veja CPU, Memória e uptime

---

## 🎉 Pronto!

Seu bot agora está rodando 24/7 na nuvem, gratuitamente! 🚀

**Dúvidas?** Verifique os logs e a documentação do Render: https://render.com/docs

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs no Render
2. Teste localmente: `python main.py`
3. Verifique as variáveis de ambiente
4. Consulte: https://community.render.com