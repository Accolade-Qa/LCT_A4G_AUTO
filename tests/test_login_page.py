import re
from urllib3 import request
from conftest import page
from pages.login_page import LoginPage
from config.config import PAGE_TITLE, USERNAME, PASSWORD, DASHBOARD_URL, BASE_URL,INVALID_PASSWORD,INVALID_USERNAME
from playwright.sync_api import expect
from utils.excel_report import write_result

def test_login(page, request):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    print("Base URL:", BASE_URL)
    login_page.login(USERNAME, PASSWORD)
    expected = DASHBOARD_URL
    actual = page.url
    print("Expected URL:", expected)
    print("Actual URL:", actual)
    request.node.expected = expected
    request.node.actual = actual
    assert actual == expected

def test_invalid_login(page):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    actual_msg = login_page.login_with_invalid_credentials(INVALID_USERNAME, INVALID_PASSWORD).strip().lower().rstrip(".")
    expected_msg = "Minimum 6 characters required".strip().lower().rstrip(".")
    print("Expected Error Message:", expected_msg)
    print("Actual Error Message:", actual_msg)
    status = "PASS" if actual_msg == expected_msg else "FAIL"
    write_result("test_invalid_login", expected_msg, actual_msg, status)
    assert actual_msg == expected_msg
 
def test_username(page):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    error_msg = login_page.login_with_usernameonly(USERNAME)
    assert error_msg != "", "Error message is empty ❌"
    expected_msg = "minimum 6 characters required"
    actual = error_msg.strip().lower().rstrip(".")
    expected = expected_msg.strip().lower().rstrip(".")
    print("Expected Error Message:", expected)
    print("Actual Error Message:", actual)
    status = "PASS" if actual == expected else "FAIL"
    write_result("test_username", expected, actual, status)
    assert actual == expected, f"Expected: {expected}, Got: {actual}"

def test_password(page):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    try:
        error_msg = login_page.login_with_passwordonly(" ",PASSWORD)
        print("Error Message:", error_msg)
        assert error_msg != "", "Error message is empty ❌"
        expected_msg = "This field is required and can't be only spaces."   # 🔥 update as per your UI
        actual = error_msg.strip().lower().rstrip(".")
        expected = expected_msg.strip().lower().rstrip(".")
        print("Expected:", expected)
        print("Actual:", actual)
        status = "PASS" if actual == expected else "FAIL"
        # ✅ ONLY ONE ENTRY WILL BE WRITTEN
        write_result("test_password", expected, actual, status)
        assert actual == expected, f"Expected: {expected}, Got: {actual}"
    except Exception as e:
        write_result("test_password", "Username error expected", "Failed", "FAIL", str(e))
        raise
       
def test_page_title(page,request):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    test_name = request.node.name
    try:
        expected = PAGE_TITLE
        actual = login_page.verify_page_title(expected)
        # Normalize
        actual_norm = actual.strip().lower()
        expected_norm = expected.strip().lower()
        status = "PASS" if actual_norm == expected_norm else "FAIL"
        print("Expected:", expected_norm)
        print("Actual:", actual_norm)
        write_result(test_name, expected, actual, status)
        assert actual_norm == expected_norm, f"Expected: {expected}, Got: {actual}"
    except Exception as e:
        write_result(test_name, expected, "ERROR", "FAIL", str(e))
        raise

def test_longusername_password(page, request):
    login_page = LoginPage(page)
    test_name = request.node.name
    expected_list = ["Please enter a valid Email ID.","Minimum 6 characters required."]
    login_page.logger.info(f"Starting test: {test_name}")
    login_page.load(BASE_URL)
    login_page.login("shital", "ABCD")
    errors = login_page.get_error_message()
    print("Errors:", errors)
    actual = ", ".join(errors) if errors else "No error message"
    expected = ", ".join(expected_list)
    try:
        # ✅ Correct validation
        assert all(
            any(exp.lower() in e.lower() for e in errors)
            for exp in expected_list
        )
        status = "PASS"
        login_page.logger.info(
            f"Test Passed | Expected: {expected} | Actual: {actual}"
        )
    except AssertionError:
        status = "FAIL"
        login_page.logger.error(
            f"Test Failed | Expected: {expected} | Actual: {actual}"
        )
    write_result(test_name, expected, actual, status)
    
