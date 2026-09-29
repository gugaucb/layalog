import json
import os
from pathlib import Path
from unittest.mock import MagicMock
import pytest

from layalog.audit import LayaAuditLogger
from layalog.classifier import LayaClassifier
from layalog.profiles import GravityProfile


def test_audit_logger_writes_jsonl(tmp_path):
    audit_file = tmp_path / "test_audit.jsonl"
    logger = LayaAuditLogger(log_path=audit_file)

    logger.log_interaction(
        incident_signature="sig_abc123",
        profile_id="prof_custom",
        profile_name="Perfil Personalizado",
        state={"error_message": "Timeout ao conectar no Postgres", "occurrences": 3},
        questions={"gravidade": {"type": "choice", "criteria": {"Baixa": "leve", "Média": "média", "Crítica": "crítica"}}},
        prediction={"gravidade": {"choice": "Crítica"}},
        duration_ms=45.2,
        status="success"
    )

    assert audit_file.exists()
    lines = audit_file.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1

    data = json.loads(lines[0])
    assert data["incident_signature"] == "sig_abc123"
    assert data["profile_id"] == "prof_custom"
    assert data["profile_name"] == "Perfil Personalizado"
    assert data["status"] == "success"
    assert data["duration_ms"] == 45.2
    assert "payload_sent" in data
    assert data["payload_sent"]["state"]["error_message"] == "Timeout ao conectar no Postgres"
    assert data["payload_sent"]["questions"]["gravidade"]["type"] == "choice"
    assert data["prediction_received"]["gravidade"]["choice"] == "Crítica"
    assert "timestamp" in data


def test_audit_logger_handles_write_error_gracefully(monkeypatch):
    logger = LayaAuditLogger(log_path=Path("/non_existent_impossible_directory_12345/audit.jsonl"))
    # Should not raise exception
    logger.log_interaction(
        incident_signature="sig_test",
        profile_id="default",
        profile_name="Padrão",
        state={},
        questions={}
    )


def test_classifier_integrates_audit_logger(tmp_path, monkeypatch):
    audit_file = tmp_path / "classifier_audit.jsonl"
    audit_logger = LayaAuditLogger(log_path=audit_file)

    mock_router_cls = MagicMock()
    mock_router_instance = MagicMock()
    mock_router_cls.return_value = mock_router_instance
    mock_router_instance.predict.return_value = {
        "setor": "Infraestrutura / Banco de Dados",
        "tipo_falha": "Database Error",
        "gravidade": {"choice": "Crítica"},
        "causa_indisponibilidade": {"probability": 0.8}
    }

    mock_laya_module = MagicMock()
    mock_laya_module.Router = mock_router_cls
    monkeypatch.setitem(__import__("sys").modules, "laya", mock_laya_module)

    classifier = LayaClassifier(preload=False, audit_logger=audit_logger)
    classifier.router = mock_router_instance

    profile = GravityProfile(
        id="ecommerce",
        name="E-Commerce Stack",
        system_context="Loja virtual com pagamentos online",
        criteria_baixa="Logs informativos",
        criteria_media="Erros pontuais",
        criteria_critica="Falha de gateway"
    )

    raw_incident = {
        "signature": "sig_db_error",
        "message": "Connection refused to database on port 5432",
        "level": "ERROR",
        "occurrences": 10,
        "first_seen_line": 1,
        "sample_raw": "2026-09-29 ERROR Connection refused",
        "sample_stacktrace": "at pg.connect"
    }

    incident = classifier.classify_incident(raw_incident, profile=profile)
    assert incident.gravidade == 3
    assert incident.gravidade_label == "Crítica"

    # Verify audit file was populated
    assert audit_file.exists()
    lines = audit_file.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1

    entry = json.loads(lines[0])
    assert entry["incident_signature"] == "sig_db_error"
    assert entry["profile_id"] == "ecommerce"
    assert entry["profile_name"] == "E-Commerce Stack"
    assert entry["status"] == "success"
    assert entry["payload_sent"]["state"]["system_context"] == "Loja virtual com pagamentos online"
    assert "gravidade" in entry["payload_sent"]["questions"]
    assert entry["payload_sent"]["questions"]["gravidade"]["criteria"]["Crítica"] == "Falha de gateway"
    assert entry["prediction_received"]["gravidade"]["choice"] == "Crítica"
