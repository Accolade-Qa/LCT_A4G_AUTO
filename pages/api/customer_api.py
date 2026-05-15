from utils.logger import get_logger
from .api_client import APIClient

logger = get_logger(__name__)


class CustomerAPI(APIClient):
    """API client for customer data operations."""

    @staticmethod
    def get_customer_list(page):
        """Fetch all customer names from API.

        Args:
            page: Playwright page object with request context.

        Returns:
            list: Customer names fetched from API.
        """
        customer_endpoint = "/customerMaster/getCustomers?page=1&size=100000&search="

        logger.info("Fetching customer list from %s", customer_endpoint)

        try:
            response_data = APIClient.send_request(page, "GET", customer_endpoint)

            customers = response_data.get("data", [])

            customer_names = [
                customer.get("customerName", "").strip()
                for customer in customers
                if customer.get("customerName")
            ]

            logger.info("Retrieved %d customer names from API", len(customer_names))
            logger.debug("Customer names: %s", customer_names)

            return customer_names
        except Exception as e:
            logger.error("Failed to fetch customer list: %s", str(e))
            raise
