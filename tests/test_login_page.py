from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD, DASHBOARD_URL, BASE_URL,INVALID_PASSWORD,INVALID_USERNAME
from playwright.sync_api import expect
 
# 🔹 Test 1: Valid Login
def test_login(page):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    print(BASE_URL)  
    login_page.login(USERNAME, PASSWORD)
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(DASHBOARD_URL)   # ✅ FIX    
   
def test_invalid_login(page):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    # 🔹 Call method
    error_msg = login_page.login_with_invalid_credentials(INVALID_USERNAME,INVALID_PASSWORD)
    print("Error Message:", error_msg)
    # 🔹 Validate error message
    assert "Minimum 6 characters required" in error_msg
 
def test_username(page):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    # 🔹 Call method
    error_msg = login_page.login_with_usernameonly(USERNAME)
    print("Error Message:", error_msg)
    # 🔹 Validate error message
    assert " " in error_msg
 
def test_password(page):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    # 🔹 Call method
    error_msg = login_page.login_with_passwordameonly(PASSWORD)
    print("Error Message:", error_msg)
    # 🔹 Validate error message
    assert " " in error_msg
    
def test_page_title(page):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    login_page.verify_page_title()
    
def test_page_title(page):
    login_page = LoginPage(page)
    login_page.load(BASE_URL)
    login_page.verify_page_title()   # uses default PAGE_TITLE