import json

from utils.logger import get_logger
from .api_client import APIClient
from config.config import API_USERNAME, API_PASSWORD

logger = get_logger(__name__)


class LoginAPI(APIClient):
    """API client for user authentication operations."""

    @staticmethod
    def login(page, username=API_USERNAME, password=API_PASSWORD):
        """Authenticate user and obtain login data.

        Args:
            page: Playwright page object with request context.
            username: User's username for authentication.
            password: User's password for authentication.

        Returns:
            dict: Login data from API response.
        """
        login_endpoint = "/users/login"

        logger.info("Attempting to log in user %s", username)

        login_payload = {
            "userEmail": API_USERNAME,
            "password": API_PASSWORD,
        }

        try:
            login_data = APIClient.send_request(
                page,
                "POST",
                login_endpoint,
                data=json.dumps(login_payload),
            )
            logger.info("Login successful for user %s", username)
            login_data = login_data.get("data")
            logger.debug("Received login data: %s", login_data)
            return login_data
        except Exception as e:
            logger.error("Login failed for user %s: %s", username, str(e))
            raise
