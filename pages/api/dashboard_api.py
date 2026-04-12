import json

from config.config import API_BASE_URL, API_PASSWORD, API_USERNAME
from utils.logger import get_logger

logger = get_logger(__name__)


class DashboardAPI:
    @staticmethod
    def _fetch_dashboard_cards_from_api(page):
        if not API_USERNAME or not API_PASSWORD:
            raise ValueError(
                "API_USERNAME / API_PASSWORD must be set in the environment "
                "(or derive from APP_USERNAME / APP_PASSWORD)."
            )

        login_url = f"{API_BASE_URL}/users/login"

        login_payload = {
            "userEmail": API_USERNAME,
            "password": API_PASSWORD,
        }

        logger.info("Logging in to API user %s", API_USERNAME)
        login_response = page.request.post(
            login_url,
            data=json.dumps(login_payload),
            headers={"Content-Type": "application/json"},
        )

        if not login_response.ok:
            raise Exception(
                f"API login failed: {login_response.status} {login_response.text()}"
            )
        logger.info("API login succeeded with status %s", login_response.status)

        login_data = login_response.json()
        token = login_data.get("data", {}).get("token")

        if not token:
            raise Exception("Token not found in login response payload")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        api_endpoints = [
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

        for title, endpoint in api_endpoints:
            logger.info("Calling API for %s (%s)", title, endpoint)
            response = page.request.get(f"{API_BASE_URL}{endpoint}", headers=headers)
            if response.ok:
                data = response.json()
                count = data.get("data")
                logger.debug("API response for '%s': %s", title, data)
                if count is None:
                    count = data.get("count")
                    logger.debug(
                        "API alternative count field for '%s': %s", title, data
                    )
                result[title] = int(count)
                logger.info("API count for '%s': %s", title, result[title])
            else:
                logger.warning("API endpoint %s returned %s", endpoint, response.status)
                result[title] = 0

        logger.info("Fetched dashboard card counts sequentially: %s", result)
        return result
