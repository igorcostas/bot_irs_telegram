# 🚀 Início Rápido - Bot IRS com Groq API

## ⚡ Comandos Essenciais

### 1️⃣ Instalar Dependências
```bash
uv add groq
```

### 2️⃣ Validar Migração
```bash
./validar_migracao.sh
```

### 3️⃣ Testar API
```bash
uv run test_groq_api.py
```

### 4️⃣ Iniciar Bot
```bash
uv run main.py
```

---

## ✅ Checklist Rápido

- [ ] Biblioteca `groq` instalada
- [ ] API key configurada em `config.py`
- [ ] Testes passando (5/5)
- [ ] Bot iniciado sem erros
- [ ] Teste no Telegram com `/start`

---

## 📋 O Que Mudou?

| Antes (xAI) | Agora (Groq) |
|-------------|--------------|
| `grok-4` | `moonshotai/kimi-k2-instruct-0905` |
| API xAI | API Groq |
| Pago | Gratuito |
| 4k tokens | 8k tokens |

---

## 🔧 Configuração

A API key já está configurada em `config.py`:

```python
GROQ_API_KEY = "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"
MODEL_NAME = "moonshotai/kimi-k2-instruct-0905"
```

✅ **Pronto para usar!**

---

## 🧪 Teste Rápido da API

```python
from llm_handler.groq_handler import GroqHandler

handler = GroqHandler()

# Teste de conexão
if handler.test_connection():
    print("✅ API funcionando!")
    
# Teste de resposta
resposta = handler.generate_response_sync("O que é IRS?")
print(resposta)
```

---

## 🤖 Testando o Bot

### No Terminal:
```bash
uv run main.py
```

**Saída esperada:**
```
✅ Main Integration module criado!
✅ Bot configurado com sistema de análise completa!
🤖 Bot Técnico Contábil Virtual iniciado!
```

### No Telegram:
1. Abra o bot
2. Envie: `/start`
3. Responda as 20 perguntas
4. Receba análise completa

---

## ⚠️ Problemas Comuns

### Erro: "groq module not found"
```bash
uv add groq
```

### Erro: "invalid API key"
Verifique `config.py`:
```python
GROQ_API_KEY = "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"
```

### Bot não responde
1. Verifique logs: `tail -f bot_contabil.log`
2. Teste API: `uv run test_groq_api.py`
3. Reinicie bot: `Ctrl+C` → `uv run main.py`

---

## 📊 Rate Limits (Tier Gratuito)

- **30 requisições/minuto**
- **10.000 tokens/minuto**

Para uso intenso, adicione delays:
```python
import asyncio
await asyncio.sleep(2)
```

---

## 📚 Documentação Completa

- `RESUMO_ALTERACOES.md` - O que mudou
- `MIGRACAO_GROQ.md` - Guia técnico completo
- `test_groq_api.py` - Suite de testes

---

## 🎯 Próximos Passos

1. ✅ Execute: `./validar_migracao.sh`
2. ✅ Se tudo OK: `uv run main.py`
3. ✅ Teste no Telegram
4. 🎉 **Pronto!**

---

## 💡 Dicas

### Respostas mais criativas:
```python
handler.set_temperature(0.9)
```

### Respostas mais longas:
```python
handler.set_max_tokens(4000)
```

### Ver configurações:
```python
print(handler.get_model_info())
```

---

## 🆘 Suporte

- **Logs:** `bot_contabil.log`
- **Groq Console:** https://console.groq.com/
- **Documentação:** `MIGRACAO_GROQ.md`

---

## ✅ Status

| Componente | Status |
|------------|--------|
| API Groq | ✅ Configurada |
| Handler | ✅ Criado |
| Testes | ✅ Disponíveis |
| Bot | ✅ Atualizado |
| **Pronto** | **🟢 SIM** |

---

**Última atualização:** 2025-01-04  
**Versão:** 2.0.0 - Groq Edition

🚀 **Comece agora:** `uv run main.py`
