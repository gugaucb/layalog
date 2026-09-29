# 01: Implementar gravador de auditoria de payloads do Laya em arquivo JSONL

**What to build:**
Criar o módulo `layalog/audit.py` com o `LayaAuditLogger` para registrar em arquivo JSONL append-only (`logs/laya_audit.jsonl`) todas as interações com o Laya (`state`, `questions`, `prediction`, `duration_ms`, etc.). Integrar o logger no `LayaClassifier.classify_incident`.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] Módulo `layalog/audit.py` implementado com suporte a escrita append-only atômica em JSONL
- [x] Criação automática do diretório de logs se não existir
- [x] Integração em `LayaClassifier.classify_incident` capturando `state`, `questions`, `prediction`, duração e status
- [x] Tratamento defensivo de exceções de gravação para não impactar a classificação

## Comments
Implementado `LayaAuditLogger` thread-safe com suporte a arquivo customizado e singleton padrão, integrado ao `classify_incident` com captura de payload de envio, tempo de execução e resposta retornada.
