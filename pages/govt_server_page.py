import logging
import re
from pages.base_page import BasePage


class GovtServerPage(BasePage):

    def __init__(self, page):
        # super().__init__(page)
        self.page = page
        self.logger = logging.getLogger(__name__)   # ✅ ADD THIS
    
           

        # ✅ Locator inside __init__
        # self.deviceutilitylink = page.locator("a.dropdown-toggle.ng-star-inserted:visible")
        # self.devicetab = page.get_by_text("DEVICE UTILITY", exact=True)
        # self.device_tab = page.get_by_role("link", name=re.compile(r"DEVICE UTILITY", re.IGNORECASE))
        
    # ✅ Method INSIDE class
    def go_to_govtserver(self, url):
        self.logger.info(f"Opening URL: {url}")
        self.page.goto(url)

    # ✅ Method INSIDE class
    def click_device_utility_tab(self):
        self.logger.info("Opening DEVICE UTILITY tab")
        device_tab = self.page.get_by_role("link", name=re.compile(r"DEVICE UTILITY", re.IGNORECASE))
        # device_tab = self.page.locator("//a[contains(text(),'DEVICE UTILITY')]")
        device_tab.wait_for(state="visible", timeout=10000)
        # Scroll into view
        device_tab.scroll_into_view_if_needed()
        # ✅ Try click instead of hover
        device_tab.click()
        # ✅ Wait for dropdown with better locator
        dropdown = self.page.locator("ul.dropdown-menu.show, ul.dropdown-menu")
        dropdown.wait_for(state="visible", timeout=10000)
        self.logger.info("DEVICE UTILITY dropdown opened successfully")
        

    def click_government_servers(self):
        gov_option = self.page.locator("//a[contains(text(),'GOVERNMENT SERVERS')]")
        gov_option.wait_for(state="visible", timeout=5000)
        gov_option.click()