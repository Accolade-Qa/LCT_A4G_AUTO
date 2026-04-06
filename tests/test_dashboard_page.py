from config.config import BASE_URL, DASHBOARD_URL, PASSWORD, USERNAME
from pages.api import dashboard_api
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

class TestDashboard:
    def _login_and_dashboard(self, page):
        login_page = LoginPage(page)
        login_page.load(BASE_URL)
        login_page.login(USERNAME, PASSWORD)

        return DashboardPage(page)

    def test_go_to_dashboard(self, page):
        dashboard_page = self._login_and_dashboard(page)
        dashboard_page.go_to_dashboard(DASHBOARD_URL)

        assert page.url == DASHBOARD_URL, f"Expected {DASHBOARD_URL}, got {page.url}"
        
    def test_dashboard_title(self, page):
        dashboard_page = self._login_and_dashboard(page)
        base_page = BasePage(page)
        dashboard_page.go_to_dashboard(DASHBOARD_URL)

        assert base_page.get_title() == "Device Dashboard", "Dashboard title is incorrect"
        
    def test_dashboard_card_visibility(self, page):
        dashboard_page = self._login_and_dashboard(page)
        dashboard_page.go_to_dashboard(DASHBOARD_URL)

        assert dashboard_page._is_cards_visible(), "Dashboard cards are not visible"
        
    def test_dashboard_cards_count(self, page):
        dashboard_page = self._login_and_dashboard(page)
        dashboard_page.go_to_dashboard(DASHBOARD_URL)

        expected_cards_count = 4
        actual_cards_count = dashboard_page.get_cards_count()

        assert actual_cards_count == expected_cards_count, f"Expected {expected_cards_count} cards, got {actual_cards_count}"

        for index in range(expected_cards_count):
            card = dashboard_page.get_card_element(index)
            assert card.is_visible(), f"Card {index} is missing or not visible"
    
    def test_dashboard_card_title(self, page):
        # make this expected capital ["Total Production Devices", "Total Dispatched Devices", "Total Installed Devices", "Total Discarded Devices"]
        expected_title = ["TOTAL PRODUCTION DEVICES", "TOTAL DISPATCHED DEVICES", "TOTAL INSTALLED DEVICES", "TOTAL DISCARDED DEVICES"]

        dashboard_page = self._login_and_dashboard(page)
        dashboard_page.go_to_dashboard(DASHBOARD_URL)

        for i, title in enumerate(expected_title):
            actual_title = dashboard_page.get_cards_title_text(i)
            assert actual_title == title, f"Expected '{title}', got '{actual_title}'"

    def test_dashboard_card_inner_actual_count(self, page):
        api_results = dashboard_api.DashboardAPI._fetch_dashboard_cards_from_api(page)
        print("API Results:", api_results)  # Debugging line to check API results
        dashboard_page = self._login_and_dashboard(page)
        dashboard_page.go_to_dashboard(DASHBOARD_URL)
        for i, title in enumerate(api_results.keys()):
            print(f"Testing card '{title}' with expected count '{api_results[title]}'")  # Debugging line to check title and expected count
            expected_count = str(api_results[title])
            print(f"Expected count for '{title}': {expected_count}")  # Debugging line to check expected count
            actual_count = dashboard_page.get_cards_inner_count(i)
            assert actual_count == expected_count, f"For '{title}', expected count '{expected_count}', got '{actual_count}'"
        
        
        
