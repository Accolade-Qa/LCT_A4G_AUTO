from utils.logger import get_logger
from .api_client import APIClient
from config.config import API_USERNAME, API_PASSWORD, API_BASE_URL

logger = get_logger(__name__)


class DeviceDashboardAPI(APIClient):
    """API client for device dashboard operations."""

    @staticmethod
    def get_device_counts(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """Fetch device counts by status from API.

        Args:
            page: Playwright page object with request context.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            dict: Device status titles mapped to their counts.
        """
        device_count_endpoints = [
            (
                "TOTAL PRODUCTION DEVICES",
                "/device/getProductionDeviceCount?selectedDeviceModelId=&selectedCustomerId=",
            ),
            (
                "TOTAL DISPATCHED DEVICES",
                "/device/getDispatchDeviceCount?selectedDeviceModelId=&selectedCustomerId=",
            ),
            (
                "TOTAL INSTALLED DEVICES",
                "/device/getInstalledDeviceCount?selectedDeviceModelId=&selectedCustomerId=",
            ),
            (
                "TOTAL DISCARDED DEVICES",
                "/device/getDiscardedDeviceCount?selectedDeviceModelId=&selectedCustomerId=",
            ),
        ]

        result = {}

        # Some projects (e.g., sampark) expose API routes under an '/api' prefix.
        # Use the same heuristic as APIClient.get_bearer_token to decide whether
        # to prepend '/api' to the endpoints.
        use_api_prefix = "sampark-qa" in api_base_url or api_base_url.rstrip(
            "/"
        ).endswith("sampark-qa.accoladeelectronics.com")

        for title, endpoint in device_count_endpoints:
            full_endpoint = (
                f"/api{endpoint}"
                if use_api_prefix and not endpoint.startswith("/api")
                else endpoint
            )
            try:
                logger.info("Fetching %s from %s", title, full_endpoint)
                data = APIClient.send_request(
                    page, api_base_url, api_username, api_password, "GET", full_endpoint
                )
                count = data.get("data")
                logger.debug("API response for '%s': %s", title, data)
                if count is None:
                    count = data.get("count")
                    logger.debug(
                        "Using alternate count field for '%s': %s", title, count
                    )
                result[title] = int(count)
                logger.info("Device count for '%s': %s", title, result[title])
            except Exception as e:
                logger.warning("Failed to fetch %s: %s", title, str(e))
                result[title] = 0

        logger.info("Fetched all device counts: %s", result)
        return result
