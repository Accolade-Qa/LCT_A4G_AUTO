import pytest
from pages.common_utils import TableSection
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.regression
class TestAeplResponseLogPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting AEPL Response Log test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "AEPL Response Log test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("AEPL Response Log test passed: %s", test_name)
        elif report.failed:
            logger.error("AEPL Response Log test failed: %s", test_name)
            logger.debug(
                "AEPL Response Log failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("AEPL Response Log test skipped: %s", test_name)

    # test that the page is loaded successfully
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_aepl_response_log_page_loaded(
        self,
        aepl_response_log_page,
        report_case,
    ):
        logger.info("Validating AEPL Response Log page load")

        is_loaded = aepl_response_log_page.is_page_loaded()

        report_case(
            expected="AEPL Response Log page should load successfully",
            actual=f"page_loaded={is_loaded}",
            message="AEPL Response Log page load validation",
        )

        assert is_loaded, "AEPL Response Log page is not loaded"

    # test that the page title is correct when page is loaded
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_aepl_response_log_page_title(
        self,
        aepl_response_log_page,
        report_case,
    ):
        logger.info("Validating AEPL Response Log page title")

        title = aepl_response_log_page.get_title()

        report_case(
            expected="AEPL Response Log page title should be correct",
            actual=f"page_title={title}",
            message="AEPL Response Log page title validation",
        )

        assert (
            title == "AIS140 Ticket AEPL Response Logs"
        ), f"AEPL Response Log page title is incorrect: {title}"

    # Do first request with valid payload
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.api
    @pytest.mark.smoke
    def test_is_request_response_valid(self, aepl_response_log_page, report_case):
        logger.info("Validating AEPL Response Log request-response pairs")
        payload, VIN, UIN, ICCID, ticket_number, data = (
            aepl_response_log_page.get_valid_request_response_by_api()
        )
        report_case(
            expected="Valid request-response pairs should be fetched from AEPL Response Log API",
            actual=f"payload={payload}, VIN={VIN}, UIN={UIN}, ICCID={ICCID}, ticket_number={ticket_number}, data={data}",
            message="AEPL Response Log request-response validation",
        )

        assert (
            payload is not None
        ), "Failed to fetch valid request-response pairs from AEPL Response Log API"
        assert VIN is not None, "VIN is None in the valid request-response pairs"
        assert UIN is not None, "UIN is None in the valid request-response pairs"
        assert ICCID is not None, "ICCID is None in the valid request-response pairs"
        assert (
            ticket_number is not None
        ), "Ticket number is None in the valid request-response pairs"
        assert isinstance(
            payload, list
        ), "Payload is not a dictionary in the valid request-response pairs"
        assert isinstance(
            ticket_number, str
        ), "Ticket number is not a string in the valid request-response pairs"
        assert isinstance(
            data, dict
        ), "Data is not a list in the valid request-response pairs"

    # Test the response on the UI of the response log page with the valid payload
    # and validate the response on the UI with the response from the API
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.api
    @pytest.mark.smoke
    def test_validate_response_log_page_with_valid_payload(
        self, aepl_response_log_page, report_case
    ):
        logger.info(
            "Validating AEPL Response Log page payload with API response"
        )

        _, VIN, UIN, ICCID, ticket_number, data = (
            aepl_response_log_page.get_valid_request_response_by_api()
        )

        logger.info(
            "API response received: VIN=%s, UIN=%s, ICCID=%s, ticket_number=%s, data=%s",
            VIN,
            UIN,
            ICCID,
            ticket_number,
            data,
        )

        report_case(
            expected="Valid payload response should be fetched from AEPL Response Log API",
            actual=(
                f"VIN={VIN}, UIN={UIN}, ICCID={ICCID}, "
                f"ticket_number={ticket_number}, data={data}"
            ),
            message="AEPL API response validation",
        )

        assert data is not None, "API response data is None"
        assert isinstance(data, dict), "API response data is not a dictionary"

        logger.info("Reloading AEPL Response Log page to fetch latest entry")

        aepl_response_log_page.page.reload(wait_until="networkidle")

        table = TableSection(aepl_response_log_page.page)
        row = table.get_row_data(0)

        logger.info("UI response log row fetched: %s", row)

        payload_data = aepl_response_log_page._normalize_payload_value(
            row["PAYLOAD"]
        )

        logger.info(
            "Payload extracted from UI: %s",
            payload_data,
        )

        report_case(
            expected="UI payload should match API response payload",
            actual=f"UI payload={payload_data}, API payload={data}",
            message="AEPL Response Log UI payload validation",
        )

        assert isinstance(payload_data, dict), "UI payload is not a dictionary"

        assert (
            payload_data["ICCID"] == data["ICCID"]
        ), "ICCID mismatch between UI payload and API response"

        assert (
            payload_data["UIN_NO"] == data["UIN_NO"]
        ), "UIN mismatch between UI payload and API response"

        assert (
            payload_data["VIN_NO"] == data["VIN_NO"]
        ), "VIN mismatch between UI payload and API response"

        logger.info(
            "AEPL Response Log payload validation completed successfully"
        )

    # Test the column data:
    # sent to - ['Generate Tickets API', 'Institutional Sale']
    # response - 200
    # VIN, UIN, ICCID validation
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.api
    @pytest.mark.smoke
    def test_validate_table_headers_and_data_as_expected(
        self, aepl_response_log_page, report_case
    ):
        logger.info(
            "Validating AEPL Response Log table data with API response"
        )

        (
            _,
            VIN,
            UIN,
            ICCID,
            ticket_number,
            data,
        ) = aepl_response_log_page.get_valid_request_response_by_api()

        logger.info(
            "API data received: VIN=%s, UIN=%s, ICCID=%s, ticket_number=%s",
            VIN,
            UIN,
            ICCID,
            ticket_number,
        )

        report_case(
            expected="AEPL Response Log API should return valid VIN, UIN and ICCID data",
            actual=(
                f"VIN={VIN}, UIN={UIN}, ICCID={ICCID}, "
                f"ticket_number={ticket_number}"
            ),
            message="AEPL API data validation",
        )

        logger.info(
            "Reloading AEPL Response Log page to get latest table data"
        )

        aepl_response_log_page.page.reload(wait_until="networkidle")

        ui_data = TableSection(
            aepl_response_log_page.page
        ).get_row_data(0)

        logger.info(
            "UI table row data fetched: %s",
            ui_data,
        )

        report_case(
            expected="AEPL Response Log table should display API data correctly",
            actual=(
                f"UI VIN={ui_data.get('VIN NO.')}, "
                f"UI UIN={ui_data.get('UIN NO.')}, "
                f"UI ICCID={ui_data.get('ICCID NO.')}"
            ),
            message="AEPL Response Log UI table data validation",
        )

        assert (
            VIN == ui_data["VIN NO."]
        ), "VIN mismatch between API response and UI table"

        assert (
            UIN == ui_data["UIN NO."]
        ), "UIN mismatch between API response and UI table"

        assert (
            ICCID == ui_data["ICCID NO."]
        ), "ICCID mismatch between API response and UI table"

        logger.info(
            "AEPL Response Log table data validation completed successfully"
        )

    # Validate the Search functionality on the response log page with the valid payload and validate the response on the ui with the response from the api

    # Validate the table headers on response log page

    # Validate the table data first row response's each data with the response from the api

    # Validate the pagination on the response log page with the valid payload and validate the response on the ui with the response from the api
