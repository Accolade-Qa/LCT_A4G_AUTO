import pytest

from pages.dashboard_page import Dashboard
from config.config import DASHBOARD_URL

@pytest.mark.usefixtures("login_page")
def test_dashboard_page_title(login_page):
    dashboard = Dashboard(login_page)
    assert dashboard.validate_page_title().text_content() == "Device Dashboard", "Dashboard page title is not visible"