from config.config import DASHBOARD_URL
from utils.logger import get_logger

logger = get_logger(__name__)


class TestDeviceDetailsPage:
    def test_device_details_page_title(self, device_details_page):
        logger.info("Testing Device Details page title")
        device_details_page.page.goto(DASHBOARD_URL)
        device_details_page.page.wait_for_load_state("networkidle")
        title = device_details_page.get_title()
        assert (
            title == "Device Details"
        ), f"Expected page title 'Device Details', but got '{title}'"

    def test_device_details_page_elements(self, device_details_page):
        logger.info("Testing Device Details page elements")

        device_details_page.page.goto(DASHBOARD_URL)
        device_details_page.page.wait_for_load_state("networkidle")

        assert (
            device_details_page.is_page_loaded()
        ), "Device Details page did not load correctly"

        assert (
            device_details_page.is_device_details_page_buttons_are_visible()
        ), "Device Details page buttons are not visible"

        assert (
            device_details_page.is_device_kpi_cards_visible()
        ), "Device KPI cards are not visible"
        logger.info("All Device Details page elements are present and visible")

    def test_go_on_device_details_page_for_particular_device(self, device_details_page):
        logger.info("Testing navigation to Device Details page for a specific device")

        device = "89916450244842405755"

        # Step 1: Go to dashboard
        device_details_page.page.goto(DASHBOARD_URL)
        device_details_page.page.wait_for_load_state("networkidle")

        # Step 2: Search device
        result = device_details_page.search_for_device(device)

        assert result["success"], f"Search failed: {result['error']}"

        # Step 3: Validate only one result
        assert (
            result["results_found"] == 1
        ), f"Expected 1 result, found {result['results_found']}"

        # Step 4: Click view icon
        device_details_page.click_on_view_device_in_table(device)

        # Step 5: Validate Device Details page
        assert device_details_page.is_page_loaded(), "Device Details page did not load"

        assert device_details_page.get_title() == "Device Details"

        assert (
            device_details_page.is_device_kpi_cards_visible()
        ), "KPI cards not visible"

        logger.info("Device Details page validation successful")
