# 02: Deterministic Brute Force Protection in Evidence Resolver

**What to build:** Extend `EvidenceExtractor` and `FinalClassificationResolver` in `layalog/evidence.py` to identify Brute Force Protector events (e.g. `Brute Force Protector`, `KC-SERVICES0053`) and deterministically ensure their severity is promoted to Critical (`3`) with sector `Autenticação / Segurança` and type `Permission / Auth`.

**Blocked by:** 01-dual-dimension-prompt-criteria.md

**Status:** ready-for-agent

- [x] Add `BRUTE_FORCE_PATTERNS` to `EvidenceExtractor` (`Brute Force Protector`, `KC-SERVICES0053`).
- [x] Add deterministic override rule in `FinalClassificationResolver` promoting brute force events to Critical (`3`), sector `Autenticação / Segurança` and type `Permission / Auth`.
- [x] Add unit tests verifying evidence extraction and resolution for Brute Force Protector incidents.
