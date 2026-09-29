# 02: Atualizar testes e validações automatizadas

**What to build:**
Atualizar os testes unitários e de integração de classificação para validar respostas com `choice` para gravidade, assegurando que 100% da suíte de testes passe verde.

**Blocked by:** 01-update-classifier-gravity-choice-schema

**Status:** resolved

- [x] Testes do classificador cobrem predições com formato `choice` para gravidade (ex: `{"choice": "Crítica"}` ou `"Crítica"`)
- [x] Todos os testes da suíte (`pytest`) executados com sucesso

## Comments
Criada a suíte `tests/test_classifier.py` com 11 cenários de teste parametrizados cobrindo todos os formatos de retorno e testando integração com `GravityProfile`. A suíte completa (32 testes) passou com sucesso.
