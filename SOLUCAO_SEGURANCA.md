# 🔒 SOLUÇÃO PARA LIMPAR CREDENCIAIS DO HISTÓRICO

## ⚠️ PROBLEMA IDENTIFICADO

Credenciais encontradas em 4 commits antigos + arquivo .env rastreado.

---

## ✅ SOLUÇÃO 1: Limpar Histórico (RECOMENDADO)

Vamos usar o BFG Repo-Cleaner para remover credenciais do histórico.

### Passo 1: Preparar Substituições

```bash
cd ~/irs_telegram_bot

# Criar arquivo com credenciais a remover
cat > credentials.txt << 'CREDS'
8384463381:AAFDUVD5pX9XQYzGWkM8Daj1yUL1fkPIIBA
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
CREDS
```

### Passo 2: Instalar BFG

```bash
# Instalar BFG
sudo apt install bfg -y

# OU baixar manualmente:
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar
```

### Passo 3: Limpar Histórico

```bash
# Backup primeiro!
cp -r ~/irs_telegram_bot ~/irs_telegram_bot_backup

cd ~/irs_telegram_bot

# Remover .env do git
git rm --cached .env
git commit -m "Remove .env from git tracking"

# Usar BFG para limpar credenciais do histórico
bfg --replace-text credentials.txt

# OU com java:
# java -jar bfg-1.14.0.jar --replace-text credentials.txt

# Limpar refs
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Passo 4: Force Push

```bash
# ⚠️ ATENÇÃO: Isso reescreve o histórico!
git push origin main --force
```

---

## ✅ SOLUÇÃO 2: Recriar Repositório do Zero (MAIS FÁCIL)

Esta é a opção mais simples e segura.

### Passo 1: Criar Novo Repositório Limpo

```bash
cd ~

# Criar novo diretório
mkdir irs_telegram_bot_clean
cd irs_telegram_bot_clean

# Inicializar git limpo
git init
git branch -M main
```

### Passo 2: Copiar Apenas Arquivos Necessários

```bash
# Copiar arquivos (SEM o .git antigo)
cp ~/irs_telegram_bot/.gitignore .
cp ~/irs_telegram_bot/README.md .
cp ~/irs_telegram_bot/*.py .
cp ~/irs_telegram_bot/*.md .
cp ~/irs_telegram_bot/*.txt .
cp ~/irs_telegram_bot/*.pdf .
cp ~/irs_telegram_bot/*.png .
cp ~/irs_telegram_bot/requirements.txt .
cp ~/irs_telegram_bot/pyproject.toml .
cp ~/irs_telegram_bot/.env.example .

# Copiar pasta llm_handler
cp -r ~/irs_telegram_bot/llm_handler .

# NÃO copiar:
# - .env (sensível)
# - .git (tem histórico sujo)
# - *.log (logs)
# - __pycache__ (cache)
# - .venv (ambiente virtual)
```

### Passo 3: Verificar Segurança

```bash
# Verificar que config.py está seguro
cat config.py | grep -A3 "TELEGRAM_BOT_TOKEN\|GROQ_API_KEY"

# Deve mostrar APENAS:
# TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# if not TELEGRAM_BOT_TOKEN:
#     raise ValueError...
```

### Passo 4: Criar Primeiro Commit Limpo

```bash
git add .
git commit -m "Initial commit: Clean IRS Telegram Bot - Marinete

- Production-ready Telegram bot for Portuguese IRS assistance
- AI-powered using Groq API with Moonshot AI Kimi K2
- Comprehensive documentation and portfolio materials
- All credentials managed via environment variables
- No sensitive data in repository"
```

### Passo 5: Reconectar ao GitHub

```bash
# Deletar repositório antigo no GitHub (via browser):
# https://github.com/igorcostas/bot_irs_telegram/settings

# OU renomear e criar novo
git remote add origin git@github.com:igorcostas/bot_irs_telegram.git

# Force push para sobrescrever
git push -u origin main --force
```

---

## ✅ SOLUÇÃO 3: Revogar e Recriar Credenciais (EXTRA)

Além de limpar o histórico, você DEVE fazer isso:

### 1. Revogar Telegram Bot Token

1. Abra Telegram e fale com @BotFather
2. Envie: `/mybots`
3. Escolha seu bot (Marinete)
4. Clique em "API Token"
5. Clique em "Revoke current token"
6. Copie o NOVO token
7. Atualize seu arquivo .env local

### 2. Revogar Groq API Key

1. Acesse: https://console.groq.com/keys
2. Delete a key antiga
3. Crie uma nova key
4. Copie a nova key
5. Atualize seu arquivo .env local

---

## 📋 CHECKLIST COMPLETO

Antes de tornar público, confirme:

- [ ] Histórico limpo (sem credenciais)
- [ ] .env NÃO está no git
- [ ] config.py sem valores padrão
- [ ] Tokens revogados e recriados
- [ ] .gitignore correto
- [ ] Teste local funciona com novas credenciais
- [ ] README atualizado
- [ ] Portfolio files incluídos

---

## 🎯 MINHA RECOMENDAÇÃO

Use **SOLUÇÃO 2** (Recriar repositório):
- ✅ Mais rápido
- ✅ Mais seguro  
- ✅ Sem complicações
- ✅ Histórico limpo garantido

**DEPOIS disso:**
- Revogue as credenciais antigas
- Crie novas credenciais
- Teste localmente
- Torne público

