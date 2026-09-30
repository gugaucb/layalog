# 07: Script Unificado de Execução, Relatórios e Validação de Suíte Completa

**What to build:** Script e comando centralizado para execução de toda a suíte de testes E2E com Playwright, geração de relatórios de cobertura/HTML, captura automática de screenshots em falhas e garantia de pipeline 100% verde.

**Blocked by:** 03, 04, 05, 06

**Status:** ready-for-agent

- [x] Configuração de comando no `pyproject.toml` ou script de conveniência `scripts/run_e2e_tests.py`
- [x] Configuração de relatórios e artefatos de depuração (screenshots/traces em falha)
- [x] Execução completa e validação de 100% dos testes E2E passando com estabilidade

