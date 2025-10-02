#!/bin/bash

# Script para corrigir erros no IRS Telegram Bot
# Autor: Assistente AI (baseado em análise de código)
# Uso: bash fix_bot.sh

# Diretório do projeto
PROJECT_DIR="$HOME/irs_telegram_bot"

# Função para backup
backup_file() {
    if [ -f "$1" ]; then
        cp "$1" "$1.bak"
        echo "✅ Backup criado: $1.bak"
    else
        echo "⚠️ Arquivo não encontrado: $1"
    fi
}

# Passo 1: Backup arquivos
echo "📂 Fazendo backups..."
backup_file "$PROJECT_DIR/main.py"
backup_file "$PROJECT_DIR/conversation_handler.py"
backup_file "$PROJECT_DIR/start_reset.py"

# Passo 2: Atualizar main.py
echo "🔄 Atualizando main.py..."
cat << 'MAIN_EOF' > "$PROJECT_DIR/main.py"
from conversation_handler import create_application

if __name__ == "__main__":
    app = create_application()
    print("🤖 Bot Técnico Contábil Virtual iniciado!")
    app.run_polling()
MAIN_EOF
echo "✅ main.py atualizado!"

# Passo 3: Corrigir conversation_handler.py (mudar TELEGRAM_TOKEN para TELEGRAM_BOT_TOKEN)
echo "🔄 Corrigindo conversation_handler.py..."
sed -i 's/TELEGRAM_TOKEN/TELEGRAM_BOT_TOKEN/g' "$PROJECT_DIR/conversation_handler.py"
echo "✅ conversation_handler.py corrigido! (TELEGRAM_TOKEN -> TELEGRAM_BOT_TOKEN)"

# Passo 4: Deletar start_reset.py (com confirmação)
read -p "❓ Deseja deletar start_reset.py (arquivo desatualizado)? [s/n]: " confirm
if [[ $confirm == [sS] || $confirm == [yY] ]]; then
    rm -f "$PROJECT_DIR/start_reset.py"
    echo "✅ start_reset.py deletado!"
else
    echo "⏩ Pulando deleção de start_reset.py."
fi

# Passo 5: Limpar cache Python
echo "🧹 Limpando cache..."
find "$PROJECT_DIR" -name "__pycache__" -exec rm -rf {} +
find "$PROJECT_DIR" -name "*.pyc" -exec rm -f {} +
echo "✅ Cache limpo!"

# Passo 6: Verificação
echo "🔍 Verificando mudanças..."
if grep -q "create_application" "$PROJECT_DIR/main.py"; then
    echo "✅ main.py parece corrigido."
else
    echo "❌ Erro ao atualizar main.py. Verifique manualmente."
fi
if grep -q "TELEGRAM_BOT_TOKEN" "$PROJECT_DIR/conversation_handler.py"; then
    echo "✅ conversation_handler.py parece corrigido."
else
    echo "❌ Erro ao atualizar conversation_handler.py. Verifique manualmente."
fi

echo "🎉 Correções aplicadas! Agora rode: python3 main.py"
echo "Se houver erros, envie o traceback para depuração."
