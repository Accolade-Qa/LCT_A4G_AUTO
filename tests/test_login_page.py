from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD, DASHBOARD_URL, BASE_URL, INVALID_PASSWORD, INVALID_USERNAME
from playwright.sync_api import expect
from utils.logger import get_logger

logger = get_logger(__name__)


class TestLoginPage:
    def test_login(self, page):
        logger.info("Starting valid login test for %s", USERNAME)
        login_page = LoginPage(page)
        login_page.load(BASE_URL)
        login_page.login(USERNAME, PASSWORD)
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(DASHBOARD_URL)

    def test_invalid_login(self, page):
        logger.info("Starting invalid login test")
        login_page = LoginPage(page)
        login_page.load(BASE_URL)
        error_msg = login_page.login_with_invalid_credentials(INVALID_USERNAME, INVALID_PASSWORD)
        logger.info("Invalid login error: %s", error_msg)
        assert "Minimum 6 characters required" in error_msg

    def test_username(self, page):
        logger.info("Starting username-only login validation")
        login_page = LoginPage(page)
        login_page.load(BASE_URL)
        error_msg = login_page.login_with_usernameonly(USERNAME)
        logger.info("Username-only login error: %s", error_msg)
        assert " " in error_msg

    def test_password(self, page):
        logger.info("Starting password-only login validation")
        login_page = LoginPage(page)
        login_page.load(BASE_URL)
        error_msg = login_page.login_with_passwordonly(PASSWORD)
        logger.info("Password-only login error: %s", error_msg)
        assert " " in error_msg
