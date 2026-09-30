# Playwright & Google Chrome Integration on macOS

Guidelines and best practices for automating and interacting with Google Chrome via Playwright and CDP (Chrome DevTools Protocol) in this repository.

## 1. Launching Google Chrome for Remote Automation

When testing or driving the user's Google Chrome visually on macOS, Chrome requires specific flags:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --remote-allow-origins="*" \
  --user-data-dir=/tmp/chrome_dev
```

### Why these flags are required:
- `--remote-debugging-port=9222`: Opens the Chrome DevTools Protocol (CDP) WebSocket port for automation commands.
- `--remote-allow-origins="*"`: Prevents CORS errors on WebSocket connections (note: in `zsh`, quote the asterisk to avoid globbing errors).
- `--user-data-dir=/tmp/chrome_dev`: Modern Chrome requires a non-default profile directory when remote debugging is enabled to protect personal user data.

## 2. Connecting Playwright via CDP

To connect Playwright to the active Google Chrome instance:

```python
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("http://127.0.0.1:8100/")
```

## 3. Headless vs Headed

- **Automated CI / Headless Tests:** Use `p.chromium.launch(headless=True)` with Playwright's bundled Chromium binary.
- **Interactive User Simulation / Visual Testing:** Connect via CDP to `http://127.0.0.1:9222` or launch with `channel="chrome"`.
