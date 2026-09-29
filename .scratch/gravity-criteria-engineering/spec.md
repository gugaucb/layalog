# Spec: Engenharia de Critérios de Gravidade Observáveis e Atualização dos Perfis

## Contexto e Objetivo
Refatorar as instruções e os critérios de gravidade do LayaLog para substituir noções abstratas por evidências técnicas observáveis no log (padrões de erro, tecnologia envolvida, comportamento e disponibilidade de serviço), atualizar e recriar todos os perfis embutidos e validar a classificação dos 10 cenários de referência.

## Requisitos
1. **Schema da pergunta de gravidade no `LayaClassifier`**:
   - `type`: `"choice"`
   - `instructions`: `"Classify the operational severity based on technical evidence, affected functionality, user impact and service availability."`
   - `criteria`: Dicionário com chaves `LOW`, `MEDIUM`, `CRITICAL` alimentadas pelos critérios operacionais do perfil ativo.
   - Parser resiliente que aceita `LOW`, `MEDIUM`, `CRITICAL`, `Baixa`, `Média`, `Crítica`, valores numéricos e strings.
2. **Atualização dos Perfis Embutidos (`layalog/profiles.py`)**:
   - Critérios operacionais em inglês/baseados em evidências concretas para todas as stacks:
     - `web-app-general` (Laravel, Node, Python)
     - `keycloak-iam` (Keycloak, OAuth2, JWT)
     - `payments-checkout` (Gateways, Ledger, Webhooks)
     - `microservices-rest` (REST, Service Discovery, Circuit Breaker)
     - `queues-workers` (Celery, Kafka, RabbitMQ)
     - `database-storage` (PostgreSQL, Oracle, MySQL, Redis)
     - `edge-infra` (Nginx, TLS, Ingress)
3. **Reset e Recriação dos Perfis no Banco SQLite**:
   - Atualizar `init_db()` em `layalog/database.py` para sincronizar os perfis embutidos existentes em `layalog.db` com as novas definições.
4. **Bateria de Testes (`tests/test_criteria_validation.py`)**:
   - Validar 100% dos 10 casos de teste de evidência operacional:
     - `JWT expired` -> LOW
     - `HTTP 422 validation error` -> LOW
     - `Invalid OAuth scope` -> LOW
     - `LDAP timeout with retry` -> MEDIUM
     - `Brute Force Protector triggered` -> MEDIUM
     - `Email SMTP timeout` -> MEDIUM
     - `ORA-02393 + HTTP 500` -> CRITICAL
     - `Database connection refused` -> CRITICAL
     - `JWKS signing failure` -> CRITICAL
     - `OutOfMemoryError` -> CRITICAL
