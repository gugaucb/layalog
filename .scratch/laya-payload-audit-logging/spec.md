# Spec: Armazenamento de Payload Enviado para o Laya em Log de Auditoria

## Contexto e Objetivo
Permitir a auditoria completa de todas as requisições e julgamentos executados pelo motor de IA Laya, persistindo em formato estruturado (JSONL/NDJSON) o payload exato (`state` e `questions`), os metadados do incidente e a predição retornada.

## Requisitos
1. Módulo dedicado `layalog/audit.py` com classe `LayaAuditLogger` (ou função helper) que gerencia o arquivo `logs/laya_audit.jsonl` (com caminho configurável e criação automática de diretório).
2. Cada registro no arquivo de auditoria deve conter:
   - `timestamp`: string ISO-8601 UTC.
   - `incident_signature`: assinatura do incidente agrupado.
   - `profile_id`: ID do perfil de calibração ativo.
   - `profile_name`: Nome do perfil de calibração ativo.
   - `state`: Dicionário exato de estado enviado para `router.predict`.
   - `questions`: Dicionário exato de perguntas e critérios enviados para `router.predict`.
   - `prediction`: Resposta bruta retornada pelo Laya ou detalhes de erro se falhou.
   - `duration_ms`: Duração da chamada em milissegundos.
   - `status`: `"success"` ou `"error"`.
3. Tratamento seguro e não-bloqueante: falhas na gravação do log de auditoria não devem quebrar o fluxo principal de classificação.
4. Testes unitários cobrindo gravação, formatação dos dados e resiliência a falhas de I/O.
