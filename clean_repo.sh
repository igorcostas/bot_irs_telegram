#!/bin/bash
set -e

echo "🔧 INICIANDO LIMPEZA DO REPOSITÓRIO"
echo "===================================="
echo ""

# 1. Remover .env do tracking
echo "📝 Passo 1: Removendo .env do git..."
if git ls-files --error-unmatch .env 2>/dev/null; then
    git rm --cached .env
    git commit -m "Remove .env from tracking" || true
    echo "✅ .env removido do tracking"
else
    echo "✅ .env já não está sendo rastreado"
fi

echo ""
echo "📝 Passo 2: Criando arquivo de substituição de credenciais..."
cat > /tmp/credentials.txt << 'CREDS'
8384463381:AAFDUVD5pX9XQYzGWkM8Daj1yUL1fkPIIBA==>***REMOVED***
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==>***REMOVED***
AAFDUVD5pX9XQYzGWkM8Daj1yUL1fkPIIBA==>***REMOVED***
BQk4o0jLcqEhHQlo7207WGdyb3FYFhNekdbYTEotULLL6Hu63SQl==>***REMOVED***
CREDS

echo "✅ Arquivo de credenciais criado"

echo ""
echo "📝 Passo 3: Verificando se BFG está disponível..."
if command -v bfg &> /dev/null; then
    echo "✅ BFG encontrado"
    USE_BFG=true
elif [ -f "/usr/bin/bfg" ]; then
    echo "✅ BFG encontrado em /usr/bin/bfg"
    USE_BFG=true
else
    echo "⚠️  BFG não encontrado, usando git filter-repo"
    USE_BFG=false
fi

echo ""
echo "📝 Passo 4: Limpando histórico..."

if [ "$USE_BFG" = true ]; then
    # Usar BFG
    echo "Usando BFG Repo-Cleaner..."
    bfg --replace-text /tmp/credentials.txt .
else
    # Usar git filter-branch (método manual)
    echo "Usando git filter-branch..."
    git filter-branch --force --index-filter \
        'git rm --cached --ignore-unmatch .env' \
        --prune-empty --tag-name-filter cat -- --all
    
    # Substituir credenciais em todos os commits
    git filter-branch --force --tree-filter \
        "find . -type f -name 'config.py' -exec sed -i 's/8384463381:AAFDUVD5pX9XQYzGWkM8Daj1yUL1fkPIIBA/***REMOVED***/g' {} \; 2>/dev/null || true; \
         find . -type f -name 'config.py' -exec sed -i 's/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/***REMOVED***/g' {} \; 2>/dev/null || true" \
        --prune-empty --tag-name-filter cat -- --all
fi

echo "✅ Histórico limpo"

echo ""
echo "📝 Passo 5: Limpando referências antigas..."
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "✅ Referências limpas"

echo ""
echo "📝 Passo 6: Verificando limpeza..."
if git log --all -p -S "8384463381" | grep -q "8384463381"; then
    echo "⚠️  Ainda há credenciais no histórico"
else
    echo "✅ Nenhuma credencial encontrada no histórico"
fi

echo ""
echo "===================================="
echo "✅ LIMPEZA CONCLUÍDA COM SUCESSO!"
echo "===================================="
echo ""
echo "Próximos passos:"
echo "1. Verificar que tudo está OK localmente"
echo "2. Revogar credenciais antigas (BotFather + Groq)"
echo "3. Criar novas credenciais"
echo "4. Atualizar .env local"
echo "5. Force push: git push origin main --force"
echo ""

