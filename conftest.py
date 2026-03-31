import pytest
from playwright.sync_api import sync_playwright
from config.config import BASE_URL, DASHBOARD_URL, BROWSER, HEADLESS, USERNAME, PASSWORD
from pages.dashboard_page import Dashboard
from pages.login_page import LoginPage

# 🔹 Playwright instance
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

# 🔹 Browser (one per session)
@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser_type = getattr(playwright_instance, BROWSER)
    browser = browser_type.launch(headless=HEADLESS)
    yield browser
    browser.close()

# 🔹 Page (new per test)
@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

# 🔹 Login Fixture
@pytest.fixture(scope="function")
def login_page(page):
    login = LoginPage(page)
    login.load(BASE_URL)
    login.login(USERNAME, PASSWORD)

    page.wait_for_load_state("networkidle")

    return page

# 🔹 Dashboard Fixture
@pytest.fixture(scope="function")
def dashboard_page(page):
    dashboard = Dashboard(page)
    dashboard.go_to_dashboard(DASHBOARD_URL)
    return dashboard

# 🔹 Screenshot on Failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)
        if page:
            page.screenshot(path=f"screenshots/{item.name}.png")
