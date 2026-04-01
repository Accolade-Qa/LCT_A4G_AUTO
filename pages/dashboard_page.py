from pages.base_page import BasePage

class Dashboard(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def validate_page_title(self):
        return self.page.get_by_text("Device Dashboard", exact=True)

    def go_to_dashboard(self, dashboard_url: str):
        self.navigate_to(dashboard_url)
        self.validate_page_title().wait_for(state="visible")
        
    def validate_page_url(self):
        return self.page.url
    
    def validate_dashboard_cards_visibility(self, timeout=5000):
        card_titles = [
            "Total Production Devices".capitalize(),
            "Total Dispatched Devices".capitalize(),
            "Total Installed Devices".capitalize(),
            "Total Discarded Devices".capitalize()
        ]
        missing = []

        for title in card_titles:
            locator = self.page.get_by_text(title, exact=True)
            print(f"Checking visibility for card: '{title}' : Locators {locator.text_content()}")  # Debugging line
            try:
                locator.wait_for(state="visible", timeout=timeout)
            except Exception:
                missing.append(title)

        if missing:
            # For debugging, keep the original boolean behavior but include details
            raise AssertionError(f"Missing or hidden dashboard cards: {', '.join(missing)}")

        return True