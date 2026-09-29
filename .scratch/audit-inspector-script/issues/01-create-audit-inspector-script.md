# 01: Criar script CLI scripts/inspect_audit.py para inspeção do raw do Laya

**What to build:**
Implementar o script executável `scripts/inspect_audit.py` com interface `argparse` para consultar registros de auditoria em `logs/laya_audit.jsonl` por assinatura, flag `--last`, flag `--list` e exibir a resposta raw do Laya em JSON formatado.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] Script `scripts/inspect_audit.py` implementado com suporte a argumentos CLI
- [x] Suporte a busca por assinatura (`item`), `--last`, `--list` e `--full`
- [x] Saída formatada em JSON legível

## Comments
Script criado com suporte completo a consulta por ID/assinatura, `--last`, `--list`, `--full`, busca parcial por texto e saída formatada com cabeçalho de metadados e resposta bruta do Laya.
