import pytest


from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.config
@pytest.mark.atcu
@pytest.mark.regression
class TestDeviceStateConfigPage:
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
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_device_state_config_page_loaded(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating ATCU state config page load")

        is_loaded = atcu_device_state_config_page.is_page_loaded()

        report_case(
            expected="ATCU state config page should load successfully",
            actual=f"page_loaded={is_loaded}"
        , message="Validate ATCU state config page loaded")

        assert is_loaded, "ATCU state config page is not loaded"

    # test that the page title is correct when page is loaded
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_device_state_config_page_title(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating ATCU state config page title")

        title = atcu_device_state_config_page.get_title()

        report_case(
            expected="ATCU state config page title should be correct",
            actual=f"page_title={title}"
        , message="Validate ATCU state config page title")

        assert (
            title == "Assign Device State"
        ), f"ATCU state config page title is incorrect: {title}"