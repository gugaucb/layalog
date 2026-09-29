# 1. Customizable Gravity Profiles with Laya Engine Calibration

Date: 2026-09-28

## Status

Accepted

## Context

LayaLog analyzes and classifies system error incidents using the Laya AI engine (System One primitives `choice`, `score`, `noul`). Previously, the criteria for determining incident severity (Baixa, Média, Crítica) were hardcoded in `LayaClassifier.build_questions()`. 

In production, severity semantics vary widely by application type:
- An authentication server (e.g. Keycloak) emitting routine user password failures or triggering brute-force thresholds has different operational risk compared to a PHP monolith experiencing unhandled exceptions or a message worker failing jobs.
- Hardcoded criteria either under-report security threats or over-report routine errors.

## Decision

1. **Model Gravity Profiles**: Introduce `GravityProfile` with mandatory three-tier criteria textareas (`criteria_baixa`, `criteria_media`, `criteria_critica`) and an optional `system_context` string.
2. **Built-in Presets vs Custom Profiles**: Provide 7 immutable built-in presets in SQLite storage (`is_builtin=True`) that users can clone and customize into new editable user profiles (`is_builtin=False`).
3. **Explicit Profile Selection**: Require explicit manual selection via dropdown on log submission (with "Aplicação Web Geral" default) to ensure deterministic classification without heuristic guessing.
4. **Dynamic Laya Scoring & State**: 
   - Pass `system_context` in Laya evaluation `state["system_context"]`.
   - Formulate question `instructions` referencing `` `system_context` ``.
   - Inject the chosen profile's criteria directly into Laya's `score` primitive criteria list (`["baixa: ...", "média: ...", "crítica: ..."]`).
5. **Historical Reproducibility**: Store `profile_id` and a JSON snapshot of the criteria inside `AnalysisRecord`.
6. **Unified UI Workflow**: Expose profile management via an accessible modal in the main view.

## Consequences

- The Laya engine receives accurate, domain-tailored semantic criteria for every log batch.
- Users gain full autonomy to adapt LayaLog to specialized technologies (Keycloak, Kafka, Payment Gateways).
- Presets provide immediate out-of-the-box value with zero required configuration.
- Profile configurations are persisted in SQLite, ensuring durability and consistency across sessions.
