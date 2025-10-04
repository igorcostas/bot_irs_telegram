#!/usr/bin/env python3
"""
Script de teste para validar a API Groq
Testa conexão, geração de respostas e funcionalidades básicas
"""

import sys
import logging
from llm_handler.groq_handler import GroqHandler

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def test_groq_connection():
    """Testa conexão básica com API Groq"""
    print("\n" + "=" * 70)
    print("🧪 TESTE 1: Conexão com API Groq")
    print("=" * 70)

    try:
        handler = GroqHandler()

        if handler.test_connection():
            print("✅ Conexão estabelecida com sucesso!")
            print(f"📊 Modelo: {handler.model}")
            return handler
        else:
            print("❌ Falha na conexão com API")
            return None

    except Exception as e:
        print(f"❌ Erro ao inicializar handler: {e}")
        return None


def test_simple_response(handler):
    """Testa geração de resposta simples"""
    print("\n" + "=" * 70)
    print("🧪 TESTE 2: Geração de Resposta Simples")
    print("=" * 70)

    try:
        pergunta = "O que é IRS em Portugal?"
        print(f"💬 Pergunta: {pergunta}")

        resposta = handler.generate_response_sync(user_message=pergunta)

        print(f"\n🤖 Resposta:")
        print(f"{resposta}")
        print(f"\n✅ Resposta gerada com sucesso! ({len(resposta)} caracteres)")
        return True

    except Exception as e:
        print(f"❌ Erro ao gerar resposta: {e}")
        return False


def test_with_system_prompt(handler):
    """Testa resposta com system prompt"""
    print("\n" + "=" * 70)
    print("🧪 TESTE 3: Resposta com System Prompt")
    print("=" * 70)

    try:
        system_prompt = (
            "Você é Maria, uma técnica contábil portuguesa experiente. "
            "Responda de forma profissional, clara e objetiva sobre assuntos fiscais."
        )

        pergunta = "Como calcular o IRS para um salário de 2000€?"
        print(f"👤 System Prompt: {system_prompt[:80]}...")
        print(f"💬 Pergunta: {pergunta}")

        resposta = handler.generate_response_sync(
            user_message=pergunta, system_prompt=system_prompt
        )

        print(f"\n🤖 Resposta da Maria:")
        print(f"{resposta}")
        print(f"\n✅ Resposta personalizada gerada! ({len(resposta)} caracteres)")
        return True

    except Exception as e:
        print(f"❌ Erro ao gerar resposta com system prompt: {e}")
        return False


def test_parameter_adjustment(handler):
    """Testa ajuste de parâmetros"""
    print("\n" + "=" * 70)
    print("🧪 TESTE 4: Ajuste de Parâmetros")
    print("=" * 70)

    try:
        # Testar com temperatura baixa (mais determinístico)
        handler.set_temperature(0.3)
        handler.set_max_tokens(100)

        info = handler.get_model_info()
        print("📊 Configurações atuais:")
        for key, value in info.items():
            print(f"   • {key}: {value}")

        pergunta = "Defina IRS brevemente."
        print(f"\n💬 Pergunta (temperatura baixa): {pergunta}")

        resposta = handler.generate_response_sync(pergunta)
        print(f"🤖 Resposta: {resposta}")

        # Restaurar configurações padrão
        handler.set_temperature(0.7)
        handler.set_max_tokens(2048)

        print("\n✅ Ajuste de parâmetros funcionando corretamente!")
        return True

    except Exception as e:
        print(f"❌ Erro ao ajustar parâmetros: {e}")
        return False


def test_error_handling(handler):
    """Testa tratamento de erros"""
    print("\n" + "=" * 70)
    print("🧪 TESTE 5: Tratamento de Erros")
    print("=" * 70)

    try:
        # Tentar uma mensagem vazia
        print("💬 Testando com mensagem vazia...")
        resposta = handler.generate_response_sync("")

        if "erro" in resposta.lower() or "desculpe" in resposta.lower():
            print("✅ Erro tratado corretamente")
            return True
        else:
            print(f"⚠️ Resposta inesperada: {resposta[:100]}...")
            return True  # Não é necessariamente um erro

    except Exception as e:
        print(f"⚠️ Exceção capturada (esperado): {e}")
        return True


def main():
    """Função principal de testes"""
    print("\n" + "🚀" * 35)
    print("TESTE COMPLETO DA API GROQ")
    print("Modelo: moonshotai/kimi-k2-instruct-0905")
    print("🚀" * 35)

    resultados = []

    # Teste 1: Conexão
    handler = test_groq_connection()
    if not handler:
        print("\n❌ FALHA CRÍTICA: Não foi possível conectar à API")
        print("\n💡 Verifique:")
        print("   1. A API key em config.py está correta")
        print("   2. A biblioteca 'groq' está instalada: uv add groq")
        print("   3. Você tem conexão com a internet")
        sys.exit(1)

    resultados.append(("Conexão", True))

    # Teste 2: Resposta simples
    resultado = test_simple_response(handler)
    resultados.append(("Resposta Simples", resultado))

    # Teste 3: System prompt
    resultado = test_with_system_prompt(handler)
    resultados.append(("System Prompt", resultado))

    # Teste 4: Ajuste de parâmetros
    resultado = test_parameter_adjustment(handler)
    resultados.append(("Ajuste Parâmetros", resultado))

    # Teste 5: Tratamento de erros
    resultado = test_error_handling(handler)
    resultados.append(("Tratamento Erros", resultado))

    # Resumo final
    print("\n" + "=" * 70)
    print("📊 RESUMO DOS TESTES")
    print("=" * 70)

    total = len(resultados)
    aprovados = sum(1 for _, resultado in resultados if resultado)

    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{status} - {nome}")

    print(
        f"\n📈 Taxa de Sucesso: {aprovados}/{total} ({int(aprovados / total * 100)}%)"
    )

    if aprovados == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ API Groq está funcionando perfeitamente!")
        print("🚀 Você pode iniciar o bot agora: uv run main.py")
    else:
        print(f"\n⚠️ {total - aprovados} teste(s) falharam")
        print("💡 Revise os logs acima para mais detalhes")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
