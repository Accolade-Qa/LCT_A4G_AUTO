import json

from config.config import API_BASE_URL, API_PASSWORD, API_USERNAME
from utils.logger import get_logger

logger = get_logger(__name__)


class CustomerDetailsAPI:
    @staticmethod
    def _fetch_customer_details_from_api(page):
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

        api_endpoint = "/customerMaster/getCustomers?page=1&size=100000&search="

        logger.info("Fetching customer details from API")

        response = page.request.get(
            f"{API_BASE_URL}{api_endpoint}",
            headers=headers,
        )

        if not response.ok:
            raise Exception(
                f"Customer API request failed: " f"{response.status} {response.text()}"
            )

        logger.info(
            "Customer details API succeeded with status %s",
            response.status,
        )

        response_data = response.json()

        customers = response_data.get("data", [])

        customer_names = [
            customer.get("customerName", "").strip()
            for customer in customers
            if customer.get("customerName")
        ]

        logger.info(
            "Fetched %s customer names from API",
            len(customer_names),
        )

        logger.debug("Customer names fetched: %s", customer_names)

        return customer_names
