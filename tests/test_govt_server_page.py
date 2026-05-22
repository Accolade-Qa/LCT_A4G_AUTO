import pytest
from utils.logger import get_logger
from pages.common.table_section import TableSection

logger = get_logger(__name__)


class TestGovtServerPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        """Automatically log test lifecycle events"""
        test_name = request.node.name
        logger.info("Starting Government Server test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Government Server test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Government Server test passed: %s", test_name)
        elif report.failed:
            logger.error("Government Server test failed: %s", test_name)
            logger.debug(
                "Government Server failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Government Server test skipped: %s", test_name)

    def test_govt_server_page_title_is_correct(self, govt_server_page, report_case):
        """Verify the title of the Government Server page"""
        logger.info("Verifying Government Server page title")

        expected_title = "Government Server"
        logger.debug("Expected page title: %s", expected_title)

        actual_title = govt_server_page.get_page_title()
        logger.debug(
            "Government Server page title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=expected_title,
            actual=actual_title,
            message="Validate Government Server page title",
        )

        assert (
            expected_title in actual_title
        ), f"Expected title '{expected_title}' to be in '{actual_title}'"
        logger.info("Government Server page title verified successfully")

    def test_govt_server_page_table_headers(self, govt_server_page, report_case):
        """Verify the table headers on the Government Server page"""
        logger.info("Verifying Government Server table headers")

        expected_headers = [
            "STATE NAME",
            "STATE CODE",
            "STATE ENABLE OTA COMMAND",
            "STATE PRIMARY IP:PORT",
            "STATE SECONDARY IP:PORT",
            "ACTION",
        ]
        logger.debug("Expected table headers: %s", expected_headers)

        actual_headers = govt_server_page.get_table_headers()
        logger.debug(
            "Government Server table headers check | expected=%s | actual=%s",
            expected_headers,
            actual_headers,
        )

        report_case(
            expected=str(expected_headers),
            actual=str(actual_headers),
            message="Validate Government Server table headers",
        )

        assert (
            actual_headers == expected_headers
        ), f"Expected headers {expected_headers}, but got {actual_headers}"

        logger.info("Government Server table headers verified successfully")

    def test_govt_server_page_table_no_data(self, govt_server_page, report_case):
        """Verify the 'No Data Found' state of the table on the Government Server page"""
        logger.info("Verifying 'No Data Found' state of Government Server table")

        expected_no_data = False
        logger.debug("Expected: Table should have no data")

        actual_has_no_data = govt_server_page.get_table_headers() == []
        logger.debug(
            "Government Server table no data check | expected=%s | actual=%s",
            expected_no_data,
            actual_has_no_data,
        )

        report_case(
            expected=expected_no_data,
            actual=actual_has_no_data,
            message="Validate 'No Data Found' state for Government Server table",
        )

        assert (
            actual_has_no_data == expected_no_data
        ), "Expected 'No Data Found' state, but data was present"
        logger.info(
            "'No Data Found' state verified successfully for Government Server table"
        )

    def test_govt_server_page_table_row_count(self, govt_server_page, report_case):
        """Verify Government Server table has rows"""

        logger.info("Verifying row count of Government Server table")

        table = TableSection(govt_server_page.page)
        actual_row_count = table.get_row_count()

        logger.debug(
            "Government Server table row count: %s",
            actual_row_count,
        )

        report_case(
            expected="Row count > 0",
            actual=actual_row_count,
            message="Validate Government Server table contains rows",
        )

        assert (
            actual_row_count > 0
        ), f"Expected row count greater than 0, but got {actual_row_count}"

        logger.info(
            "Government Server table contains %s rows",
            actual_row_count,
        )
