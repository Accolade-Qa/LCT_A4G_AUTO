import pytest
from playwright.sync_api import sync_playwright
from config.config import BASE_URL, BROWSER, DASHBOARD_URL, SIM_DATA_DETAILS_URL,HEADLESS, USERNAME, PASSWORD
from config.global_var import SCREENSHOT_PATH
from pages.login_page import LoginPage

ZOOM_SCRIPT = """
() => {
    const applyZoom = () => {
        const root = document.documentElement;
        if (root) {
            root.style.setProperty('zoom', '0.67', 'important');
        }
        if (document.body) {
            document.body.style.setProperty('zoom', '0.67', 'important');
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
    with sync_playwright() as p:
        yield p


# 🔹 Browser
@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser_type = getattr(playwright_instance, BROWSER)

    browser = browser_type.launch(
        headless=HEADLESS,
        args=["--start-maximized"],
    )

    yield browser
    browser.close()


def _new_context_with_zoom(browser, **kwargs):
    default_viewport = {
        "viewport": {"width": 1920, "height": 1080},
        "screen": {"width": 1920, "height": 1080},
    }
    default_viewport.update(kwargs)
    context = browser.new_context(**default_viewport)
    context.add_init_script(ZOOM_SCRIPT)
    return context


def _apply_zoom_to_page(page):
    page.evaluate(
        """
        () => {
            const root = document.documentElement;
            if (root) {
                root.style.setProperty('zoom', '0.67', 'important');
            }
            if (document.body) {
                document.body.style.setProperty('zoom', '0.67', 'important');
            }
        }
        """
    )


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

@pytest.fixture
def sim_data_details_page(page):
    from pages.sim_data_details_page import SimDataDetailsPage
    sim_data_details = SimDataDetailsPage(page)
    sim_data_details.go_to_simbatchpage(SIM_DATA_DETAILS_URL)
    return sim_data_details
