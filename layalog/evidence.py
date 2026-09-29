import re
from typing import Any, Dict, List, Tuple


class EvidenceExtractor:
    """
    Inspeciona error_message, raw_snippet e sample_stacktrace para extrair
    evidências técnicas determinísticas (padrões de banco, falhas HTTP, falta de memória, JWT, etc.).
    """

    # Database error patterns
    DB_PATTERNS = [
        (r"\bORA-\d{4,5}\b", "ORA error code"),
        (r"\bSQLSTATE\[[A-Z0-9]+\]", "SQLSTATE error"),
        (r"\b(?:Illuminate\\Database\\)?QueryException\b", "Database QueryException"),
        (r"\bJDBC\b", "JDBC error"),
        (r"\bdatabase\s+connection\b", "Database connection issue"),
        (r"\bdeadlock\b", "Database deadlock"),
        (r"\bPDOException\b", "PDOException"),
        (
            r"\bConnection\s+refused.*(?:5432|3306|1521|1433|database|postgres|mysql|oracle)",
            "Database connection refused",
        ),
    ]

    # HTTP failure patterns
    HTTP_PATTERNS = [
        (
            r"\b(?:HTTP(?:\/1\.[01]|\/2)?\s+)?500(?:\s+Internal\s+Server\s+Error)?\b",
            "HTTP 500 Internal Server Error",
        ),
        (
            r"\b(?:HTTP(?:\/1\.[01]|\/2)?\s+)?502(?:\s+Bad\s+Gateway)?\b",
            "HTTP 502 Bad Gateway",
        ),
        (
            r"\b(?:HTTP(?:\/1\.[01]|\/2)?\s+)?503(?:\s+Service\s+Unavailable)?\b",
            "HTTP 503 Service Unavailable",
        ),
        (
            r"\b(?:HTTP(?:\/1\.[01]|\/2)?\s+)?504(?:\s+Gateway\s+Timeout)?\b",
            "HTTP 504 Gateway Timeout",
        ),
    ]

    # Memory exhaustion patterns
    OOM_PATTERNS = [
        (r"\bOutOfMemoryError\b", "Java OutOfMemoryError"),
        (
            r"\bAllowed\s+memory\s+size\s+of\s+\d+\s+bytes\s+exhausted\b",
            "PHP Memory exhaustion",
        ),
        (
            r"\bFatalErrorException:\s+Allowed\s+memory\b",
            "Fatal memory error",
        ),
        (
            r"\bJavaScript\s+heap\s+out\s+of\s+memory\b",
            "Node.js heap out of memory",
        ),
    ]

    # JWT / Token expired patterns
    JWT_EXPIRED_PATTERNS = [
        (r"\bJWT\s+expired\b", "JWT expired"),
        (r"\bThe\s+token\s+is\s+expired\b", "Token expired"),
        (r"\bTokenExpiredError\b", "TokenExpiredError"),
        (r"\btoken\s+expired\b", "Token expired"),
        (r"\bExpiredJwtException\b", "ExpiredJwtException"),
    ]

    def extract(self, raw_incident: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa error_message, raw_snippet e sample_stacktrace.
        Retorna dicionário com flags booleanas e a lista legível de evidências encontradas.
        """
        message = str(raw_incident.get("message") or "")
        raw_snippet = str(raw_incident.get("sample_raw") or "")
        stacktrace = str(raw_incident.get("sample_stacktrace") or "")

        combined_text = f"{message}\n{raw_snippet}\n{stacktrace}"

        evidences: List[str] = []
        is_database_error = False
        is_http_failure = False
        is_out_of_memory = False
        is_jwt_expired = False

        # Check DB
        for pattern, _ in self.DB_PATTERNS:
            match = re.search(pattern, combined_text, re.IGNORECASE)
            if match:
                is_database_error = True
                matched_str = match.group(0).strip()
                # Clean backslashes for clean presentation
                matched_clean = matched_str.replace("\\", " ")
                evidences.append(f"{matched_clean} detected")

        # Check HTTP failure
        for pattern, _ in self.HTTP_PATTERNS:
            match = re.search(pattern, combined_text, re.IGNORECASE)
            if match:
                is_http_failure = True
                matched_str = match.group(0).strip()
                evidences.append(f"{matched_str} detected")

        # Check OOM
        for pattern, _ in self.OOM_PATTERNS:
            match = re.search(pattern, combined_text, re.IGNORECASE)
            if match:
                is_out_of_memory = True
                matched_str = match.group(0).strip()
                evidences.append(f"{matched_str} detected")

        # Check JWT expired
        for pattern, _ in self.JWT_EXPIRED_PATTERNS:
            match = re.search(pattern, combined_text, re.IGNORECASE)
            if match:
                is_jwt_expired = True
                matched_str = match.group(0).strip()
                evidences.append(f"{matched_str} detected")

        # Deduplicate while preserving order
        unique_evidences: List[str] = []
        for ev in evidences:
            if ev not in unique_evidences:
                unique_evidences.append(ev)

        return {
            "is_database_error": is_database_error,
            "is_http_failure": is_http_failure,
            "is_out_of_memory": is_out_of_memory,
            "is_jwt_expired": is_jwt_expired,
            "classification_evidence": unique_evidences,
        }


class FinalClassificationResolver:
    """
    Aplica regras determinísticas de resolução final para corrigir e sobrepor
    a classificação do Laya quando existirem evidências técnicas fortes.
    """

    def resolve(
        self,
        predicted_setor: str,
        predicted_tipo_falha: str,
        predicted_gravidade: int,
        predicted_causa_indisponibilidade: bool,
        evidence: Dict[str, Any],
    ) -> Tuple[str, str, int, bool, List[str]]:
        """
        Retorna (setor, tipo_falha, gravidade, causa_indisponibilidade, classification_evidence).
        """
        setor = predicted_setor
        tipo_falha = predicted_tipo_falha
        gravidade = predicted_gravidade
        causa_indisponibilidade = predicted_causa_indisponibilidade
        evidence_list = list(evidence.get("classification_evidence", []))

        is_db = evidence.get("is_database_error", False)
        is_http_fail = evidence.get("is_http_failure", False)
        is_oom = evidence.get("is_out_of_memory", False)
        is_jwt_exp = evidence.get("is_jwt_expired", False)

        # Regra 1: DATABASE_ERROR + HTTP_FAILURE
        if is_db and is_http_fail:
            tipo_falha = "Database Error"
            setor = "Infraestrutura / Banco de Dados"
            gravidade = 3  # Crítica
            causa_indisponibilidade = True

        # Regra 2: OutOfMemoryError / Esgotamento de Memória
        if is_oom:
            gravidade = 3  # Crítica
            causa_indisponibilidade = True

        # Regra 3: JWT expired (quando não há falha crítica concomitante como DB, OOM ou HTTP 5xx)
        if is_jwt_exp and not (is_db or is_oom or is_http_fail):
            gravidade = 1  # Baixa

        return (
            setor,
            tipo_falha,
            gravidade,
            causa_indisponibilidade,
            evidence_list,
        )
