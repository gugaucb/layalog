# Domain Model: LayaLog

Glossary of canonical domain concepts and terminology for LayaLog.

## Core Concepts

### Log Entry
A single parsed record from an uploaded log stream, containing line number, timestamp, log level (e.g. INFO, WARN, ERROR), raw content, message, and optional stack trace.

### Error Incident
An aggregated group of error log entries that share a common cryptographic/structural signature. An incident is classified by the Laya AI engine with technical attributes: sector, failure type, severity, and unavailability flag.

### Gravity Profile (`GravityProfile`)
A specialized classification configuration tailored to a specific technology stack or business domain (e.g., Keycloak/IAM, Web App PHP, Payment Gateway). It customizes the semantic criteria used by the Laya AI engine to judge error severity and provides operational context.

### Built-in Preset (`PresetProfile`)
An immutable, out-of-the-box `GravityProfile` provided by the system (e.g., General Web App, Keycloak / Auth, Workers & Queues). Presets cannot be deleted or directly modified, but can be duplicated (cloned) into custom profiles.

### Custom Profile (`CustomProfile`)
A user-defined `GravityProfile` created through the UI or API. Users have full control to edit or delete custom profiles.

### Severity Criteria (`SeverityCriteria`)
The triple of semantic descriptions for the three ordered severity tiers evaluated by Laya's `score` primitive:
- **Baixa (1)**: Minor warning, expected business validation error, or routine failure without functional degradation.
- **Média (2)**: Failure in a secondary feature, active security defense triggering, or partial degradation without total system outage.
- **Crítica (3)**: Core service down, primary database failure, authentication lockout, or severe system-wide outage.

### System Context (`SystemContext`)
An optional descriptive field within a `GravityProfile` passed directly into Laya's evaluation `state["system_context"]` and referenced in question `instructions` to supply programmable common sense.

### Analysis Snapshot (`ProfileSnapshot`)
An immutable capture of the `profile_id`, profile name, and exact text criteria used during a log analysis run, stored within `AnalysisRecord` for historical auditability.
