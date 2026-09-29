import logging
import time
from typing import Dict, Any, Optional
from layalog.models import ErrorIncident, GravityProfile
from layalog.profiles import get_default_profile
from layalog.audit import get_audit_logger, LayaAuditLogger
from layalog.evidence import EvidenceExtractor, FinalClassificationResolver

logger = logging.getLogger("layalog.classifier")

class LayaClassifier:
    def __init__(self, preload: bool = True, audit_logger: Optional[LayaAuditLogger] = None):
        self.router = None
        self.initialized = False
        self.audit_logger = audit_logger or get_audit_logger()
        self.evidence_extractor = EvidenceExtractor()
        self.classification_resolver = FinalClassificationResolver()
        self._init_router(preload)

    def _init_router(self, preload: bool):
        try:
            from laya import Router
            logger.info("Initializing Laya Router...")
            self.router = Router(preload=preload)
            self.initialized = True
            logger.info("Laya Router initialized successfully.")
        except ImportError as e:
            logger.error("Failed to import laya: %s", e)
            raise RuntimeError(
                "A biblioteca 'laya' não está instalada no ambiente Python. "
                "Por favor, execute: pip install laya"
            ) from e
        except Exception as e:
            logger.error("Error initializing Laya Router: %s", e)
            raise RuntimeError(f"Erro ao inicializar o motor Laya: {str(e)}") from e

    def build_questions(self, profile: Optional[GravityProfile] = None) -> Dict[str, Any]:
        p = profile or get_default_profile()
        return {
            "setor": {
                "type": "choice",
                "instructions": "Qual setor ou camada técnica do sistema é responsável ou mais diretamente associado a este erro de sistema?",
                "criteria": {
                    "Infraestrutura / Banco de Dados": "falhas de conexão, timeout de banco, queries SQL, storage, infraestrutura e disco",
                    "Autenticação / Segurança": "tokens expirados, falhas de autorização, Keycloak, permissões, middleware de autenticação",
                    "Negócio / Regras da Aplicação": "regras de validação, controllers, fluxos de domínio, tipos de dados incompatíveis, lógica interna e exceptions de código",
                    "Integrações Externas / E-mail / APIs": "falhas de comunicação com serviços de terceiros, SMTP, envio de e-mails, webhooks, chamadas HTTP externas"
                }
            },
            "tipo_falha": {
                "type": "choice",
                "instructions": "Qual é a categoria técnica principal desta falha no log?",
                "criteria": {
                    "Null Pointer / Type Error": "acesso a propriedades de objetos nulos, tipos incorretos, TypeErrors, NullPointerExceptions, retorno de tipo inválido",
                    "Database Error": "erros SQL, violações de integridade, deadlocks, falha de conexão com banco de dados",
                    "Network / Timeout": "timeouts de requisição, connection refused, DNS, perda de conexão com rede",
                    "Permission / Auth": "não autorizado, 401, 403, falha de token, credenciais inválidas",
                    "HTTP 5xx Server Error": "erro genérico de servidor interno 500, resposta HTTP malformada ou inesperada",
                    "Outros": "outros erros ou advertências não contempladas nas categorias anteriores"
                }
            },
            "gravidade": {
                "type": "choice",
                "instructions": "Classify the operational severity based on technical evidence, affected functionality, user impact and service availability.",
                "criteria": {
                    "LOW": p.criteria_baixa,
                    "MEDIUM": p.criteria_media,
                    "CRITICAL": p.criteria_critica
                }
            },
            "causa_indisponibilidade": {
                "type": "noul",
                "instructions": "Este erro representa que o sistema, serviço principal ou endpoint crítico está indisponível para o usuário final?"
            }
        }

    def classify_incident(self, raw_incident: Dict[str, Any], profile: Optional[GravityProfile] = None) -> ErrorIncident:
        if not self.router:
            raise RuntimeError("Laya Router não está instanciado.")

        active_profile = profile or get_default_profile()

        # Extract deterministic technical evidence across message, raw snippet and stacktrace
        evidence = self.evidence_extractor.extract(raw_incident)

        # Build token-safe state strictly respecting the 512-1024 token window
        state = {
            "error_message": (raw_incident.get("message") or "")[:600],
            "first_seen_time": str(raw_incident.get("first_seen_time") or ""),
            "log_level": str(raw_incident.get("level") or "ERROR"),
            "total_occurrences": int(raw_incident.get("occurrences", 1)),
            "system_context": (active_profile.system_context or "Sistema geral")[:300],
            "stacktrace_sample": (raw_incident.get("sample_stacktrace") or "")[:600],
            "raw_snippet": (raw_incident.get("sample_raw") or "")[:500]
        }

        questions = self.build_questions(active_profile)

        start_t = time.perf_counter()
        try:
            prediction = self.router.predict(state, questions)
        except Exception as e:
            duration_ms = (time.perf_counter() - start_t) * 1000
            if self.audit_logger:
                self.audit_logger.log_interaction(
                    incident_signature=raw_incident.get("signature", "unknown"),
                    profile_id=active_profile.id,
                    profile_name=active_profile.name,
                    state=state,
                    questions=questions,
                    prediction=None,
                    duration_ms=duration_ms,
                    status="error",
                    error_message=str(e)
                )
            logger.error(f"Erro ao executar router.predict do Laya: {e}")
            raise RuntimeError(f"Erro ao classificar incidente com o Laya: {str(e)}") from e

        duration_ms = (time.perf_counter() - start_t) * 1000
        if self.audit_logger:
            self.audit_logger.log_interaction(
                incident_signature=raw_incident.get("signature", "unknown"),
                profile_id=active_profile.id,
                profile_name=active_profile.name,
                state=state,
                questions=questions,
                prediction=prediction,
                duration_ms=duration_ms,
                status="success"
            )

        # Extract values from Laya prediction
        setor = "Negócio / Regras da Aplicação"
        if "setor" in prediction:
            pred_setor = prediction["setor"]
            if isinstance(pred_setor, dict):
                setor = pred_setor.get("choice") or pred_setor.get("value") or setor
            elif isinstance(pred_setor, str):
                setor = pred_setor

        tipo_falha = "Outros"
        if "tipo_falha" in prediction:
            pred_tipo = prediction["tipo_falha"]
            if isinstance(pred_tipo, dict):
                tipo_falha = pred_tipo.get("choice") or pred_tipo.get("value") or tipo_falha
            elif isinstance(pred_tipo, str):
                tipo_falha = pred_tipo

        grav_map = {
            "baixa": 1,
            "baixo": 1,
            "low": 1,
            "1": 1,
            "média": 2,
            "media": 2,
            "médio": 2,
            "medio": 2,
            "medium": 2,
            "2": 2,
            "crítica": 3,
            "critica": 3,
            "crítico": 3,
            "critico": 3,
            "critical": 3,
            "high": 3,
            "3": 3,
        }

        gravidade_val = 2
        if "gravidade" in prediction:
            pred_grav = prediction["gravidade"]
            if isinstance(pred_grav, dict):
                choice_raw = pred_grav.get("choice") or pred_grav.get("value") or pred_grav.get("label")
                if choice_raw is not None and str(choice_raw).strip().lower() in grav_map:
                    gravidade_val = grav_map[str(choice_raw).strip().lower()]
                elif "score" in pred_grav:
                    try:
                        grav_score = float(pred_grav["score"])
                        gravidade_val = max(1, min(3, round(grav_score * 2 + 1)))
                    except (ValueError, TypeError):
                        gravidade_val = 2
            elif isinstance(pred_grav, str):
                normalized = pred_grav.strip().lower()
                if normalized in grav_map:
                    gravidade_val = grav_map[normalized]
            elif isinstance(pred_grav, (int, float)):
                gravidade_val = max(1, min(3, int(round(float(pred_grav)))))

        causa_indisponibilidade = False
        if "causa_indisponibilidade" in prediction:
            pred_indisp = prediction["causa_indisponibilidade"]
            if isinstance(pred_indisp, dict):
                prob = pred_indisp.get("probability") or pred_indisp.get("value") or 0.0
                causa_indisponibilidade = bool(prob > 0.5)
            elif isinstance(pred_indisp, bool):
                causa_indisponibilidade = pred_indisp
            elif isinstance(pred_indisp, (int, float)):
                causa_indisponibilidade = bool(pred_indisp > 0.5)

        # Apply deterministic resolution based on strong technical evidence
        setor, tipo_falha, gravidade_val, causa_indisponibilidade, classification_evidence = (
            self.classification_resolver.resolve(
                predicted_setor=setor,
                predicted_tipo_falha=tipo_falha,
                predicted_gravidade=gravidade_val,
                predicted_causa_indisponibilidade=causa_indisponibilidade,
                evidence=evidence
            )
        )

        grav_label_map = {1: "Baixa", 2: "Média", 3: "Crítica"}
        gravidade_label = grav_label_map.get(gravidade_val, "Média")

        # Create title and technical summary
        msg_cleaned = raw_incident.get("message") or ""
        title = msg_cleaned.split("\n")[0][:120]
        technical_summary = self._generate_summary(title, setor, tipo_falha, gravidade_label, causa_indisponibilidade)
        recommendation = self._generate_recommendation(setor, tipo_falha, causa_indisponibilidade)

        return ErrorIncident(
            id=raw_incident["signature"],
            signature=raw_incident["signature"],
            title=title,
            setor=setor,
            tipo_falha=tipo_falha,
            gravidade=gravidade_val,
            gravidade_label=gravidade_label,
            causa_indisponibilidade=causa_indisponibilidade,
            total_occurrences=raw_incident["occurrences"],
            first_seen_line=raw_incident["first_seen_line"],
            first_seen_time=raw_incident.get("first_seen_time"),
            lines=raw_incident.get("lines", []),
            sample_raw=raw_incident["sample_raw"],
            sample_stacktrace=raw_incident.get("sample_stacktrace"),
            technical_summary=technical_summary,
            recommendation=recommendation,
            laya_raw_output=prediction,
            classification_evidence=classification_evidence
        )

    def _generate_summary(self, title: str, setor: str, tipo_falha: str, gravidade: str, indisponibilidade: bool) -> str:
        indisp_text = "com risco de indisponibilidade para os usuários" if indisponibilidade else "sem impacto na disponibilidade geral"
        return f"Falha classificada como {gravidade} no setor {setor} (Tipo: {tipo_falha}), {indisp_text}."

    def _generate_recommendation(self, setor: str, tipo_falha: str, indisponibilidade: bool) -> str:
        if "Autenticação" in setor or tipo_falha == "Permission / Auth":
            return "Verificar configuração de chaves Keycloak/OAuth, expiração de tokens e headers de autorização."
        if "Banco" in setor or tipo_falha == "Database Error":
            return "Inspecionar integridade de constraints, pool de conexões do banco de dados e índices de busca."
        if "E-mail" in setor or "Integrações" in setor:
            return "Validar conectividade com o serviço de SMTP/APIs externas e implementar retry/fallback assíncrono com filas."
        if tipo_falha == "Null Pointer / Type Error":
            return "Implementar checagem defensiva de nulidade de atributos e assegurar que as rotas de API retornem JSON serializável."
        return "Analisar as linhas de stacktrace indicadas e adicionar tratamento de exceção adequado."
