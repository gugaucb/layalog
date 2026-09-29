import pytest
from unittest.mock import MagicMock
from layalog.classifier import LayaClassifier
from layalog.profiles import GravityProfile

@pytest.fixture
def mock_classifier(monkeypatch):
    # Mock laya.Router to avoid loading heavy models during fast unit tests
    mock_router_cls = MagicMock()
    mock_router_instance = MagicMock()
    mock_router_cls.return_value = mock_router_instance
    
    mock_laya_module = MagicMock()
    mock_laya_module.Router = mock_router_cls
    
    monkeypatch.setitem(__import__("sys").modules, "laya", mock_laya_module)
    
    classifier = LayaClassifier(preload=False)
    classifier.router = mock_router_instance
    return classifier

def test_build_questions_gravidade_is_choice(mock_classifier):
    profile = GravityProfile(
        id="test-prof",
        name="Test Profile",
        system_context="E-commerce",
        criteria_baixa="Avisos leves",
        criteria_media="Erros intermitentes",
        criteria_critica="Queda no checkout"
    )
    questions = mock_classifier.build_questions(profile)
    
    assert "gravidade" in questions
    assert questions["gravidade"]["type"] == "choice"
    assert isinstance(questions["gravidade"]["criteria"], dict)
    assert questions["gravidade"]["criteria"]["LOW"] == "Avisos leves"
    assert questions["gravidade"]["criteria"]["MEDIUM"] == "Erros intermitentes"
    assert questions["gravidade"]["criteria"]["CRITICAL"] == "Queda no checkout"

@pytest.mark.parametrize("pred_gravidade,expected_val,expected_label", [
    ({"choice": "CRITICAL"}, 3, "Crítica"),
    ({"choice": "MEDIUM"}, 2, "Média"),
    ({"choice": "LOW"}, 1, "Baixa"),
    ({"choice": "Crítica"}, 3, "Crítica"),
    ({"choice": "critica"}, 3, "Crítica"),
    ({"value": "Baixa"}, 1, "Baixa"),
    ({"label": "Média"}, 2, "Média"),
    ("CRITICAL", 3, "Crítica"),
    ("MEDIUM", 2, "Média"),
    ("LOW", 1, "Baixa"),
    ("Crítica", 3, "Crítica"),
    ("baixa", 1, "Baixa"),
    ("Média", 2, "Média"),
    (1, 1, "Baixa"),
    (2, 2, "Média"),
    (3, 3, "Crítica"),
])
def test_classify_incident_gravidade_choice_parsing(mock_classifier, pred_gravidade, expected_val, expected_label):
    raw_incident = {
        "signature": "sig_123",
        "message": "NullPointerException at line 42",
        "level": "ERROR",
        "occurrences": 5,
        "first_seen_line": 10,
        "sample_raw": "2026-09-29 ERROR NullPointerException",
        "sample_stacktrace": "at com.example.App.main"
    }

    mock_classifier.router.predict.return_value = {
        "setor": {"choice": "Negócio / Regras da Aplicação"},
        "tipo_falha": {"choice": "Null Pointer / Type Error"},
        "gravidade": pred_gravidade,
        "causa_indisponibilidade": {"probability": 0.9}
    }

    incident = mock_classifier.classify_incident(raw_incident)

    assert incident.gravidade == expected_val
    assert incident.gravidade_label == expected_label
    assert incident.causa_indisponibilidade is True
    assert incident.tipo_falha == "Null Pointer / Type Error"
    assert incident.setor == "Negócio / Regras da Aplicação"
