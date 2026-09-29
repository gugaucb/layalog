from typing import List
from layalog.models import GravityProfile

BUILTIN_PROFILES: List[GravityProfile] = [
    GravityProfile(
        id="web-app-general",
        name="Aplicação Web Geral (PHP / Node / Python)",
        description="Padrão para aplicações web monolíticas, portais e APIs com rotas HTTP.",
        system_context="Aplicação web com rotas de usuário, controladores de negócio e painel administrativo.",
        criteria_baixa="Expected behavior, validation failure, expired session or isolated user issue without service impact. Examples: ValidationException (HTTP 422), NotFoundHttpException (HTTP 404), route not found, invalid input payload.",
        criteria_media="Operational degradation affecting a feature, email or integration while the main application remains available. Examples: Swift_TransportException SMTP timeout, background sync failure, report generation timeout with retry.",
        criteria_critica="Technical evidence indicates core outage, database failure, application crash or essential API failure. Examples: Illuminate Database QueryException with connection refused or ORA error, PHP Fatal error Allowed memory size exhausted, HTTP 500 on core endpoints.",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-29T00:00:00",
    ),
    GravityProfile(
        id="keycloak-iam",
        name="Autenticação & Identidade (Keycloak / OAuth)",
        description="Otimizado para servidores de autenticação, SSO, IdPs e emissão de tokens JWT/OAuth2.",
        system_context="Servidor central de autenticação, SSO e emissão de tokens JWT/OAuth2 com auditoria de segurança constante.",
        criteria_baixa="Normal session/token lifecycle conditions or client configuration issues. Examples: JWT expired, session expired, invalid_scope, user entered invalid password, normal token refresh.",
        criteria_media="Security protections or identity provider degradation while the authentication service is operational. Examples: Brute Force Protector triggered, LDAP Federation timeout with retry, user authentication failed with bad credentials.",
        criteria_critica="Central authentication is compromised or inaccessible. Examples: unable to obtain JDBC connection, JWKS signing key unavailable, Master Realm unavailable, java.lang.OutOfMemoryError.",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-29T00:00:00",
    ),
    GravityProfile(
        id="payments-checkout",
        name="Pagamentos & Transações Financeiras",
        description="Foco em alta confiabilidade transacional, gateways bancários e conciliação.",
        system_context="Microsserviço de checkout e processamento de pagamentos com alta exigência de consistência transacional.",
        criteria_baixa="Isolated payment refusal or routine fraud check without service impact. Examples: card declined for insufficient funds, invalid card format, 3DS verification canceled.",
        criteria_media="Temporary payment provider latency or retryable webhook delay. Examples: gateway timeout with retry scheduled, async receipt email failure, transient banking webhook delay.",
        criteria_critica="Payment processing completely halted, ledger database deadlock or mass transaction failure. Examples: payment gateway connection refused, database deadlock on balance ledger, lost webhook callbacks.",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-29T00:00:00",
    ),
    GravityProfile(
        id="microservices-rest",
        name="Microsserviços & APIs REST Internas",
        description="Para arquiteturas distribuídas, service discovery e chamadas inter-serviço.",
        system_context="Arquitetura de microsserviços distribuídos com comunicação síncrona HTTP/gRPC entre serviços.",
        criteria_baixa="Client side bad requests or non-critical rate limits. Examples: HTTP 400 Bad Request, client rate limit exceeded, deprecated endpoint warning.",
        criteria_media="Inter-service latency or circuit breaker activation for satellite services. Examples: circuit breaker open on recommendation service, downstream API timeout with fallback.",
        criteria_critica="Core service mesh failure, cascading 503s or health check outage. Examples: service discovery unavailable, HTTP 503 Service Unavailable on primary API gateway, cascading connection pool exhaustion.",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-29T00:00:00",
    ),
    GravityProfile(
        id="queues-workers",
        name="Filas & Workers Assíncronos (RabbitMQ / Kafka / Celery)",
        description="Processamento em background, mensageria distribuída e consumers de eventos.",
        system_context="Processamento assíncrono de jobs em segundo plano e mensageria distribuída.",
        criteria_baixa="Routine job retries or duplicate message discards. Examples: task retry within configured limit, idempotent deduplication discard.",
        criteria_media="Non-critical job failed after retries or moderate queue backlog. Examples: task moved to DLQ, Celery task timeout with retry scheduled, background worker latency spike.",
        criteria_critica="Broker disconnect or worker crash loop. Examples: RabbitMQ/Kafka connection refused, fatal OutOfMemoryError terminating worker processes, unrecoverable poison pill.",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-29T00:00:00",
    ),
    GravityProfile(
        id="database-storage",
        name="Banco de Dados & Storage (PostgreSQL / MySQL / Redis)",
        description="Observabilidade de persistência, queries, conexões e integridade de dados.",
        system_context="Camada de persistência relacional/NoSQL e gerenciamento de conexões.",
        criteria_baixa="Non-blocking slow query notification or idle connection cleanup. Examples: slow query log warning, idle connection terminated normally.",
        criteria_media="Transient deadlock recovered by retry or elevated connection pool usage. Examples: deadlock resolved by automatic rollback, connection pool at 80%, moderate replication lag.",
        criteria_critica="Database outage, connection refusal or storage exhaustion. Examples: connection refused to port 5432/1521/3306, ORA-02393 exceeded limit, SQLSTATE[HY000], disk full, table corruption.",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-29T00:00:00",
    ),
    GravityProfile(
        id="edge-infra",
        name="Infraestrutura, Edge & Proxy (Nginx / Ingress / Cloudflare)",
        description="Camada de borda, terminação TLS, proxy reverso e roteamento de tráfego.",
        system_context="Camada de borda, terminação TLS, proxy reverso e roteamento de tráfego externo.",
        criteria_baixa="Routine edge filtering or scanner block. Examples: WAF block, IP rate limiting, 404 from internet bots.",
        criteria_media="Single upstream recycle timeout while cluster is healthy. Examples: sporadic 502 on single backend recycle, upstream timeout with backup server.",
        criteria_critica="Total ingress failure, expired SSL or universal 502/504. Examples: SSL certificate expired, DNS resolution failure, 100% backends down returning 502/503.",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-29T00:00:00",
    ),
]


def get_builtin_profiles() -> List[GravityProfile]:
    return [p.model_copy() for p in BUILTIN_PROFILES]


def get_default_profile() -> GravityProfile:
    return BUILTIN_PROFILES[0].model_copy()
