from .base_page import BasePage
from .api.login_api import LoginAPI
from utils.logger import get_logger

logger = get_logger(__name__)


class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def get_login_data(self):
        """Fetch login data using LoginAPI client."""
        logger.info("Fetching login data using LoginAPI client")
        try:
            login_data = LoginAPI.login(self.page)
            logger.info("Successfully fetched login data")
            return login_data
        except Exception as e:
            logger.error("Failed to fetch login data: %s", str(e))
            raise
