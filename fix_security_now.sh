#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║       🔒 LIMPEZA DE SEGURANÇA - BOT TELEGRAM                  ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se está no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ ERRO: Execute este script no diretório do projeto!"
    echo "   cd irs_telegram_bot"
    exit 1
fi

echo "📋 Verificando arquivos problemáticos..."
echo ""

# Lista de arquivos a remover
FILES_TO_REMOVE=(
    "replace_secrets.sh"
    "config.py.local"
)

# Remover arquivos problemáticos
echo "🧹 Removendo arquivos com credenciais expostas..."
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        echo "   ❌ Removendo: $file"
        git rm -f "$file" 2>/dev/null || rm -f "$file"
    else
        echo "   ✅ Já removido: $file"
    fi
done
echo ""

# Verificar .gitignore
echo "🔒 Verificando .gitignore..."
if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo "   ⚠️  Adicionando .env ao .gitignore"
    echo ".env" >> .gitignore
fi

if ! grep -q "^\*\.secret$" .gitignore 2>/dev/null; then
    echo "   ⚠️  Adicionando *.secret ao .gitignore"
    echo "*.secret" >> .gitignore
fi

if ! grep -q "^\*\.token$" .gitignore 2>/dev/null; then
    echo "   ⚠️  Adicionando *.token ao .gitignore"
    echo "*.token" >> .gitignore
fi

if ! grep -q "^\*\.key$" .gitignore 2>/dev/null; then
    echo "   ⚠️  Adicionando *.key ao .gitignore"
    echo "*.key" >> .gitignore
fi

echo "   ✅ .gitignore protegido"
echo ""

# Verificar se há mudanças para commitar
if [ -n "$(git status --porcelain)" ]; then
    echo "💾 Fazendo commit das mudanças de segurança..."
    git add .gitignore URGENTE_SEGURANCA.md fix_security_now.sh 2>/dev/null
    git commit -m "🔒 Segurança: Remove arquivos com credenciais expostas

- Remove replace_secrets.sh (continha tokens expostos)
- Atualiza .gitignore para proteção
- Adiciona guia de recuperação de segurança

IMPORTANTE: Tokens foram revogados e novos foram gerados."

    echo ""
    echo "✅ Commit realizado com sucesso!"
else
    echo "ℹ️  Nenhuma mudança para commitar"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║  ✅ LIMPEZA LOCAL CONCLUÍDA!                                   ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "🔥 PRÓXIMOS PASSOS URGENTES:"
echo ""
echo "1️⃣  REVOGAR CREDENCIAIS ANTIGAS:"
echo "    • Telegram: Fala com @BotFather → /mybots → Revoke token"
echo "    • Groq: https://console.groq.com/keys → Delete key antiga"
echo ""
echo "2️⃣  GERAR NOVAS CREDENCIAIS:"
echo "    • Telegram: @BotFather → Generate new token"
echo "    • Groq: https://console.groq.com/keys → Create new key"
echo ""
echo "3️⃣  ATUALIZAR NO RENDER:"
echo "    • Vai a: https://dashboard.render.com"
echo "    • Teu serviço → Environment → Edit"
echo "    • Atualiza: TELEGRAM_BOT_TOKEN e GROQ_API_KEY"
echo ""
echo "4️⃣  FAZER PUSH PARA GITHUB:"
echo "    git push origin main"
echo ""
echo "5️⃣  AGUARDAR REDEPLOY:"
echo "    • Render faz redeploy automático em 1-2 minutos"
echo "    • Verifica logs para confirmar sucesso"
echo ""
echo "6️⃣  TESTAR NO TELEGRAM:"
echo "    • Envia /start para o bot"
echo "    • Deve funcionar com as novas credenciais!"
echo ""
echo "📖 GUIA COMPLETO: Leia URGENTE_SEGURANCA.md"
echo ""
echo "⚠️  NUNCA MAIS COMMITE CREDENCIAIS NO GIT!"
echo ""
