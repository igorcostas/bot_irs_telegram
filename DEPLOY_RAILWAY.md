# 🚂 Deploy Gratuito no Railway.app

Guia completo para fazer deploy do seu bot Telegram no Railway.app - Uma alternativa ao Render.com.

## 🎯 Por que Railway?

- ✅ **$5 de crédito gratuito/mês** (suficiente para bot pequeno/médio)
- ✅ **Interface muito intuitiva**
- ✅ **Deploy automático do GitHub**
- ✅ **Logs em tempo real excelentes**
- ✅ **Não hiberna** (bot sempre ativo)
- ⚠️ **Requer cartão de crédito** (não cobra se ficar dentro dos $5)

---

## 📋 Pré-requisitos

- ✅ Código no GitHub
- ✅ Token do Telegram Bot
- ✅ Groq API Key
- ⚠️ Cartão de crédito (não será cobrado no plano gratuito)

---

## 🚀 Passo a Passo Completo

### 1️⃣ Criar Conta no Railway

1. Acesse: **https://railway.app**
2. Clique em **"Login"** no canto superior direito
3. Escolha **"Login with GitHub"**
4. Autorize o Railway a acessar sua conta GitHub
5. Você será redirecionado para o Dashboard

### 2️⃣ Adicionar Método de Pagamento (Obrigatório)

Mesmo usando o plano gratuito, Railway exige cartão:

1. Clique no seu avatar (canto superior direito)
2. Vá em **"Account Settings"**
3. Clique em **"Billing"**
4. Adicione seu cartão
   - ⚠️ **Não se preocupe**: Você só será cobrado se ultrapassar os $5/mês
   - ✅ Para um bot Telegram simples, **raramente ultrapassa $2-3/mês**

### 3️⃣ Criar Novo Projeto

1. No Dashboard, clique em **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Se for a primeira vez:
   - Clique em **"Configure GitHub App"**
   - Autorize o Railway nos seus repositórios
   - Você pode escolher "All repositories" ou selecionar apenas o do bot
4. Volte ao Railway e clique em **"Deploy from GitHub repo"** novamente
5. Selecione o repositório **`irs_telegram_bot`**

### 4️⃣ Configurar o Deploy

Após selecionar o repositório:

1. O Railway detecta automaticamente que é Python
2. Aguarde alguns segundos...
3. Seu serviço será criado automaticamente!

**O Railway usa automaticamente:**
- `requirements.txt` para instalar dependências
- `Procfile` para saber como iniciar o bot
- `runtime.txt` para versão do Python

### 5️⃣ Adicionar Variáveis de Ambiente

**CRÍTICO**: Sem as variáveis, o bot não funciona!

1. Na página do projeto, clique no seu serviço
2. Vá para a aba **"Variables"**
3. Clique em **"New Variable"** e adicione uma por uma:

```
TELEGRAM_BOT_TOKEN
valor: seu_token_do_botfather

GROQ_API_KEY
valor: sua_chave_groq

MODEL_NAME
valor: moonshotai/kimi-k2-instruct-0905
```

4. Clique em **"Add"** para cada uma

**Onde obter:**
- **Telegram Token**: @BotFather no Telegram → `/newbot` ou `/token`
- **Groq API**: https://console.groq.com/keys

### 6️⃣ Fazer Deploy

1. Depois de adicionar as variáveis, clique em **"Deploy"** (canto superior direito)
2. Ou simplesmente aguarde - Railway faz deploy automático após adicionar variáveis
3. Acompanhe os logs na aba **"Deployments"**

### 7️⃣ Verificar se Está Funcionando

#### No Railway:

1. Clique no seu serviço
2. Vá para aba **"Logs"** (ou **"Deployments"** → clique no deploy ativo)
3. Você deve ver:

```
🤖 Bot Técnico Contábil Virtual iniciado!
📊 Sistema de análise completa ativo
🔥 API: Groq (Moonshot AI - Kimi K2)
✅ Bot está rodando...
```

#### No Telegram:

1. Abra o Telegram
2. Procure seu bot
3. Envie `/start`
4. **Sucesso!** 🎉

---

## 💰 Gerenciar Custos (Ficar no Gratuito)

### Ver Uso Atual:

1. Clique no seu projeto
2. Vá em **"Usage"** (ícone de gráfico na barra lateral)
3. Veja quanto já usou dos $5

### Custos Típicos:

Um bot Telegram simples consome:
- **CPU**: Muito baixo (apenas quando recebe mensagens)
- **RAM**: ~100-200 MB
- **Network**: Mínimo
- **Custo estimado**: **$1-3/mês** ✅

