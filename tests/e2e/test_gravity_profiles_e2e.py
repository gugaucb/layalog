import pytest
from playwright.sync_api import Page, expect
from tests.e2e.helpers import LayaLogPage

def test_view_builtin_profiles_protected(page: Page, server: str):
    """Testa visualização dos perfis nativos (built-in) e proteção contra exclusão direta."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    app_page.open_profile_modal()

    # Verificar itens da lista de perfis
    items = page.locator(".profile-list-item")
    expect(items.first).to_be_visible()
    assert items.count() >= 3

    # Primeiro perfil selecionado é nativo
    expect(page.locator("#v2ProfileBuiltinBadge")).to_contain_text("Nativo")
    
    # Botão de excluir deve estar oculto para perfil nativo
    expect(page.locator("#v2DeleteProfileBtn")).to_be_hidden()

    app_page.close_profile_modal()

def test_create_and_edit_custom_profile(page: Page, server: str):
    """Testa criação e posterior edição de um perfil customizado."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    app_page.open_profile_modal()

    # Clicar em Novo
    page.locator("#v2NewProfileBtn").click()
    expect(page.locator("#v2ProfileFormTitle")).to_have_text("Novo Perfil de Gravidade")

    # Preencher dados
    custom_name = "E2E Test Stack Python Fast"
    page.fill("#v2FormProfileName", custom_name)
    page.fill("#v2FormProfileDesc", "Perfil criado via teste automatizado E2E")
    page.fill("#v2FormProfileContext", "API FastAPI com mensageria Redis")
    page.fill("#v2FormCriteriaBaixa", "Erros 404 pontuais e tokens expirados")
    page.fill("#v2FormCriteriaMedia", "Timeout transitório em fila secundária")
    page.fill("#v2FormCriteriaCritica", "Queda de conexão com PostgreSQL ou Redis indisponível")

    # Salvar Perfil
    page.locator("#v2SaveProfileBtn").click()

    # Verificar que o perfil foi salvo e aparece na lista
    custom_item = page.locator(f".profile-list-item:has-text('{custom_name}')")
    expect(custom_item).to_be_visible(timeout=5000)
    expect(custom_item.locator(".badge")).to_have_text("Custom")

    # Editar a descrição do perfil
    updated_desc = "Descrição atualizada via E2E test"
    page.fill("#v2FormProfileDesc", updated_desc)
    page.locator("#v2SaveProfileBtn").click()
    page.wait_for_timeout(500)

    # Verificar que o texto atualizado foi persistido
    expect(page.locator(f".profile-list-item:has-text('{custom_name}') .profile-item-desc")).to_have_text(updated_desc)

    app_page.close_profile_modal()

    # Verificar se o perfil aparece disponível no dropdown do topbar
    expect(page.locator(f"#v2ProfileSelect option:has-text('{custom_name}')")).to_be_attached()

def test_clone_preset_profile(page: Page, server: str):
    """Testa a duplicação/clonagem de um perfil nativo."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    app_page.open_profile_modal()

    # Selecionar primeiro perfil nativo
    page.locator(".profile-list-item").first.click()

    cloned_name = "Clone E2E Profile"
    page.on("dialog", lambda dialog: dialog.accept(cloned_name))

    # Clicar em duplicar
    page.locator("#v2CloneProfileBtn").click()
    page.wait_for_timeout(800)

    # Verificar que o perfil clonado aparece como custom
    cloned_item = page.locator(f".profile-list-item:has-text('{cloned_name}')")
    expect(cloned_item).to_be_visible(timeout=5000)
    expect(cloned_item.locator(".badge")).to_have_text("Custom")

    app_page.close_profile_modal()

def test_delete_custom_profile(page: Page, server: str):
    """Testa a exclusão de um perfil customizado da listagem."""
    app_page = LayaLogPage(page, server)
    app_page.goto_home()

    # Criar um perfil temporário para exclusão
    temp_profile_name = "Profile To Be Deleted"
    app_page.create_custom_profile(
        name=temp_profile_name,
        desc="Temporário",
        context="Contexto temp",
        baixa="Critério 1",
        media="Critério 2",
        critica="Critério 3"
    )

    app_page.open_profile_modal()

    target_item = page.locator(f".profile-list-item:has-text('{temp_profile_name}')")
    expect(target_item).to_be_visible()

    # Aceitar confirmação de exclusão
    page.on("dialog", lambda dialog: dialog.accept())

    # Clicar no botão de lixeira do item
    del_btn = target_item.locator(".profile-item-delete-btn")
    del_btn.click()
    page.wait_for_timeout(800)

    # Verificar que o item foi removido da lista
    expect(target_item).to_have_count(0)

    app_page.close_profile_modal()

    # Verificar que não está mais no dropdown do topbar
    expect(page.locator(f"#v2ProfileSelect option:has-text('{temp_profile_name}')")).to_have_count(0)
