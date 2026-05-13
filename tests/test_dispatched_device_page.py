from pages.common.table_section import TableSection
from pages.common.pagination import PaginationHelper
from utils.logger import get_logger
from config.config import DISPATCHED_DEVICE_URL
import pytest
from pages.base_page import BasePage

logger = get_logger(__name__)


class TestDispatchedDevicePage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Dispatched Device test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Dispatched Device test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Dispatched Device test passed: %s", test_name)
        elif report.failed:
            logger.error("Dispatched Device test failed: %s", test_name)
            logger.debug(
                "Dispatched Device failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Dispatched Device test skipped: %s", test_name)

    def test_dispatched_device_page(self, dispatched_device_page, report_case):
        logger.debug(
            "Dispatched Device URL check | expected=%s | actual=%s",
            DISPATCHED_DEVICE_URL,
            dispatched_device_page.page.url,
        )
        report_case(
            expected=DISPATCHED_DEVICE_URL, actual=dispatched_device_page.page.url
        )

        assert (
            dispatched_device_page.page.url == DISPATCHED_DEVICE_URL
        ), f"Expected URL to be '{DISPATCHED_DEVICE_URL}', got {dispatched_device_page.page.url}"

    """ Dispatched Device Page Test Cases """

    def test_dispatched_device_page_title(self, dispatched_device_page, report_case):
        expected_title = "Dispatched Devices"
        actual_title = dispatched_device_page.page.title()
        logger.debug(
            "Dispatched Device page title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )
        report_case(expected=expected_title, actual=actual_title)

        assert (
            actual_title == expected_title
        ), f"Expected page title to be '{expected_title}', got '{actual_title}'"

    def test_dispatched_device_page_elements(self, dispatched_device_page, report_case):
        elements_checks = {
            "Manual Upload button": dispatched_device_page.is_manual_upload_button_visible(),
            "Bulk Upload button": dispatched_device_page.is_bulk_upload_button_visible(),
            "Checkbox": dispatched_device_page.is_checkbox_visible(),
            # "View Actions button": dispatched_device_page.is_view_actions_button_visible(),
            # "Delete Action button": dispatched_device_page.is_delete_action_button_visible(),
            "Dispatched Device table": dispatched_device_page.is_dispatched_device_table_visible(),
            "Search box": dispatched_device_page.is_search_box_visible(),
        }

        for element_name, is_visible in elements_checks.items():
            logger.debug(
                "%s visibility check | expected=True | actual=%s",
                element_name,
                is_visible,
            )
            report_case(
                expected=True, actual=is_visible, message=f"{element_name} visibility"
            )
            assert (
                is_visible
            ), f"Expected {element_name} to be visible on Dispatched Device page"

    def test_component_title_dispatched_device_page(
        self, dispatched_device_page, report_case
    ):
        base_page = BasePage(dispatched_device_page.page)
        expected_title = "Dispatched Device List"
        actual_title = base_page.get_component_title()
        logger.debug(
            "Dispatched Device component title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )
        report_case(expected=expected_title, actual=actual_title)

        assert (
            actual_title == expected_title
        ), f"Expected component title to be '{expected_title}', got '{actual_title}'"

    def test_table_headers_dispatched_device_page(
        self, dispatched_device_page, report_case
    ):
        expected_headers = [
            "UID",
            "IMEI",
            "ICCID",
            "MODEL NAME",
            "CUSTOMER NAME",
            "ACTION",
        ]
        actual_headers = dispatched_device_page.get_table_headers()
        logger.debug(
            "Dispatched Device table headers check | expected=%s | actual=%s",
            expected_headers,
            actual_headers,
        )
        report_case(expected=expected_headers, actual=actual_headers)
        assert (
            actual_headers == expected_headers
        ), f"Expected table headers to be {expected_headers}, got {actual_headers}"

    def test_table_data_dispatched_device_page(
        self, dispatched_device_page, report_case
    ):
        table = TableSection(dispatched_device_page.page)
        table_data = table.get_table_data()
        logger.debug(
            "Dispatched Device table data check | extracted data=%s", table_data
        )
        report_case(expected="Valid table data", actual=table_data)
        assert isinstance(
            table_data, list
        ), "Expected table data to be a list of dictionaries"
        for row in table_data:
            assert isinstance(row, dict), "Expected each row data to be a dictionary"
            assert "IMEI" in row, "Expected 'IMEI' key in row data"
            assert "ICCID" in row, "Expected 'ICCID' key in row data"

    def test_no_data_message_dispatched_device_page_if_no_data(
        self, dispatched_device_page, report_case
    ):
        table = TableSection(dispatched_device_page.page)
        actual_has_no_data = table.has_no_data()
        expected_has_no_data = table.get_row_count() == 0
        logger.debug(
            "Dispatched Device no data message check | expected=%s | actual=%s",
            expected_has_no_data,
            actual_has_no_data,
        )
        report_case(expected=expected_has_no_data, actual=actual_has_no_data)
        assert isinstance(
            actual_has_no_data, bool
        ), "Expected actual_has_no_data to be a boolean value indicating presence of 'No Data Found' message"
        if expected_has_no_data:
            assert (
                actual_has_no_data
            ), "Expected 'No Data Found' message to be displayed when table is empty"

    ## Pagination test case should be added
