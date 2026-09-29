# Ticket 01: Implementar Endpoint de Análise com Streaming de Progresso

**Status:** resolved  
**Type:** task  
**Feature:** processing-progress-indicator  
**Blocked by:** none  

## Descrição
Implementar um endpoint que processe o upload de log emitindo eventos de progresso e porcentagem em tempo real via Server-Sent Events (SSE) ou NDJSON (Newline Delimited JSON) conforme cada etapa (parsing, agrupamento, inferência no Laya para cada erro único, salvamento) é concluída.

## Requisitos
1. No arquivo `layalog/app.py`:
   - Criar endpoint `POST /api/analyze-stream` aceitando `UploadFile`.
   - Utilizar `StreamingResponse` com `media_type="text/event-stream"` ou `application/x-ndjson`.
   - Calcular porcentagem dinâmica:
     - Início / Parsing do log: `10%`
     - Agrupamento de incidentes: `20%`
     - Loop de classificação do Laya: progresso linear de `20%` a `90%` com base em `(idx + 1) / total_incidents`.
     - Finalização e gravação no banco: `100%`.
   - Emitir evento final de sucesso com o payload completo da análise (`AnalysisRecord`).
   - Tratamento de erro com emissão de evento de erro caso o parsing ou Laya falhem.
2. Adicionar testes unitários no `tests/test_api.py`.

## Critérios de Aceite
- O endpoint emite múltiplos eventos intermediários com `percent` crescente de 0 a 100%.
- O evento final entrega a análise pronta idêntica ao endpoint anterior.
- Testes com `pytest` passando com sucesso.
