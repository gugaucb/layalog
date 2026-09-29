from typing import List, Optional
from datetime import datetime
from layalog.models import GravityProfile

BUILTIN_PROFILES: List[GravityProfile] = [
    GravityProfile(
        id="web-app-general",
        name="Aplicação Web Geral (PHP / Node / Python)",
        description="Padrão para aplicações web monolíticas, portais e APIs com rotas HTTP.",
        system_context="Aplicação web com rotas de usuário, controladores de negócio e painel administrativo.",
        criteria_baixa="erros de validação de formulário (422), rotas não encontradas (404), warnings de depreciação e assets estáticos ausentes",
        criteria_media="exceções não tratadas em páginas secundárias ou relatórios não críticos e timeouts com fallback ativo",
        criteria_critica="exceções não tratadas no kernel/middleware global, indisponibilidade do banco de dados ou crash do processo web",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-28T00:00:00"
    ),
    GravityProfile(
        id="keycloak-iam",
        name="Autenticação & Identidade (Keycloak / OAuth)",
        description="Otimizado para servidores de autenticação, SSO, IdPs e emissão de tokens JWT/OAuth2.",
        system_context="Servidor central de autenticação, SSO e emissão de tokens JWT/OAuth2 com auditoria de segurança constante.",
        criteria_baixa="tokens expirados em rotina normal de clientes, escopos inválidos de requisição ou avisos informativos de sessão",
        criteria_media="falhas de login, eventos do Brute Force Protector, tentativas de acesso não autorizado e lentidão em federação externa (LDAP/IdP)",
        criteria_critica="banco de dados do Keycloak inacessível, falha de chaves de assinatura JWKS, indisponibilidade do Master Realm ou travamento da JVM",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-28T00:00:00"
    ),
    GravityProfile(
        id="payments-checkout",
        name="Pagamentos & Transações Financeiras",
        description="Foco em alta confiabilidade transacional, gateways bancários e conciliação.",
        system_context="Microsserviço de checkout e processamento de pagamentos com alta exigência de consistência transacional.",
        criteria_baixa="recusa de cartão por saldo insuficiente do cliente ou bloqueio de rotina em antifraude",
        criteria_media="timeout temporário com adquirente que entra em fila de retry e falha no envio de notificações de recibo",
        criteria_critica="perda de comunicação total com o gateway bancário, deadlocks em tabelas de ledger/saldo ou falha na confirmação de webhooks com perda de pedidos",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-28T00:00:00"
    ),
    GravityProfile(
        id="microservices-rest",
        name="Microsserviços & APIs REST Internas",
        description="Para arquiteturas distribuídas, service discovery e chamadas inter-serviço.",
        system_context="Arquitetura de microsserviços distribuídos com comunicação síncrona HTTP/gRPC entre serviços.",
        criteria_baixa="bad request de clientes (400), rate limit preventivo atingido e chamadas a endpoints descontinuados",
        criteria_media="circuit breaker aberto temporariamente para um serviço satélite e degradação de latência acima do threshold",
        criteria_critica="falha no service discovery / service mesh, loop infinito de chamadas esgotando portas ou erro 500 no endpoint de health check causando cascata de restarts",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-28T00:00:00"
    ),
    GravityProfile(
        id="queues-workers",
        name="Filas & Workers Assíncronos (RabbitMQ / Kafka / Celery)",
        description="Processamento em background, mensageria distribuída e consumers de eventos.",
        system_context="Processamento assíncrono de jobs em segundo plano e mensageria distribuída.",
        criteria_baixa="retry automático de tarefa dentro do limite configurado e descarte esperado de eventos duplicados",
        criteria_media="tarefa secundária movida para Dead Letter Queue (DLQ) após esgotar retries e acúmulo de mensagens sem parada de workers",
        criteria_critica="desconexão total com o broker de mensagens, poison pill travando todos os workers em loop ou perda de mensagens persistidas",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-28T00:00:00"
    ),
    GravityProfile(
        id="database-storage",
        name="Banco de Dados & Storage (PostgreSQL / MySQL / Redis)",
        description="Observabilidade de persistência, queries, conexões e integridade de dados.",
        system_context="Camada de persistência relacional/NoSQL e gerenciamento de conexões.",
        criteria_baixa="notificações de queries lentas pontuais e encerramento de conexões ociosas",
        criteria_media="deadlocks esporádicos resolvidos por rollback, conexões do pool acima de 80% e lag moderado de replicação",
        criteria_critica="esgotamento total do connection pool (Too many connections), corrupção de tabelas, falha do primário sem failover e disco de storage cheio",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-28T00:00:00"
    ),
    GravityProfile(
        id="edge-infra",
        name="Infraestrutura, Edge & Proxy (Nginx / Ingress / Cloudflare)",
        description="Camada de borda, terminação TLS, proxy reverso e roteamento de tráfego.",
        system_context="Camada de borda, terminação TLS, proxy reverso e roteamento de tráfego externo.",
        criteria_baixa="bloqueios de WAF/IP, scanners automatizados na internet e 404 de URLs inexistentes",
        criteria_media="timeouts de upstream para instâncias isoladas em reciclagem e picos esporádicos de 502 com réplicas saudáveis",
        criteria_critica="certificado SSL expirado, falha total de DNS, 100% dos backends inacessíveis (502 Bad Gateway generalizado)",
        is_builtin=True,
        created_at="2026-09-28T00:00:00",
        updated_at="2026-09-28T00:00:00"
    )
]

def get_builtin_profiles() -> List[GravityProfile]:
    return [p.model_copy() for p in BUILTIN_PROFILES]

def get_default_profile() -> GravityProfile:
    return BUILTIN_PROFILES[0].model_copy()
