from conftest import tml_request_log_page
from pages.atcu.atcu_aepl_response_log_page import AtcuAeplResponseLogPage
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
