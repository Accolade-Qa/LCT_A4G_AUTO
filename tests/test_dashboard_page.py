import pytest

from pages.dashboard_page import Dashboard
from config.config import DASHBOARD_URL

@pytest.fixture(scope="function")
def dashboard(page):
    dashboard = Dashboard(page)
    dashboard.go_to_dashboard(DASHBOARD_URL)
    return dashboard

def test_dashboard_page_title(dashboard):
    assert dashboard.is_page_title_visible(), "Dashboard page title is not visible"


def test_dashboard_url(dashboard):
    assert dashboard.validate_page_url(DASHBOARD_URL), "Dashboard page URL is incorrect"


def test_dashboard_cards_visibility(dashboard):
    assert dashboard.validate_dashboard_cards_visibility(), "One or more dashboard cards are not visible"


def test_dashboard_card_counts(dashboard):
    counts = dashboard.validate_dashboard_card_counts()
    for title, value in counts.items():
        assert value > 0, f"{title} count should be greater than 0, got {value}"


def test_dashboard_graphs_visible(dashboard):
    assert dashboard.validate_dashboard_graphs(), "Dashboard graphs are not visible"
