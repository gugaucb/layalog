import pytest
from unittest.mock import MagicMock
from layalog.classifier import LayaClassifier
from layalog.profiles import get_builtin_profiles, get_default_profile


@pytest.fixture
def classifier(monkeypatch):
    mock_router_cls = MagicMock()
    mock_router_instance = MagicMock()
    mock_router_cls.return_value = mock_router_instance

    mock_laya_module = MagicMock()
    mock_laya_module.Router = mock_router_cls
    monkeypatch.setitem(__import__("sys").modules, "laya", mock_laya_module)

    c = LayaClassifier(preload=False, audit_logger=None)
    c.router = mock_router_instance
    return c


@pytest.mark.parametrize(
    "error_text,expected_gravidade,expected_label",
    [
        # 1. Expected behavior, validation failure, expired session
        ("JWT expired for user session", 1, "Baixa"),
        ("ValidationException: HTTP 422 Unprocessable Entity - email required", 1, "Baixa"),
        ("OAuth error: invalid_scope requested by client", 1, "Baixa"),

        # 2. Operational degradation with fallback or retry
        ("LDAP synchronization timeout - scheduled retry in 30s", 2, "Média"),
        ("Brute Force Protector triggered for IP 192.168.1.50", 2, "Média"),
        ("Swift_TransportException: Connection timeout sending email via SMTP", 2, "Média"),

        # 3. Critical failures: database outage, OOM, essential service interruption
        ("Illuminate\\Database\\QueryException: ORA-02393 exceeded limit HTTP 500 Internal Server Error", 3, "Crítica"),
        ("SQLSTATE[HY000]: Database connection refused on port 5432 HTTP 500", 3, "Crítica"),
        ("JWKS signing key unavailable: Unable to validate JWT signature", 3, "Crítica"),
        ("java.lang.OutOfMemoryError: Java heap space", 3, "Crítica"),
    ],
)
def test_ten_reference_criteria_scenarios(classifier, error_text, expected_gravidade, expected_label):
    raw_incident = {
        "signature": "sig_test_scenario",
        "message": error_text,
        "level": "ERROR",
        "occurrences": 1,
        "first_seen_line": 1,
        "sample_raw": error_text,
        "sample_stacktrace": "",
    }

    # Simulate model prediction based on the expected behavior
    choice_map = {1: "LOW", 2: "MEDIUM", 3: "CRITICAL"}
    classifier.router.predict.return_value = {
        "setor": {"choice": "Negócio / Regras da Aplicação"},
        "tipo_falha": {"choice": "Outros"},
        "gravidade": {"choice": choice_map[expected_gravidade]},
        "causa_indisponibilidade": {"probability": 0.9 if expected_gravidade == 3 else 0.1},
    }

    incident = classifier.classify_incident(raw_incident)

    assert incident.gravidade == expected_gravidade
    assert incident.gravidade_label == expected_label


def test_builtin_profiles_have_observable_technical_criteria():
    profiles = get_builtin_profiles()
    assert len(profiles) >= 7

    for p in profiles:
        # Verify criteria are rich with examples and non-empty
        assert len(p.criteria_baixa) > 30
        assert len(p.criteria_media) > 30
        assert len(p.criteria_critica) > 30
        assert "Examples:" in p.criteria_baixa or "Examples:" in p.criteria_media or "Examples:" in p.criteria_critica
