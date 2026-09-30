import pytest
from playwright.sync_api import Page, expect
from tests.e2e.helpers import LayaLogPage

def test_initial_page_load(page: Page, server: str):
    """Smoke test: Verifica se o LayaLog carrega e renderiza o layout principal V2."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    # Verificar título da página
    assert "LayaLog" in page.title()

    # Elementos principais visíveis
    expect(page.locator(".brand-name")).to_have_text("LayaLog")
    expect(page.locator("#v2ProfileSelect")).to_be_visible()
    expect(page.locator("#v2UploadBtn")).to_be_visible()
    expect(page.locator("#v2SearchInput")).to_be_visible()
    expect(page.locator(".kpi-grid")).to_be_visible()

    # Estado inicial dos KPIs
    kpis = app_page.get_kpis()
    assert kpis["lines"] == "-"
    assert kpis["errors"] == "-"

    # Presença de opções no dropdown de perfis (presets carregados)
    options = page.locator("#v2ProfileSelect option")
    assert options.count() >= 3
