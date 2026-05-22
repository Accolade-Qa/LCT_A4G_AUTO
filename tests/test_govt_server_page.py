import pytest
from pages.common.pagination import PaginationHelper
from pages.common.search import SearchHelper
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

    def test_govt_server_page_table_data_validation(
        self, govt_server_page, report_case
    ):
        """Verify the data in the Government Server table matches expected values"""
        logger.info("Validating data in Government Server table")

        expected_data = [
            {
                "STATE NAME": "Auto FOTA",
                "STATE CODE": "AF",
                "STATE ENABLE OTA COMMAND": "--",
                "STATE PRIMARY IP:PORT": "--:--",
                "STATE SECONDARY IP:PORT": "--:--",
                "ACTION": "visibility\ndelete",
            }
        ]

        table = TableSection(govt_server_page.page)
        actual_row_data = table.get_row_data(0)
        logger.debug(
            "Government Server table row data validation | expected=%s | actual=%s",
            expected_data[0],
            actual_row_data,
        )
        report_case(
            expected=str(expected_data[0]),
            actual=str(actual_row_data),
            message="Validate data of first row in Government Server table",
        )
        assert (
            actual_row_data == expected_data[0]
        ), f"Expected row data {expected_data[0]}, but got {actual_row_data}"
        logger.info(
            "Data in Government Server table validated successfully for first row"
        )

    def test_govt_server_page_search_functionality(self, govt_server_page, report_case):
        """Verify the search functionality of the Government Server table"""
        logger.info("Verifying search functionality of Government Server table")

        search_query = "Auto FOTA"

        search_helper = SearchHelper(govt_server_page.page)
        search_result = search_helper.run_search(search_query)
        logger.debug(
            "Government Server table search result for query '%s': %s",
            search_query,
            search_result,
        )
        report_case(
            expected=f"At least 1 result containing '{search_query}'",
            actual=f"{search_result['results_found']} results found",
            message="Validate search functionality of Government Server table",
        )
        assert search_result[
            "success"
        ], f"Search failed with error: {search_result['error']}"
        assert (
            search_result["results_found"] > 0
        ), f"Expected at least 1 search result for query '{search_query}', but found none"
        assert any(
            search_query in result for result in search_result["results"]
        ), f"Expected search results to contain '{search_query}', but got {search_result['results']}"
        logger.info(
            "Search functionality of Government Server table verified successfully for query '%s'",
            search_query,
        )

    def test_govt_server_page_table_action_buttons(self, govt_server_page, report_case):
        """Verify the presence of action buttons in the Government Server table"""
        logger.info("Verifying action buttons in Government Server table")

        table = TableSection(govt_server_page.page)
        action_buttons = table.get_action_buttons(
            1
        )  # this should be 1 cause 0 th row is headers row
        expected_buttons = ["visibility", "delete"]

        logger.debug(
            "Government Server table action buttons check | expected=%s | actual=%s",
            expected_buttons,
            action_buttons,
        )

        report_case(
            expected=str(expected_buttons),
            actual=str(action_buttons),
            message="Validate presence of action buttons in Government Server table",
        )

        assert set(action_buttons) == set(
            expected_buttons
        ), f"Expected action buttons {expected_buttons}, but got {action_buttons}"
        logger.info(
            "Action buttons in Government Server table verified successfully for first row"
        )

    def test_govt_server_page_pagination_validations(
        self, govt_server_page, report_case
    ):
        """Verify pagination controls of the Government Server table"""
        logger.info("Verifying pagination controls of Government Server table")
        pagination = PaginationHelper(govt_server_page.page)
        pagination_result = pagination.verify(include_backward=True)
        logger.debug(
            "Government Server table pagination verification result: %s",
            pagination_result,
        )
        report_case(
            expected="Pagination should work correctly in both directions",
            actual=str(pagination_result),
            message="Validate pagination controls of Government Server table",
        )
        assert pagination_result[
            "success"
        ], f"Pagination verification failed: {pagination_result['error']}"
        if pagination_result["total_pages"] > 1:
            assert len(pagination_result["pages_visited"]) > 1, (
                "Expected to visit multiple pages during pagination verification, "
                "but only one page was visited"
            )
        else:
            logger.info(
                "Only one page available in pagination. Navigation validation skipped."
            )
        logger.info(
            "Pagination controls of Government Server table verified successfully, pages visited: %s",
            pagination_result["pages_visited"],
        )
