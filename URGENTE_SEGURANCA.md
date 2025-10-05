# 🚨 URGENTE - RECUPERAÇÃO DE SEGURANÇA

## ⚠️ PROBLEMA IDENTIFICADO

Suas credenciais (Token Telegram + Groq API Key) foram **expostas publicamente no GitHub** através do arquivo `replace_secrets.sh`.

**Status atual:**
- ❌ Token Telegram: **COMPROMETIDO** - Já foi revogado pelo Telegram (erro 401)
- ❌ Groq API Key: **EXPOSTA** - Pode estar comprometida
- ❌ Histórico Git: Contém credenciais antigas

---

## 🔥 AÇÃO IMEDIATA (FAÇA AGORA!)

### 1️⃣ REVOGAR TOKEN ANTIGO DO TELEGRAM

1. Abre o **Telegram**
2. Procura o bot **@BotFather**
3. Envia: `/mybots`
4. Seleciona o teu bot
5. Clica em **"API Token"**
6. Clica em **"Revoke current token"** (se ainda não foi)
7. Confirma a revogação

### 2️⃣ GERAR NOVO TOKEN DO TELEGRAM

1. Ainda no @BotFather
2. Seleciona o teu bot novamente
3. Clica em **"API Token"**
4. Clica em **"Generate new token"**
5. **COPIA o novo token** (começa com números:letras)
6. **⚠️ NUNCA partilhe este token com ninguém!**

Formato: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789`

### 3️⃣ REVOGAR CHAVE ANTIGA DA GROQ

1. Vai a: **https://console.groq.com/keys**
2. Faz login
3. Procura a chave antiga (se ainda existe)
4. Clica em **"Delete"** ou **"Revoke"**
5. Confirma

### 4️⃣ GERAR NOVA CHAVE GROQ

1. No mesmo site: https://console.groq.com/keys
2. Clica em **"Create API Key"**
3. Dá um nome: `Bot IRS - Nova`
4. **COPIA a chave** (começa com `gsk_`)
5. **⚠️ Esta chave só aparece UMA VEZ!**

---

## 🔒 ATUALIZAR NO RENDER (URGENTE!)

### Opção 1: Via Dashboard Render

1. Vai a: **https://dashboard.render.com**
2. Clica no teu serviço do bot
3. Vai para a aba **"Environment"**
4. Encontra a variável **`TELEGRAM_BOT_TOKEN`**
5. Clica em **"Edit"**
6. Cola o **NOVO token** do Telegram
7. Clica em **"Save"**
8. Encontra a variável **`GROQ_API_KEY`**
9. Clica em **"Edit"**
10. Cola a **NOVA chave** da Groq
11. Clica em **"Save"**
12. O Render vai fazer **redeploy automático** em 1-2 minutos

### Opção 2: Deletar e Recriar Variáveis

1. Delete as variáveis antigas
2. Cria novas:
   - `TELEGRAM_BOT_TOKEN` = novo_token_aqui
   - `GROQ_API_KEY` = nova_key_aqui
   - `MODEL_NAME` = moonshotai/kimi-k2-instruct-0905
3. Salva tudo
4. Aguarda redeploy

---

## 🧹 LIMPAR O REPOSITÓRIO GIT (IMPORTANTE!)

### Opção A: Remover Arquivo Problemático (Recomendado)

```bash
cd irs_telegram_bot

# Deletar o arquivo que expôs as credenciais
git rm replace_secrets.sh

# Commitar
git add .
git commit -m "🔒 Remove arquivo com credenciais expostas"

# Push
git push origin main
```

### Opção B: Criar Repositório Limpo (Mais Seguro)

Se quiser começar com repositório 100% limpo:

```bash
# 1. Criar novo diretório temporário
cd ..
mkdir irs_telegram_bot_limpo
cd irs_telegram_bot_limpo

