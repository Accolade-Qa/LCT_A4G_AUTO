from utils.logger import get_logger

logger = get_logger(__name__)


class TestDeviceDetailsPage:
    def test_device_details_page_title(self, device_details_page):
        logger.info("Testing Device Details page title")
        title = device_details_page.get_title()
        assert (
            title == "Device Details"
        ), f"Expected page title 'Device Details', but got '{title}'"

    def test_device_details_page_elements(self, device_details_page):
        logger.info("Testing Device Details page elements")

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
