from faker.generator import random

from pages.common.table_section import TableSection
from pages.common.search import SearchHelper
from utils.logger import get_logger
from pages.base_page import BasePage
from utils.helpers import Helpers

logger = get_logger(__name__)


class GovtServerPage(BasePage):
    def __init__(self, page):
        self.page = page

    def get_page_title(self):
        """Get the title of the Government Server page"""
        title = super().get_title()
        logger.debug("Retrieved Government Server page title: %s", title)
        return title

    def get_component_title(self):
        """Get the title of the Government Server component"""
        component_title = super().get_component_title()
        logger.debug("Retrieved Government Server component title: %s", component_title)
        return component_title

    def get_table_headers(self):
        """Get the headers of the table on the Government Server page"""
        table = TableSection(self.page)
        if table.has_no_data():
            logger.warning(
                "Government Server table has no data, cannot retrieve headers"
            )
            return []

        headers = table.get_headers()
        logger.debug("Retrieved Government Server table headers: %s", headers)
        return headers

    def is_add_govt_server_button_visible_and_enabled(self):
        """Check if the 'Add Government Server' button is visible and enabled"""
        button_locator = self.page.get_by_text("Add Government Server open_in_new")
        is_visible = button_locator.is_visible()
        is_enabled = button_locator.is_enabled()
        logger.debug(
            "'Add Government Server' button visibility: %s, enabled state: %s",
            is_visible,
            is_enabled,
        )
        return is_visible, is_enabled

    def click_add_govt_server_button(self):
        """Click the 'Add Government Server' button"""
        button_locator = self.page.get_by_text("Add Government Server open_in_new")
        if button_locator.is_visible() and button_locator.is_enabled():
            button_locator.click()
            self.page.wait_for_url("**/govt-servers-add")
            self.page.wait_for_load_state("networkidle")
            logger.info("Clicked 'Add Government Server' button")
        else:
            logger.error(
                "'Add Government Server' button is not clickable. Visible: %s, Enabled: %s",
                button_locator.is_visible(),
                button_locator.is_enabled(),
            )
            raise Exception("'Add Government Server' button is not clickable")

    def get_input_fields_locators(self):
        return {
            "state": self.page.locator("input[formcontrolname='state']"),
            "stateCode": self.page.locator("input[formcontrolname='stateCode']"),
            "govtIp1": self.page.locator("input[formcontrolname='govtIp1']"),
            "port1": self.page.locator("input[formcontrolname='port1']"),
            "govtIp2": self.page.locator("input[formcontrolname='govtIp2']"),
            "port2": self.page.locator("input[formcontrolname='port2']"),
            "stateEnable": self.page.locator("input[formcontrolname='stateEnable']"),
        }

    def get_valid_invalid_inputs_for_field(self):
        """
        Return dictionary containing invalid inputs and expected error messages
        for each field.

        Format:
        {
            "field_name": [
                ("invalid_input", "expected_error_message"),
            ]
        }
        """

        return {
            "state": [
                (
                    " ",
                    "This field is required and can't be only spaces.",
                ),
                (
                    f"invalid_{Helpers.generate_random_state_name()}",
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    Helpers.generate_random_number(5),
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    "@#$%",
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    f" {Helpers.generate_random_string(5)}",
                    "Remove leading or trailing spaces.",
                ),
                (
                    f"{Helpers.generate_random_string(5)} ",
                    "Remove leading or trailing spaces.",
                ),
            ],
            "stateCode": [
                (
                    " ",
                    "This field is required and can't be only spaces.",
                ),
                (
                    f"invalid_{Helpers.generate_random_state_abbreviation()}",
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    Helpers.generate_random_number(5),
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    "@#$%",
                    "Only alphabets and spaces are allowed.",
                ),
                (
                    f" {Helpers.generate_random_string(3)}",
                    "Remove leading or trailing spaces.",
                ),
                (
                    f"{Helpers.generate_random_string(3)} ",
                    "Remove leading or trailing spaces.",
                ),
            ],
            "govtIp1": [
                # (
                #     f"invalid_{Helpers.generate_random_ip()}",
                #     "Please enter a valid IP Address.",
                # ),
                # (
                #     f" {Helpers.generate_random_ip()}QW@#@#$",
                #     "Please enter a valid IP Address.",
                # ),
                (
                    f"{Helpers.generate_random_ip() + Helpers.generate_random_ip()}",
                    "Maximum 20 characters allowed.",
                ),
            ],
            "port1": [
                (
                    " ",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    f"invalid_{Helpers.generate_random_number(5)}",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "#@!$!@#",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    Helpers.generate_random_number(10),
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "0",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "65536",
                    "Enter a valid port number (1-65535).",
                ),
            ],
            "govtIp2": [
                # (
                #     f"invalid_{Helpers.generate_random_ip()}",
                #     "Please enter a valid IP Address.",
                # ),
                # (
                #     f" {Helpers.generate_random_ip()}QW@#@#$",
                #     "Please enter a valid IP Address.",
                # ),
                (
                    f"{Helpers.generate_random_ip() + Helpers.generate_random_ip()}",
                    "Maximum 20 characters allowed.",
                ),
            ],
            "port2": [
                (
                    " ",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    f"invalid_{Helpers.generate_random_number(5)}",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "#@!$!@#",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    Helpers.generate_random_number(10),
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "0",
                    "Enter a valid port number (1-65535).",
                ),
                (
                    "65536",
                    "Enter a valid port number (1-65535).",
                ),
            ],
            "stateEnable": [
                (
                    " ",
                    "Please enter a valid State Enable.",
                ),
                (
                    "invalid_input",
                    "Please enter a valid State Enable.",
                ),
                (
                    "#@!$!@#",
                    "Please enter a valid State Enable.",
                ),
            ],
        }

    def enter_valid_input_for_field(self):
        return {
            "state": Helpers.generate_random_state_name(),
            "stateCode": Helpers.generate_random_state_abbreviation(),
            "govtIp1": Helpers.generate_random_ip(),
            "port1": random.randint(1, 65535),
            "govtIp2": Helpers.generate_random_ip(),
            "port2": random.randint(1, 65535),
            "stateEnable": "true",
        }

    def get_error_message_from_field(self, field_name):
        """Get error message displayed for specific field"""

        field_locator = self.get_input_fields_locators()[field_name]

        error_locator = field_locator.locator(
            "xpath=ancestor::mat-form-field//mat-error"
        )

        try:
            error_locator.first.wait_for(state="visible", timeout=3000)

            error_message = error_locator.first.inner_text().strip()

            logger.debug(
                "Retrieved error message for field '%s': %s",
                field_name,
                error_message,
            )

            return error_message

        except Exception:
            logger.debug(
                "No visible error message found for field '%s'",
                field_name,
            )

            return None

    def click_submit_button(self):
        """Click Submit button"""

        submit_button = self.page.get_by_role("button", name="Submit")

        submit_button.wait_for(state="visible")

        submit_button.click(force=True)

        logger.info("Clicked Submit button")

    def click_outside_to_get_error_msg(self):
        component_title = self.page.locator("h6.component-title")
        component_title.click()

    def is_submit_button_enabled(self):
        """Check whether Submit button is enabled"""

        submit_button = self.page.get_by_role("button", name="Submit")

        submit_button.wait_for(state="visible")

        is_enabled = submit_button.is_enabled()

        logger.debug(
            "Submit button enabled state: %s",
            is_enabled,
        )

        return is_enabled

    def get_success_message(self):
        """Get success message displayed after form submission"""

        success_message_locator = self.page.locator("simple-snack-bar").filter(
            has_text="Data Fetched Successfully"
        )

        success_message_locator.wait_for(state="visible")

        success_message = success_message_locator.first.inner_text().strip()

        logger.info(
            "Retrieved success message: %s",
            success_message,
        )

        return success_message

    def get_page_title_on_view_page(self):

        search_helper = SearchHelper(self.page)

        response = search_helper.run_search("Shital")

        logger.info(
            "Result of searched row is -> %s",
            response["results"],
        )

        view_button = self.page.get_by_text("visibility").first
        view_button.click()

        page_title = self.page.locator("span.page-title")
        return page_title.inner_text()

    def search_server(self, server_name):
        """Search for a specific server"""

        search_helper = SearchHelper(self.page)

        response = search_helper.run_search(server_name)

        logger.info(
            "Result of searched row is -> %s",
            response["results"],
        )

        return response

    def get_view_button(self):
        """Get view button locator"""

        return self.page.get_by_text("visibility").first

    def click_view_button(self):
        """Click on view button"""

        logger.info("Clicking on view button")

        view_button = self.get_view_button()

        view_button.click()

        self.page.wait_for_load_state("networkidle")

    def get_page_title_on_view_page(self):
        """Get page title on view page"""

        page_title = self.page.locator("span.page-title")

        return page_title.inner_text()
