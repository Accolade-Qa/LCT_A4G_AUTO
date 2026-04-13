import os
import sys
import pytest
from playwright.sync_api import sync_playwright
<<<<<<< HEAD
from config.config import BASE_URL, BROWSER, HEADLESS, USERNAME, PASSWORD,DASHBOARD_URL
from config.global_var import SCREENSHOT_PATH
=======

from datetime import datetime
from config.config import BASE_URL, BROWSER, HEADLESS, USERNAME, PASSWORD, DASHBOARD_URL
from config.global_var import DOWNLOADS_PATH, SCREENSHOT_PATH

from utils.excel_report import write_result
>>>>>>> Shital
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


# 🔹 Browser
@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser_type = getattr(playwright_instance, BROWSER)

    browser = browser_type.launch(
        headless=HEADLESS,
        args=["--start-maximized"]
    )

    yield browser
    # browser.close()

<<<<<<< HEAD

def _new_context_with_zoom(browser, **kwargs):
    context = browser.new_context(**kwargs)
    context.add_init_script("() => document.body.style.zoom = '0.75'")
    return context


# 🔥 Authenticated Context (BEST PRACTICE)
@pytest.fixture(scope="session")
def auth_context(browser):
    context = _new_context_with_zoom(browser, viewport={"width": 1920, "height": 1080})
=======
# 🔹 Page
@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(no_viewport=True)  # 🔹 disables fixed viewport
>>>>>>> Shital
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

<<<<<<< HEAD
    page.locator("text=Dashboard").wait_for(timeout=20000)

    return page 

    login = LoginPage(page)
    login.load(BASE_URL)
    login.login(USERNAME, PASSWORD)

    # page.wait_for_url(DASHBOARD_URL, timeout=15000)
    # page.wait_for_load_state("networkidle")

    # Save login state
    context.storage_state(path="auth.json")
    context.close()

    # Reuse logged-in session
    auth_context = _new_context_with_zoom(
        browser,
        storage_state="auth.json",
        accept_downloads=True,
    )
    yield auth_context
    auth_context.close()

    page.wait_for_url("**/dashboard**", timeout=20000)
    page.wait_for_load_state("domcontentloaded")
    return page

# 🔹 Page per test
@pytest.fixture(scope="function")
def page(auth_context):
    page = auth_context.new_page()
    yield page
    page.close()

# 🔹 Screenshot on Failure
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == "call" and report.failed:
#         page = item.funcargs.get("page", None)
#         if page:
#             page.screenshot(path=f"{SCREENSHOT_PATH}/{item.name}.png")

=======
    return page

@pytest.fixture(scope="session")
def context(browser):
    context = browser.new_context()
    yield context
    # ❌ Do not close context
    
        
>>>>>>> Shital
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

<<<<<<< HEAD
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
=======
        write_result(test_name, expected, actual, status, error)
        
def pytest_sessionfinish(session, exitstatus):
    from utils.excel_report import remove_duplicates  # adjust path
    remove_duplicates()
>>>>>>> Shital
