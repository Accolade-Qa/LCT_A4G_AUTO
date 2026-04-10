import pytest
from playwright.sync_api import sync_playwright
from config.config import BASE_URL, BROWSER, DASHBOARD_URL, SIM_DATA_DETAILS_URL,HEADLESS, USERNAME, PASSWORD
from config.global_var import SCREENSHOT_PATH
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)

ZOOM_SCRIPT = """
() => {
    const applyZoom = () => {
        const root = document.documentElement;
        if (root) {
            root.style.setProperty('zoom', '0.9', 'important');
        }
        if (document.body) {
            document.body.style.setProperty('zoom', '0.9', 'important');
        }
    };
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        applyZoom();
    } else {
        document.addEventListener('DOMContentLoaded', applyZoom, { once: true });
    }
    const observer = new MutationObserver(() => applyZoom());
    if (document.documentElement) {
        observer.observe(document.documentElement, { childList: true, subtree: true });
    }
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
    browser.close()
    logger.info("Browser instance closed")


def _new_context_with_zoom(browser, **kwargs):
    default_viewport = {
        "viewport": {"width": 1920, "height": 1080},
        "screen": {"width": 1920, "height": 1080},
    }
    default_viewport.update(kwargs)
    context = browser.new_context(**default_viewport)
    context.add_init_script(ZOOM_SCRIPT)
    logger.debug("Created new browser context with viewport=%s", default_viewport)
    return context


def _apply_zoom_to_page(page):
    page.evaluate(
        """
        () => {
            const root = document.documentElement;
            if (root) {
                root.style.setProperty('zoom', '0.80', 'important');
            }
            if (document.body) {
                document.body.style.setProperty('zoom', '0.80', 'important');
            }
        }
        """
    )
    logger.debug("Applied DOM zoom to page %s", page.url)


# 🔥 Authenticated Context (BEST PRACTICE)
@pytest.fixture(scope="function")
def page(browser):
    context = _new_context_with_zoom(
        browser,
        accept_downloads=True,
    )
    page = context.new_page()
    _apply_zoom_to_page(page)
    page.on("load", lambda _: _apply_zoom_to_page(page))
    page.on("framenavigated", lambda _: _apply_zoom_to_page(page))
    logger.info("New page opened and zoom applied")

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
            page.screenshot(
                path=f"{SCREENSHOT_PATH}/{item.name}.png",
                full_page=True
            )
            
            
            
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
