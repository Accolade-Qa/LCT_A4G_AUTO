from pages.base_page import BasePage


class Dashboard(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def is_page_title_visible(self):
        return self.page.get_by_text("Device Dashboard", exact=True).is_visible()

    def go_to_dashboard(self, dashboard_url: str):
        self.navigate_to(dashboard_url)
        self.page.wait_for_load_state("networkidle")

    def validate_page_url(self, expected_url):
        self.page.wait_for_url(expected_url)
        return self.page.url == expected_url

    def validate_dashboard_cards_visibility(self, timeout=5000):
        card_titles = [
            "Total Production Devices",
            "Total Dispatched Devices",
            "Total Installed Devices",
            "Total Discarded Devices"
        ]

        missing = []

        for title in card_titles:
            locator = self.page.get_by_text(title, exact=True)
            print(f"Checking visibility for card: '{title}'")
            try:
                locator.wait_for(state="visible", timeout=timeout)
            except Exception:
                missing.append(title)

        if missing:
            raise AssertionError(f"Missing or hidden dashboard cards: {', '.join(missing)}")

        return True