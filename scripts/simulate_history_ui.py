import asyncio
import os
from playwright.async_api import async_playwright

async def run_e2e_simulation():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        logs = []
        page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: logs.append(f"[PAGE ERROR] {err}"))

        print("1. Navegando para a aplicação em http://localhost:8100/...")
        await page.goto("http://localhost:8100/")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(500)

        # 2. Localizar e inspecionar o botão Gerenciar Histórico
        manage_btn = page.locator("#v2ManageHistoryBtn")
        assert await manage_btn.count() == 1, "Botão #v2ManageHistoryBtn não encontrado no DOM!"
        print("2. Botão #v2ManageHistoryBtn encontrado no cabeçalho.")

        # 3. Clicar no botão para abrir a modal
        print("3. Clicando no botão #v2ManageHistoryBtn...")
        await manage_btn.click()
        await page.wait_for_timeout(400)

        modal = page.locator("#v2HistoryModal")
        is_active = await modal.evaluate("el => el.classList.contains('active')")
        is_visible = await modal.is_visible()
        print(f"   Status da modal: active={is_active}, visible={is_visible}")
        assert is_active and is_visible, "A modal de histórico não abriu ou não está visível!"

        # 4. Capturar screenshot com a modal aberta
        os.makedirs("uploads", exist_ok=True)
        screenshot_path = "uploads/modal_historico_aberta.png"
        await page.screenshot(path=screenshot_path)
        print(f"4. Screenshot salvo com sucesso em: {screenshot_path}")

        # 5. Inspecionar itens renderizados na lista
        items = page.locator(".history-card-item")
        items_count = await items.count()
        print(f"5. Total de análises listadas na modal: {items_count}")

        # 6. Testar fechar a modal pelo botão '✕'
        close_btn = page.locator("#v2CloseHistoryModalBtn")
        await close_btn.click()
        await page.wait_for_timeout(300)
        is_active_closed = await modal.evaluate("el => el.classList.contains('active')")
        print(f"6. Modal fechada com sucesso: active={is_active_closed}")
        assert not is_active_closed, "A modal não fechou após clicar em fechar!"

        # 7. Testar reabertura e fechamento pelo botão 'Fechar' no rodapé
        await manage_btn.click()
        await page.wait_for_timeout(300)
        footer_close_btn = page.locator("#v2CloseHistoryFooterBtn")
        await footer_close_btn.click()
        await page.wait_for_timeout(300)
        is_active_footer_closed = await modal.evaluate("el => el.classList.contains('active')")
        print(f"7. Modal fechada pelo rodapé com sucesso: active={is_active_footer_closed}")
        assert not is_active_footer_closed

        # 8. Testar reabertura e fechamento por tecla Escape
        await manage_btn.click()
        await page.wait_for_timeout(300)
        assert await modal.evaluate("el => el.classList.contains('active')")
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)
        is_active_escape = await modal.evaluate("el => el.classList.contains('active')")
        print(f"8. Modal fechada com tecla Escape: active={is_active_escape}")
        assert not is_active_escape

        # 9. Testar reabertura e fechamento por clique no Backdrop
        await manage_btn.click()
        await page.wait_for_timeout(300)
        assert await modal.evaluate("el => el.classList.contains('active')")
        # Click on backdrop outside modal window
        await modal.click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(300)
        is_active_backdrop = await modal.evaluate("el => el.classList.contains('active')")
        print(f"9. Modal fechada por clique no backdrop: active={is_active_backdrop}")
        assert not is_active_backdrop

        print("\n=== Console Logs Capturados ===")
        for log in logs:
            print("  ", log)

        await browser.close()
        print("\n✅ Simulação Playwright E2E concluída com 100% de sucesso!")

if __name__ == "__main__":
    asyncio.run(run_e2e_simulation())
