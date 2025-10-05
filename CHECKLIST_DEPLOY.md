# ✅ Checklist de Deploy - Bot IRS Telegram

Use esta checklist para garantir que tudo está pronto para o deploy!

---

## 📋 ANTES DO DEPLOY

### Preparação Local
- [ ] Código do bot está funcionando localmente
- [ ] Testou com `python main.py`
- [ ] Tem arquivo `requirements.txt` atualizado
- [ ] Tem arquivo `.gitignore` configurado
- [ ] Arquivo `.env` NÃO está no repositório (segurança!)

### Credenciais Necessárias
- [ ] Token do Telegram Bot (@BotFather)
- [ ] Groq API Key (https://console.groq.com/keys)
- [ ] Conta no GitHub criada
- [ ] Repositório criado no GitHub

---

## 🔒 SEGURANÇA

- [ ] Arquivo `.env` está no `.gitignore`
- [ ] NÃO há API keys no código
- [ ] `config.py` usa `os.getenv()` para todas as credenciais
- [ ] Testou que o bot funciona com variáveis de ambiente

---

## 🌐 GITHUB

- [ ] Código está no GitHub:
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  git branch -M main
  git remote add origin https://github.com/SEU_USER/SEU_REPO.git
  git push -u origin main
  ```

- [ ] Repositório está público ou Render tem acesso
- [ ] Último push foi bem-sucedido

---

## 🚀 RENDER.COM

### Criar Conta
- [ ] Acessou https://render.com
- [ ] Fez login com GitHub
- [ ] Autorizou acesso aos repositórios

### Criar Serviço
- [ ] Clicou em "New +" → "Background Worker"
- [ ] Selecionou o repositório correto
- [ ] Configurou:
  - [ ] Name: `meu-bot-irs` (ou seu nome)
  - [ ] Region: `Frankfurt (EU Central)`
  - [ ] Branch: `main`
  - [ ] Runtime: `Python 3`
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `python main.py`
  - [ ] Plan: **Free** ✅

### Variáveis de Ambiente
- [ ] Adicionou `TELEGRAM_BOT_TOKEN`
- [ ] Adicionou `GROQ_API_KEY`
- [ ] Adicionou `MODEL_NAME` = `moonshotai/kimi-k2-instruct-0905`
- [ ] Salvou as configurações

### Deploy
- [ ] Clicou em "Create Background Worker"
- [ ] Build iniciou (aparece progresso)
- [ ] Build concluído com sucesso (sem erros vermelhos)

---

## ✅ VERIFICAÇÃO

### Logs no Render
- [ ] Acessou a aba "Logs"
- [ ] Viu a mensagem: `🤖 Bot Técnico Contábil Virtual iniciado!`
- [ ] Viu: `✅ Bot está rodando...`
- [ ] Não há erros nos logs

### Teste no Telegram
- [ ] Abriu o Telegram
- [ ] Procurou seu bot pelo username
- [ ] Enviou `/start`
- [ ] Bot respondeu! 🎉
- [ ] Testou outros comandos (`/help`, etc.)

---

## 🎯 PRÓXIMOS PASSOS (OPCIONAL)

### Monitoramento
- [ ] Configurou UptimeRobot ou Cron-Job (para ping)
- [ ] Salvou URL dos logs do Render
- [ ] Configurou notificações de status

### Melhorias
- [ ] Adicionou README com instruções de uso
- [ ] Documentou comandos do bot
- [ ] Criou backup das credenciais (em local seguro!)

---

## 🔄 PARA FUTURAS ATUALIZAÇÕES

Sempre que fizer mudanças no código:

```bash
git add .
git commit -m "Descrição da mudança"
git push origin main
```

O Render detecta e faz redeploy automático! ✨

---

## 🆘 PROBLEMAS COMUNS

### ❌ Build falhou
- [ ] Verificou `requirements.txt`
- [ ] Tentou mudar `runtime.txt` para `python-3.11.0`
- [ ] Verificou logs de erro

### ❌ Bot não responde
- [ ] Verificou variáveis de ambiente
- [ ] Token do Telegram está correto
- [ ] Groq API Key está válida
- [ ] Bot está rodando (logs mostram "running")

### ❌ Bot para após alguns minutos
- [ ] Criou "Background Worker" (não Web Service)
- [ ] Verificou logs para mensagens de erro
- [ ] Confirmou que Python não está em modo debug

---

## 📞 RECURSOS

- 📖 Guia Completo: `DEPLOY_GRATUITO.md`
- ⚡ Guia Rápido: `QUICK_DEPLOY.md`
- 🌐 Render Docs: https://render.com/docs
- 💬 Render Community: https://community.render.com

---

## 🎉 DEPLOY CONCLUÍDO!

- [ ] Bot está rodando 24/7
- [ ] Testei todos os comandos
- [ ] Salvei credenciais em local seguro
- [ ] Documentei para referência futura

**Parabéns! Seu bot está no ar! 🚀🎊**