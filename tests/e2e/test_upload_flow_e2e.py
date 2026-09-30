import os
from pathlib import Path
from playwright.sync_api import Page, expect
from tests.e2e.helpers import LayaLogPage

def test_upload_log_and_view_kpis(page: Page, server: str):
    """Testa o fluxo completo de upload de log, barra de progresso e renderização dos KPIs."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    log_file = Path("log/log.txt").resolve()
    assert log_file.exists(), "log/log.txt deve existir para o teste"

    # Realizar upload
    app_page.upload_log(str(log_file), wait_completed=True)

    # Verificar breadcrumb e contexto de arquivo
    expect(page.locator("#v2ContextFilename")).to_have_text("log.txt")
    expect(page.locator("#v2BreadcrumbFile")).to_contain_text("log.txt")

    # Verificar KPIs atualizados
    kpis = app_page.get_kpis()
    assert kpis["lines"] != "-" and int(kpis["lines"]) > 0
    assert kpis["errors"] != "-" and int(kpis["errors"]) > 0

    # Verificar que o botão de exportar MD foi habilitado
    expect(page.locator("#v2ExportBtn")).to_be_enabled()

    # Verificar cards de incidentes renderizados
    incident_cards = page.locator(".incident-row-card")
    expect(incident_cards.first).to_be_visible()
    assert incident_cards.count() >= 1


def test_cancel_upload(page: Page, server: str):
    """Testa o cancelamento de processamento via botão Cancelar do modal de progresso."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    log_file = Path("log/log.txt").resolve()
    app_page.cancel_upload(str(log_file))

    # O modal de progresso deve ter sido fechado
    expect(page.locator("#v2LoadingModal")).not_to_have_class("active")

def test_profile_selection_before_upload(page: Page, server: str):
    """Testa seleção de Gravity Profile antes do upload e verificação no fluxo."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    # Selecionar profile Keycloak
    page.select_option("#v2ProfileSelect", value="keycloak-iam")
    
    log_file = Path("log/log.txt").resolve()
    app_page.upload_log(str(log_file), wait_completed=True)

    # Verificar conclusão e KPIs
    kpis = app_page.get_kpis()
    assert int(kpis["lines"]) > 0
    expect(page.locator("#v2BreadcrumbFile")).to_contain_text("Autenticação")

