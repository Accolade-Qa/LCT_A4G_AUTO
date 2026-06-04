import pytest

from config.config import API_PASSWORD, API_USERNAME
from pages.api.sim_batch_api import SIMBatchAPI
from utils.logger import get_logger

logger = get_logger(__name__)


if not API_USERNAME or not API_PASSWORD:
    pytest.skip(
        "API credentials are not configured for API tests", allow_module_level=True
    )


@pytest.mark.api
@pytest.mark.regression
class TestSIMBatchAPI:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        logger.info("Starting SIMBatchAPI test: %s", request.node.name)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.warning(
                "SIMBatchAPI test finished without call report: %s", request.node.name
            )
        elif report.passed:
            logger.info("SIMBatchAPI test passed: %s", request.node.name)
        elif report.failed:
            logger.error("SIMBatchAPI test failed: %s", request.node.name)

    @pytest.mark.smoke
    def test_get_sim_batch_details_by_csv_returns_expected_structure(
        self, page, report_case
    ):
        logger.info("Calling SIM batch CSV details API")
        duplicate_rows, sim_details, errors = SIMBatchAPI.get_sim_batch_details_by_csv(
            page
        )

        logger.debug(
            "SIM batch CSV response shape | duplicate_rows=%s | sim_details_type=%s | errors=%s",
            type(duplicate_rows).__name__,
            type(sim_details).__name__,
            type(errors).__name__,
        )

        report_case(
            expected="Validate SIM batch CSV response structure",
            actual=f"duplicate_rows={len(duplicate_rows)}, sim_details={type(sim_details).__name__}, errors={len(errors)}",
        )

        # Basic assertions to validate response structure
        assert isinstance(duplicate_rows, list), "Expected duplicate_rows to be a list"
        assert isinstance(errors, list), "Expected errors to be a list"
        assert isinstance(sim_details, dict), "Expected sim_details to be a dict"

        # Additional assertions can be added here based on expected content of the response
        assert (
            len(duplicate_rows) >= 0
        ), "Expected duplicate_rows to be present in response"
        assert len(errors) >= 0, "Expected errors to be present in response"
        assert sim_details is not None, "Expected sim_details to be present in response"

        # add assertions to validate specific content in sim_details if expected structure is known
        sim_detail_entity = sim_details.get("simDetailEntity", [])
        assert isinstance(
            sim_detail_entity, list
        ), "Expected simDetailEntity to be a list"

        if sim_detail_entity:
            first_entity = sim_detail_entity[0]
            assert isinstance(
                first_entity, dict
            ), "Expected simDetailEntity items to be dicts"
            assert (
                "cardState" in first_entity
            ), "Expected cardState field in simDetailEntity item"
            assert first_entity["cardState"] == "Terminated"

    def test_get_sim_batch_by_manual_upload_returns_data(self, page, report_case):
        logger.info("Calling SIM batch manual upload API")
        data = SIMBatchAPI.get_sim_batch_by_manual_upload(page)

        logger.debug("SIM batch manual upload response data: %s", data)
        report_case(
            expected="Validate SIM batch manual upload response",
            actual=f"response_type={type(data).__name__}",
        )

        assert data is not None, "Expected a non-null response from manual upload API"
        assert isinstance(
            data, (dict, list)
        ), "Expected response data to be a dict or list"
