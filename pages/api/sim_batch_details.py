import json

from config.config import API_BASE_URL, API_PASSWORD, API_USERNAME
from utils.logger import get_logger

logger = get_logger(__name__)


class SIMBatchDetailsAPI:
    @staticmethod
    def _fetch_sim_details_from_api(page):
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

        api_endpoint = "/sensoriseSimData/getSimDetailsByIccidUsingCsv"

        logger.info("Fetching SIM details from API endpoint %s", api_endpoint)

        # endpoint expects a CSV file with ICCID
        sim_details_response = page.request.post(
            f"{API_BASE_URL}{api_endpoint}",
            headers=headers,
            data=json.dumps(
                {"iccidList": ["89916450344844659043"]}
            ),  # example ICCID list
        )

        if not sim_details_response.ok:
            raise Exception(
                f"API request for SIM details failed: {sim_details_response.status} {sim_details_response.text()}"
            )
        logger.info(
            "API request for SIM details succeeded with status %s",
            sim_details_response.status,
        )
        sim_details_data = sim_details_response.json()
        print(
            "SIM details API response data:", sim_details_data
        )  # Debug log for API response
        return sim_details_data.get("data", {})
