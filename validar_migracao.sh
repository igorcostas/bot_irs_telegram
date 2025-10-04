#!/bin/bash
# Script de Validação da Migração xAI → Groq
# Versão: 1.0.0
# Data: 2025-01-04

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Emojis
CHECK="✅"
CROSS="❌"
WARN="⚠️"
INFO="ℹ️"
ROCKET="🚀"

echo -e "${BLUE}${BOLD}"
echo "════════════════════════════════════════════════════════════"
echo "  VALIDAÇÃO DA MIGRAÇÃO: xAI Grok → Groq API"
echo "  Modelo: moonshotai/kimi-k2-instruct-0905"
echo "════════════════════════════════════════════════════════════"
echo -e "${NC}"

ERRORS=0
WARNINGS=0

# Função para mostrar progresso
show_step() {
    echo -e "\n${BOLD}${BLUE}▶ $1${NC}"
}

# Função para sucesso
show_success() {
    echo -e "  ${GREEN}${CHECK} $1${NC}"
}

# Função para erro
show_error() {
    echo -e "  ${RED}${CROSS} $1${NC}"
    ((ERRORS++))
}

# Função para aviso
show_warning() {
    echo -e "  ${YELLOW}${WARN} $1${NC}"
    ((WARNINGS++))
}

# Função para info
show_info() {
    echo -e "  ${BLUE}${INFO} $1${NC}"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASSO 1: Verificar Python
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_step "Verificando Python..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    show_success "Python instalado: $PYTHON_VERSION"
else
    show_error "Python3 não encontrado!"
    exit 1
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASSO 2: Verificar biblioteca groq
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_step "Verificando biblioteca 'groq'..."

if python3 -c "import groq" 2>/dev/null; then
    GROQ_VERSION=$(python3 -c "import groq; print(groq.__version__)" 2>/dev/null || echo "desconhecida")
    show_success "Biblioteca 'groq' instalada (versão: $GROQ_VERSION)"
else
    show_error "Biblioteca 'groq' NÃO instalada!"
    show_info "Execute: uv add groq"
    show_info "ou: pip install groq"
    exit 1
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASSO 3: Verificar config.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_step "Verificando config.py..."

if [ -f "config.py" ]; then
    show_success "Arquivo config.py encontrado"

    # Verificar GROQ_API_KEY
    if grep -q "GROQ_API_KEY" config.py; then
        show_success "GROQ_API_KEY configurada"

        # Verificar se a chave está preenchida
        if grep -q 'GROQ_API_KEY = "gsk_' config.py; then
            show_success "API Key parece válida (começa com 'gsk_')"
        else
            show_warning "API Key pode estar incorreta"
        fi
    else
        show_error "GROQ_API_KEY não encontrada em config.py"
    fi

    # Verificar MODEL_NAME
    if grep -q "moonshotai/kimi-k2-instruct" config.py; then
        show_success "Modelo Moonshot AI configurado"
    else
        show_warning "Modelo pode não estar configurado corretamente"
    fi

    # Verificar LLM_PROVIDER
    if grep -q 'LLM_PROVIDER = "groq"' config.py; then
        show_success "LLM_PROVIDER configurado como 'groq'"
    else
        show_warning "LLM_PROVIDER pode não estar configurado"
    fi
else
    show_error "config.py não encontrado!"
    exit 1
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASSO 4: Verificar groq_handler.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_step "Verificando groq_handler.py..."

if [ -f "llm_handler/groq_handler.py" ]; then
    show_success "Handler groq_handler.py encontrado"

    if grep -q "class GroqHandler" llm_handler/groq_handler.py; then
        show_success "Classe GroqHandler definida"
    else
        show_error "Classe GroqHandler não encontrada no arquivo"
    fi
else
    show_error "llm_handler/groq_handler.py não encontrado!"
    exit 1
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASSO 5: Verificar conversation_handler.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_step "Verificando conversation_handler.py..."

if [ -f "conversation_handler.py" ]; then
    show_success "Arquivo conversation_handler.py encontrado"

    if grep -q "from llm_handler.groq_handler import GroqHandler" conversation_handler.py; then
        show_success "Import do GroqHandler correto"
    else
        show_error "Import do GroqHandler não encontrado!"
        show_info "Deveria ter: from llm_handler.groq_handler import GroqHandler"
    fi

    if grep -q "self.groq = GroqHandler()" conversation_handler.py; then
        show_success "Instância do GroqHandler criada"
    else
        show_warning "Instância do GroqHandler pode não estar criada"
    fi
else
    show_error "conversation_handler.py não encontrado!"
    exit 1
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASSO 6: Executar testes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_step "Executando testes da API Groq..."

if [ -f "test_groq_api.py" ]; then
    show_info "Executando test_groq_api.py..."

    if python3 test_groq_api.py 2>&1 | tee /tmp/groq_test.log; then
        if grep -q "TODOS OS TESTES PASSARAM" /tmp/groq_test.log; then
            show_success "Todos os testes passaram!"
        else
            show_warning "Alguns testes podem ter falhado"
            show_info "Verifique o output acima para detalhes"
        fi
    else
        show_error "Erro ao executar testes"
        show_info "Verifique os logs acima"
    fi
else
    show_warning "test_groq_api.py não encontrado - testes não executados"
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PASSO 7: Verificar arquivos antigos
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_step "Verificando arquivos antigos (backup)..."

if [ -f "llm_handler/grok_handler.py" ]; then
    show_info "grok_handler.py (xAI) ainda existe - pode ser usado como backup"
fi

if [ -f "llm_handler/llm_handler.py" ]; then
    show_info "llm_handler.py antigo ainda existe - pode ser removido"
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RESUMO FINAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "\n${BLUE}${BOLD}"
echo "════════════════════════════════════════════════════════════"
echo "  RESUMO DA VALIDAÇÃO"
echo "════════════════════════════════════════════════════════════"
echo -e "${NC}"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}${BOLD}🎉 PERFEITO! Migração concluída com sucesso!${NC}\n"
    echo -e "${GREEN}${CHECK} Erros: 0${NC}"
    echo -e "${GREEN}${CHECK} Avisos: 0${NC}"
    echo ""
    echo -e "${BLUE}${BOLD}${ROCKET} Próximos passos:${NC}"
    echo -e "  1. Execute: ${BOLD}uv run main.py${NC}"
    echo -e "  2. No Telegram, envie: ${BOLD}/start${NC}"
    echo -e "  3. Complete o questionário de 20 perguntas"
    echo ""
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}${BOLD}${WARN} Migração OK com alguns avisos${NC}\n"
    echo -e "${GREEN}${CHECK} Erros: 0${NC}"
    echo -e "${YELLOW}${WARN} Avisos: $WARNINGS${NC}"
    echo ""
    echo -e "${BLUE}${INFO} Revise os avisos acima, mas você pode prosseguir.${NC}"
    echo -e "${BLUE}${BOLD}${ROCKET} Execute: ${NC}uv run main.py${NC}"
    echo ""
else
    echo -e "${RED}${BOLD}${CROSS} Migração incompleta - corrija os erros${NC}\n"
    echo -e "${RED}${CROSS} Erros: $ERRORS${NC}"
    echo -e "${YELLOW}${WARN} Avisos: $WARNINGS${NC}"
    echo ""
    echo -e "${RED}${INFO} Corrija os erros listados acima antes de continuar.${NC}"
    echo ""
    exit 1
fi

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

# Retornar código de saída apropriado
if [ $ERRORS -gt 0 ]; then
    exit 1
else
    exit 0
fi
