# 02: Integração no LayaClassifier e Validação de Casos Críticos (ORA-02393 + HTTP 500)

**What to build:**
Integrar `EvidenceExtractor` e `FinalClassificationResolver` no fluxo de `classify_incident` em `layalog/classifier.py`. Criar a suíte de testes em `tests/test_evidence.py` e atualizar `tests/test_classifier.py` cobrindo o cenário `ORA-02393 + HTTP 500`, `OutOfMemoryError`, `JWT expired` e validações de ocorrência única.

**Blocked by:** 01-evidence-extractor-and-resolver-module

**Status:** resolved

- [x] `classify_incident` integrado com `EvidenceExtractor` e `FinalClassificationResolver`
- [x] Ocorrências únicas preservam gravidade Crítica sem redução indevida
- [x] Testes em `tests/test_evidence.py` validam regras e cenários obrigatórios (ORA-02393 + HTTP 500, OOM, JWT)
- [x] 100% da suíte de testes passando verde

## Comments
Integrado `EvidenceExtractor` e `FinalClassificationResolver` no `LayaClassifier.classify_incident`. Validado com testes automatizados dedicados cobrindo `ORA-02393 + HTTP 500`, `OutOfMemoryError` e `JWT expired`, além de suporte a ocorrência única com gravidade Crítica. Todos os 49 testes da suíte passaram verde.
