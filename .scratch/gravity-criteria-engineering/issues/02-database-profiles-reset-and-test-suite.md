# 02: Reset e Recriação dos Perfis no Banco SQLite e Bateria de Testes dos 10 Cenários

**What to build:**
Atualizar `init_db()` em `layalog/database.py` para resetar/atualizar as definições dos perfis embutidos no banco SQLite. Criar a suíte `tests/test_criteria_validation.py` com os 10 cenários de evidência operacional e validar 100% dos testes da aplicação.

**Blocked by:** 01-update-profiles-and-classifier-schema

**Status:** resolved

- [x] `layalog/database.py` sincroniza e atualiza os perfis embutidos no SQLite
- [x] Criado `tests/test_criteria_validation.py` cobrindo os 10 cenários especificados
- [x] Toda a suíte de testes passa com 100% de sucesso (66/66 testes)

## Comments
Perfis no banco SQLite sincronizados com as novas definições baseadas em evidências. Criado `tests/test_criteria_validation.py` cobrindo todos os 10 cenários operacionais de teste. Toda a suíte de testes da aplicação (66 testes) passou verde.
