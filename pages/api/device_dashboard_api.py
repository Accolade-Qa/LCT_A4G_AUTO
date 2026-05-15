from utils.logger import get_logger
from .api_client import APIClient

logger = get_logger(__name__)


class DeviceDashboardAPI(APIClient):
    """API client for device dashboard operations."""

    @staticmethod
    def get_device_counts(page):
        """Fetch device counts by status from API.

        Args:
            page: Playwright page object with request context.

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

        for title, endpoint in device_count_endpoints:
            try:
                logger.info("Fetching %s from %s", title, endpoint)
                data = APIClient.send_request(page, "GET", endpoint)
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
