import pytest
from playwright.sync_api import sync_playwright
from config.config import BASE_URL, BROWSER, HEADLESS, USERNAME, PASSWORD
from config.global_var import DOWNLOADS_PATH, SCREENSHOT_PATH
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser_type = getattr(playwright_instance, BROWSER)
    browser = browser_type.launch(
        headless=HEADLESS,
        args=["--start-maximized"],
        downloads_path=DOWNLOADS_PATH,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def login_page(page):
    login = LoginPage(page)
    login.load(BASE_URL)
    login.login(USERNAME, PASSWORD)
    page.wait_for_load_state("networkidle")
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)
        if page:
            page.screenshot(path=f"{SCREENSHOT_PATH}/{item.name}.png")
