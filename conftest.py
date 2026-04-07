import pytest
from playwright.sync_api import sync_playwright
from config.config import BASE_URL, BROWSER, HEADLESS, USERNAME, PASSWORD, DASHBOARD_URL
from config.global_var import DOWNLOADS_PATH, SCREENSHOT_PATH
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
    browser = browser_type.launch(
        headless=HEADLESS,
        args=["--start-maximized"],
        downloads_path=DOWNLOADS_PATH,
        )
    yield browser
    browser.close()

# 🔹 Page (new per test)
@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(
        viewport={'width': 1280, 'height': 720}
    )
    page = context.new_page()
    page.evaluate("document.body.style.zoom = '0.67'")
    yield page
    context.close()
    
@pytest.fixture(scope="function")
def login_page(page):
    login = LoginPage(page)
    login.load(BASE_URL)
    login.login(USERNAME, PASSWORD)

    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    page.locator("text=Dashboard").wait_for(timeout=20000)

    return page 

# 🔹 Login Fixture
@pytest.fixture(scope="function")
def login_page(page):
    login = LoginPage(page)
    login.load(BASE_URL)
    login.login(USERNAME, PASSWORD)

    # page.wait_for_url(DASHBOARD_URL, timeout=15000)
    # page.wait_for_load_state("networkidle")

    page.wait_for_url("**/dashboard**", timeout=20000)
    page.wait_for_load_state("domcontentloaded")
    return page


# 🔹 Screenshot on Failure
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == "call" and report.failed:
#         page = item.funcargs.get("page", None)
#         if page:
#             page.screenshot(path=f"{SCREENSHOT_PATH}/{item.name}.png")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page:
            try:
                # ✅ Fast + no font wait
                page.screenshot(
                    path=f"{SCREENSHOT_PATH}/{item.name}.png",
                    timeout=2000,
                    animations="disabled"
                )
            except Exception as e:
                print("Screenshot failed (ignored):", e)
 
 
                
# @pytest.fixture(scope="function")
# def page(browser):
#     context = browser.new_context(
#         viewport={'width': 1280, 'height': 720}
#     )

#     # 🚀 BLOCK FONTS (PERMANENT FIX)
#     def handle_route(route, request):
#         if request.resource_type == "font":
#             route.abort()
#         else:
#             route.continue_()

#     context.route("**/*", handle_route)

#     page = context.new_page()

#     try:
#         page.evaluate("document.body.style.zoom = '0.67'")
#     except:
#         pass

#     yield page
#     context.close()