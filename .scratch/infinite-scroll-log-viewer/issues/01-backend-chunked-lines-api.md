# Ticket 01: Implementar Endpoint de Linhas Paginadas no Backend

**Status:** resolved  
**Type:** task  
**Feature:** infinite-scroll-log-viewer  

## Descrição
Atualmente, o backend envia todo o texto bruto do log no endpoint `/api/analyze` e `/api/analyses/{id}`. Para logs com milhares de linhas, isso consome memória excessiva do cliente e gera payloads pesados.

## Requisitos
1. Adicionar função no `layalog/database.py` para ler um intervalo de linhas (`start_line`, `limit`) de um arquivo salvo no banco sem carregar tudo desnecessariamente na memória.
2. Criar endpoint na API:
   - `GET /api/analyses/{analysis_id}/lines?start_line=1&limit=200`
   - Retorno JSON:
     ```json
     {
       "analysis_id": "...",
       "start_line": 1,
       "limit": 200,
       "total_lines": 13620,
       "lines": ["linha 1...", "linha 2..."]
     }
     ```
3. Remover o campo `raw_log_text` pesado das respostas padrão de `/api/analyze` e `/api/analyses/{id}`, mantendo apenas metadados e estatísticas.
4. Adicionar testes unitários no `tests/test_api.py` e `tests/test_database.py`.

## Critérios de Aceite
- Requisições para `/api/analyses/{id}/lines?start_line=100&limit=50` retornam exatamente 50 linhas a partir da linha 100 com status 200.
- Requisição com ID inválido retorna 404.
- Testes automatizados passando com `pytest`.
