from config.config import CUSTOMER_MASTER_URL
from .base_page import BasePage
from utils.logger import get_logger
from .common.table_section import TableSection

logger = get_logger(__name__)


class CustomerMasterPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.nav_bar_locator = page.locator("ul.nav-list")
        self.page_title_locator = page.get_by_text("Customer Management", exact=True)
        self.add_customer_locator = page.get_by_text(
            "Add Customer open_in_new", exact=True
        )
        self.search_field_locator = page.get_by_placeholder(
            "Search and Press Enter", exact=True
        )
        self.search_icon_locator = page.get_by_text("search", exact=True)
        self.customer_name_locator = page.get_by_placeholder(
            "Customer Name", exact=True
        )
        self.submit_btn_locator = page.get_by_role("button")
        self.refresh_btn_locator = page.get_by_text("refresh", exact=True)
        self.view_icon = page.locator(
            "//button[@class='primary-button view-button ng-star-inserted']"
        ).first
        self.delete_icon = page.locator(
            "//button[@class='primary-button delete-button ng-star-inserted']"
        ).first

    def go_to_customer(self, url):
        self.page.goto(url)

    def _nav_list_enability(self):

        logger.info("Checking navigation bar enable state")
        self.nav_bar_locator.wait_for(state="visible")
        self.highlight(self.nav_bar_locator)
        is_enabled = self.nav_bar_locator.is_enabled()
        logger.debug("Navigation bar enabled status: %s", is_enabled)
        return is_enabled

    def _is_PageTitle_Visible(self):
        self.page.goto(CUSTOMER_MASTER_URL)
        logger.info("Checking the visibility of the page title")
        self.page_title_locator.wait_for(state="visible")
        self.highlight(self.page_title_locator)
        logger.debug("Page title is visible: %s", self.page_title_locator.is_visible())
        return self.page_title_locator.is_visible()

    def _element_enability(self):

        logger.info("Checking enability of elements")
        self.add_customer_locator.wait_for(state="visible")
        self.highlight(self.add_customer_locator)

        self.search_field_locator.wait_for(state="visible")
        self.highlight(self.search_field_locator)

        self.search_icon_locator.wait_for(state="visible")
        self.highlight(self.search_icon_locator)

        is_enabled = (
            self.add_customer_locator.is_enabled()
            and self.search_field_locator.is_enabled()
            and self.search_icon_locator.is_enabled()
        )

        logger.debug("Elements enable status: %s", is_enabled)

        return is_enabled

    def _click_add_customer(self):
        logger.info("Clicking on Add Customer button")
        self.add_customer_locator.wait_for(state="visible")
        self.highlight(self.add_customer_locator)
        self.add_customer_locator.click()
        logger.debug("Clicked on Add Customer button")
        self.customer_name_locator.wait_for(state="visible", timeout=5000)

    def get_visible_error(self):

        error_locator = self.page.locator("mat-error:visible")

        error_locator.wait_for(state="visible", timeout=5000)

        return error_locator.text_content().strip()

    def validate_field(self, field_locator, blur_locator, test_cases, open_form=True):

        results = {}

        # Open modal/form once
        if open_form:
            self.add_customer_locator.wait_for(state="visible")
            self.highlight(self.add_customer_locator)
            self.add_customer_locator.click()

        for input_value, result_key in test_cases.items():

            # Optional reset
            self.refresh_btn_locator.click()

            # Wait for field
            field_locator.wait_for(state="visible", timeout=5000)

            # Clear old value
            field_locator.fill("")

            # Fill test value
            field_locator.fill(input_value)

            # Trigger blur validation
            blur_locator.click()

            # Capture error
            error_text = self.get_visible_error()

            results[result_key] = error_text

            print(f"{result_key}: {repr(error_text)}")

        return results

    def customer_name_field(self):
        logger.info("Validating customer name field with various test cases")
        test_cases = {
            "": "name_blank_text",
            "123": "name_num_text",
            "!@#$": "name_sp_char_text",
            " ": "name_space_text",
            "abc ": "name_char_space_text",
        }

        return self.validate_field(
            field_locator=self.page.get_by_placeholder("Customer Name", exact=True),
            blur_locator=self.page.get_by_text("Add Customer", exact=True),
            test_cases=test_cases,
        )

    def new_customer(self):

        logger.info("Adding new customer")
        self.add_customer_locator.wait_for(state="visible")
        self.highlight(self.add_customer_locator)
        self.add_customer_locator.click()

        self.customer_name_locator.fill("Test Customer")
        self.submit_btn_locator.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)
        logger.debug("New Customer added successfully")

    def search_and_update_customer(self):

        logger.info("Searching and updating customer")
        self.search_field_locator.fill("Test Customer")
        self.search_icon_locator.click()
        self.view_icon.wait_for(state="visible", timeout=5000)
        self.view_icon.click()
        self.customer_name_locator.wait_for(state="visible", timeout=5000)
        self.customer_name_locator.fill("Update Customer")
        self.submit_btn_locator.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)
        logger.debug("Customer updated successfully")

    def search_and_delete_customer(self):

        logger.info("Searching and deleting customer")
        self.search_field_locator.fill("Update Customer")
        self.search_icon_locator.click()
        self.delete_icon.wait_for(state="visible", timeout=5000)
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.delete_icon.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)
        logger.debug("Customer deleted successfully")
