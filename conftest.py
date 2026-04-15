import os
import sys
import pytest
from playwright.sync_api import sync_playwright
from config.config import (
    BASE_URL,
    BROWSER,
    DASHBOARD_URL,
    ROLE_GROUP_URL,
    ROLE_MANAGEMENT_URL,
    SIM_DATA_DETAILS_URL,
    HEADLESS,
    USERNAME,
    PASSWORD,
)
from config.global_var import SCREENSHOT_PATH
from pages.login_page import LoginPage

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ Ensure folders exist
os.makedirs("reports", exist_ok=True)
os.makedirs(SCREENSHOT_PATH, exist_ok=True)

from utils.logger import get_logger

logger = get_logger(__name__)

# ✅ Single source of truth for page zoom
ZOOM_SCRIPT = """
() => {
    const applyZoom = () => {
        const zoomLevel = '0.8';

        if (document.documentElement) {
            document.documentElement.style.zoom = zoomLevel;
        }

        if (document.body) {
            document.body.style.zoom = zoomLevel;
        }
    };

    applyZoom();

    new MutationObserver(applyZoom).observe(document.documentElement, {
        childList: true,
        subtree: true
    });
}
"""


# 🔹 Playwright instance
@pytest.fixture(scope="session")
def playwright_instance():
    logger.info("Starting Playwright session")
    with sync_playwright() as p:
        yield p
    logger.info("Playwright session ended")


# 🔹 Browser
@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser_type = getattr(playwright_instance, BROWSER)

    browser = browser_type.launch(
        headless=HEADLESS,
        args=["--start-maximized"],
    )
    logger.info("Launched browser instance (%s) headless=%s", BROWSER, HEADLESS)

    yield browser
    logger.info("Browser instance closed")


# 🔹 Context with zoom applied
def _new_context_with_zoom(browser, **kwargs):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        screen={"width": 1920, "height": 1080},
        **kwargs,
    )
    context.add_init_script(ZOOM_SCRIPT)
    logger.debug("Created new browser context with zoom applied")
    return context


# 🔥 Authenticated Page Fixture
@pytest.fixture(scope="function")
def page(browser):
    context = _new_context_with_zoom(
        browser,
        accept_downloads=True,
    )

    page = context.new_page()
    logger.info("New page opened")

    login = LoginPage(page)
    login.load(BASE_URL)
    login.login(USERNAME, PASSWORD)

    page.wait_for_load_state("networkidle")
    logger.info("Authenticated context ready: %s", page.url)

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
            logger.warning("Test %s failed, capturing screenshot", item.name)
            page.screenshot(path=f"{SCREENSHOT_PATH}/{item.name}.png", full_page=True)


# 🔹 Page Fixtures
@pytest.fixture
def dashboard_page(page):
    from pages.dashboard_page import DashboardPage

    dashboard = DashboardPage(page)
    dashboard.go_to_dashboard(DASHBOARD_URL)
    logger.info("Dashboard page fixture ready")
    return dashboard


@pytest.fixture
def sim_data_details_page(page):
    from pages.sim_data_details_page import SimDataDetailsPage

    sim_data_details = SimDataDetailsPage(page)
    sim_data_details.go_to_simbatchpage(SIM_DATA_DETAILS_URL)
    logger.info("SIM data details fixture ready")
    return sim_data_details


@pytest.fixture
def role_management_page(page):
    from pages.role_management_page import RoleManagementPage

    role_management = RoleManagementPage(page)
    role_management.go_to_rolemanagementpage(ROLE_MANAGEMENT_URL)
    logger.info("Role Management page fixture ready")
    return role_management


@pytest.fixture
def role_group_page(page):
    from pages.role_group_page import RoleGroupPage

    role_group = RoleGroupPage(page)
    role_group.go_to_role_group_page(ROLE_GROUP_URL)
    logger.info("Role Group page fixture ready")
    return role_group