# 2. Copiar APENAS arquivos necessários (SEM .git)
cp ../irs_telegram_bot/*.py .
cp ../irs_telegram_bot/requirements.txt .
cp ../irs_telegram_bot/Procfile .
cp ../irs_telegram_bot/runtime.txt .
cp ../irs_telegram_bot/*.md .
cp -r ../irs_telegram_bot/llm_handler .

# 3. Criar novo .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[oc]
.venv/
*.egg-info

# Credenciais
.env
.env.local
*.log
config.py.local
*.secret
*.key
*.token
EOF

# 4. Iniciar novo Git
git init
git add .
git commit -m "🎉 Repositório limpo - início seguro"

# 5. Criar novo repositório no GitHub
# Vai a: https://github.com/new
# Nome: irs_telegram_bot_novo
# NÃO inicializar com nada

# 6. Push para novo repositório
git remote add origin https://github.com/SEU_USER/irs_telegram_bot_novo.git
git branch -M main
git push -u origin main

# 7. Atualizar Render para usar novo repositório
```

### Opção C: Limpar Histórico (Avançado)

⚠️ **Cuidado**: Isto reescreve TODO o histórico Git!

```bash
# Usar BFG Repo-Cleaner (mais seguro que git filter-branch)
# Instalar: https://rtyley.github.io/bfg-repo-cleaner/

# Ou manualmente:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch replace_secrets.sh" \
  --prune-empty --tag-name-filter cat -- --all

# Limpar
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (CUIDADO!)
git push origin --force --all
```

---

## ✅ VERIFICAR SE RESOLVEU

### 1. Verificar Logs no Render

1. Vai a: Dashboard Render → Teu serviço → **Logs**
2. Deve aparecer:
   ```
   🚀 Iniciando Bot Técnico Contábil Virtual...
   🤖 Bot Técnico Contábil Virtual iniciado!
   ✅ Bot está rodando...
   ```
3. **NÃO** deve ter erro 401 Unauthorized

### 2. Testar no Telegram

1. Abre o Telegram
2. Procura o teu bot
3. Envia: `/start`
4. **O bot deve responder!** 🎉

Se funcionar: **PROBLEMA RESOLVIDO!** ✅

---

## 📋 CHECKLIST DE SEGURANÇA

- [ ] Token antigo do Telegram revogado
- [ ] Novo token do Telegram gerado
- [ ] Chave antiga da Groq revogada
- [ ] Nova chave da Groq gerada
- [ ] Variáveis atualizadas no Render
- [ ] Arquivo `replace_secrets.sh` removido do Git
- [ ] Git push feito
- [ ] Bot testado e funcionando
- [ ] Logs do Render sem erros
- [ ] Bot responde no Telegram

---

## 🛡️ PREVENIR NO FUTURO

### ✅ SEMPRE FAÇA:

1. **Use variáveis de ambiente** (.env + config.py)
2. **`.env` no .gitignore`** - SEMPRE!
3. **NUNCA** commite credenciais no código
4. **Verifique antes de commit**:
   ```bash
   git diff  # Ver o que vai commitar
   git status # Confirmar arquivos
   ```
5. **Use .env.example** para templates (sem valores reais)

### ❌ NUNCA FAÇA:

1. ❌ Colocar tokens diretamente no código
2. ❌ Commitar arquivo `.env`
3. ❌ Partilhar credenciais em chat/email
4. ❌ Usar mesmas credenciais em múltiplos projetos
5. ❌ Deixar credenciais em scripts `.sh`

---

## 🔐 ESTRUTURA SEGURA

```
irs_telegram_bot/
├── .env              ← NUNCA commitar (no .gitignore)
├── .env.example      ← Template SEM valores reais (pode commitar)
├── config.py         ← Usa os.getenv() (pode commitar)
├── main.py           ← Importa config (pode commitar)
└── .gitignore        ← Contém .env (SEMPRE commitar)
```

**Exemplo .env:**
```env
TELEGRAM_BOT_TOKEN=seu_token_aqui
GROQ_API_KEY=sua_key_aqui
MODEL_NAME=moonshotai/kimi-k2-instruct-0905
```

**Exemplo .env.example:**
```env
TELEGRAM_BOT_TOKEN=cole_seu_token_aqui
GROQ_API_KEY=cole_sua_key_aqui
MODEL_NAME=moonshotai/kimi-k2-instruct-0905
```

---

## 🆘 AINDA COM PROBLEMAS?

### Erro 401 Unauthorized persiste?

1. Confirma que atualizaste o token no Render
2. Aguarda 2-3 minutos para redeploy
3. Força redeploy manual:
   - Dashboard Render → Teu serviço → **"Manual Deploy"** → **"Deploy latest commit"**

### Bot não responde?

1. Vê logs no Render
2. Confirma que as 3 variáveis estão corretas
3. Testa localmente:
   ```bash
   # Cria .env local com novas credenciais
   echo "TELEGRAM_BOT_TOKEN=novo_token" > .env
   echo "GROQ_API_KEY=nova_key" >> .env
   echo "MODEL_NAME=moonshotai/kimi-k2-instruct-0905" >> .env
   
   # Testa
   python main.py
   ```

### Groq API não funciona?

1. Verifica em: https://console.groq.com/keys
2. Confirma que a chave existe e está ativa
3. Testa no playground: https://console.groq.com/playground

---

## 📞 SUPORTE

- **Render**: https://community.render.com
- **Telegram Bot API**: https://core.telegram.org/bots/faq
- **Groq**: https://console.groq.com/docs

---

## ✅ RESUMO RÁPIDO

1. **Revogar credenciais antigas** (Telegram + Groq)
2. **Gerar novas credenciais**
3. **Atualizar no Render** (variáveis de ambiente)
4. **Remover arquivo problemático** do Git
5. **Push** e aguardar redeploy
6. **Testar** no Telegram

**Tempo total: 10-15 minutos**

---

## 🎉 PROBLEMA RESOLVIDO!

Quando tudo funcionar:

✅ Bot rodando com novas credenciais seguras  
✅ Nada exposto no GitHub  
✅ Histórico limpo  
✅ Futuro protegido  

**Parabéns! Agora está tudo seguro! 🔒**

---

**Última atualização**: Agora  
**Prioridade**: 🔥 CRÍTICA - Faça imediatamente