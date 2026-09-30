import re
from pathlib import Path
from playwright.sync_api import Page, expect
from tests.e2e.helpers import LayaLogPage


def test_history_modal_listing_and_reload(page: Page, server: str):
    """Testa a abertura do modal de histórico, visualização de metadados e recarregamento de análise."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    # Upload inicial para gerar histórico
    log_file = Path("log/log.txt").resolve()
    app_page.upload_log(str(log_file), wait_completed=True)

    # Abrir modal de histórico
    app_page.open_history_modal()

    # Verificar presença dos cards de histórico
    cards = page.locator(".history-card-item")
    expect(cards.first).to_be_visible(timeout=5000)
    expect(page.locator(".history-card-filename").first).to_contain_text("log.txt")
    expect(cards.first.locator(".history-card-metrics")).to_be_visible()

    # Clicar em Abrir para recarregar
    cards.first.locator(".btn-load-history").click()
    expect(page.locator("#v2HistoryModal")).not_to_have_class("active")

    # Verificar dashboard ativo após reload
    kpis = app_page.get_kpis()
    assert int(kpis["lines"]) > 0

def test_delete_analysis_from_history_modal(page: Page, server: str):
    """Testa a exclusão de uma análise através do modal de histórico com confirmação."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    log_file = Path("log/log.txt").resolve()
    app_page.upload_log(str(log_file), wait_completed=True)

    app_page.open_history_modal()
    cards = page.locator(".history-card-item")
    expect(cards.first).to_be_visible()

    initial_count = cards.count()

    # Clicar no botão de lixeira do primeiro item
    cards.first.locator(".btn-delete-history").click()

    # Modal de confirmação deve aparecer
    confirm_modal = page.locator("#v2ConfirmModal")
    expect(confirm_modal).to_be_visible()
    expect(confirm_modal).to_have_class(re.compile(r"active"))

    # Confirmar exclusão definitiva
    page.locator("#v2ConfirmAcceptBtn").click()

    # Modal de confirmação deve fechar
    expect(confirm_modal).not_to_have_class(re.compile(r"active"))
    page.wait_for_timeout(600)

    # Contagem de cards deve ter reduzido
    remaining_cards = page.locator(".history-card-item")
    assert remaining_cards.count() < initial_count or page.locator(".history-empty-state").is_visible()

    app_page.close_history_modal()

def test_delete_current_active_analysis(page: Page, server: str):
    """Testa a exclusão da análise atualmente ativa através do botão do topo."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    log_file = Path("log/log.txt").resolve()
    app_page.upload_log(str(log_file), wait_completed=True)

    del_active_btn = page.locator("#v2DeleteCurrentAnalysisBtn")
    expect(del_active_btn).to_be_visible()

    # Clicar no botão de exclusão da análise ativa
    del_active_btn.click()

    # Confirmar no modal
    confirm_modal = page.locator("#v2ConfirmModal")
    expect(confirm_modal).to_have_class(re.compile(r"active"))
    page.locator("#v2ConfirmAcceptBtn").click()
    expect(confirm_modal).not_to_have_class(re.compile(r"active"))
    page.wait_for_timeout(500)

    # Verificar que o estado foi limpo
    kpis = app_page.get_kpis()
    assert kpis["lines"] == "-"
    expect(page.locator("#v2ContextFilename")).to_contain_text("Nenhum")

