import json
import sys
from pathlib import Path

# Ensure root directory is in sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from scripts.inspect_audit import (
    load_audit_records,
    find_record,
    format_output,
    main
)


@pytest.fixture
def sample_audit_file(tmp_path):
    audit_file = tmp_path / "test_audit.jsonl"
    records = [
        {
            "timestamp": "2026-09-29T10:00:00Z",
            "incident_signature": "sig_postgres_timeout",
            "profile_id": "default",
            "profile_name": "Padrão",
            "status": "success",
            "duration_ms": 120.5,
            "payload_sent": {
                "state": {"error_message": "PostgreSQL connection timed out"},
                "questions": {"gravidade": {"type": "choice"}}
            },
            "prediction_received": {
                "setor": "Infraestrutura / Banco de Dados",
                "tipo_falha": "Database Error",
                "gravidade": {"choice": "Crítica"},
                "causa_indisponibilidade": {"probability": 0.85}
            }
        },
        {
            "timestamp": "2026-09-29T10:05:00Z",
            "incident_signature": "sig_null_pointer",
            "profile_id": "ecommerce",
            "profile_name": "E-Commerce",
            "status": "success",
            "duration_ms": 85.2,
            "payload_sent": {
                "state": {"error_message": "NullPointerException on user cart"},
                "questions": {"gravidade": {"type": "choice"}}
            },
            "prediction_received": {
                "setor": "Negócio / Regras da Aplicação",
                "tipo_falha": "Null Pointer / Type Error",
                "gravidade": {"choice": "Média"},
                "causa_indisponibilidade": {"probability": 0.15}
            }
        }
    ]
    with open(audit_file, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    return audit_file


def test_load_audit_records(sample_audit_file):
    records = load_audit_records(sample_audit_file)
    assert len(records) == 2
    assert records[0]["incident_signature"] == "sig_postgres_timeout"
    assert records[1]["incident_signature"] == "sig_null_pointer"


def test_find_record_by_signature(sample_audit_file):
    records = load_audit_records(sample_audit_file)
    r = find_record(records, "sig_null_pointer")
    assert r is not None
    assert r["profile_name"] == "E-Commerce"


def test_find_record_by_index(sample_audit_file):
    records = load_audit_records(sample_audit_file)
    r = find_record(records, "1")
    assert r is not None
    assert r["incident_signature"] == "sig_postgres_timeout"


def test_find_record_by_partial_text(sample_audit_file):
    records = load_audit_records(sample_audit_file)
    r = find_record(records, "postgres")
    assert r is not None
    assert r["incident_signature"] == "sig_postgres_timeout"


def test_format_output_prediction_raw(sample_audit_file):
    records = load_audit_records(sample_audit_file)
    out = format_output(records[0], show_full=False)
    data = json.loads(out)
    assert data["setor"] == "Infraestrutura / Banco de Dados"
    assert data["gravidade"]["choice"] == "Crítica"


def test_format_output_full(sample_audit_file):
    records = load_audit_records(sample_audit_file)
    out = format_output(records[0], show_full=True)
    data = json.loads(out)
    assert "payload_sent" in data
    assert "prediction_received" in data
    assert data["duration_ms"] == 120.5


def test_main_cli_last(sample_audit_file, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["inspect_audit.py", "-p", str(sample_audit_file), "--last"])
    ret = main()
    assert ret == 0
    captured = capsys.readouterr()
    assert "sig_null_pointer" in captured.out
    assert "Null Pointer / Type Error" in captured.out


def test_main_cli_signature_query(sample_audit_file, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["inspect_audit.py", "-p", str(sample_audit_file), "sig_postgres_timeout"])
    ret = main()
    assert ret == 0
    captured = capsys.readouterr()
    assert "sig_postgres_timeout" in captured.out
    assert "Infraestrutura / Banco de Dados" in captured.out


def test_main_cli_list(sample_audit_file, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["inspect_audit.py", "-p", str(sample_audit_file), "--list"])
    ret = main()
    assert ret == 0
    captured = capsys.readouterr()
    assert "Últimos 2 registros de auditoria" in captured.out
    assert "sig_postgres_timeout" in captured.out
