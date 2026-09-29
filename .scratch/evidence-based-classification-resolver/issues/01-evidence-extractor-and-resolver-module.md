# 01: Modelo e Módulo de Extração e Resolução de Evidências (EvidenceExtractor e FinalClassificationResolver)

**What to build:**
Adicionar o campo `classification_evidence: List[str]` ao modelo `ErrorIncident` (e banco/exportador). Criar o módulo `layalog/evidence.py` contendo `EvidenceExtractor` (inspecionando message, raw snippet e stacktrace) e `FinalClassificationResolver` aplicando as regras de correção mandatórias.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] Campo `classification_evidence: List[str]` adicionado em `layalog/models.py`
- [x] Mapeamento no SQLite (`layalog/database.py`) e exportadores (`layalog/exporter.py`)
- [x] `EvidenceExtractor` implementado em `layalog/evidence.py` com detecção de `DATABASE_ERROR`, `HTTP_FAILURE`, `OUT_OF_MEMORY`, `JWT_EXPIRED`
- [x] `FinalClassificationResolver` implementado com regras de sobreposição determinística

## Comments
Implementado `layalog/evidence.py` com extração regex multi-fonte (`message`, `raw_snippet`, `stacktrace`) e resolução determinística para sobreposição das predições do Laya.
