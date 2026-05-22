import os
import sys
import pytest
from playwright.sync_api import sync_playwright
from config.config import (
    BASE_URL,
    DISPATCHED_DEVICE_URL,
    IMEI,
    BROWSER,
    DASHBOARD_URL,
    PROFILE_URL,
    ROLE_GROUP_URL,
    ROLE_MANAGEMENT_URL,
    GOVERNMENT_SERVERS_URL,
    SIM_DATA_DETAILS_URL,
    OTA_URL,
    HEADLESS,
    USERNAME,
    PASSWORD,
)
from config.global_var import SCREENSHOT_PATH
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.device_details_page import DeviceDetailsPage
from pages.login_page import LoginPage

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.makedirs("reports", exist_ok=True)
os.makedirs(SCREENSHOT_PATH, exist_ok=True)

from utils.logger import get_logger

logger = get_logger(__name__)

ZOOM_SCRIPT = """
() => {
    const applyZoom = () => {
        const zoomLevel = '0.75';

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


# Playwright instance
@pytest.fixture(scope="session")
def playwright_instance():
    logger.info("Starting Playwright session")
    with sync_playwright() as p:
        yield p
    logger.info("Playwright session ended")


# Browser
@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser_type = getattr(playwright_instance, BROWSER)

    browser = browser_type.launch(
        headless=HEADLESS,
        args=["--start-maximized", "--kiosk"],
    )
    logger.info(
        "Launched browser instance (%s) headless=%s in fullscreen mode",
        BROWSER,
        HEADLESS,
    )

    yield browser
    logger.info("Browser instance closed")


# Context with zoom applied
def _new_context_with_zoom(browser, **kwargs):
    context = browser.new_context(viewport=None)
    context.add_init_script(ZOOM_SCRIPT)
    logger.debug("Created new browser context with zoom applied")
    return context


# Authenticated Page Fixture
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


@pytest.fixture
def report_case(record_property):
    def _report_case(expected="", actual="", result="", message=""):
        # Always record properties, even if empty, to ensure they're in the report
        record_property("expected", str(expected) if expected != "" else "")
        record_property("actual", str(actual) if actual != "" else "")
        if result:
            record_property("result", result)
        if message:
            record_property("message", message)

    return _report_case


# Screenshot on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call":
        existing_properties = {name for name, _ in item.user_properties}

        # 🔹 Extract expected from docstring or test name
        expected = (getattr(item.function, "__doc__", "") or "").strip()
        if not expected:
            expected = item.name.strip()

        # 🔹 Extract actual based on test outcome
        if report.passed:
            actual = "Test passed"
        elif report.skipped:
            actual = "Test skipped"
        else:
            # For failed tests, use the failure reason
            actual = str(report.longrepr) if report.longrepr else "Test failed"

        # 🔹 Only add default properties if they weren't explicitly set by report_case
        if "expected" not in existing_properties and expected:
            item.user_properties.append(("expected", expected))
        if "actual" not in existing_properties and actual:
            item.user_properties.append(("actual", actual))
        if "result" not in existing_properties:
            item.user_properties.append(("result", report.outcome))

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            logger.warning("Test %s failed, capturing screenshot", item.name)
            page.screenshot(path=f"{SCREENSHOT_PATH}/{item.name}.png", full_page=True)


# Page Fixtures
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


@pytest.fixture
def device_details_page(page):
    device = IMEI

    base = BasePage(page)
    dashboard = DashboardPage(page)
    device_details = DeviceDetailsPage(page)

    base.navigate_to(DASHBOARD_URL)

    result = dashboard.search_helper.run_search(device)
    assert result["success"], f"Search failed: {result['error']}"
    assert result["results_found"] == 1

    dashboard.click_on_view_device_in_table(device)

    page.wait_for_url("**/device-details")
    page.wait_for_load_state("networkidle")

    return device_details


@pytest.fixture
def ota_page(page):
    from pages.ota_page import OtaPage
    from pages.base_page import BasePage

    ota = OtaPage(page)
    base = BasePage(page)

    base.navigate_to(OTA_URL)
    return ota


@pytest.fixture
def dispatched_device_page(page):
    from pages.dispatched_device_page import DispatchedDevicePage
    from pages.base_page import BasePage

    dispatched_device = DispatchedDevicePage(page)
    base = BasePage(page)
    base.navigate_to(DISPATCHED_DEVICE_URL)
    logger.info("Dispatched Device page fixture ready")
    return dispatched_device


@pytest.fixture
def govt_server_page(page):
    from pages.govt_server_page import GovtServerPage
    from pages.base_page import BasePage

    govtserver = GovtServerPage(page)
    base = BasePage(page)
    base.navigate_to(GOVERNMENT_SERVERS_URL)

    logger.info("Government Server page ready via UI navigation")

    return govtserver


@pytest.fixture
def profile_page(page):
    from pages.profile_page import ProfilePage
    from pages.base_page import BasePage

    profile = ProfilePage(page)
    base = BasePage(page)

    base.navigate_to(PROFILE_URL)

    logger.info("Profile page fixture ready")
    return profile
