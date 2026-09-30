import pytest
from pathlib import Path
from layalog.models import AnalysisRecord, LogStats, ErrorIncident
from layalog.database import init_db, save_analysis, list_analyses, get_analysis, get_analysis_lines, delete_analysis

def test_database_crud(tmp_path):
    db_file = tmp_path / "test_layalog.db"
    init_db(db_file)

    stats = LogStats(
        total_lines=100,
        total_errors=5,
        unique_errors=1,
        critical_errors=5,
        medium_errors=0,
        low_errors=0,
        unavailability_rate=100.0,
        most_affected_department="Infraestrutura",
        department_counts={"Infraestrutura": 5},
        severity_counts={"Crítica": 5, "Média": 0, "Baixa": 0},
        failure_type_counts={"Database Error": 5}
    )

    inc = ErrorIncident(
        id="db_err",
        signature="db_err",
        title="Connection Refused to Postgres",
        setor="Infraestrutura",
        tipo_falha="Database Error",
        gravidade=3,
        gravidade_label="Crítica",
        causa_indisponibilidade=True,
        total_occurrences=5,
        first_seen_line=1,
        lines=[1, 2, 3, 4, 5],
        sample_raw="[2026-09-25 00:00:00] ERROR: Connection refused",
        technical_summary="Falha no PostgreSQL"
    )

    record = AnalysisRecord(
        id="rec-1",
        filename="db.log",
        created_at="2026-09-28 12:00:00",
        total_lines=100,
        stats=stats,
        incidents=[inc]
    )

    multiline_text = "\n".join([f"Line {i}: Log event info" for i in range(1, 101)])
    save_analysis(record, raw_text=multiline_text, db_path=db_file)

    # List
    history = list_analyses(db_path=db_file)
    assert len(history) == 1
    assert history[0]["id"] == "rec-1"
    assert history[0]["filename"] == "db.log"

    # Detail (without raw text by default)
    detail = get_analysis("rec-1", include_raw=False, db_path=db_file)
    assert detail is not None
    assert detail["raw_log_text"] is None
    assert len(detail["incidents"]) == 1

    # Chunked lines
    chunk = get_analysis_lines("rec-1", start_line=10, limit=5, db_path=db_file)
    assert chunk is not None
    assert chunk["start_line"] == 10
    assert chunk["limit"] == 5
    assert len(chunk["lines"]) == 5
    assert chunk["lines"][0] == "Line 10: Log event info"
    assert chunk["lines"][4] == "Line 14: Log event info"

    # Delete
    deleted = delete_analysis("rec-1", db_path=db_file)
    assert deleted is True
    assert get_analysis("rec-1", db_path=db_file) is None
    assert delete_analysis("rec-1", db_path=db_file) is False

def test_delete_analysis_removes_physical_file(tmp_path):
    db_file = tmp_path / "test_layalog_delete.db"
    init_db(db_file)

    log_file = tmp_path / "upload_sample.log"
    log_file.write_text("sample log line 1\nsample log line 2\n")

    stats = LogStats(
        total_lines=2,
        total_errors=0,
        unique_errors=0,
        critical_errors=0,
        medium_errors=0,
        low_errors=0,
        unavailability_rate=0.0,
        most_affected_department="Nenhum",
        department_counts={},
        severity_counts={"Crítica": 0, "Média": 0, "Baixa": 0},
        failure_type_counts={}
    )

    record = AnalysisRecord(
        id="rec-to-delete",
        filename="upload_sample.log",
        created_at="2026-09-28 12:00:00",
        total_lines=2,
        stats=stats,
        incidents=[]
    )

    save_analysis(record, raw_text="sample log line 1\nsample log line 2\n", file_path=str(log_file), db_path=db_file)
    assert log_file.exists()

    # Perform complete deletion
    res = delete_analysis("rec-to-delete", db_path=db_file)
    assert res is True
    assert not log_file.exists()
    assert get_analysis("rec-to-delete", db_path=db_file) is None

