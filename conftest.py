import pytest
from playwright.sync_api import sync_playwright
from config.config import BASE_URL, BROWSER, DASHBOARD_URL, HEADLESS, USERNAME, PASSWORD
from config.global_var import SCREENSHOT_PATH
from pages.login_page import LoginPage


# 🔹 Playwright instance
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


# 🔹 Browser
@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser_type = getattr(playwright_instance, BROWSER)

    browser = browser_type.launch(
        headless=HEADLESS,
        args=["--start-maximized"]
    )

    yield browser
    browser.close()


def _new_context_with_zoom(browser, **kwargs):
    context = browser.new_context(**kwargs)
    context.add_init_script("() => document.body.style.zoom = '0.75'")
    return context


# 🔥 Authenticated Context (BEST PRACTICE)
@pytest.fixture(scope="function")
def page(browser):
    context = _new_context_with_zoom(
        browser,
        viewport={"width": 1920, "height": 1080},
        accept_downloads=True,
    )
    page = context.new_page()

    login = LoginPage(page)
    login.load(BASE_URL)
    login.login(USERNAME, PASSWORD)
    page.wait_for_load_state("networkidle")

    yield page
    page.close()
    context.close()

# 🔹 Screenshot on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            page.screenshot(
                path=f"{SCREENSHOT_PATH}/{item.name}.png",
                full_page=True
            )
            
            
            
@pytest.fixture
def dashboard_page(page):
    from pages.dashboard_page import DashboardPage
    dashboard = DashboardPage(page)
    dashboard.go_to_dashboard(DASHBOARD_URL)
    return dashboard
