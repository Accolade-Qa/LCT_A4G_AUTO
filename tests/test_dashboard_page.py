from pages.dashboard_page import Dashboard

def test_dashboard_page_title(Dashboard):
    assert Dashboard.validate_page_title().is_visible(), "Dashboard page title is not visible"