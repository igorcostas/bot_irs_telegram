#!/bin/bash
echo "🔧 Correção Simples do Bot"

# Backup
cp main.py main.py.backup

# Ver estrutura
echo "🔍 Analisando estrutura..."
echo "Classes:"
grep "^class " conversation_handler.py
echo "Funções:"
grep "^def " conversation_handler.py

# Correção baseada no padrão mais comum
echo "📝 Aplicando correção..."

# Tentar correção 1: create_application
sed -i '3s/.*/from conversation_handler import create_application/' main.py
sed -i 's/app = Application.builder().token(TOKEN).build()/app = create_application()/' main.py
sed -i '/MessageHandler.*handle_conversation/d' main.py

echo "✅ Correção aplicada!"
echo "🧪 Testando..."
uv run main.py
