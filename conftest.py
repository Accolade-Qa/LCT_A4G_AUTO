import importlib
import json
import os
import sys
from pathlib import Path
from config.config import CUSTOMER_MASTER_URL

import pytest
from playwright.sync_api import sync_playwright

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config.config as config_module
from config.global_var import SCREENSHOT_PATH
from pages.base_page import BasePage

os.makedirs(SCREENSHOT_PATH, exist_ok=True)

# Path to cached authenticated storage state to avoid UI login every test
STORAGE_STATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "storage_state.json"
)

from utils.logger import get_logger

logger = get_logger(__name__)

ZOOM_SCRIPT = """
() => {
    const applyZoom = () => {
        const zoomLevel = '1';

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
    browser_type = getattr(playwright_instance, config_module.BROWSER)

    browser = browser_type.launch(
        headless=config_module.HEADLESS,
        args=["--start-maximized", "--kiosk"],
    )
    logger.info(
        "Launched browser instance (%s) headless=%s in fullscreen mode",
        config_module.BROWSER,
        config_module.HEADLESS,
    )

    yield browser
    logger.info("Browser instance closed")


# Context with zoom applied
def _new_context_with_zoom(browser, **kwargs):
    context = browser.new_context(viewport=None)

    context.add_init_script(ZOOM_SCRIPT)
    logger.debug("Created new browser context with zoom applied")
    return context


def pytest_addoption(parser):
    parser.addoption(
        "--iterations",
        action="store",
        default=1,
        type=int,
        help="Number of times to run the loop test",
    )
    parser.addoption(
        "--project",
        action="store",
        default=os.getenv("PROJECT", "lct"),
        help="Project name to select the configuration",
    )


def pytest_configure(config):
    project = config.getoption("--project", os.getenv("PROJECT", "lct")).lower()
    os.environ["PROJECT"] = project
    importlib.reload(config_module)


@pytest.fixture(scope="session")
def project_config():
    return {
        "project": os.getenv("PROJECT", "lct").lower(),
        "base_url": config_module.BASE_URL,
        "username": config_module.USERNAME,
        "password": config_module.PASSWORD,
        "invalid_username": config_module.INVALID_USERNAME,
        "invalid_password": config_module.INVALID_PASSWORD,
        "dashboard_url": config_module.DASHBOARD_URL,
        "sim_data_details_url": config_module.SIM_DATA_DETAILS_URL,
        "role_management_url": config_module.ROLE_MANAGEMENT_URL,
        "role_group_url": config_module.ROLE_GROUP_URL,
        "device_details_url": config_module.DEVICE_DETAILS_URL,
        "ota_url": config_module.OTA_URL,
        "production_page_url": config_module.PRODUCTION_PAGE_URL,
        "create_production_url": config_module.CREATE_PRODUCTION_URL,
        "add_production_url": config_module.ADD_PRODUCTION_URL,
        "user_management_url": config_module.USER_MANAGEMENT_URL,
        "government_servers_url": config_module.GOVERNMENT_SERVERS_URL,
        "dispatched_device_url": config_module.DISPATCHED_DEVICE_URL,
        "profile_url": config_module.PROFILE_URL,
        "model_url": config_module.MODEL_URL,
        "create_new_model": config_module.CREATE_NEW_MODEL,
        "update_model": config_module.UPDATE_MODEL,
        "api_base_url": config_module.API_BASE_URL,
        "page_title": config_module.PAGE_TITLE,
        "imei": config_module.IMEI,
        "browser": config_module.BROWSER,
        "headless": config_module.HEADLESS,
        "video_recording": config_module.VIDEO_RECORDING,
        "screenshot_on_failure": config_module.SCREENSHOT_ON_FAILURE,
        "log_level": config_module.LOG_LEVEL,
        "api_username": config_module.API_USERNAME,
        "api_password": config_module.API_PASSWORD,
    }


@pytest.fixture(scope="session")
def test_data(project_config):
    project = project_config["project"]
    path = Path(__file__).parent / "test_data" / project / "login.json"
    if path.exists():
        with path.open("r", encoding="utf-8") as json_file:
            return json.load(json_file)
    return {}


@pytest.fixture
def login_page(browser):
    context = _new_context_with_zoom(browser, accept_downloads=True)
    page = context.new_page()

    from pages.login_page import LoginPage

    login = LoginPage(page)
    yield login

    page.close()
    context.close()


# Authenticated Page Fixture
@pytest.fixture(scope="function")
def page(browser, project_config):
    context = _new_context_with_zoom(
        browser,
        accept_downloads=True,
    )

    page = context.new_page()
    logger.info("New page opened")

    from pages.login_page import LoginPage

    login = LoginPage(page)
    login.load(project_config["base_url"])
    login.login(project_config["username"], project_config["password"])

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

        if message:
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
def dashboard_page(page, project_config):
    from pages.dashboard_page import DashboardPage

    dashboard = DashboardPage(page)
    dashboard.go_to_dashboard(project_config["dashboard_url"])
    logger.info("Dashboard page fixture ready")
    return dashboard


@pytest.fixture
def sim_data_details_page(page, project_config):
    from pages.sim_data_details_page import SimDataDetailsPage

    sim_data_details = SimDataDetailsPage(page)
    sim_data_details.go_to_simbatchpage(project_config["sim_data_details_url"])
    logger.info("SIM data details fixture ready")
    return sim_data_details


@pytest.fixture
def role_management_page(page, project_config):
    from pages.role_management_page import RoleManagementPage

    role_management = RoleManagementPage(page)
    role_management.go_to_rolemanagementpage(project_config["role_management_url"])
    logger.info("Role Management page fixture ready")
    return role_management


@pytest.fixture
def role_group_page(page, project_config):
    from pages.role_group_page import RoleGroupPage

    role_group = RoleGroupPage(page)
    role_group.go_to_role_group_page(project_config["role_group_url"])
    logger.info("Role Group page fixture ready")
    return role_group


@pytest.fixture
def device_details_page(page, project_config, test_data):
    # Prefer IMEI defined in project-specific test_data, otherwise fall back to project config
    device = test_data.get("valid_imei") or project_config.get(
        "imei", "866677075606341"
    )

    from pages.dashboard_page import DashboardPage
    from pages.device_details_page import DeviceDetailsPage

    base = BasePage(page)
    dashboard = DashboardPage(page)
    device_details = DeviceDetailsPage(page)

    base.navigate_to(project_config["dashboard_url"])

    result = dashboard.search_helper.run_search(device)
    assert result["success"], f"Search failed: {result['error']}"
    assert result["results_found"] == 1

    dashboard.click_on_view_device_in_table(device)

    page.wait_for_url("**/device-details")
    page.wait_for_load_state("networkidle")

    return device_details


@pytest.fixture
def ota_page(page, project_config):
    from pages.ota_page import OtaPage
    from pages.base_page import BasePage

    ota = OtaPage(page)
    base = BasePage(page)

    base.navigate_to(project_config["ota_url"])
    return ota


@pytest.fixture
def dispatched_device_page(page, project_config):
    from pages.dispatched_device_page import DispatchedDevicePage
    from pages.base_page import BasePage

    dispatched_device = DispatchedDevicePage(page)
    base = BasePage(page)
    base.navigate_to(project_config["dispatched_device_url"])
    logger.info("Dispatched Device page fixture ready")
    return dispatched_device


@pytest.fixture
def govt_server_page(page, project_config):
    from pages.govt_server_page import GovtServerPage
    from pages.base_page import BasePage

    govtserver = GovtServerPage(page)
    base = BasePage(page)
    base.navigate_to(project_config["government_servers_url"])

    logger.info("Government Server page ready via UI navigation")

    return govtserver


@pytest.fixture
def profile_page(page, project_config):
    from pages.profile_page import ProfilePage
    from pages.base_page import BasePage

    profile = ProfilePage(page)
    base = BasePage(page)

    base.navigate_to(project_config["profile_url"])

    logger.info("Profile page fixture ready")
    return profile


@pytest.fixture
def customer_master(page):
    from pages.customer_master_page import CustomerMasterPage

    customermaster = CustomerMasterPage(page)
    customermaster.go_to_customer(CUSTOMER_MASTER_URL)
    return customermaster


@pytest.fixture
def user_management(page, project_config):
    from pages.user_management import UserManagementPage

    usermanagement = UserManagementPage(page)
    usermanagement.go_to_user(project_config["user_management_url"])
    return usermanagement


@pytest.fixture
def model_page(page, project_config):
    from pages.model_page import DeviceModel

    model = DeviceModel(page)
    model.go_to_model(project_config["model_url"])
    logger.info("Model page fixture ready")
    return model


@pytest.fixture
def production_devices_page(page, project_config):
    from pages.production_devices_page import ProductionDevices

    production = ProductionDevices(page)
    base = BasePage(page)
    base.navigate_to(project_config["production_page_url"])
    logger.info("Production devices page fixture ready")
    return production


# API Fixtures
@pytest.fixture
def api_context(project_config):
    """Provide API context with credentials for API tests."""
    return {
        "api_base_url": project_config["api_base_url"],
        "api_username": project_config["api_username"],
        "api_password": project_config["api_password"],
    }


@pytest.fixture
def sim_batch_api(page, api_context):
    from pages.api.sim_batch_api import SIMBatchAPI

    return SIMBatchAPI


@pytest.fixture
def customer_api(page, api_context):
    from pages.api.customer_api import CustomerAPI

    return CustomerAPI


@pytest.fixture
def device_dashboard_api(page, api_context):
    from pages.api.device_dashboard_api import DeviceDashboardAPI

    return DeviceDashboardAPI


@pytest.fixture
def login_api_fixture(page, api_context):
    from pages.api.login_api import LoginAPI

    return LoginAPI


@pytest.fixture
def govt_server_api(page, api_context):
    from pages.api.government_server_api import GovtServerAPI

    return GovtServerAPI
