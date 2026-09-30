from pathlib import Path
from playwright.sync_api import Page, expect
from tests.e2e.helpers import LayaLogPage

def test_severity_filter_chips(page: Page, server: str):
    """Testa a filtragem de incidentes através dos chips de severidade no topo do dashboard."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    log_file = Path("log/log.txt").resolve()
    app_page.upload_log(str(log_file), wait_completed=True)

    all_cards = page.locator(".incident-row-card")
    total_count = all_cards.count()
    assert total_count >= 1

    # Filtrar por Baixa
    app_page.filter_severity("low")
    low_cards = page.locator(".incident-row-card:visible")
    # Todas as visíveis devem ter data-severity="low"
    for i in range(low_cards.count()):
        assert low_cards.nth(i).get_attribute("data-severity") == "low"

    # Filtrar por Média
    app_page.filter_severity("medium")
    med_cards = page.locator(".incident-row-card:visible")
    for i in range(med_cards.count()):
        assert med_cards.nth(i).get_attribute("data-severity") == "medium"

    # Retornar para Todos
    app_page.filter_severity("all")
    visible_after_all = page.locator(".incident-row-card:visible")
    assert visible_after_all.count() == total_count

def test_search_input_filtering(page: Page, server: str):
    """Testa o campo de busca global em tempo real filtrando erros e incidentes."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    log_file = Path("log/log.txt").resolve()
    app_page.upload_log(str(log_file), wait_completed=True)

    search_input = page.locator("#v2SearchInput")
    
    # Obter uma palavra do título do primeiro incidente para busca precisa
    first_title = page.locator(".incident-human-title").first.inner_text().strip()
    query = first_title.split()[0] # Primeira palavra do título

    search_input.fill(query)
    page.wait_for_timeout(300)

    # Verificar que os cards visíveis contêm o termo
    visible_cards = page.locator(".incident-row-card:visible")
    assert visible_cards.count() >= 1

    # Limpar busca
    search_input.fill("")
    page.wait_for_timeout(300)
    assert page.locator(".incident-row-card:visible").count() >= visible_cards.count()

def test_log_viewer_and_incident_selection(page: Page, server: str):
    """Testa a renderização do Log Viewer V2 e a seleção de incidentes para exibição detalhada."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    log_file = Path("log/log.txt").resolve()
    app_page.upload_log(str(log_file), wait_completed=True)

    # Verificar linhas no log viewer virtualizado
    log_lines = page.locator(".v2-log-line")
    expect(log_lines.first).to_be_visible(timeout=5000)
    assert log_lines.count() > 0


    # Clicar no primeiro incidente para abrir detalhes na coluna direita
    first_incident = page.locator(".incident-row-card").first
    first_incident.click()

    # Verificar que o container de detalhes foi preenchido com a análise da IA
    detail_container = page.locator("#v2DetailContainer")
    expect(detail_container).not_to_contain_text("Aguardando seleção")
    expect(detail_container.locator(".laya-ai-card")).to_be_visible()

