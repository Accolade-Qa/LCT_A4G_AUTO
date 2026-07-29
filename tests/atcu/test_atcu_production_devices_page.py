import os
from pathlib import Path

import pytest

from pages.common_base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

TEST_DATA_DIR_PROD = Path(__file__).resolve().parent.parent / "test_data" / "production_devices"


@pytest.mark.atcu
@pytest.mark.production
@pytest.mark.regression
class TestProductionDevicesPage:

    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Production Devices test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Production Devices test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Production Devices test passed: %s", test_name)
        elif report.failed:
            logger.error("Production Devices test failed: %s", test_name)
            logger.debug(
                "Production Devices failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Production Devices test skipped: %s", test_name)