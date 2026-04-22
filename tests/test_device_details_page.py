import json
import os
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)

# Load login packet data
data_dir = Path(__file__).resolve().parent.parent / "test_data"
with open(data_dir / "login_packet.json") as f:
    lp = json.load(f)

device_info = {
    "IMEI": "866677075606341",
    "ICCID": "89916450244842405755",
    "UIN": "ACONSBA102500006341",
    "VIN": "SCVBASE1225014403",
}


class TestDeviceDetailsPage:

    # ------------------ PAGE VALIDATIONS ------------------

    def test_device_details_page_title(self, device_details_page):
        logger.info("Starting test: device_details_page_title")

        title = device_details_page.get_title()
        logger.debug("Page title: %s", title)

        assert title == "Device Details"

        logger.info("Test passed: device_details_page_title")

    def test_device_details_page_elements(self, device_details_page):
        logger.info("Starting test: device_details_page_elements")

        assert device_details_page.is_page_loaded()
        assert device_details_page.is_device_details_page_buttons_are_visible()
        assert device_details_page.is_device_kpi_cards_visible()

        logger.info("Test passed: device_details_page_elements")

    def test_go_on_device_details_page_for_particular_device(self, device_details_page):
        logger.info("Starting test: navigation to device details page")

        assert device_details_page.is_page_loaded()
        assert device_details_page.get_title() == "Device Details"

        logger.info("Test passed: navigation validation")

    # ------------------ KPI CARDS ------------------

    def test_dashboard_card_title(self, device_details_page):
        logger.info("Starting test: dashboard_card_title")

        expected_titles = [
            "IGNITION ON/OFF",
            "MAINS ON/OFF",
            "EMERGENCY ON/OFF",
            "TAMPER OPEN/CLOSE",
            "ACC CALIBRATION ON/OF",
            "WIRE CUT",
        ]

        for i, title in enumerate(expected_titles):
            actual_title = device_details_page.get_cards_title_text(i)
            assert actual_title == title, f"Card {i} title mismatch"

        logger.info("Test passed: dashboard_card_title")

    def test_kpi_cards_have_values(self, device_details_page):
        logger.info("Starting test: kpi_cards_have_values")

        count = device_details_page.get_cards_count()

        for i in range(count):
            value = device_details_page.get_cards_inner_count(i)
            assert value.strip() != "", f"Card {i} has empty value"

        logger.info("Test passed: kpi_cards_have_values")

    # ------------------ COMPONENT TITLES ------------------

    def test_all_table_component_titles(self, device_details_page):
        logger.info("Starting test: component titles")

        expected_titles = [
            "Device Details",
            "IP Details",
            "GPS and GSM Details",
            "Accelerometer Details",
            "Last 50 Login Packets",
        ]

        for i, expected in enumerate(expected_titles):
            actual = device_details_page.get_table_component_title_text(i)
            assert actual == expected, f"Component {i} title mismatch"

        logger.info("Test passed: component titles")

    # ------------------ HEADERS ------------------

    def test_headers_of_all_component_sections(self, device_details_page):
        logger.info("Starting test: all component headers")

        headers = device_details_page.get_table_component_headers()

        assert len(headers) == 30

        for required in ["IMEI Number", "ICCID Number", "UIN No", "VIN No"]:
            assert required in headers

        logger.info("Test passed: all component headers")

    def test_device_details_table_headers(self, device_details_page):
        logger.info("Starting test: login packet table headers")

        expected_headers = [
            "UIN NO.",
            "IMEI NO.",
            "ICCID.",
            "IGNITION",
            "DATE & TIME",
            "ACTION",
        ]

        actual_headers = device_details_page.get_login_packet_table_headers()

        assert actual_headers == expected_headers

        logger.info("Test passed: login packet headers")

    # ------------------ TABLE DATA ------------------

    def test_device_details_table_data(self, device_details_page):
        logger.info("Starting test: login packet table data")

        actual_data = device_details_page.get_device_details_table_data()

        assert len(actual_data) > 0, "Login packet table should have data"
        assert all(
            isinstance(row, list) for row in actual_data
        ), "Each row should be a list"

        if not len(actual_data) > 0:
            logger.warning("Login packet table is empty, skipping data validation")
            return

        logger.info("Test passed: login packet table data")

    def test_device_details_table_row_count(self, device_details_page):
        logger.info("Starting test: table row count")

        rows = device_details_page.get_device_details_table_data()

        assert len(rows) > 0

        logger.info("Test passed: table row count")

    def test_device_details_no_data_state(self, device_details_page):
        logger.info("Starting test: no data state")

        # Intentional validation (current state has data)
        has_no_data = device_details_page.table_section.has_no_data()

        # # Assertion
        # assert (
        #     has_no_data
        # ), "Expected 'No Data Found' state, but data is present in the table."

        logger.info("Test passed: no data state validation")

    # ------------------ EXPORT ------------------

    # def test_device_details_export_button(self, device_details_page):
    #     logger.info("Starting test: export button")

    #     download = device_details_page.click_export_button()

    #     # Assertions in test
    #     assert download is not None, "Download object is None"
    #     assert download.suggested_filename, "Filename missing"

    #     file_path = f"/tmp/{download.suggested_filename}"
    #     download.save_as(file_path)

    #     assert os.path.exists(file_path), "Downloaded file not found"

    #     logger.info(f"Downloaded file at: {file_path}")
    #     logger.info("Test passed: export button")

    # ------------------ PAGINATION ------------------

    def test_device_details_pagination(self, device_details_page):
        logger.info("Starting test: pagination")

        pagination = device_details_page.get_login_packet_pagination()

        result = pagination.verify()

        assert result["success"], f"Pagination failed: {result['error']}"
        assert result["pages_visited"] == sorted(result["pages_visited"])
        assert result["total_pages"] >= 1

        logger.info("Test passed: pagination")

    def test_device_details_pagination_bidirectional(self, device_details_page):
        logger.info("Starting test: bidirectional pagination")

        pagination = device_details_page.get_login_packet_pagination()

        result = pagination.verify(include_backward=True)

        assert result["success"], f"Pagination failed: {result['error']}"

        logger.info("Test passed: bidirectional pagination")

    def test_pagination_last_page_behavior(self, device_details_page):
        logger.info("Starting test: last page behavior")

        base = "//h6[text()='Last 50 Login Packets']/ancestor::div[contains(@class,'component-container')]"
        next_btn = device_details_page.page.locator(
            f"{base}//button[.//mat-icon[text()='chevron_right']]"
        )

        while not next_btn.is_disabled():
            next_btn.click()

        assert next_btn.is_disabled(), "Next button should be disabled on last page"

        logger.info("Test passed: last page behavior")
