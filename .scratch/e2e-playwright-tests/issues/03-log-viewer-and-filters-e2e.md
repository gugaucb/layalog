# 03: Testes E2E do Visualizador de Logs, Filtros e Virtual Scroll

**What to build:** Testes E2E que validam as operações interativas no Log Viewer V2: alternância entre abas de severidade (ALL, ERROR, WARN, INFO), busca textual em tempo real, virtual scroll com grandes volumes de registros e expansão de detalhes de linha/stack trace.

**Blocked by:** 02 (Testes E2E do Fluxo de Upload, Progresso e Cancelamento de Logs)

**Status:** ready-for-agent

- [x] Teste de filtragem por abas de nível de log (ALL, ERROR, WARN, INFO) com contadores e renderização correspondente
- [x] Teste de busca textual dinâmica no visualizador de logs com validação de match e debounce
- [x] Teste de rolagem e virtual scroll garantindo fluidez e renderização progressiva de lotes de linhas
- [x] Teste de clique para expandir/recolher detalhes da linha de log e stack trace

