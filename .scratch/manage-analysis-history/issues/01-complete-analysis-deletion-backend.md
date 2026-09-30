# 01: Remoção completa de análise (Banco de Dados + Arquivo Físico)

**What to build:** O backend garante que ao excluir uma análise via endpoint `DELETE /api/analyses/{analysis_id}`, tanto o registro correspondente no SQLite quanto o arquivo de log físico em disco (`file_path` / pasta `uploads/`) sejam completamente removidos. Caso a análise não exista, retorna erro 404 apropriado.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [x] `delete_analysis` em `layalog/database.py` localiza e remove o arquivo físico apontado por `file_path` (ou `uploads/{id}_*`) caso exista em disco
- [x] `delete_analysis` remove o registro da tabela `analyses` no SQLite
- [x] Endpoint `DELETE /api/analyses/{analysis_id}` em `layalog/app.py` retorna 200 com payload `{"status": "deleted", "id": analysis_id}` ou 404 se não existir
- [x] Testes automatizados em `tests/test_database.py` e `tests/test_api.py` verificando remoção no banco e no disco
