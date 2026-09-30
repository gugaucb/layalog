import time
from pathlib import Path
from typing import Dict, Any, Optional
from playwright.sync_api import Page, expect

class LayaLogPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto_home(self):
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("domcontentloaded")
        # Ensure profiles dropdown has options attached
        self.page.wait_for_selector("#v2ProfileSelect option:not([value=''])", state="attached", timeout=10000)


    def upload_log(self, file_path: str, wait_completed: bool = True, timeout: int = 30000):
        # Set file input
        self.page.set_input_files("#v2FileInput", file_path)
        if wait_completed:
            # Wait for modal to become hidden/inactive
            self.page.wait_for_selector("#v2LoadingModal.active", timeout=5000)
            self.page.wait_for_selector("#v2LoadingModal:not(.active)", timeout=timeout)
            # Ensure KPI cards or incidents are updated
            self.page.wait_for_selector("#v2KpiLines:not(:text('-'))", timeout=5000)

    def cancel_upload(self, file_path: str):
        self.page.set_input_files("#v2FileInput", file_path)
        # Wait for cancel button and click it
        cancel_btn = self.page.locator("#v2BtnCancelProcess")
        cancel_btn.wait_for(state="visible", timeout=5000)
        cancel_btn.click()
        # Modal should close
        self.page.wait_for_selector("#v2LoadingModal:not(.active)", timeout=5000)

    def get_kpis(self) -> Dict[str, str]:
        return {
            "lines": self.page.locator("#v2KpiLines").inner_text().strip(),
            "errors": self.page.locator("#v2KpiErrors").inner_text().strip(),
            "critical": self.page.locator("#v2KpiCritical").inner_text().strip(),
            "unavailability": self.page.locator("#v2KpiUnavail").inner_text().strip(),
        }

    def filter_severity(self, severity: str):
        # severity: all, critical, high, medium, low
        chip = self.page.locator(f".severity-chip[data-severity='{severity}']")
        chip.click()
        time.sleep(0.3)

    def open_profile_modal(self):
        self.page.locator("#v2ManageProfilesBtn").click()
        self.page.wait_for_selector("#v2ProfileModal.active", timeout=5000)

    def close_profile_modal(self):
        self.page.locator("#v2CloseProfileModalBtn").click()
        self.page.wait_for_selector("#v2ProfileModal:not(.active)", timeout=5000)

    def create_custom_profile(self, name: str, desc: str, context: str, baixa: str, media: str, critica: str):
        self.open_profile_modal()
        self.page.locator("#v2NewProfileBtn").click()
        self.page.fill("#v2FormProfileName", name)
        self.page.fill("#v2FormProfileDesc", desc)
        self.page.fill("#v2FormProfileContext", context)
        self.page.fill("#v2FormCriteriaBaixa", baixa)
        self.page.fill("#v2FormCriteriaMedia", media)
        self.page.fill("#v2FormCriteriaCritica", critica)
        self.page.locator("#v2SaveProfileBtn").click()
        # Wait for profile to appear in sidebar list
        self.page.wait_for_selector(f".profile-list-item:has-text('{name}')", timeout=5000)
        self.close_profile_modal()

    def open_history_modal(self):
        self.page.locator("#v2ManageHistoryBtn").click()
        self.page.wait_for_selector("#v2HistoryModal.active", timeout=5000)

    def close_history_modal(self):
        self.page.locator("#v2CloseHistoryModalBtn").click()
        self.page.wait_for_selector("#v2HistoryModal:not(.active)", timeout=5000)
