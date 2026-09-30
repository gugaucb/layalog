# 01: Setup do ambiente de testes E2E com Playwright & Pytest Fixtures

**What to build:** Infraestrutura base de testes automatizados com Playwright e Pytest: servidor FastAPI efêmero em porta dinâmica/isolada, banco de dados SQLite isolado por execução, fixtures de browser/page para testes assíncronos e helpers/page objects reutilizáveis.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [x] Fixture em `tests/e2e/conftest.py` para iniciar e parar o servidor LayaLog em thread/processo em segundo plano usando porta livre
- [x] Isolamento de banco de dados (`layalog.db` temporário por sessão/teste) e diretório de uploads isolado
- [x] Configuração de fixture `page` do Playwright com suporte headless para execução rápida e helpers de navegação
- [x] Smoke test `tests/e2e/test_smoke_e2e.py` verificando carregamento da página principal e elementos essenciais do DOM

