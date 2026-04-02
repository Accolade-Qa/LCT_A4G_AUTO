import pytest

from pages.dashboard_page import Dashboard
from config.config import DASHBOARD_URL


@pytest.mark.usefixtures("login_page")
def test_dashboard_page_title(login_page):
    dashboard = Dashboard(login_page)
    assert dashboard.validate_page_title().text_content() == "Device Dashboard", "Dashboard page title is not visible"
    
@pytest.mark.usefixtures("login_page")
def test_dashboard_url(login_page):
    dashboard = Dashboard(login_page)
    assert dashboard.validate_page_url() == DASHBOARD_URL, "Dashboard page URL is incorrect"
    
# validate all 4 dashboard cards are visible
@pytest.mark.usefixtures("login_page")
def test_dashboard_cards_visibility(login_page):
    dashboard = Dashboard(login_page)
    assert dashboard.validate_dashboard_cards_visibility(), "One or more dashboard cards are not visible"






# validate the 1st card is titled "Total production Devices"
# validate the total devices count is a number
# validate the total devices count is visible and greater than 0 

# validate the 2nd card is titled "Total Dispatched Devices"
# validate the dispatched devices count is a number
# validate the dispatched devices count is visible and greater than 0

# validate the 3rd card is titled "Total Installed Devices"
# validate the installed devices count is a number
# validate the installed devices count is visible and greater than 0

# validate the 4th card is titled "Total Discarded Devices"
# validate the discarded devices count is a number
# validate the discarded devices count is visible and greater than 0

# validate the 2 graphs are visible on the dashboard page
# validate the 1st graph is titled "Device Activity Overview"

# Verify "Device Activity Overview" graph is visible
# Verify "Firmware Wise Devices" graph is visible
# Verify no broken UI or blank graph area
# Verify graphs load within acceptable time
# Verify bar values match API/backend response
# Verify total count of devices matches expected sum
# Verify each category count is correct (e.g., Today = 0, Five Days = 1, etc.)
# Verify firmware counts match expected values