def test_shortusername_password(page, request):
    login_page = LoginPage(page)
    test_name = request.node.name
    expected_list = ["Please enter a valid Email ID.","Minimum 6 characters required."]
    login_page.logger.info(f"Starting test: {test_name}")
    login_page.load(BASE_URL)
    login_page.login("shital", "ABCD")
    errors = login_page.get_error_message()
    print("Errors:", errors)
    actual = ", ".join(errors) if errors else "No error message"
    expected = ", ".join(expected_list)
    try:
        # ✅ Correct validation
        assert all(
            any(exp.lower() in e.lower() for e in errors)
            for exp in expected_list
        )
        status = "PASS"
        login_page.logger.info(
            f"Test Passed | Expected: {expected} | Actual: {actual}"
        )
    except AssertionError:
        status = "FAIL"
        login_page.logger.error(
            f"Test Failed | Expected: {expected} | Actual: {actual}"
        )
    write_result(test_name, expected, actual, status)

        
#     # 🔹 Footer Tests
#     # 🔹 Test: Footer links present
def test_footer_links(page, request):
    login_page = LoginPage(page)
    test_name = request.node.name
    login_page.logger.info(f"Starting test: {test_name}")
    login_page.load(BASE_URL)
    # ✅ Define expected links (update as per your UI)
    expected_links = ["Accolade Electronics Pvt. Ltd."]
    # ✅ Get actual links
    links = login_page.verify_footer_links_present()
    actual = ", ".join(links) if links else "No links found"
    expected = ", ".join(expected_links)
    try:
        # ✅ Validate all expected links are present
        assert all(
            any(exp.lower() in link.lower() for link in links)
            for exp in expected_links
        )
        status = "PASS"
        login_page.logger.info(
            f"Test Passed | Expected: {expected} | Actual: {actual}"
        )
    except AssertionError:
        status = "FAIL"
        login_page.logger.error(
            f"Test Failed | Expected: {expected} | Actual: {actual}"
        )
    # ✅ Write to Excel
    write_result(test_name, expected, actual, status)
    
def test_footer_links_clickable(page, request):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    test_name = request.node.name
    try:
        results = login_page.verify_footer_links_clickable()
        # Check if all clickable
        all_clickable = all(link["clickable"] for link in results)
        actual = ", ".join(
            [f'{link["text"]}: {link["clickable"]}' for link in results]
        )
        expected = "All footer links should be clickable"
        status = "PASS" if all_clickable else "FAIL"
        write_result(test_name, expected, actual, status)
        assert all_clickable, "Some footer links are not clickable"
    except Exception as e:
        write_result(test_name, "All footer links clickable", "ERROR", "FAIL", str(e))
        raise

def test_footer_year(page, request):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    test_name = request.node.name
    try:
        footer_text, current_year = login_page.verify_footer_year()
        actual = footer_text
        expected = f"Footer should contain year {current_year}"
        status = "PASS" if current_year in footer_text else "FAIL"
        write_result(test_name, expected, actual, status)
        assert current_year in footer_text, f"Year {current_year} not found in footer"
    except Exception as e:
        write_result(test_name, "Footer year validation", "ERROR", "FAIL", str(e))
        raise

def test_get_build_version(page):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    test_name = "test_get_build_version"
    try:
        version = login_page.get_build_version()
        expected = "Build version should be in format X.Y.Z"
        # ✅ Validations
        not_empty = version is not None and version != ""
        valid_format = bool(re.search(r"\d+\.\d+\.\d+", version))
        status = "PASS" if (not_empty and valid_format) else "FAIL"
        actual = version
        print("Build Version:", version)
        write_result(test_name, expected, actual, status)
        assert not_empty, "Build version is empty ❌"
        assert valid_format, f"Invalid version format: {version}"
    except Exception as e:
        write_result(test_name, expected, "ERROR", "FAIL", str(e))
        raise
    
