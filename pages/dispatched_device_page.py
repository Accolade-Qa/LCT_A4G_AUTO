import os

from click import Path

from config.global_var import DOWNLOADS_PATH
from utils.logger import get_logger
from pages.common.table_section import TableSection
from pages.base_page import BasePage

logger = get_logger(__name__)


class DispatchedDevicePage:
    def __init__(self, page):
        logger.debug("Initializing Dispatched Devices Page with page object")
        self.page = page
        logger.info("DispatchedDevicePage initialized successfully")

    def go_to_dispatcheddevicepage(self, url):
        logger.info("Navigating to Dispatched Device page: %s", url)
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        logger.info("Navigation to Dispatched Device page completed: %s", url)

    def is_page_loaded(self):
        logger.debug("Checking if Dispatched Device page is loaded")
        return self.page.url.endswith("/dispatched-devices")

    def is_manual_upload_button_visible(self):
        logger.debug("Checking visibility of Manual Upload button")
        manual_upload = self.page.locator("//div[@class='page-header']//button[1]")
        return manual_upload.is_visible()

    def is_bulk_upload_button_visible(self):
        logger.debug("Checking visibility of Bulk Upload button")
        bulk_upload = self.page.locator("//div[@class='page-header']//button[2]")
        return bulk_upload.is_visible()

    def is_checkbox_visible(self):
        logger.debug("Checking visibility of checkbox in Dispatched Device page")
        checkbox = self.page.locator("span:has-text('Select Customer')")
        return checkbox.is_visible()

    def is_view_actions_button_visible(self):
        logger.debug("Checking visibility of View Actions button")
        view_actions = (
            self.page.locator("mat-icon").filter(has_text="visibility").last()
        )
        return view_actions.is_visible()

    def is_delete_action_button_visible(self):
        logger.debug("Checking visibility of Delete Action button")
        delete_action = self.page.locator("mat-icon").filter(has_text="delete").last()
        return delete_action.is_visible()

    def is_dispatched_device_table_visible(self):
        logger.debug("Checking visibility of Dispatched Device table")
        table = self.page.locator("//div[@class='component-body']")
        return table.is_visible()

    def is_search_box_visible(self):
        logger.debug("Checking visibility of Search box")
        search_box = self.page.get_by_placeholder("Search and Press Enter")
        return search_box.is_visible()

    def get_table_headers(self):
        logger.debug("Retrieving table headers from Dispatched Device page")
        table = TableSection(self.page)
        headers = table.get_headers()
        logger.info("Table headers retrieved: %s", headers)
        return headers

    def get_customer_list(self):
        logger.debug("Retrieving customer list from Select Customer dropdown")
        dropdown = self.page.locator("div.dropdown-placeholder-wrapper")
        dropdown.click()
        options = self.page.locator("div.list-items ul li").all_inner_texts()
        dropdown.press("Escape")
        logger.info("Customer list retrieved: %s", options)
        return options

    def get_customer_list_from_manual_upload(self):
        logger.debug(
            "Retrieving customer list from Select Customer dropdown in Manual Upload form"
        )
        dropdown = self.page.locator("mat-select[role='combobox']")
        dropdown.click()
        options = self.page.locator("mat-option span").all_inner_texts()
        dropdown.press("Escape")
        logger.info("Customer list retrieved from Manual Upload form: %s", options)
        return options

    def select_customer(self, customer_name):
        logger.debug("Selecting customer '%s' from dropdown", customer_name)
        dropdown = self.page.locator("mat-select[role='combobox']")
        dropdown.click()
        option = self.page.locator(f"mat-option span:has-text('{customer_name}')")
        option.click()
        logger.info("Customer '%s' selected from dropdown", customer_name)

    def select_customer_dispatched_device_page(self, customer_name):
        logger.debug(
            "Selecting customer '%s' from dropdown on dispatched device page",
            customer_name,
        )
        dropdown = self.page.locator("div.dropdown-placeholder-wrapper")
        dropdown.click()
        option = self.page.locator(f"div.list-items ul li:has-text('{customer_name}')")
        option.click()
        logger.info(
            "Customer '%s' selected from dropdown on dispatched device page",
            customer_name,
        )

    def is_select_customer_dropdown_visible(self):
        logger.debug("Checking visibility of Select Customer dropdown")
        dropdown = self.page.locator("mat-select[role='combobox']")
        return dropdown.is_visible()

    def click_manual_upload_button(self):
        logger.debug("Clicking Manual Upload button")
        manual_upload = self.page.locator("//div[@class='page-header']//button[1]")
        manual_upload.click()
        logger.info("Manual Upload button clicked")

    def get_manual_upload_page_title(self):
        base = BasePage(self.page)
        logger.debug("Retrieving Manual Upload page title")
        title = base.get_title()
        logger.info("Manual Upload page title retrieved: %s", title)
        return title

    def fill_uid_input(self, value):
        logger.debug("Filling UID input field with value: %s", value)
        uid_input = self.page.locator("input[id='uid']")
        uid_input.clear()
        uid_input.fill(value)
        logger.info("UID input field filled with value: %s", value)

    def clear_uid_input_and_click(self):
        logger.debug("Clearing UID input field")
        uid_input = self.page.locator("input[id='uid']")
        uid_input.clear()
        uid_input.click()
        logger.info("UID input field cleared")

    def click_on_outside(self):
        logger.debug("Clicking on outside to trigger validation")
        out = self.page.locator("div.button-group")
        out.click()
        logger.info("Outside clicked to trigger validation")

    def get_uid_error_message(self):
        logger.debug("Retrieving UID field error message")
        error_message_element = self.page.locator(
            "//mat-error[contains(text(), '') or contains(text(), 'Special') or contains(text(), 'Remove')]"
        )
        error_message = (
            error_message_element.text_content().strip()
            if error_message_element.is_visible()
            else ""
        )
        logger.info("UID error message retrieved: %s", error_message)
        return error_message

    def fill_customer_part_number_input(self, value):
        logger.debug("Filling Customer Part Number input field with value: %s", value)
        cpn_input = self.page.locator("input[formcontrolname='customerPartNumber']")
        cpn_input.clear()
        cpn_input.fill(value)
        logger.info("Customer Part Number input field filled with value: %s", value)

    def clear_customer_part_number_input(self):
        logger.debug("Clearing Customer Part Number input field")
        cpn_input = self.page.locator("input[formcontrolname='customerPartNumber']")
        cpn_input.clear()
        logger.info("Customer Part Number input field cleared")

    def get_customer_part_number_error_message(self):
        logger.debug("Retrieving Customer Part Number field error message")
        error_message_element = self.page.locator(
            "//mat-error[contains(text(), '') or contains(text(), 'Remove')]"
        )
        error_message = (
            error_message_element.text_content().strip()
            if error_message_element.is_visible()
            else ""
        )
        logger.info("Customer Part Number error message retrieved: %s", error_message)
        return error_message

    def click_save_button_on_manual_upload_form(self):
        logger.debug("Clicking Save button on Manual Upload form")
        save_button = self.page.locator("//button[contains(text(), 'Submit')]")
        save_button.click()
        logger.info("Save button clicked on Manual Upload form")

    def is_save_button_disabled(self):
        logger.debug("Checking if Save button on Manual Upload form is disabled")
        save_button = self.page.locator("//button[contains(text(), 'Submit')]")
        is_disabled = save_button.is_disabled()
        logger.info("Save button disabled state: %s", is_disabled)
        return is_disabled

    def get_manual_upload_success_message(self):
        logger.debug("Retrieving success message after manual upload")
        success_message_element = self.page.locator("//simple-snack-bar")
        success_message = (
            success_message_element.text_content().strip()
            if success_message_element.is_visible()
            else ""
        )
        logger.info("Manual upload success message retrieved: %s", success_message)
        return success_message

    def click_bulk_upload_button(self):
        logger.debug("Clicking Bulk Upload button for the first device in the table")
        bulk = self.page.locator("//div[@class='page-header']//button[2]")
        bulk.click()
        logger.info("Bulk Upload button clicked for the first device in the table")

    def get_bulk_upload_page_title(self):
        base = BasePage(self.page)
        logger.debug("Retrieving Bulk Upload page title")
        title = base.get_title()
        logger.info("Bulk Upload page title retrieved: %s", title)
        return title

    def click_download_sample_file_button(self):
        logger.debug("Clicking Download Sample File button")

        before_files = set(os.listdir(DOWNLOADS_PATH))

        download_button = self.page.locator(
            "//button[contains(text(), 'Download Sample')]"
        )

        download_button.click(force=True)

        self.page.wait_for_timeout(5000)

        after_files = set(os.listdir(DOWNLOADS_PATH))

        new_files = after_files - before_files

        assert new_files, "No file downloaded"

        downloaded_file = list(new_files)[0]

        download_path = os.path.join(
            DOWNLOADS_PATH,
            downloaded_file,
        )

        logger.info("Downloaded file path: %s", download_path)

        return download_path
