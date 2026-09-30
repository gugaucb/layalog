import pytest
import json
from fastapi.testclient import TestClient
from layalog.app import app
from layalog.database import init_db
from pathlib import Path

SAMPLE_LOG_DATA = """[2026-09-25 00:01:13] production.ERROR: Erro no envio de e-mail: Trying to get property 'seccional_id' of non-object
[2026-09-25 00:04:06] production.ERROR: Erro no envio de e-mail: Trying to get property 'seccional_id' of non-object
[2026-09-25 09:26:32] production.ERROR: The Response content must be a string or object implementing __toString()
[stacktrace]
#0 /var/www/html/sistema/vendor/Response.php(45): setContent()
"""

@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test_api.db"
    init_db(test_db)
    monkeypatch.setattr("layalog.app.get_analysis", lambda aid, include_raw=False: None if aid == "invalid" else {
        "id": aid,
        "filename": "test.log",
        "created_at": "2026-09-28 14:00:00",
        "total_lines": 10,
        "stats": {
            "total_lines": 10,
            "total_errors": 2,
            "unique_errors": 1,
            "critical_errors": 1,
            "medium_errors": 1,
            "low_errors": 0,
            "unavailability_rate": 50.0,
            "most_affected_department": "Negócio",
            "department_counts": {"Negócio": 2},
            "severity_counts": {"Crítica": 1, "Média": 1, "Baixa": 0},
            "failure_type_counts": {"Null Pointer / Type Error": 2}
        },
        "incidents": [{
            "id": "inc-1",
            "signature": "sig-1",
            "title": "Error title",
            "setor": "Negócio",
            "tipo_falha": "Null Pointer / Type Error",
            "gravidade": 3,
            "gravidade_label": "Crítica",
            "causa_indisponibilidade": True,
            "total_occurrences": 2,
            "first_seen_line": 1,
            "first_seen_time": "2026-09-25 00:00:00",
            "lines": [1, 2],
            "sample_raw": "log sample",
            "technical_summary": "Summary",
            "recommendation": "Fix it"
        }],
        "raw_log_text": "Sample raw text"
    })
    return TestClient(app)

def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"

def test_root_and_v2_endpoints(client):
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert "LayaLog" in res_root.text

    res_v2 = client.get("/v2", follow_redirects=True)
    assert res_v2.status_code == 200
    assert "LayaLog" in res_v2.text

def test_export_md_endpoint(client):
    res = client.get("/api/analyses/test-123/export-md")
    assert res.status_code == 200
    assert "text/markdown" in res.headers["content-type"]
    assert "# Relatório de Análise de Log - LayaLog" in res.text

def test_lines_chunk_endpoint(client, monkeypatch):
    monkeypatch.setattr("layalog.app.get_analysis_lines", lambda aid, start_line, limit: {
        "analysis_id": aid,
        "start_line": start_line,
        "limit": limit,
        "total_lines": 100,
        "lines": [f"Line {i}" for i in range(start_line, start_line + limit)]
    } if aid != "invalid" else None)

    res = client.get("/api/analyses/test-123/lines?start_line=1&limit=5")
    assert res.status_code == 200
    data = res.json()
    assert data["start_line"] == 1
    assert data["limit"] == 5
    assert len(data["lines"]) == 5
    assert data["lines"][0] == "Line 1"

    res_404 = client.get("/api/analyses/invalid/lines?start_line=1&limit=5")
    assert res_404.status_code == 404

def test_analyze_stream_endpoint(client, monkeypatch):
    class DummyClassifier:
        def classify_incident(self, raw_incident):
            from layalog.models import ErrorIncident
            return ErrorIncident(
                id=raw_incident["signature"],
                signature=raw_incident["signature"],
                title="Mock error",
                setor="Negócio",
                tipo_falha="Null Pointer / Type Error",
                gravidade=2,
                gravidade_label="Média",
                causa_indisponibilidade=False,
                total_occurrences=raw_incident["occurrences"],
                first_seen_line=raw_incident["first_seen_line"],
                first_seen_time="2026-09-25 00:00:00",
                lines=raw_incident["lines"],
                sample_raw=raw_incident["sample_raw"],
                technical_summary="Resumo",
                recommendation="Recomendação"
            )

    monkeypatch.setattr("layalog.app.get_classifier", lambda: DummyClassifier())

    test_content = b"[2026-09-25 00:01:13] production.ERROR: Sample error line 1\n[2026-09-25 00:02:13] production.ERROR: Sample error line 2\n"
    res = client.post("/api/analyze-stream", files={"file": ("test.log", test_content, "text/plain")})
    assert res.status_code == 200
    
    events = [json.loads(line) for line in res.text.strip().split("\n") if line.strip()]
    assert len(events) >= 3
    assert events[0]["type"] == "progress"
    assert any(e["type"] == "progress" and e["percent"] == 100 for e in events)
    assert events[-1]["type"] == "complete"
    assert events[-1]["data"]["stats"]["total_errors"] == 2

def test_delete_analysis_endpoint(client, monkeypatch):
    monkeypatch.setattr("layalog.app.delete_analysis", lambda aid: True if aid == "existing-123" else False)

    res_ok = client.delete("/api/analyses/existing-123")
    assert res_ok.status_code == 200
    assert res_ok.json() == {"status": "deleted", "id": "existing-123"}

    res_404 = client.delete("/api/analyses/not-found-999")
    assert res_404.status_code == 404
    assert "não encontrada" in res_404.json()["detail"]

