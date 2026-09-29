import pytest
from unittest.mock import MagicMock
from layalog.evidence import EvidenceExtractor, FinalClassificationResolver
from layalog.classifier import LayaClassifier
from layalog.profiles import GravityProfile


def test_evidence_extractor_detects_all_sources():
    extractor = EvidenceExtractor()

    # Evidence in error_message, raw_snippet, and stacktrace
    raw_incident = {
        "message": "Illuminate\\Database\\QueryException: ORA-02393 exceeded limit",
        "sample_raw": "HTTP 500 Internal Server Error [2026-09-29 10:00:00]",
        "sample_stacktrace": "at PDOStatement->execute() in /app/db.php:40"
    }

    result = extractor.extract(raw_incident)
    assert result["is_database_error"] is True
    assert result["is_http_failure"] is True
    assert result["is_out_of_memory"] is False
    assert result["is_jwt_expired"] is False

    evidence_list = result["classification_evidence"]
    assert any("ORA-02393" in e for e in evidence_list)
    assert any("QueryException" in e for e in evidence_list)
    assert any("500" in e for e in evidence_list)


def test_resolver_ora_and_http500_overrides_to_critical():
    resolver = FinalClassificationResolver()
    evidence = {
        "is_database_error": True,
        "is_http_failure": True,
        "is_out_of_memory": False,
        "is_jwt_expired": False,
        "classification_evidence": ["ORA-02393 detected", "HTTP 500 detected"]
    }

    # Model predicted incorrect sector/severity (e.g. Auth and Medium)
    setor, tipo_falha, gravidade, causa_indisp, ev_list = resolver.resolve(
        predicted_setor="Autenticação / Segurança",
        predicted_tipo_falha="Outros",
        predicted_gravidade=2,
        predicted_causa_indisponibilidade=False,
        evidence=evidence
    )

    assert setor == "Infraestrutura / Banco de Dados"
    assert tipo_falha == "Database Error"
    assert gravidade == 3
    assert causa_indisp is True
    assert "ORA-02393 detected" in ev_list


def test_resolver_out_of_memory_overrides_to_critical():
    resolver = FinalClassificationResolver()
    evidence = {
        "is_database_error": False,
        "is_http_failure": False,
        "is_out_of_memory": True,
        "is_jwt_expired": False,
        "classification_evidence": ["OutOfMemoryError detected"]
    }

    setor, tipo_falha, gravidade, causa_indisp, ev_list = resolver.resolve(
        predicted_setor="Negócio / Regras da Aplicação",
        predicted_tipo_falha="Outros",
        predicted_gravidade=2,
        predicted_causa_indisponibilidade=False,
        evidence=evidence
    )

    assert gravidade == 3
    assert causa_indisp is True
    assert "OutOfMemoryError detected" in ev_list


def test_resolver_jwt_expired_overrides_to_low_severity():
    resolver = FinalClassificationResolver()
    evidence = {
        "is_database_error": False,
        "is_http_failure": False,
        "is_out_of_memory": False,
        "is_jwt_expired": True,
        "classification_evidence": ["JWT expired detected"]
    }

    setor, tipo_falha, gravidade, causa_indisp, ev_list = resolver.resolve(
        predicted_setor="Autenticação / Segurança",
        predicted_tipo_falha="Permission / Auth",
        predicted_gravidade=2,
        predicted_causa_indisponibilidade=False,
        evidence=evidence
    )

    assert gravidade == 1
    assert "JWT expired detected" in ev_list


