import os
import random
import string
import time
from datetime import datetime

from utils.logger import get_logger

logger = get_logger(__name__)


class Helpers:

    @staticmethod
    def generate_random_string(length=6):
        """Generate a random alphabetic string."""
        if length <= 0:
            raise ValueError("length must be a positive integer")
        logger.debug("Generating random string of length %s", length)
        return "".join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def generate_random_number(length=6):
        """Generate a random numeric string (digits only)."""
        if length <= 0:
            raise ValueError("length must be a positive integer")
        logger.debug("Generating random number of length %s", length)
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def generate_random_email(prefix="user", domain="example.com"):
        """Generate a random email address."""
        logger.debug(
            "Generating random email with prefix %s and domain %s", prefix, domain
        )
        username = f"{prefix}_{Helpers.generate_random_string(6).lower()}"
        return f"{username}@{domain}"

    @staticmethod
    def generate_random_phone(country_code="+91", length=10):
        """Generate a random phone number string."""
        if length <= 0:
            raise ValueError("length must be a positive integer")
        number = "".join(random.choices(string.digits, k=length))
        logger.debug("Generated phone number with country code %s", country_code)
        return f"{country_code}{number}"

    @staticmethod
    def get_timestamp(fmt="%Y%m%d%H%M%S"):
        """Return current timestamp string in given format."""
        logger.debug("Generating timestamp with format %s", fmt)
        return datetime.now().strftime(fmt)

    @staticmethod
    def sleep(seconds=1):
        """Pause execution for the given number of seconds."""
        if seconds < 0:
            raise ValueError("seconds must be non-negative")
        logger.debug("Sleeping for %s seconds", seconds)
        time.sleep(seconds)

    @staticmethod
    def ensure_dir(path):
        """Create directory if it does not exist."""
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        logger.debug("Ensured directory exists: %s", path)
        return path

    @staticmethod
    def maximize_browser(page):
        """Maximize the browser window in Playwright."""
        if page is None:
            raise ValueError("page cannot be None")
        logger.debug("Maximizing browser viewport")
        page.set_viewport_size({"width": None, "height": None})
