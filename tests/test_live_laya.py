import pytest
from layalog.parser import LogParser
from layalog.classifier import LayaClassifier
from pathlib import Path

def test_laya_live_classification_on_log1():
    log_path = Path("log/log1.txt")
    if not log_path.exists():
        pytest.skip("log1.txt não encontrado")

    # Read first 100 lines for fast integration test
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        sample_lines = "".join([f.readline() for _ in range(200)])

    parser = LogParser()
    blocks, total_lines = parser.parse_text(sample_lines)
    grouped = parser.group_incidents(blocks)
    
    assert len(grouped) >= 1

    classifier = LayaClassifier(preload=True)
    first_group = list(grouped.values())[0]
    incident = classifier.classify_incident(first_group)

    assert incident.setor in [
        "Infraestrutura / Banco de Dados",
        "Autenticação / Segurança",
        "Negócio / Regras da Aplicação",
        "Integrações Externas / E-mail / APIs"
    ]
    assert incident.gravidade in [1, 2, 3]
    assert isinstance(incident.causa_indisponibilidade, bool)
    assert incident.total_occurrences >= 1
