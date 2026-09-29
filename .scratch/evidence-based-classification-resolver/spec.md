# Spec: Camada de Extração e Resolução de Evidências Técnicas (EvidenceExtractor & FinalClassificationResolver)

## Contexto e Objetivo
Evitar erros de classificação do modelo de IA (como classificar falhas de banco ORA-02393 + HTTP 500 como Autenticação ou gravidade Média) através de uma camada determinística pré/pós Laya baseada em evidências técnicas fortes.

## Requisitos
1. **EvidenceExtractor**:
   - Analisar conjuntamente `error_message`, `raw_snippet` e `stacktrace_sample`.
   - Detectar categorias:
     - `DATABASE_ERROR`: `ORA-`, `SQLSTATE`, `QueryException`, `JDBC`, `database connection`, `deadlock`, etc.
     - `HTTP_FAILURE`: Códigos `500`, `502`, `503`, `504` (ex: `HTTP 500`, `500 Internal Server Error`, etc.).
     - `OUT_OF_MEMORY`: `OutOfMemoryError`, `memory size of ... exhausted`, `FatalErrorException: Allowed memory`, etc.
     - `JWT_EXPIRED`: `JWT expired`, `Token expired`, `The token is expired`, etc.
   - Gerar lista legível de evidências (`classification_evidence`), ex: `["ORA-02393 detected", "Illuminate Database QueryException detected", "HTTP 500 detected"]`.
2. **FinalClassificationResolver**:
   - Corrigir a classificação após a inferência do Laya quando houver evidência forte:
     - Regra 1: `DATABASE_ERROR` + `HTTP_FAILURE` -> `tipo_falha = "Database Error"`, `setor = "Infraestrutura / Banco de Dados"`, `gravidade = 3` (`"Crítica"`).
     - Regra 2: `OUT_OF_MEMORY` -> `gravidade = 3` (`"Crítica"`).
     - Regra 3: `JWT_EXPIRED` (sem falhas críticas concomitantes) -> `gravidade = 1` (`"Baixa"`).
3. **Modelo e Armazenamento**:
   - Adicionar campo `classification_evidence: List[str]` em `ErrorIncident`.
   - Suporte transparente no banco de dados SQLite e exportadores.
4. **Sem Redução por Contagem de Ocorrências**:
   - Uma única ocorrência pode ser classificada como Crítica.
5. **Testes Obrigatórios**:
   - Cenário `ORA-02393 + HTTP 500` -> `Crítica`, `Infraestrutura / Banco de Dados`, `Database Error`.
   - `OutOfMemoryError` -> `Crítica`.
   - `JWT expired` -> `Baixa`.
