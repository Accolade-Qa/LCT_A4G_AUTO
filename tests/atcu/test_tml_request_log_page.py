import pytest
import json

from pages.atcu.tml_request_log_page import TmlRequestLogPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.log
@pytest.mark.atcu
@pytest.mark.regression
class TestTmlRequestLogPage:

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

    # test that the page is loaded successfully
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_tml_request_log_page_loaded(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating TML Request Log page load")

        is_loaded = tml_request_log_page.is_page_loaded()

        report_case(
            expected="TML Request Log page should load successfully",
            actual=f"page_loaded={is_loaded}",
        )

        assert is_loaded, "TML Request Log page is not loaded"

    # test that the page title is correct when page is loaded
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_tml_request_log_page_title(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating TML Request Log page title")

        title = tml_request_log_page.get_title()

        report_case(
            expected="TML Request Log page title should be correct",
            actual=f"page_title={title}",
        )

        assert (
            title == "AIS140 Ticket TML Request Logs"
        ), f"TML Request Log page title is incorrect: {title}"

    # test that the search functionality is working as expected

    @pytest.mark.ui
    @pytest.mark.smoke
    def test_tml_request_log_page_search(
        self,
        tml_request_log_page,
        project_config,
        report_case,
    ):
        logger.info("Validating TML Request Log page search functionality")

        search_term = project_config["imei"]

        search_result = tml_request_log_page.search_logs(search_term)

        logger.debug(
            "Search completed. Success=%s, Results Found=%s",
            search_result["success"],
            search_result["results_found"],
        )

        report_case(
            expected=f"Search should execute successfully for '{search_term}'",
            actual=(
                f"success={search_result['success']}, "
                f"results_found={search_result['results_found']}"
            ),
        )

        # Search execution should always succeed
        assert search_result["success"], f"Search failed: {search_result['error']}"

        # If no records exist, helper should return an empty result set
        if search_result["results_found"] == 0:
            logger.info("No records found for search term '%s'", search_term)

            assert (
                search_result["results"] == []
            ), "Expected empty results when 'No Data Found' is displayed."

            assert (
                search_result["error"] is None
            ), "No error should be reported when there are simply no matching records."

            return

        # Otherwise validate the returned data
        logger.info(
            "%s matching record(s) found for '%s'",
            search_result["results_found"],
            search_term,
        )

        assert (
            len(search_result["results"]) == search_result["results_found"]
        ), "Results count does not match the reported results_found value."

        assert all(
            row.strip() for row in search_result["results"]
        ), "One or more returned rows are empty."

        assert any(
            search_term.lower() in row.lower() for row in search_result["results"]
        ), f"Search term '{search_term}' was not found in any returned row."

    # test that the table headers are showned is correct
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_tml_request_log_page_table_headers(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating TML Request Log page table headers")

        expected_headers = [
            "VIN NO.",
            "ICCID NO.",
            "UIN NO.",
            "SENT BY",
            "RESPONSE",
            "PAYLOAD",
            "SENT AT",
        ]

        actual_headers = tml_request_log_page.get_table_headers()

        logger.debug("Expected headers: %s", expected_headers)
        logger.debug("Actual headers: %s", actual_headers)

        report_case(
            expected=f"Table headers should match: {expected_headers}",
            actual=f"headers={actual_headers}",
        )

        # Validate the number of headers
        assert len(actual_headers) == len(expected_headers), (
            f"Expected {len(expected_headers)} headers, "
            f"but found {len(actual_headers)}."
        )

        # Validate the exact headers
        assert actual_headers == expected_headers, (
            f"Table headers do not match.\n"
            f"Expected: {expected_headers}\n"
            f"Actual: {actual_headers}"
        )

        logger.info("TML Request Log table headers validated successfully.")

    # test that the first data in the table is equal with the sent request payload
    @pytest.mark.regression
    def test_tml_request_log_page_payload_validation_on_ui(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating TML Request Log payload on UI")

        # Trigger API and fetch request payload
        (
            api_payload,
            expected_vin,
            expected_uin,
            expected_iccid,
            ticket_number,
        ) = tml_request_log_page.get_tml_request_payload_by_api()

        # Read latest UI payloads
        ui_payloads = tml_request_log_page.get_tml_request_payload_by_ui()

        logger.debug(
            "UI Payload Count: %s | Ticket No: %s",
            len(ui_payloads),
            ticket_number,
        )

        report_case(
            expected="Latest UI payload should match the API request payload",
            actual=f"ui_payload_count={len(ui_payloads)}, ticket_number={ticket_number}",
        )

        assert ui_payloads, "No payloads found in the TML Request Log table."

        # API payload is returned as list[dict]
        expected_payload = json.dumps(
            api_payload, separators=(",", ":"), sort_keys=True
        )

        payload_found = False

        for payload in ui_payloads:
            try:
                ui_json = json.loads(payload)

                ui_payload = json.dumps(
                    ui_json,
                    separators=(",", ":"),
                    sort_keys=True,
                )

                if ui_payload == expected_payload:
                    payload_found = True
                    logger.info("Matching payload found in UI.")
                    break

            except Exception as exc:
                logger.warning("Unable to parse UI payload: %s", exc)

        assert (
            payload_found
        ), "The API request payload was not found in the UI payload column."

        logger.info(
            "Payload validation completed successfully. VIN=%s, UIN=%s, ICCID=%s",
            expected_vin,
            expected_uin,
            expected_iccid,
        )

    # test that the pagingation is working as expected
    @pytest.mark.smoke
    def test_tml_request_log_page_pagination(
        self,
        tml_request_log_page,
        report_case,
    ):
        logger.info("Validating pagination on the TML Request Log page")

        pagination_result = tml_request_log_page.validate_pagination()

        logger.debug(
            "Pagination Result: success=%s, pages_visited=%s, total_pages=%s, error=%s",
            pagination_result["success"],
            pagination_result["pages_visited"],
            pagination_result["total_pages"],
            pagination_result["error"],
        )

        report_case(
            expected="Pagination should navigate correctly across all available pages",
            actual=(
                f"success={pagination_result['success']}, "
                f"pages_visited={pagination_result['pages_visited']}, "
                f"total_pages={pagination_result['total_pages']}, "
                f"error={pagination_result['error']}"
            ),
        )

        # Pagination verification should succeed
        assert pagination_result[
            "success"
        ], f"Pagination validation failed: {pagination_result['error']}"

        # At least one page should always be visited
        assert (
            len(pagination_result["pages_visited"]) > 0
        ), "No pages were visited during pagination validation."

        # The first visited page should always be page 1
        assert pagination_result["pages_visited"][0] == 1, (
            f"Pagination should start from page 1, but started from "
            f"{pagination_result['pages_visited'][0]}."
        )

        # The number of visited pages should never exceed the total pages
        assert (
            len(pagination_result["pages_visited"]) <= pagination_result["total_pages"]
        ), "Visited pages exceed the total page count."

        logger.info("Pagination validated successfully.")
