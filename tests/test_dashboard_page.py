from config.config import DASHBOARD_URL
from pages.api import dashboard_api
from pages.base_page import BasePage

class TestDashboard:

    def test_go_to_dashboard(self, page):
        assert page.url == DASHBOARD_URL, f"Expected {DASHBOARD_URL}, got {page.url}"
        
    def test_dashboard_title(self, page):
        base_page = BasePage(page)

        assert base_page.get_title() == "Device Dashboard", "Dashboard title is incorrect"
           
    def test_dashboard_page_all_elements(self, dashboard_page):
        assert dashboard_page._is_cards_visible(), "Dashboard cards are not visible"
        assert dashboard_page.get_cards_count() == 4, "Expected 4 cards on the dashboard"
        assert dashboard_page._is_graph_visible(), "Dashboard graph is not visible"
        assert dashboard_page._is_table_visible(), "Dashboard table is not visible"
        # assert dashboard_page._is_buttons_visible(), "Dashboard buttons are not visible"

        
    def test_dashboard_card_visibility(self, dashboard_page):
        assert dashboard_page._is_cards_visible(), "Dashboard cards are not visible"
        
    def test_dashboard_cards_count(self, dashboard_page):
        expected_cards_count = 4
        actual_cards_count = dashboard_page.get_cards_count()

        assert actual_cards_count == expected_cards_count, f"Expected {expected_cards_count} cards, got {actual_cards_count}"

        for index in range(expected_cards_count):
            card = dashboard_page.get_card_element(index)
            assert card.is_visible(), f"Card {index} is missing or not visible"
    
    def test_dashboard_card_title(self, dashboard_page):
        expected_title = ["TOTAL PRODUCTION DEVICES", "TOTAL DISPATCHED DEVICES", "TOTAL INSTALLED DEVICES", "TOTAL DISCARDED DEVICES"]

        for i, title in enumerate(expected_title):
            actual_title = dashboard_page.get_cards_title_text(i)
            assert actual_title == title, f"Expected '{title}', got '{actual_title}'"

    def test_dashboard_card_inner_actual_count(self, page, dashboard_page):
        api_results = dashboard_api.DashboardAPI._fetch_dashboard_cards_from_api(page)
        for i, title in enumerate(api_results.keys()):
            expected_count = str(api_results[title])
            actual_count = dashboard_page.get_cards_inner_count(i)
            assert actual_count == expected_count, f"For '{title}', expected count '{expected_count}', got '{actual_count}'"
       
    def test_graph_visibility(self, dashboard_page):
        assert dashboard_page._is_graph_visible(), "Dashboard graph is not visible"   
        
    def test_graph_title(self, dashboard_page):
        expected_graph_title = ["Device Activity Overview", "Firmware Wise Devices"]
        
        for title in expected_graph_title:
            actual_graph_title = dashboard_page.get_graph_title(title)
            assert actual_graph_title == title, f"Expected graph title '{title}', got '{actual_graph_title}'"  
        
    def test_table_visibility(self, dashboard_page):
        assert dashboard_page._is_table_visible(), "Dashboard table is not visible"
        
    def test_cards_and_graph_clicks_have_table_title(self, dashboard_page):
        expected_table_title = ["Total Production Devices", "Total Dispatched Devices", "Total Installed Devices", "Total Discarded Devices"]
        
        for title in expected_table_title:
            actual_table_title = dashboard_page.get_table_title_after_card_click(title)
            assert actual_table_title == title, f"Expected table title '{title}', got '{actual_table_title}'"
            
    def test_export_button_functionality(self, dashboard_page):
        result = dashboard_page.check_export_button()

        assert result["success"], f"Export button functionality failed: {result['error']}"
        
    def test_search_functionality(self, dashboard_page):
        search_query = "866677075606341"
        result = dashboard_page.check_search_functionality(search_query)

        assert result["success"], f"Search functionality failed: {result['error']}"
        assert result["results_found"] > 0, f"No results found for search query '{search_query}'"
        assert all(search_query in item for item in result["results"]), "Search results do not match the query"
    
    def test_table_headers(self, dashboard_page):
        expected_headers = ["UIN NO.", "IMEI NO.", "ICCID NO.", "MODEL NAME.", "ACTION"]
        actual_headers = dashboard_page.get_table_headers()
        print(f"Actual headers: {actual_headers}")
        assert actual_headers == expected_headers, f"Expected table headers {expected_headers}, got {actual_headers}"

    def test_pagination(self, dashboard_page):
        result = dashboard_page.check_pagination()
        assert result["success"], f"Pagination failed: {result['error']}"
        assert result["total_pages"] > 1, "Pagination did not move beyond first page"
        assert result["pages_visited"] == sorted(result["pages_visited"]), "Pages not in order"
