# 1. Limpar conflitos de ambiente
cat << 'EOF' > corrigir_ambiente.py
import subprocess
import sys

def instalar_deps_uv():
    """Instala dependências principais com uv"""
    deps = [
        'requests',
        'python-telegram-bot',
        'python-dotenv',
        'openai'
    ]

    for dep in deps:
        try:
            result = subprocess.run(['uv', 'add', dep],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {dep} instalado")
            else:
                print(f"❌ {dep}: {result.stderr}")
        except Exception as e:
            print(f"⚠️ {dep}: {e}")

if __name__ == "__main__":
    instalar_deps_uv()
EOF

# Executar correção
uv run corrigir_ambiente.py
