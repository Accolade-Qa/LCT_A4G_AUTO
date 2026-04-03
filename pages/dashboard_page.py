import re

from config.config import DASHBOARD_URL
from pages.base_page import BasePage
from pages.login_page import LoginPage as Login


class Dashboard(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.login = Login(page)

    def is_page_title_visible(self, timeout=5000):
        self.go_to_dashboard(DASHBOARD_URL)
        locator = self.page.get_by_text("Device Dashboard", exact=True)
        locator.wait_for(state="visible", timeout=timeout)
        return locator.is_visible()

    def go_to_dashboard(self, dashboard_url: str):
        self.login.login()
        self.navigate_to(dashboard_url)
        self.page.wait_for_load_state("networkidle")

    def validate_page_url(self, expected_url):
        current = self.page.url.rstrip("/")
        expected = expected_url.rstrip("/")

        return current == expected or current.startswith(expected)

    def _card_titles(self):
        return [
            "Total Production Devices",
            "Total Dispatched Devices",
            "Total Installed Devices",
            "Total Discarded Devices",
        ]

    def validate_dashboard_cards_visibility(self, timeout=5000):
        missing = []

        for title in self._card_titles():
            locator = self.page.get_by_text(title, exact=True)
            print(f"Checking visibility for card: '{title}'")
            try:
                locator.wait_for(state="visible", timeout=timeout)
            except Exception:
                missing.append(title)

        if missing:
            raise AssertionError(f"Missing or hidden dashboard cards: {', '.join(missing)}")

        return True

    def _find_card_container(self, title):
        title_locator = self.page.get_by_text(title, exact=True)
        return title_locator.locator("xpath=ancestor::div[1]")

    def _extract_numeric_from_text(self, text):
        match = re.search(r"(\d[\d,]*)", text)
        if not match:
            raise AssertionError("Could not find a numeric value in card text")

        return int(match.group(1).replace(",", ""))

    def get_card_value(self, title):
        container = self._find_card_container(title)
        card_text = container.inner_text().strip()
        return self._extract_numeric_from_text(card_text)

    def validate_dashboard_card_counts(self, minimum=1):
        counts = {}
        for title in self._card_titles():
            value = self.get_card_value(title)
            if value < minimum:
                raise AssertionError(f"{title} card has an unexpected count: {value}")
            counts[title] = value
        return counts

    def validate_dashboard_graphs(self, timeout=5000):
        graph_titles = ["Device Activity Overview", "Firmware Wise Devices"]
        missing = []

        for title in graph_titles:
            locator = self.page.get_by_text(title, exact=True)
            try:
                locator.wait_for(state="visible", timeout=timeout)
            except Exception:
                missing.append(title)

        if missing:
            raise AssertionError(f"Missing or hidden graphs: {', '.join(missing)}")

        return True
