import json

from utils.logger import get_logger
from .api_client import APIClient

logger = get_logger(__name__)


class SIMBatchAPI(APIClient):
    """API client for SIM batch data operations."""

    @staticmethod
    def get_sim_batch_details(page):
        """Fetch SIM batch details from API by ICCID list.

        Args:
            page: Playwright page object with request context.

        Returns:
            dict: SIM batch details from API response.
        """
        sim_details_endpoint = "/sensoriseSimData/getSimDetailsByIccidUsingCsv"

        logger.info("Fetching SIM batch details from %s", sim_details_endpoint)

        try:
            sim_details_data = APIClient.send_request(
                page,
                "POST",
                sim_details_endpoint,
                data=json.dumps({"iccidList": ["89916450344844659043"]}),
            )
            logger.info("Successfully fetched SIM batch details")
            sim_details = sim_details_data.get("data", {})
            logger.debug("SIM batch details: %s", sim_details)
            return sim_details
        except Exception as e:
            logger.error("Failed to fetch SIM batch details: %s", str(e))
            raise
