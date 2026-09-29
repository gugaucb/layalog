import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def capture():
    assets_dir = Path("docs/assets")
    assets_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2 # Retina 2x high-DPI quality
        )
        page = await context.new_page()

        print("Navigating to http://localhost:8100 ...")
        await page.goto("http://localhost:8100", wait_until="networkidle")
        await asyncio.sleep(1)

        # 1. Check if history exists and select an item with rich incidents
        history_select = page.locator("#v2HistorySelect")
        options = await history_select.locator("option").all()
        
        selected = False
        for opt in options:
            text = await opt.inner_text()
            if "log1" in text:
                val = await opt.get_attribute("value")
                if val:
                    await history_select.select_option(value=val)
                    selected = True
                    break
        
        if not selected and len(options) > 1:
            await history_select.select_option(index=1)

        await page.wait_for_timeout(2000)

        # Click first incident if available
        first_incident = page.locator(".incident-row-card").first
        if await first_incident.count() > 0:
            await first_incident.click()
            await page.wait_for_timeout(1000)

        # Screenshot 1: Dashboard Overview (Viewport 1440x900)
        dashboard_path = assets_dir / "01-dashboard-triagem.png"
        await page.screenshot(path=str(dashboard_path), full_page=False)
        print(f"Captured: {dashboard_path}")

        # Screenshot 2: Profiles Modal
        profiles_btn = page.locator("#v2ManageProfilesBtn")
        if await profiles_btn.count() > 0:
            await profiles_btn.click()
            await asyncio.sleep(0.8)
            profiles_path = assets_dir / "02-perfis-gravidade.png"
            await page.screenshot(path=str(profiles_path), full_page=False)
            print(f"Captured: {profiles_path}")

            # Close modal
            close_btn = page.locator("#v2CloseProfilesModal")
            if await close_btn.count() > 0:
                await close_btn.click()
                await asyncio.sleep(0.5)

        # Screenshot 3: Log Explorer
        log_section = page.locator("#v2LogViewerSection")
        if await log_section.count() > 0:
            await log_section.scroll_into_view_if_needed()
            await asyncio.sleep(0.8)
            explorer_path = assets_dir / "03-explorador-logs.png"
            await page.screenshot(path=str(explorer_path), full_page=False)
            print(f"Captured: {explorer_path}")

        await browser.close()
        print("All screenshots successfully captured!")

if __name__ == "__main__":
    asyncio.run(capture())