def test_classifier_e2e_ora_and_http500_single_occurrence(monkeypatch):
    mock_router_cls = MagicMock()
    mock_router_instance = MagicMock()
    mock_router_cls.return_value = mock_router_instance

    # Model incorrectly returns Autenticação and Média
    mock_router_instance.predict.return_value = {
        "setor": {"choice": "Autenticação / Segurança"},
        "tipo_falha": {"choice": "Outros"},
        "gravidade": {"choice": "Média"},
        "causa_indisponibilidade": {"probability": 0.2}
    }

    mock_laya_module = MagicMock()
    mock_laya_module.Router = mock_router_cls
    monkeypatch.setitem(__import__("sys").modules, "laya", mock_laya_module)

    classifier = LayaClassifier(preload=False, audit_logger=None)
    classifier.router = mock_router_instance

    # Incident with a single occurrence
    raw_incident = {
        "signature": "sig_ora_http500",
        "message": "Illuminate\\Database\\QueryException: ORA-02393 exceeded limit",
        "level": "ERROR",
        "occurrences": 1,
        "first_seen_line": 150,
        "first_seen_time": "2026-09-29 10:00:00",
        "sample_raw": "HTTP 500 Internal Server Error [2026-09-29 10:00:00]",
        "sample_stacktrace": "at PDOStatement->execute()"
    }

    incident = classifier.classify_incident(raw_incident)

    # Mandatory assertions
    assert incident.gravidade == 3
    assert incident.gravidade_label == "Crítica"
    assert incident.setor == "Infraestrutura / Banco de Dados"
    assert incident.tipo_falha == "Database Error"
    assert incident.causa_indisponibilidade is True
    assert incident.total_occurrences == 1
    assert len(incident.classification_evidence) >= 2
    assert any("ORA-02393" in ev for ev in incident.classification_evidence)
    assert any("500" in ev for ev in incident.classification_evidence)


def test_resolver_brute_force_protector_overrides_to_critical():
    resolver = FinalClassificationResolver()
    evidence = {
        "is_database_error": False,
        "is_http_failure": False,
        "is_out_of_memory": False,
        "is_jwt_expired": False,
        "is_brute_force": True,
        "classification_evidence": ["Brute Force Protector triggered detected", "KC-SERVICES0053 detected"]
    }

    # If Laya returns Medium severity for the security event
    setor, tipo_falha, gravidade, causa_indisp, ev_list = resolver.resolve(
        predicted_setor="Autenticação / Segurança",
        predicted_tipo_falha="Outros",
        predicted_gravidade=2,
        predicted_causa_indisponibilidade=False,
        evidence=evidence
    )

    assert setor == "Autenticação / Segurança"
    assert tipo_falha == "Permission / Auth"
    assert gravidade == 3  # Critical
    assert "Brute Force Protector triggered detected" in ev_list


def test_classifier_e2e_brute_force_protector_lockout(monkeypatch):
    mock_router_cls = MagicMock()
    mock_router_instance = MagicMock()
    mock_router_cls.return_value = mock_router_instance

    # Model returns Medium initially
    mock_router_instance.predict.return_value = {
        "setor": {"choice": "Autenticação / Segurança"},
        "tipo_falha": {"choice": "Outros"},
        "gravidade": {"choice": "MEDIUM"},
        "causa_indisponibilidade": {"probability": 0.05}
    }

    mock_laya_module = MagicMock()
    mock_laya_module.Router = mock_router_cls
    monkeypatch.setitem(__import__("sys").modules, "laya", mock_laya_module)

    classifier = LayaClassifier(preload=False, audit_logger=None)
    classifier.router = mock_router_instance

    raw_incident = {
        "signature": "sig_brute_force",
        "message": "[org.keycloak.services] (Brute Force Protector) KC-SERVICES0053: login failure for user 930e369e-4d57-43ea-9f54-7464d050905e from ip 172.16.200.67",
        "level": "WARN",
        "occurrences": 77,
        "first_seen_line": 923,
        "first_seen_time": "2026-09-28 07:18:59,383",
        "sample_raw": "2026-09-28 07:18:59,383 WARN  [org.keycloak.services] (Brute Force Protector) KC-SERVICES0053: login failure for user 930e369e-4d57-43ea-9f54-7464d050905e from ip 172.16.200.67",
        "sample_stacktrace": ""
    }

    incident = classifier.classify_incident(raw_incident)

    assert incident.gravidade == 3
    assert incident.gravidade_label == "Crítica"
    assert incident.setor == "Autenticação / Segurança"
    assert incident.tipo_falha == "Permission / Auth"
    assert any("Brute Force Protector" in ev for ev in incident.classification_evidence)

