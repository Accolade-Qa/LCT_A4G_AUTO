import re

from playwright.async_api import expect
from streamlit import title
# from conftest import page
from pages.base_page import BasePage
from config.config import BASE_URL, PAGE_TITLE, USERNAME, PASSWORD,INVALID_USERNAME,INVALID_PASSWORD
 
class LoginPage(BasePage):
 
    def __init__(self, page):
        super().__init__(page)
 
        # ✅ Enable locators
        self.username = page.get_by_placeholder("Your Email Address")
        self.password = page.get_by_placeholder("Password")
        self.login_btn = page.get_by_role("button", name=re.compile(r"Sign in", re.IGNORECASE))
        self.errormsg = page.get_by_text("Minimum 6 characters required.")
        self.wrongusername = page.locator("//div[@class='cdk-overlay-container']")
        self.emptyusername = page.locator("//mat-error[@id='mat-mdc-error-1']")
        self.page_title1 = page.locator("div.site-name-text-section:visible")
 
    # 🔹 Open Login Page
    def load(self, url=BASE_URL):
        self.page.goto(url, timeout=60000)
        self.page.wait_for_load_state("domcontentloaded")
 
    # 🔹New Method 1: Perform Login
    def login(self, username=USERNAME, password=PASSWORD):
        self.username.fill(username)
        self.password.fill(password)
        self.login_btn.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_url(DASHBOARD_URL, timeout=60000)
 
# 🔹 New Method 2: Invalid Login Method
    def login_with_invalid_credentials(self, username=INVALID_USERNAME, password=INVALID_PASSWORD):
            self.username.fill(username)
            self.password.fill(password)
            self.login_btn.click()
    # 🔹 Wait for error message
            self.errormsg.wait_for(state="visible", timeout=5000)
            return self.errormsg.text_content()
 
#  🔹 New Method 3: Login with username
    def login_with_usernameonly(self, username = USERNAME):
        self.username.fill(username)
        self.login_btn.click()
        # 🔹 Wait for error message
        self.wrongusername.wait_for(state="visible", timeout=5000)
        return self.wrongusername.text_content()
   
    #  🔹 New Method 4: Login with password
    def login_with_passwordameonly(self, password = PASSWORD):
        self.password.fill(password)
        self.login_btn.click()
        # 🔹 Wait for error message
        self.wrongusername.wait_for(state="visible", timeout=5000)
        return self.wrongusername.text_content()
    
  # 🔹 Verify Page Title
    def verify_page_title(self, name=PAGE_TITLE):
        self.page.wait_for_load_state("load")   # ✅ ensure page is loaded
        title = self.get_page_title()           # ✅ calling BasePage method
        print("Page Title:", title)
