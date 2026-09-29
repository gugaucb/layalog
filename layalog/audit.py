import json
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("layalog.audit")

DEFAULT_AUDIT_LOG_PATH = Path("logs/laya_audit.jsonl")


class LayaAuditLogger:
    """
    Registra payloads e predições do Laya em formato JSON Lines (NDJSON)
    para rastreabilidade, calibração e auditoria operacional.
    """

    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = Path(log_path) if log_path else DEFAULT_AUDIT_LOG_PATH
        self._lock = threading.Lock()
        self._ensure_log_dir()

    def _ensure_log_dir(self) -> None:
        try:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.warning(
                "Não foi possível criar o diretório de auditoria %s: %s",
                self.log_path.parent,
                e,
            )

    def log_interaction(
        self,
        incident_signature: str,
        profile_id: Optional[str],
        profile_name: Optional[str],
        state: Dict[str, Any],
        questions: Dict[str, Any],
        prediction: Optional[Dict[str, Any]] = None,
        duration_ms: float = 0.0,
        status: str = "success",
        error_message: Optional[str] = None,
    ) -> None:
        """
        Escreve um registro de auditoria em arquivo JSONL de maneira thread-safe e resiliente.
        """
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "incident_signature": incident_signature,
            "profile_id": profile_id or "default",
            "profile_name": profile_name or "Padrão",
            "status": status,
            "duration_ms": round(duration_ms, 2),
            "payload_sent": {
                "state": state,
                "questions": questions,
            },
            "prediction_received": prediction,
            "error": error_message,
        }

        try:
            line = json.dumps(record, ensure_ascii=False) + "\n"
            with self._lock:
                self._ensure_log_dir()
                with open(self.log_path, "a", encoding="utf-8") as f:
                    f.write(line)
        except Exception as e:
            logger.error("Falha ao gravar registro no log de auditoria Laya: %s", e)


_default_audit_logger: Optional[LayaAuditLogger] = None


def get_audit_logger() -> LayaAuditLogger:
    global _default_audit_logger
    if _default_audit_logger is None:
        _default_audit_logger = LayaAuditLogger()
    return _default_audit_logger
