from pathlib import Path
from playwright.sync_api import Page, expect
from tests.e2e.helpers import LayaLogPage

def test_incident_inspection_and_laya_ai_details(page: Page, server: str):
    """Testa a inspeção de incidentes, exibição de evidências da IA Laya, resumo e saltos de linha."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    log_file = Path("log/log.txt").resolve()
    app_page.upload_log(str(log_file), wait_completed=True)

    # Clicar no primeiro incidente
    first_incident = page.locator(".incident-row-card").first
    first_incident.click()

    # Validar presença do Laya AI Observability Engine Card
    laya_card = page.locator(".laya-ai-card")
    expect(laya_card).to_be_visible()
    expect(laya_card).to_contain_text("Laya AI Observability Engine")
    expect(page.locator(".ai-recommendation-box")).to_be_visible()

    # Validar seção de evidências e stacktrace
    stacktrace_box = page.locator("#stacktraceText")
    expect(stacktrace_box).to_be_visible()
    assert len(stacktrace_box.inner_text().strip()) > 0

    # Validar pílulas de ocorrência e clique para scroll
    pills = page.locator(".line-pill")
    if pills.count() > 0:
        pills.first.click()
        # Verificar que a linha foi destacada no log viewer
        highlighted = page.locator(".v2-log-line.highlight-line")
        expect(highlighted.first).to_be_visible(timeout=3000)

def test_markdown_export_download(page: Page, server: str):
    """Testa a exportação de relatório Markdown validando o arquivo baixado."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    log_file = Path("log/log.txt").resolve()
    app_page.upload_log(str(log_file), wait_completed=True)

    export_btn = page.locator("#v2ExportBtn")
    expect(export_btn).to_be_enabled()

    # Interceptar download do arquivo
    with page.expect_download() as download_info:
        export_btn.click()
    
    download = download_info.value
    assert download.suggested_filename.endswith(".md")
    assert "analise_" in download.suggested_filename

    # Validar conteúdo do arquivo Markdown
    download_path = download.path()
    content = Path(download_path).read_text(encoding="utf-8")
    assert "# Relatório de Análise de Logs" in content or "LayaLog" in content or "Diagnóstico" in content
    assert "log.txt" in content
