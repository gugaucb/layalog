import os
import sys
import time
import socket
import tempfile
import threading
from pathlib import Path
from typing import Generator
import pytest
import uvicorn
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

class ServerThread(threading.Thread):
    def __init__(self, app, host: str, port: int):
        super().__init__(daemon=True)
        self.host = host
        self.port = port
        self.config = uvicorn.Config(app=app, host=host, port=port, log_level="warning")
        self.server = uvicorn.Server(config=self.config)

    def run(self):
        self.server.run()

    def stop(self):
        self.server.should_exit = True

@pytest.fixture(scope="session")
def test_env() -> Generator[dict, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        db_path = temp_path / "test_layalog.db"
        upload_dir = temp_path / "test_uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)

        old_db_env = os.environ.get("LAYALOG_DB_PATH")
        old_up_env = os.environ.get("LAYALOG_UPLOAD_DIR")

        os.environ["LAYALOG_DB_PATH"] = str(db_path)
        os.environ["LAYALOG_UPLOAD_DIR"] = str(upload_dir)

        from layalog.database import init_db
        init_db(db_path)

        yield {
            "temp_dir": temp_path,
            "db_path": db_path,
            "upload_dir": upload_dir
        }

        if old_db_env is not None:
            os.environ["LAYALOG_DB_PATH"] = old_db_env
        else:
            os.environ.pop("LAYALOG_DB_PATH", None)

        if old_up_env is not None:
            os.environ["LAYALOG_UPLOAD_DIR"] = old_up_env
        else:
            os.environ.pop("LAYALOG_UPLOAD_DIR", None)

@pytest.fixture(scope="session")
def server(test_env) -> Generator[str, None, None]:
    from layalog.app import app
    
    port = get_free_port()
    host = "127.0.0.1"
    server_thread = ServerThread(app, host=host, port=port)
    server_thread.start()

    base_url = f"http://{host}:{port}"
    
    # Wait for server to start responding
    max_wait = 15.0
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                break
        except (OSError, ConnectionRefusedError):
            time.sleep(0.1)
    else:
        raise RuntimeError(f"Server did not start within {max_wait}s on {base_url}")

    yield base_url

    server_thread.stop()
    server_thread.join(timeout=5)

@pytest.fixture(scope="session")
def browser_instance() -> Generator[Browser, None, None]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def context(browser_instance: Browser) -> Generator[BrowserContext, None, None]:
    context = browser_instance.new_context(
        viewport={"width": 1440, "height": 900},
        accept_downloads=True
    )
    yield context
    context.close()

@pytest.fixture
def page(context: BrowserContext, server: str) -> Generator[Page, None, None]:
    page = context.new_page()
    # Default navigation timeout
    page.set_default_timeout(10000)
    yield page
    page.close()
