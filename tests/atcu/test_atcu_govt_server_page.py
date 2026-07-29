from playwright.sync_api import expect
from pages.common_utils.pagination import PaginationHelper
from pages.common_utils.search import SearchHelper
from pages.common_utils.table_section import TableSection
from api.government_server_api import GovtServerAPI
from utils.helpers import Helpers
from config.config import GOVERNMENT_SERVERS_URL
from utils.logger import get_logger

import os
import pytest

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestGovtServerPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        """Automatically log test lifecycle events"""
        test_name = request.node.name
        project = os.getenv("PROJECT", "lct").lower()

        # Skip Open CPU related tests for sampark at autouse level
        open_cpu_indicators = [
            "open_cpu",
            "open cpu",
            "open-cpu",
            "oc_firmware",
            "add_open_cpu",
        ]
        if project == "sampark":
            name_lower = request.node.name.lower()
            nodeid_lower = request.node.nodeid.lower()
            if any(
                ind in name_lower or ind in nodeid_lower for ind in open_cpu_indicators
            ):
                pytest.skip("Open CPU tests are not applicable for sampark")
        logger.info("Starting Government Server test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Government Server test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Government Server test passed: %s", test_name)
        elif report.failed:
            logger.error("Government Server test failed: %s", test_name)
            logger.debug(
                "Government Server failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Government Server test skipped: %s", test_name)