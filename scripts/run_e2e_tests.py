#!/usr/bin/env python3
"""
Script de execução unificada para a suíte completa de testes E2E com Playwright no LayaLog.
Uso:
    python scripts/run_e2e_tests.py
    python scripts/run_e2e_tests.py --verbose
    python scripts/run_e2e_tests.py --headed
"""

import sys
import subprocess
from pathlib import Path

def main():
    root_dir = Path(__file__).parent.parent.resolve()
    
    # Arguments forwarded to pytest
    pytest_args = [
        sys.executable,
        "-m",
        "pytest",
        "tests/e2e",
        "-v",
        "--tb=short"
    ]

    # Check if extra flags were provided
    if "--headed" in sys.argv:
        pytest_args.append("--headed")
    
    if "--report" in sys.argv or "--html" in sys.argv:
        report_path = root_dir / "e2e_report.html"
        pytest_args.extend(["--html", str(report_path), "--self-contained-html"])

    print("=" * 70)
    print("🚀 Iniciando Suíte de Testes Automatizados E2E (Playwright) - LayaLog")
    print("=" * 70)
    print(f"Comando: {' '.join(pytest_args)}")
    print("-" * 70)

    result = subprocess.run(pytest_args, cwd=str(root_dir))
    
    print("-" * 70)
    if result.returncode == 0:
        print("✅ Todos os testes E2E foram executados e APROVADOS com sucesso!")
    else:
        print(f"❌ Falha na execução da suíte E2E (código de saída: {result.returncode})")
    print("=" * 70)

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
