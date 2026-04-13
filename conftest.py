import os
import sys
import pytest
from playwright.sync_api import sync_playwright

from datetime import datetime
from config.config import BASE_URL, BROWSER, HEADLESS, USERNAME, PASSWORD, DASHBOARD_URL
from config.global_var import DOWNLOADS_PATH, SCREENSHOT_PATH

from utils.excel_report import write_result
from pages.login_page import LoginPage
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ Ensure folders exist
os.makedirs("reports", exist_ok=True)
os.makedirs(SCREENSHOT_PATH, exist_ok=True)

# 🔹 Playwright instance
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

# 🔹 Browser (one per session)
@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser_type = getattr(playwright_instance, BROWSER)
    browser = browser_type.launch(
        headless=HEADLESS,
        args=["--start-maximized"],
        downloads_path=DOWNLOADS_PATH,
        )
    yield browser
    # browser.close()

# 🔹 Page
@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(no_viewport=True)  # 🔹 disables fixed viewport
    page = context.new_page()
    page.goto("about:blank")  # optional
    yield page
    context.close()
    
@pytest.fixture(scope="function")
def login_page(page):
    login = LoginPage(page)
    login.load(BASE_URL)
    login.login(USERNAME, PASSWORD)

    page.wait_for_url(DASHBOARD_URL, timeout=20000)
    page.wait_for_load_state("domcontentloaded")

    return page

@pytest.fixture(scope="session")
def context(browser):
    context = browser.new_context()
    yield context
    # ❌ Do not close context
    
        
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        test_name = item.name
        # Get actual & expected if stored
        expected = getattr(item, "expected", "N/A")
        actual = getattr(item, "actual", "N/A")
        if report.passed:
            status = "PASS"
            error = ""
        else:
            status = "FAIL"
            error = str(report.longrepr)

        write_result(test_name, expected, actual, status, error)
        
def pytest_sessionfinish(session, exitstatus):
    from utils.excel_report import remove_duplicates  # adjust path
    remove_duplicates()