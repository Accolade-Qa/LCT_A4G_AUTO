import logging
import logging
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD, DASHBOARD_URL, BASE_URL
from config.config import USERNAME, PASSWORD, DASHBOARD_URL, BASE_URL
from playwright.sync_api import expect
from utils.excel_report import write_result
from pages.govt_server_page import GovtServerPage
logger = logging.getLogger(__name__)


# def test_login_govt_server(page, request):
#     login_page = LoginPage(page)
#     test_name = request.node.name
#     logger.info(f"Starting test: {test_name}")
#     try:
#         login_page.load(BASE_URL)
#         logger.info(f"Base URL opened: {BASE_URL}")
#         login_page.login(USERNAME, PASSWORD)
#         page.wait_for_load_state("networkidle")
#         expect(page).to_have_url(DASHBOARD_URL)
#         logger.info("Login test PASSED")
#         write_result(
#             test_name,
#             expected=DASHBOARD_URL,
#             actual=page.url,
#             status="PASS"
#         )

#     except Exception as e:
#         logger.error(f"Login test FAILED: {str(e)}")
#         write_result(
#             test_name,
#             expected=DASHBOARD_URL,
#             actual=page.url,
#             status="FAIL",
#             error=str(e)
#         )
#         raise

def test_govt_server_page(page, request):
from pages.govt_server_page import GovtServerPage
logger = logging.getLogger(__name__)


# def test_login_govt_server(page, request):
#     login_page = LoginPage(page)
#     test_name = request.node.name
#     logger.info(f"Starting test: {test_name}")
#     try:
#         login_page.load(BASE_URL)
#         logger.info(f"Base URL opened: {BASE_URL}")
#         login_page.login(USERNAME, PASSWORD)
#         page.wait_for_load_state("networkidle")
#         expect(page).to_have_url(DASHBOARD_URL)
#         logger.info("Login test PASSED")
#         write_result(
#             test_name,
#             expected=DASHBOARD_URL,
#             actual=page.url,
#             status="PASS"
#         )

#     except Exception as e:
#         logger.error(f"Login test FAILED: {str(e)}")
#         write_result(
#             test_name,
#             expected=DASHBOARD_URL,
#             actual=page.url,
#             status="FAIL",
#             error=str(e)
#         )
#         raise

def test_govt_server_page(page, request):
    login_page = LoginPage(page)
    govt_server_page = GovtServerPage(page)

    test_name = request.node.name
    login_page.logger.info(f"Starting test: {test_name}")

    # ❌ REMOVE THIS
    # login_page.login(USERNAME, PASSWORD)

    expected = "DEVICE UTILITY dropdown should be visible"

    try:
        govt_server_page.click_device_utility_tab()

        dropdown = page.locator("ul.dropdown-menu.show")
        dropdown.wait_for(state="visible", timeout=10000)

        assert dropdown.is_visible()

        actual = "DEVICE UTILITY dropdown is visible"
        status = "PASS"

        login_page.logger.info(actual)

    except Exception as e:
        actual = "DEVICE UTILITY dropdown is not visible"
        status = "FAIL"

        login_page.logger.error(f"{actual} | Error: {str(e)}")
        raise

    print(f"{test_name} | Expected: {expected} | Actual: {actual} | Status: {status}")
    
def test_govt_server_page(govt_server_page, request):
    test_name = request.node.name

    expected = "DEVICE UTILITY dropdown should be visible"

    try:
        # Validation (dropdown should already be open or page loaded)
        dropdown = govt_server_page.page.locator("ul.dropdown-menu.show")
        dropdown.wait_for(state="visible", timeout=10000)

        assert dropdown.is_visible()

        actual = "DEVICE UTILITY dropdown is visible"
        status = "PASS"

    except Exception as e:
        actual = "DEVICE UTILITY dropdown is not visible"
        status = "FAIL"
        raise

    print(f"{test_name} | Expected: {expected} | Actual: {actual} | Status: {status}")