# 🚀 Deploy Rápido - 5 Minutos

Guia super rápido para colocar seu bot no ar GRATUITAMENTE!

## ⚡ Passo a Passo Rápido

### 1. Push para GitHub
```bash
git add .
git commit -m "Deploy bot"
git push origin main
```

### 2. Criar Conta no Render
- Acesse: https://render.com
- Faça login com GitHub
- Autorize acesso aos repositórios

### 3. Criar Background Worker
1. Clique em **"New +"** → **"Background Worker"**
2. Selecione seu repositório `irs_telegram_bot`
3. Configure:
   - **Name**: `meu-bot-irs`
   - **Region**: `Frankfurt (EU Central)`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: **Free**

### 4. Adicionar Variáveis de Ambiente
Na aba **Environment**, adicione:

```
TELEGRAM_BOT_TOKEN = seu_token_do_botfather
GROQ_API_KEY = sua_chave_groq
MODEL_NAME = moonshotai/kimi-k2-instruct-0905
```

**Onde conseguir:**
- Telegram Token: Fale com @BotFather no Telegram
- Groq API Key: https://console.groq.com/keys

### 5. Deploy!
Clique em **"Create Background Worker"** e aguarde 2-5 minutos.

### 6. Verificar
- **Logs no Render**: Deve mostrar "✅ Bot está rodando..."
- **Telegram**: Envie `/start` para seu bot

## ✅ Pronto!

Seu bot agora está rodando 24/7 na nuvem! 🎉

---

## 🔄 Para Atualizar
```bash
git add .
git commit -m "Atualização"
git push origin main
```
O Render faz redeploy automático!

---

## ❓ Problemas?

**Bot não responde:**
- Verifique os logs no Render
- Confirme as variáveis de ambiente

**Erro de build:**
- Verifique `requirements.txt`
- Tente Python 3.11 no `runtime.txt`

**Mais detalhes:** Veja `DEPLOY_GRATUITO.md`
