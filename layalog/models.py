from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class LogEntry(BaseModel):
    line_number: int
    timestamp: Optional[str] = None
    level: str = "ERROR"
    message: str
    raw_content: str
    stacktrace: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ErrorIncident(BaseModel):
    id: str
    signature: str
    title: str
    setor: str
    tipo_falha: str
    gravidade: int  # 1 (Baixa), 2 (Média), 3 (Crítica)
    gravidade_label: str
    causa_indisponibilidade: bool
    total_occurrences: int
    first_seen_line: int
    first_seen_time: Optional[str] = None
    lines: List[int] = Field(default_factory=list)
    sample_raw: str
    sample_stacktrace: Optional[str] = None
    technical_summary: str
    recommendation: Optional[str] = None
    laya_raw_output: Optional[Dict[str, Any]] = None

class LogStats(BaseModel):
    total_lines: int
    total_errors: int
    unique_errors: int
    critical_errors: int
    medium_errors: int
    low_errors: int
    unavailability_rate: float
    most_affected_department: str
    department_counts: Dict[str, int]
    severity_counts: Dict[str, int]
    failure_type_counts: Dict[str, int]

class GravityProfile(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = ""
    system_context: Optional[str] = ""
    criteria_baixa: str
    criteria_media: str
    criteria_critica: str
    is_builtin: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class ProfileSnapshot(BaseModel):
    profile_id: str
    profile_name: str
    system_context: Optional[str] = ""
    criteria_baixa: str
    criteria_media: str
    criteria_critica: str

class AnalysisRecord(BaseModel):
    id: str
    filename: str
    created_at: str
    total_lines: int
    stats: LogStats
    incidents: List[ErrorIncident]
    raw_log_sample: Optional[str] = None
    profile_id: Optional[str] = None
    profile_snapshot: Optional[ProfileSnapshot] = None
