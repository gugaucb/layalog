import pytest
from layalog.models import AnalysisRecord, LogStats, ErrorIncident
from layalog.exporter import MarkdownExporter

def test_markdown_export():
    stats = LogStats(
        total_lines=500,
        total_errors=10,
        unique_errors=2,
        critical_errors=4,
        medium_errors=6,
        low_errors=0,
        unavailability_rate=40.0,
        most_affected_department="Negócio / Regras da Aplicação",
        department_counts={"Negócio / Regras da Aplicação": 6, "Autenticação": 4},
        severity_counts={"Crítica": 4, "Média": 6, "Baixa": 0},
        failure_type_counts={"Null Pointer / Type Error": 10}
    )

    incident = ErrorIncident(
        id="sig123",
        signature="sig123",
        title="NullPointerException in UserHandler",
        setor="Negócio / Regras da Aplicação",
        tipo_falha="Null Pointer / Type Error",
        gravidade=3,
        gravidade_label="Crítica",
        causa_indisponibilidade=True,
        total_occurrences=4,
        first_seen_line=12,
        first_seen_time="2026-09-25 10:00:00",
        lines=[12, 55, 90, 110],
        sample_raw="[2026-09-25 10:00:00] ERROR: NullPointerException",
        sample_stacktrace="#0 /app/UserHandler.php",
        technical_summary="Falha crítica no UserHandler",
        recommendation="Adicionar verificação de nulo"
    )

    record = AnalysisRecord(
        id="test-id",
        filename="app.log",
        created_at="2026-09-28 14:00:00",
        total_lines=500,
        stats=stats,
        incidents=[incident]
    )

    md = MarkdownExporter.export(record)
    assert "# Relatório de Análise de Log - LayaLog" in md
    assert "**Arquivo Analisado:** `app.log`" in md
    assert "[CRÍTICA] #1 - NullPointerException in UserHandler" in md
    assert "40.0%" in md
