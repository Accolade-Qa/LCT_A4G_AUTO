import re
from urllib3 import request
from conftest import page
from pages.login_page import LoginPage
from config.config import PAGE_TITLE, USERNAME, PASSWORD, DASHBOARD_URL, BASE_URL
from playwright.sync_api import expect
from utils.excel_report import write_result

def test_login(page, request):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    print("Base URL:", BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    expected = DASHBOARD_URL
    actual = page.url
    print("Expected URL:", expected)
    print("Actual URL:", actual)
    request.node.expected = expected
    request.node.actual = actual
    assert actual == expected
   


