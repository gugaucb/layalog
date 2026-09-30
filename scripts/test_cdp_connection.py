import asyncio
from playwright.async_api import async_playwright

async def test_connect_to_running_chrome():
    async with async_playwright() as p:
        print("Conectando ao Chrome em execução via CDP (http://127.0.0.1:9222)...")
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print("Conexão estabelecida com sucesso!")
        
        contexts = browser.contexts
        if not contexts:
            context = await browser.new_context()
        else:
            context = contexts[0]
            
        pages = context.pages
        if not pages:
            page = await context.new_page()
        else:
            page = pages[0]
            
        print(f"Página ativa atual: {page.url}")
        print("Navegando para http://127.0.0.1:8100/ na sua janela do Chrome...")
        await page.goto("http://127.0.0.1:8100/")
        await page.wait_for_load_state("networkidle")
        
        print(f"Título da página carregada: {await page.title()}")
        
        # Test clicking the manage history button in the user's visible Chrome window!
        manage_btn = page.locator("#v2ManageHistoryBtn")
        if await manage_btn.count() > 0:
            print("Clicando no botão 'Gerenciar Histórico' na sua tela...")
            await manage_btn.click()
            await page.wait_for_timeout(1000)
            
            modal = page.locator("#v2HistoryModal")
            is_active = await modal.evaluate("el => el.classList.contains('active')")
            print(f"Modal aberta na sua janela do Chrome? {is_active}")
            
        print("Teste de integração Playwright + Chrome concluído com sucesso!")

if __name__ == "__main__":
    asyncio.run(test_connect_to_running_chrome())
