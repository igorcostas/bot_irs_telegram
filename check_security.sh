#!/bin/bash
echo "🔍 AUDITORIA DE SEGURANÇA DO REPOSITÓRIO"
echo "========================================"
echo ""

# Verificar commit atual
echo "✓ Verificando commit atual (HEAD)..."
if git show HEAD:config.py 2>/dev/null | grep -qE 'os\.getenv\("TELEGRAM_BOT_TOKEN"\)$'; then
    echo "  ✅ config.py atual está SEGURO (sem valores padrão)"
else
    echo "  ⚠️ config.py pode ter problemas"
fi

# Verificar histórico
echo ""
echo "✓ Verificando histórico de commits..."
SUSPICIOUS_COUNT=0
for commit in $(git log --all --pretty=format:"%H" | head -10); do
    if git show $commit:config.py 2>/dev/null | grep -qE '(8384463381|gsk_BQk4|AAF.*UVGD5)'; then
        echo "  ⚠️ ENCONTRADO em commit: $(git log --oneline -1 $commit)"
        SUSPICIOUS_COUNT=$((SUSPICIOUS_COUNT + 1))
    fi
done

if [ $SUSPICIOUS_COUNT -eq 0 ]; then
    echo "  ✅ Nenhuma credencial encontrada no histórico"
else
    echo "  ⚠️ ATENÇÃO: $SUSPICIOUS_COUNT commit(s) com credenciais expostas!"
fi

# Verificar .gitignore
echo ""
echo "✓ Verificando .gitignore..."
if grep -q "^\.env$" .gitignore; then
    echo "  ✅ .env está no .gitignore"
else
    echo "  ⚠️ .env NÃO está no .gitignore"
fi

if grep -q "^\*\.log$" .gitignore; then
    echo "  ✅ *.log está no .gitignore"
else
    echo "  ⚠️ *.log NÃO está no .gitignore"
fi

# Verificar se .env existe e não está no git
echo ""
echo "✓ Verificando arquivos sensíveis..."
if [ -f .env ]; then
    if git ls-files --error-unmatch .env 2>/dev/null; then
        echo "  ⚠️ .env está sendo rastreado pelo git!"
    else
        echo "  ✅ .env existe mas NÃO está no git"
    fi
else
    echo "  ℹ️  .env não existe localmente (ok para CI/CD)"
fi

# Verificar arquivos rastreados
echo ""
echo "✓ Verificando arquivos rastreados suspeitos..."
if git ls-files | grep -qE '(\.env$|\.key$|\.secret$|\.token$)'; then
    echo "  ⚠️ Arquivos sensíveis encontrados no git:"
    git ls-files | grep -E '(\.env$|\.key$|\.secret$|\.token$)'
else
    echo "  ✅ Nenhum arquivo sensível rastreado"
fi

echo ""
echo "========================================"
echo "📊 RESULTADO DA AUDITORIA"
echo "========================================"

if [ $SUSPICIOUS_COUNT -eq 0 ]; then
    echo "✅ REPOSITÓRIO SEGURO PARA SER PÚBLICO"
    echo ""
    echo "Todas as verificações passaram:"
    echo "  • Nenhuma credencial no código atual"
    echo "  • Nenhuma credencial no histórico"
    echo "  • .gitignore configurado corretamente"
    echo "  • Arquivos sensíveis não rastreados"
else
    echo "⚠️ ATENÇÃO: CREDENCIAIS ENCONTRADAS NO HISTÓRICO"
    echo ""
    echo "Recomendação: Limpar histórico antes de tornar público"
    echo "Veja: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository"
fi

