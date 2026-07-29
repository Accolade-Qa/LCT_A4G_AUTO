from pathlib import Path
from config.config import SIM_DATA_DETAILS_URL
from utils.logger import get_logger
import pytest

logger = get_logger(__name__)

TEST_DATA_DIR = Path(__file__).resolve().parents[2] / "test_data" / "atcu"


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestSimBatchDataDetailsPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting SIM Batch Data Details test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "SIM Batch Data Details test finished without call report: %s",
                test_name,
            )
        elif report.passed:
            logger.info("SIM Batch Data Details test passed: %s", test_name)
        elif report.failed:
            logger.error("SIM Batch Data Details test failed: %s", test_name)
            logger.debug(
                "SIM Batch Data Details failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("SIM Batch Data Details test skipped: %s", test_name)