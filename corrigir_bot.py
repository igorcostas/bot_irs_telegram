#!/usr/bin/env python3
import re
import os
import subprocess

def analisar_conversation_handler():
    """Analisa conversation_handler.py para encontrar estrutura correta"""
    print("🔍 Analisando conversation_handler.py...")
    
    with open('conversation_handler.py', 'r') as f:
        content = f.read()
    
    # Encontrar classes
    classes = re.findall(r'^class (\w+)', content, re.MULTILINE)
    print(f"📦 Classes encontradas: {classes}")
    
    # Encontrar funções standalone
    functions = re.findall(r'^def (\w+)', content, re.MULTILINE)
    print(f"⚙️ Funções standalone: {functions}")
    
    # Verificar se get_conversation_handler está dentro de classe
    if 'get_conversation_handler' in content:
        # Encontrar em qual classe está
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'def get_conversation_handler' in line:
                # Buscar classe acima desta linha
                for j in range(i-1, -1, -1):
                    if lines[j].startswith('class '):
                        classe = re.findall(r'class (\w+)', lines[j])[0]
                        print(f"🎯 get_conversation_handler está na classe: {classe}")
                        return classe, functions
                break
    
    return None, functions

def corrigir_main_py(classe_handler, functions):
    """Corrige main.py baseado na análise"""
    print("🔧 Corrigindo main.py...")
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Backup
    with open('main.py.backup', 'w') as f:
        f.write(content)
    print("💾 Backup criado: main.py.backup")
    
    # Corrigir imports
    if classe_handler and 'create_application' in functions:
        new_import = f"from conversation_handler import {classe_handler}, create_application"
    elif classe_handler:
        new_import = f"from conversation_handler import {classe_handler}"
    elif 'create_application' in functions:
        new_import = "from conversation_handler import create_application"
    else:
        print("❌ Não consegui identificar o que importar!")
        return False
    
    # Substituir import na linha 3
    content = re.sub(r'^from conversation_handler import.*$', new_import, content, flags=re.MULTILINE)
    
    # Corrigir uso do handler
    if classe_handler:
        # Opção 1: Usar classe + método
        old_pattern = r'app\.add_handler\(MessageHandler\(filters\.TEXT & ~filters\.COMMAND, .*?\)\)'
        new_handler = f"""handler_instance = {classe_handler}()
conversation_handler_obj = handler_instance.get_conversation_handler()
app.add_handler(conversation_handler_obj)"""
        content = re.sub(old_pattern, new_handler, content)
    
    elif 'create_application' in functions:
        # Opção 2: Usar create_application
        content = re.sub(r'app\.add_handler\(MessageHandler.*?\)', '# Handler adicionado via create_application', content)
        content = re.sub(r'app = Application\.builder.*?\.build\(\)', 'app = create_application()', content)
    
    # Salvar arquivo corrigido
    with open('main.py', 'w') as f:
        f.write(content)
    
    print("✅ main.py corrigido!")
    return True

def testar_correcao():
    """Testa se a correção funcionou"""
    print("🧪 Testando correção...")
    
    try:
        result = subprocess.run(['uv', 'run', 'python3', '-c', 
                               'import main; print("✅ main.py importa sem erros")'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Import test passou!")
            return True
        else:
            print(f"❌ Import test falhou: {result.stderr}")
            return False
    except Exception as e:
        print(f"⚠️ Erro no teste: {e}")
        return False

def main():
    print("🚀 Script de Correção Automática do Bot IRS")
    print("=" * 50)
    
    # Verificar se arquivos existem
    if not os.path.exists('conversation_handler.py'):
        print("❌ conversation_handler.py não encontrado!")
        return
    
    if not os.path.exists('main.py'):
        print("❌ main.py não encontrado!")
        return
    
    # Analisar estrutura
    classe_handler, functions = analisar_conversation_handler()
    
    # Corrigir main.py
    if corrigir_main_py(classe_handler, functions):
        # Testar correção
        if testar_correcao():
            print("\n🎉 Correção bem-sucedida!")
            print("Agora execute: uv run main.py")
        else:
            print("\n⚠️ Correção aplicada, mas ainda há erros.")
            print("Verifique o arquivo manualmente.")
    else:
        print("\n❌ Falha na correção automática.")
        print("Será necessário correção manual.")

if __name__ == "__main__":
    main()

