import pytest
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

        assert payload is not None, "Failed to fetch valid request-response pairs from AEPL Response Log API"
        assert VIN is not None, "VIN is None in the valid request-response pairs"
        assert UIN is not None, "UIN is None in the valid request-response pairs"
        assert ICCID is not None, "ICCID is None in the valid request-response pairs"
        assert ticket_number is not None, "Ticket number is None in the valid request-response pairs"
        assert isinstance(payload, list), "Payload is not a dictionary in the valid request-response pairs"
        assert isinstance(ticket_number, str), "Ticket number is not a string in the valid request-response pairs"
        assert isinstance(data, dict), "Data is not a list in the valid request-response pairs"

    # Test the response on the ui of the response log page with the valid payload and validate the response on the ui with the response from the api
    def test_validate_response_log_page_with_valid_payload(
        self, aepl_response_log_page, report_case
    ):
        logger.info("Validating AEPL Response Log page with valid payload")

        _, _, _, _, _, data = (
            aepl_response_log_page.get_valid_request_response_by_api()
        )

        if not data.get("TICKET_NO") or data.get("status") is False:
            report_case(
                expected="API should return a valid ticket with status=True",
                actual=f"status={data.get('status')}, ticket_no={data.get('TICKET_NO')}, validation_error={data.get('VALIDATION_ERROR')}",
                message="API request validation",
            )
            pytest.skip(
                f"API request failed: {data.get('message')} - {data.get('VALIDATION_ERROR')}"
            )

        matching_row_data = aepl_response_log_page.get_matching_row_for_api_data(data)
        payload_data = matching_row_data.get("PAYLOAD") if matching_row_data else None

        report_case(
            expected="AEPL Response Log page should display correct data for valid payload",
            actual=f"matching_row_data={matching_row_data}, payload_data={payload_data}, api_data={data}",
            message="AEPL Response Log page data validation with valid payload",
        )
        assert matching_row_data is not None, "No matching row found for the API response payload"

        assert isinstance(payload_data, dict), "UI payload is not a dictionary"

        if data.get("VIN_NO"):
            assert payload_data.get("VIN_NO") == data.get("VIN_NO"), "VIN mismatch between UI payload and API response"
        if data.get("ICCID"):
            assert payload_data.get("ICCID") == data.get("ICCID"), "ICCID mismatch between UI payload and API response"
        if data.get("UIN_NO"):
            assert payload_data.get("UIN_NO") == data.get("UIN_NO"), "UIN mismatch between UI payload and API response"


    # Test the two rows data's sent to should be from 'TML CRM' and 'TML FE' and validate the response on the ui with the response from the api

    # Test the response with 'TML CRM' should have payload like example this - { "status": true, "message": "Data Saved Successfully!!", "VIN_NO": "MAT00007241590101", "ICCID": "89916450344843492941", "UIN_NO": "ACON4IA202200075879", "TICKET_NO": "AEPL-260720-1", "VALIDATION_ERROR": [] }

    # Validate the Search functionality on the response log page with the valid payload and validate the response on the ui with the response from the api

    # Validate the table headers on response log page

    # Validate the table data first row response's each data with the response from the api

    # Validate the pagination on the response log page with the valid payload and validate the response on the ui with the response from the api