from playwright.sync_api import expect
from utils.logger import get_logger

import pytest

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestModelPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Model page test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Model page test finished without call report: %s",
                test_name,
            )
        elif report.passed:
            logger.info("Model page test passed: %s", test_name)
        elif report.failed:
            logger.error("Model page test failed: %s", test_name)
            logger.debug(
                "Model page failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Model page test skipped: %s", test_name)

 