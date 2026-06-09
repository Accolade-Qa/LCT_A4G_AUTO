import json

from utils.logger import get_logger
from .api_client import APIClient
from .login_api import LoginAPI

logger = get_logger(__name__)


class UserAPI(APIClient):
    """API client for user-related operations."""

    @staticmethod
    def get_user_data_by_id(
        page, username, password, api_base_url, api_username, api_password
    ):
        """Authenticate user and obtain user data.

        Args:
            page: Playwright page object with request context.
            username: User's username for logging.
            password: User's password for logging.
            api_base_url: Base URL for API.
            api_username: API username for authentication.
            api_password: API password for authentication.

        Returns:
            dict: User data from API response.
        """

        login_data = LoginAPI.login(
            page, username, password, api_base_url, api_username, api_password
        )

        id = login_data.get("id")

        login_endpoint = f"/users/getUserdetails?id={id}"

        logger.info("Attempting to log in user %s", username)

        try:
            user_data = APIClient.send_request(
                page, api_base_url, api_username, api_password, "GET", login_endpoint
            )

            logger.info("User data retrieval successful for user %s", username)
            user_data = user_data.get("data")
            logger.debug("Received user data: %s", user_data)
            return user_data
        except Exception as e:
            logger.error("User data retrieval failed for user %s: %s", username, str(e))
            raise
