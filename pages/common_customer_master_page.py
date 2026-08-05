from config.config import CUSTOMER_MASTER_URL
from .common_base_page import BasePage
from utils.logger import get_logger
from utils.helpers import Helpers

logger = get_logger(__name__)


class CustomerMasterPage(BasePage):
    random_new_customer_name = None
    random_updated_customer_name = None

    def __init__(self, page):
        super().__init__(page)

        self.nav_bar_locator = page.locator("ul.nav-list")
        self.page_title_locator = page.locator("span.page-title")
        self.add_customer_locator = page.locator("button:has-text('Add Customer')")
        self.search_field_locator = page.locator("input[formcontrolname='searchInput']")
        self.search_icon_locator = page.locator("button:has(mat-icon:has-text('search'))").first
        self.customer_name_locator = page.locator("input[id='customerName']")
        self.submit_btn_locator = page.locator("button.submit-button")
        self.update_btn_locator = page.locator("button:has-text('Update')")
        self.refresh_btn_locator = page.get_by_text("refresh", exact=True)
        self.view_button_selector = (
            "//table//tbody//tr[1]//button[contains(@class, 'view-button')]"
        )
        self.delete_button_selector = (
            "//table//tbody//tr[1]//button[contains(@class, 'delete-button')]"
        )

    def go_to_customer(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle", timeout=15000)

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
            blur_locator=self.page_title_locator,
            test_cases=test_cases,
        )

    def new_customer(self):
        logger.info("Adding new customer")
        self.add_customer_locator.wait_for(state="visible")
        self.highlight(self.add_customer_locator)
        self.add_customer_locator.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1500)

        CustomerMasterPage.random_new_customer_name = Helpers.generate_random_string(5).upper()
        self.customer_name_locator.wait_for(state="visible", timeout=5000)
        self.customer_name_locator.fill(CustomerMasterPage.random_new_customer_name)
        try:
            self.submit_btn_locator.click(timeout=5000)
        except Exception:
            self.submit_btn_locator.click(force=True)
        self.page.wait_for_load_state("networkidle", timeout=10000)
        logger.debug("New Customer added successfully")

    def search_and_update_customer(self):
        # Search for the newly added customer and update its name
        self.add_customer_locator.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(1500)

        # Refresh the table via the UI refresh button
        self.refresh_btn_locator.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1500)

        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(
            page=self.page,
            input_selector="input[formcontrolname='searchInput']",
            row_selector="tr"
        )
        search_result = search_helper.run_search(CustomerMasterPage.random_new_customer_name)
        assert search_result["success"], f"Search failed: {search_result['error']}"

        # Wait for the searched customer row to appear in the table and click its view button
        customer_row = self.page.locator("tr").filter(has_text=CustomerMasterPage.random_new_customer_name)
        customer_row.wait_for(state="visible", timeout=10000)
        view_button = customer_row.locator("button.view-button")

        # Clear the search field in the DOM and trigger Angular's enter key handler
        # to clear the active search filter, avoiding a 404 on automatic table refresh
        self.search_field_locator.evaluate("""el => {
            el.value = '';
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
            el.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
        }""")

        try:
            view_button.click(timeout=5000)
        except Exception:
            view_button.click(force=True)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1500)
        
        # Wait for the edit/view modal to load customer details before trying to fill the field
        # This prevents a race condition where the GET request overrides our input value
        self.customer_name_locator.wait_for(state="visible", timeout=5000)
        for _ in range(50):
            if self.customer_name_locator.input_value().upper() == CustomerMasterPage.random_new_customer_name:
                break
            self.page.wait_for_timeout(100)

        CustomerMasterPage.random_updated_customer_name = "UPDATE" + Helpers.generate_random_string(5).upper()
        self.customer_name_locator.fill(CustomerMasterPage.random_updated_customer_name)
        try:
            self.update_btn_locator.click(timeout=5000)
        except Exception:
            self.update_btn_locator.click(force=True)
        self.page.wait_for_load_state("networkidle", timeout=10000)
        logger.debug("Customer updated successfully")


    def search_and_delete_customer(self):
        self.add_customer_locator.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(1500)

        # Refresh the table via the UI refresh button
        self.refresh_btn_locator.click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1500)

        from pages.common_utils.search import SearchHelper
        search_helper = SearchHelper(
            page=self.page,
            input_selector="input[formcontrolname='searchInput']",
            row_selector="tr"
        )
        search_result = search_helper.run_search(CustomerMasterPage.random_updated_customer_name)
        assert search_result["success"], f"Search failed: {search_result['error']}"

        # Wait for the searched customer row to appear in the table and click its delete button
        customer_row = self.page.locator("tr").filter(has_text=CustomerMasterPage.random_updated_customer_name)
        customer_row.wait_for(state="visible", timeout=10000)

        # Clear the search field in the DOM and trigger Angular's enter key handler
        # to clear the active search filter, avoiding a 404 on automatic table refresh
        self.search_field_locator.evaluate("""el => {
            el.value = '';
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
            el.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
        }""")

        delete_button = customer_row.locator("button.delete-button")

        self.page.on("dialog", lambda dialog: dialog.accept())
        delete_button.click()

        self.page.wait_for_load_state("networkidle", timeout=10000)
        logger.debug("Customer deleted successfully")

    def get_dashboard_customer_list(self, dashboard_url):
        logger.info("Navigating to Dashboard URL: %s", dashboard_url)
        self.page.goto(dashboard_url)
        self.page.wait_for_load_state("networkidle")
        
        # Target the customer dropdown specifically using placeholders/text to distinguish it from the model dropdown
        dropdown_selectors = [
            "mat-select:has-text('Select Customer')",
            "div.dropdown-placeholder-wrapper:has-text(' Select Customer Name ')",
            "span:has-text('Select Customer')",
            "mat-select:has-text('Customer')",
            "div.dropdown-placeholder-wrapper:has-text('Customer')"
        ]
        
        dropdown = None
        for selector in dropdown_selectors:
            loc = self.page.locator(selector)
            try:
                if loc.count() > 0 and loc.first.is_visible():
                    dropdown = loc.first
                    logger.info("Found customer dropdown on dashboard using selector: %s", selector)
                    break
            except Exception:
                pass
                
        if dropdown:
            dropdown.click()
            self.page.wait_for_timeout(1000)
            tag_name = (dropdown.evaluate("el => el.tagName") or "").lower()
            if "mat-select" in tag_name:
                options = [txt.strip() for txt in self.page.locator("mat-option span").all_inner_texts()]
            else:
                options = [txt.strip() for txt in self.page.locator("div.list-items ul li").all_inner_texts()]
            dropdown.press("Escape")
            return options
        return None

    def get_dispatched_device_customer_lists(self, dispatched_device_url):
        logger.info("Navigating to Dispatched Device URL: %s", dispatched_device_url)
        self.page.goto(dispatched_device_url)
        self.page.wait_for_load_state("networkidle")
        
        from pages.common_dispatched_device_page import DispatchedDevicePage
        dispatched_page = DispatchedDevicePage(self.page)
        
        # Get header dropdown list
        header_customers = dispatched_page.get_customer_list()
        
        # Get manual upload dropdown list
        dispatched_page.click_manual_upload_button()
        self.page.wait_for_timeout(1000)
        manual_customers = dispatched_page.get_customer_list_from_manual_upload()
        
        # Close manual upload modal
        cancel_btn = self.page.locator("button:has-text('Cancel')").first
        if cancel_btn.is_visible():
            cancel_btn.click()
        else:
            self.page.keyboard.press("Escape")
            
        return {
            "header": [c.strip() for c in header_customers],
            "manual": [c.strip() for c in manual_customers]
        }
