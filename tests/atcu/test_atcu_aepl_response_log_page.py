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
        )

        assert (
            title == "AIS140 Ticket AEPL Response Logs"
        ), f"AEPL Response Log page title is incorrect: {title}"

    # Do first request with valid payload 

    # Test the response on the ui of the response log page with the valid payload and validate the response on the ui with the response from the api

    # Test the two rows data's sent to should be from 'TML CRM' and 'TML FE' and validate the response on the ui with the response from the api

    # Test the response with 'TML CRM' should have payload like example this - { "Asset_Number": "MAT00007241590101", "ICCID": "89916450344843492941", "TM_AIS_140_Ticket_No": "AEPL-260720-1", "TM_Ticket_Handler": "Pratik Kundle", "TM_Ticket_Stage": "Stage 1", "TM_Activity": "FOTA / OTA Activities", "TM_Ticket_Status": "Assigned", "TM_Ticket_Completion_Date": "", "TM_KYC_Remark": "", "TM_KYC_Certificate_Date": "", "TM_Certificate_Expiry_Date": "", "TM_Certificate_File_Link": "" }

    # Test the response with 'TML FE' should have payload like example this - { "Ticket_No": "AEPL-260720-1", "Ticket_Handler": "Pratik Kundle", "Ticket_Handler_Contact": "8999027261", "Ticket_Stage": "Stage 1", "Ticket_Activity": "FOTA / OTA Activities", "Ticket_Status": "Assigned", "Ticket_Remark": "", "VIN_NO": "MAT00007241590101", "ICCID": "89916450344843492941", "UIN_NO": "ACON4IA202200075879", "RTO_STATE": "MH", "RTO_OFFICE_CODE": "MH12", "Process_End_Date_and_Time": "", "Certification_Registration_Date_and_Time": "", "Certification_Expiry_Date": "", "Certificate_File_Location": "", "Certificate_File_Names": [] }

    # Validate the Search functionality on the response log page with the valid payload and validate the response on the ui with the response from the api

    # Validate the table headers on response log page

    # Validate the table data first row response's each data with the response from the api

    # Validate the pagination on the response log page with the valid payload and validate the response on the ui with the response from the api