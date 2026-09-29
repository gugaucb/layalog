# Spec: Script CLI para Inspeção e Validação dos Itens de Auditoria do Laya

## Contexto e Objetivo
Permitir a inspeção rápida e direta via terminal dos payloads e respostas brutas (*raw prediction*) retornadas pelo Laya registradas no arquivo de log de auditoria (`logs/laya_audit.jsonl`).

## Requisitos
1. Criar o script executável `scripts/inspect_audit.py`.
2. Funcionalidades do CLI:
   - Consulta por assinatura ou ID de incidente: `python scripts/inspect_audit.py <item_signature>`
   - Consulta ao último registro gravado: `python scripts/inspect_audit.py --last` (ou `-l`)
   - Listar últimos N registros com seus resumos: `python scripts/inspect_audit.py --list` (ou `-n 10`)
   - Exibir a resposta bruta do Laya (`prediction_received`) por padrão formatada em JSON legível (*pretty-printed*).
   - Opção `--full` / `-f` para exibir o registro completo (metadados + payload enviado + prediction recebida).
   - Suporte a caminho customizado do arquivo de log via `--file` / `-p`.
3. Tratamento defensivo de erros (arquivo inexistente, nenhum registro encontrado, etc.).
4. Testes automatizados em `tests/test_inspect_audit.py`.
