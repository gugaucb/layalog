# Spec: Migração de Gravidade para o Tipo "choice" no LayaClassifier

## Contexto e Objetivo
Garantir que a classificação de gravidade pelo Laya utilize o tipo primitivo `"choice"` com critérios estruturados em formato de chave-valor (dicionário), alinhado com as convenções do TypeSafe/Laya para opções discretas (`Baixa`, `Média`, `Crítica`).

## Requisitos
1. No método `build_questions(profile)` de `layalog/classifier.py`, a pergunta `"gravidade"` deve ter `"type": "choice"` e `criteria` estruturado como:
   ```python
   {
       "Baixa": p.criteria_baixa,
       "Média": p.criteria_media,
       "Crítica": p.criteria_critica,
   }
   ```
2. No método `classify_incident`, o resultado de `prediction["gravidade"]` deve extrair a escolha feita pelo modelo (seja como objeto com chave `choice`/`value` ou string direta) e mapear confiavelmente para o nível numérico correspondente:
   - "Baixa" -> 1
   - "Média" -> 2
   - "Crítica" -> 3
   Mantendo suporte para retrocompatibilidade/fallback caso venha valor numérico ou score.
3. Testes unitários e mocks devem validar a classificação via `choice`.
