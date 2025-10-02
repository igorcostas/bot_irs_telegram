# Criar script de correção automática
cat << 'EOF' > corrigir_referencias.sh
#!/bin/bash
echo "🔧 Corrigindo referências ao requirements.txt..."

# Corrigir em arquivos Python
find . -name "*.py" -type f -exec sed -i 's/requeriments\.txt/requirements.txt/g' {} \;

# Corrigir em arquivos Markdown
find . -name "*.md" -type f -exec sed -i 's/requeriments\.txt/requirements.txt/g' {} \;

# Corrigir em outros arquivos de texto (exceto binários)
find . -name "*.txt" -type f -exec sed -i 's/requeriments\.txt/requirements.txt/g' {} \;

echo "✅ Correções aplicadas!"
echo "🔍 Verificando se restou alguma referência..."
grep -r "requeriments" . --exclude-dir=__pycache__ --exclude-dir=.venv 2>/dev/null || echo "✅ Nenhuma referência antiga encontrada!"
EOF

# Dar permissão e executar
chmod +x corrigir_referencias.sh
./corrigir_referencias.sh
