from utils.logger import get_logger

import pytest

logger = get_logger(__name__)


@pytest.mark.device
@pytest.mark.atcu
@pytest.mark.regression
class TestDeviceDetailsPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Device Details test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Device Details test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Device Details test passed: %s", test_name)
        elif report.failed:
            logger.error("Device Details test failed: %s", test_name)
            logger.debug(
                "Device Details failure details for %s: %s", test_name, report.longrepr
            )
        elif report.skipped:
            logger.warning("Device Details test skipped: %s", test_name)

