import logging
import re

from pytest_playwright.pytest_playwright import page

from pages.login_page import LoginPage
from utils.excel_report import write_result   # ✅ ADD THIS
from utils.logger import get_logger           # (if using custom logger)
from playwright.async_api import expect
from streamlit import text, title
from pages.base_page import BasePage
from datetime import datetime
from config.config import BASE_URL, PAGE_TITLE, USERNAME, PASSWORD
 
 
class GovtServerPage(BasePage):
 
    def __init__(self, page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)
        
def test_login_govt_server(page):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)

    test_name = "test_login_govt_server"
    try:
        result = login_page.login(USERNAME, PASSWORD)
        expected = "User should login successfully"
        actual = "Login successful" if result else "Login failed"
        status = "PASS" if result else "FAIL"
        write_result(test_name, expected, actual, status)
        assert result, "Login failed ❌"
    except Exception as e:
        write_result(test_name, expected, "ERROR", "FAIL", str(e))
        raise