### Dicas para Economizar:

1. ✅ Use apenas 1 serviço (não crie múltiplos)
2. ✅ Não use banco de dados pesado (se não precisar)
3. ✅ Railway é "pay per use" - quanto menos mensagens, menos custa

---

## 🔄 Atualizar o Bot

Railway faz **auto-deploy do GitHub**!

```bash
# Faça suas alterações
git add .
git commit -m "Melhoria no bot"
git push origin main
```

🎉 **Railway detecta e faz redeploy automático em 1-2 minutos!**

### Desativar Auto-Deploy:

1. Settings do serviço
2. Vá em **"Deploy"**
3. Desmarque **"Deploy on Push"**

---

## 📊 Monitoramento

### Logs em Tempo Real:

1. Aba **"Logs"** no serviço
2. Atualiza automaticamente
3. Pode filtrar por tipo (info, error, etc.)

### Métricas:

1. Aba **"Metrics"**
2. Veja CPU, RAM e Network em tempo real
3. Gráficos bonitos e úteis 📈

### Notificações:

Railway pode notificar você sobre:
- Erros no deploy
- Uso próximo do limite
- Downtime

Configure em: **Project Settings → Integrations**

---

## 🔧 Troubleshooting

### ❌ Bot não inicia

**Problema**: Logs mostram erro de importação

**Solução**:
```bash
# Verifique requirements.txt
cat requirements.txt

# Deve ter:
python-telegram-bot==21.4
groq
python-dotenv
```

### ❌ Variável de ambiente não encontrada

**Problema**: `ValueError: TELEGRAM_BOT_TOKEN not found`

**Solução**:
1. Vá em **Variables**
2. Verifique se adicionou todas as 3 variáveis
3. **Importante**: Após adicionar, clique em **"Redeploy"**

### ❌ Deploy falha

**Problema**: Build error no Railway

**Solução**:
1. Verifique logs do build
2. Garanta que `runtime.txt` tem: `python-3.11.9`
3. Verifique se `Procfile` tem: `worker: python main.py`

### ❌ Bot responde lento

**Problema**: Groq API timeout

**Solução**:
1. Verifique sua cota da Groq
2. Teste: https://console.groq.com/playground
3. Considere adicionar retry no código

### ❌ Usando muito crédito

**Problema**: Ultrapassou $3-4/mês

**Solução**:
1. Verifique métricas de uso
2. Pode ter loop infinito no código
3. Considere otimizar requests à API

---

## 🆚 Railway vs Render

| Recurso | Railway | Render |
|---------|---------|--------|
| **Plano Gratuito** | $5 crédito/mês | 750h/mês gratuito |
| **Cartão Necessário** | ✅ Sim | ❌ Não |
| **Interface** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Logs** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Deploy Speed** | ⚡ Muito rápido | ⚡ Rápido |
| **Auto-deploy** | ✅ Sim | ✅ Sim |
| **Hibernação** | ❌ Nunca | ⚠️ Em Web Services |
| **Suporte** | Discord ativo | Fórum |

**Recomendação:**
- **Sem cartão?** → Use **Render**
- **Tem cartão?** → Use **Railway** (melhor UX)

---

## 🎁 Bônus: Comandos Railway CLI

Instale o CLI para gerenciar do terminal:

```bash
# Instalar
npm i -g @railway/cli

# Fazer login
railway login

# Ver projetos
railway list

# Ver logs
railway logs

# Abrir dashboard
railway open
```

---

## 📞 Suporte

- 📖 **Documentação**: https://docs.railway.app
- 💬 **Discord**: https://discord.gg/railway
- 🐦 **Twitter**: @Railway

---

## 🎉 Checklist Final

- [ ] Conta Railway criada
- [ ] Cartão adicionado
- [ ] Projeto criado do GitHub
- [ ] 3 variáveis de ambiente configuradas
- [ ] Deploy concluído com sucesso
- [ ] Logs mostram "Bot está rodando"
- [ ] Testei no Telegram com `/start`
- [ ] Bot responde normalmente
- [ ] Monitorando uso em "Usage"

**Parabéns! Bot no ar 24/7! 🚂🎊**

---

## 💡 Próximos Passos

1. Configure alertas de uso
2. Adicione analytics ao bot
3. Configure backup automático
4. Documente comandos do bot
5. Compartilhe com amigos! 😊

**Dúvidas?** Entre no Discord do Railway - comunidade muito ativa!