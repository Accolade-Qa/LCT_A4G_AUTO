from random import randint
from pages.common_utils.table_section import TableSection
from pages.common_utils.pagination import PaginationHelper
from pages.common_utils.search import SearchHelper
from test_data.atcu.device_data import DeviceData
from utils.logger import get_logger
from pages.common_base_page import BasePage
from api.customer_api import CustomerAPI
from config.config import DISPATCHED_DEVICE_URL

import pytest

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestDispatchedDevicePage:
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