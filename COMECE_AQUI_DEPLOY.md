# 🚀 COMECE AQUI - Deploy Gratuito do Bot

Guia super rápido em português para colocar o teu bot a funcionar 24h por dia, GRÁTIS!

---

## ⚡ Início Rápido (10 minutos)

### O que vais precisar:
- ✅ Token do teu bot Telegram
- ✅ Chave API da Groq
- ✅ Conta no GitHub (grátis)
- ❌ Cartão de crédito **NÃO** é necessário!

---

## 🎯 Escolhe a Plataforma

### **Render.com** - RECOMENDADO! 
- ✅ 100% gratuito
- ✅ Não precisa cartão
- ✅ Super fácil
- 📖 **Guia**: `QUICK_DEPLOY.md` ou `DEPLOY_GRATUITO.md`

### **Railway.app** - Alternativa (requer cartão)
- ✅ $5 grátis/mês (suficiente)
- ⚠️ Precisa cartão de crédito
- ✅ Interface bonita
- 📖 **Guia**: `DEPLOY_RAILWAY.md`

---

## 📝 Passo a Passo - Render.com

### 1. Preparar o GitHub

```bash
# Se ainda não fizeste:
git init
git add .
git commit -m "Bot pronto para deploy"
git branch -M main
git remote add origin https://github.com/TEU_USER/TEU_REPO.git
git push -u origin main
```

### 2. Criar Conta no Render

1. Vai a: **https://render.com**
2. Clica em **"Get Started for Free"**
3. Faz login com o GitHub
4. Autoriza o Render

### 3. Criar o Serviço

1. No Dashboard, clica em **"New +"**
2. Escolhe **"Background Worker"** (importante!)
3. Conecta o teu repositório `irs_telegram_bot`
4. Configura:
   - **Name**: `meu-bot-irs`
   - **Region**: `Frankfurt (EU Central)`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Escolhe **Free** (0€/mês)

### 4. Adicionar as Variáveis de Ambiente

**IMPORTANTE!** Sem isto o bot não funciona!

Na página de configuração:
1. Vai à secção **"Environment"**
2. Clica em **"Add Environment Variable"**
3. Adiciona estas 3 variáveis:

```
Nome: TELEGRAM_BOT_TOKEN
Valor: (cola aqui o token do @BotFather)

Nome: GROQ_API_KEY
Valor: (cola aqui a tua chave da Groq)

Nome: MODEL_NAME
Valor: moonshotai/kimi-k2-instruct-0905
```

**Onde obter:**
- **Token Telegram**: Abre o Telegram → fala com @BotFather → escreve `/token`
- **Groq API**: Vai a https://console.groq.com/keys → cria uma chave

### 5. Fazer Deploy!

1. Clica em **"Create Background Worker"**
2. Aguarda 2-5 minutos enquanto faz o build
3. Observa os logs

### 6. Verificar se Funciona

**No Render:**
- Vai à aba **"Logs"**
- Deve aparecer: `✅ Bot está rodando...`

**No Telegram:**
- Abre o Telegram
- Procura o teu bot
- Envia `/start`
- **Pronto! Está a funcionar!** 🎉

---

## 🔄 Para Atualizar o Bot

Sempre que fizeres alterações ao código:

```bash
git add .
git commit -m "Atualizações"
git push origin main
```

O Render deteta automaticamente e atualiza o bot! ✨

---

## ❓ Problemas Comuns

### O bot não responde
- ✅ Verifica se as variáveis de ambiente estão corretas
- ✅ Confirma que o token do Telegram está bem
- ✅ Vê os logs no Render para erros

### Erro no build
- ✅ Confirma que `requirements.txt` existe
- ✅ Tenta mudar `runtime.txt` para `python-3.11.9`

### Bot para depois de uns minutos
- ✅ Certifica-te que criaste **Background Worker** (não Web Service)
- ✅ Verifica os logs para mensagens de erro

---

## 📚 Mais Ajuda

- 📖 **Guia Completo**: `DEPLOY_GRATUITO.md`
- ⚡ **Guia Rápido**: `QUICK_DEPLOY.md`
- ✅ **Checklist**: `CHECKLIST_DEPLOY.md`
- 🚂 **Railway**: `DEPLOY_RAILWAY.md`
- 🆚 **Comparar Opções**: `COMPARATIVO_HOSPEDAGEM.md`

---

## 🎉 Parabéns!

O teu bot agora está a funcionar 24 horas por dia, 7 dias por semana, sem gastar nada! 🚀

**Dúvidas?** Lê os guias detalhados acima ou verifica os logs no Render.

**Boa sorte! 🇵🇹**