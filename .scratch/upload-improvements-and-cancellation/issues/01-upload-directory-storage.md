# Ticket 01: Implementar Armazenamento de Logs na Pasta de Uploads

**Status:** resolved  
**Type:** task  
**Feature:** upload-improvements-and-cancellation  
**Blocked by:** none  

## Descrição
Garantir que todos os arquivos de log enviados pelos usuários sejam salvos em uma pasta física `uploads/` no backend, mantendo a referência persistida no SQLite e garantindo que o arquivo não seja perdido ou inacessível.

## Requisitos
1. Criar pasta `uploads/` (e incluir em `.gitignore`).
2. No `layalog/app.py`:
   - Ao receber o arquivo em `/api/analyze-stream` e `/api/analyze`, salvar o stream de bytes em `uploads/{analysis_id}_{filename}`.
   - Atualizar `layalog/database.py` para salvar o caminho do arquivo físico (`file_path`).
   - Na função `get_analysis_lines`, se o arquivo físico existir em `uploads/`, realizar a leitura otimizada de linhas diretamente do arquivo em disco (ou fallback para o banco de dados).
3. Atualizar testes unitários no `tests/test_api.py` e `tests/test_database.py`.

## Critérios de Aceite
- Ao enviar um arquivo de log, o arquivo é salvo no diretório `uploads/`.
- O endpoint de linhas busca o conteúdo preservando integridade mesmo após reiniciar o servidor.
