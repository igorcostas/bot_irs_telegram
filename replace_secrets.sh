#!/bin/bash
export FILTER_BRANCH_SQUELCH_WARNING=1

echo "🔐 Substituindo credenciais no histórico..."

git filter-branch --force --tree-filter '
for file in $(find . -type f -name "*.py" 2>/dev/null); do
    if [ -f "$file" ]; then
        sed -i "s/8384463381:AAFDUVD5pX9XQYzGWkM8Daj1yUL1fkPIIBA/***TELEGRAM_TOKEN_REMOVED***/g" "$file" 2>/dev/null || true
        sed -i "s/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/***GROQ_API_KEY_REMOVED***/g" "$file" 2>/dev/null || true
    fi
done
' --tag-name-filter cat -- --all

echo "✅ Credenciais substituídas"

# Limpar referências antigas
echo "🧹 Limpando referências antigas..."
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "✅ Limpeza completa!"
