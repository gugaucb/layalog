# 01: Configurar gravidade como primitive choice no LayaClassifier

**What to build:**
Definir a pergunta de gravidade no `LayaClassifier.build_questions` utilizando `"type": "choice"` com dicionário de critérios com as chaves `Baixa`, `Média` e `Crítica`. Em `classify_incident`, processar o retorno de `choice` ou `value` mapeando para os valores numéricos 1, 2, 3 e seus respectivos rótulos, com tratamento defensivo.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] `build_questions` usa `"type": "choice"` com dict `{"Baixa": ..., "Média": ..., "Crítica": ...}`
- [x] `classify_incident` extrai `choice` / `value` como string ou objeto e mapeia `"Baixa"` -> 1, `"Média"` -> 2, `"Crítica"` -> 3
- [x] Fallbacks e robustez mantidos para compatibilidade

## Comments
Implementado em `layalog/classifier.py` com suporte completo ao formato de dicionário de opções no critério de gravidade e normalização flexível para os níveis 1, 2 e 3.
