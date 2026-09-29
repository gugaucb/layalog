# 02: Adicionar testes automatizados para o script de inspeção

**What to build:**
Criar testes unitários em `tests/test_inspect_audit.py` validando todas as opções do CLI (`--last`, busca por assinatura, `--list`, `--full`, casos de arquivo vazio e registro não encontrado).

**Blocked by:** 01-create-audit-inspector-script

**Status:** resolved

- [x] Testes em `tests/test_inspect_audit.py` cobrem busca por assinatura, `--last`, `--list`, `--full` e tratamento de erros
- [x] Todos os testes (`pytest`) executados com sucesso

## Comments
Criada suíte completa em `tests/test_inspect_audit.py` com 9 testes automatizados cobrindo carga de dados JSONL, filtragem, formatação e execução CLI com argumentos variados.
