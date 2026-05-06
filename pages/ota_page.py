import re

from pages.base_page import BasePage
from pages.common.search import SearchHelper
from pages.common.table_section import TableSection
from utils.logger import get_logger

logger = get_logger(__name__)


class OtaPage(BasePage):
    """Page object for OTA Batch and OTA Master pages."""

    # Locators as class constants
    BUTTON_LOCATOR = "//button"
    TABLE_LOCATOR = "//div[@class='component-body']"
    SEARCH_BOX_LOCATOR = "Search and Press Enter"
    OTA_MASTER_BUTTON_TEXT = "OTA Master open_in_new"
    OTA_MASTER_PAGE_TITLE = "span:has-text('OTA Master')"
    OTA_BATCH_URL_SUFFIX = "/ota-batch-page"
    OTA_MASTER_URL_SUFFIX = "/ota-master"
    OTA_MASTER_URL_PATTERN = "**/ota-master*"
    ADD_OTA_COMMAND_BUTTON = "Add OTA Command open_in_new"
    ADD_OTA_COMMAND_PAGE_TITLE = "h6:has-text('Add OTA Command')"

    # Add OTA Command Form Locators
    OTA_NAME_FIELD = "input[formcontrolname='name']"
    OTA_COMMAND_FIELD = "input[formcontrolname='otaCommand']"
    OTA_TYPE_DROPDOWN = "mat-select[formcontrolname='otaCommandType']"
    EXAMPLE_FIELD = "input[formcontrolname='otaCommandExample']"
    INPUT_FIELD_REQUIRED_DROPDOWN = "mat-select[formcontrolname='isInputFieldRequired']"
    SUBMIT_BUTTON = "button:has-text('Submit')"
    SEARCH_BUTTON = "button:has-text('Search search')"
    MAT_OPTION = "mat-option"

    def __init__(self, page):
        """Initialize OTA page object.

        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        logger.debug("Initialized OtaPage")

    def get_title(self) -> str:
        """Get the page title from parent class.

        Returns:
            str: The page title
        """
        return super().get_title()

    def get_page_title(self) -> str:
        """Get the OTA Master page title text.

        Returns:
            str: The OTA Master page title
        """
        logger.debug("Retrieving OTA Master page title")
        return self.page.locator(self.OTA_MASTER_PAGE_TITLE).inner_text()

    def is_page_loaded(self) -> bool:
        """Check if OTA Batch page is loaded.

        Returns:
            bool: True if page loaded, False otherwise
        """
        logger.debug("Checking if ota batch page is loaded")
        return self.page.url.endswith(self.OTA_BATCH_URL_SUFFIX)

    def is_ota_master_page_loaded(self) -> bool:
        """Check if OTA Master page is loaded.

        Returns:
            bool: True if OTA Master page loaded, False otherwise
        """
        logger.debug("Checking if OTA Master page is loaded")
        return self.page.url.endswith(self.OTA_MASTER_URL_SUFFIX)

    def is_ota_batch_page_buttons_visible(self) -> bool:
        """Check if OTA Batch page buttons are visible.

        Returns:
            bool: True if any button is visible, False otherwise
        """
        logger.debug("Checking visibility of OTA Batch page buttons")
        ota_page_buttons = self.page.locator(self.BUTTON_LOCATOR)
        for button in ota_page_buttons.all():
            if button.is_visible():
                return True
        return False

    def is_ota_batch_table_visible(self) -> bool:
        """Check if OTA Batch table is visible.

        Returns:
            bool: True if table is visible, False otherwise
        """
        logger.debug("Checking visibility of OTA Batch table")
        table = self.page.locator(self.TABLE_LOCATOR)
        return table.is_visible()

    def is_search_box_visible(self) -> bool:
        """Check if search box is visible.

        Returns:
            bool: True if search box is visible, False otherwise
        """
        logger.debug("Checking visibility of Search box")
        search_box = self.page.get_by_placeholder(self.SEARCH_BOX_LOCATOR)
        return search_box.is_visible()

    def is_ota_master_page_button_visible(self) -> bool:
        """Check if OTA Master page button is visible.

        Returns:
            bool: True if button is visible, False otherwise
        """
        logger.debug("Checking visibility of OTA Master page button")
        ota_master_button = self.page.get_by_text(self.OTA_MASTER_BUTTON_TEXT)
        return ota_master_button.is_visible()

    def go_to_ota_master_page(self) -> None:
        """Navigate to OTA Master page by clicking the button.

        Raises:
            Exception: If OTA Master page button is not visible
        """
        logger.debug("Navigating to OTA Master page")

        self.page.get_by_text(self.OTA_MASTER_BUTTON_TEXT).click()
        self.page.wait_for_url(self.OTA_MASTER_URL_PATTERN)

    def search_in_batch_page(self, query: str) -> dict:
        """Search for OTA batches using search functionality.

        Args:
            query: Search query string

        Returns:
            dict: Search results containing success status, count, and results
        """
        logger.debug("Searching for OTA batch: %s", query)
        search = SearchHelper(self.page)
        return search.run_search(query)

    def search_in_master_page(self, query: str) -> dict:
        """Search for OTA masters using search functionality.

        Args:
            query: Search query string

        Returns:
            dict: Search results containing success status, count, and results
        """
        logger.debug("Searching for OTA master: %s", query)
        search = SearchHelper(self.page)
        return search.run_search(query)

    def get_batch_table_data(self) -> list[str]:
        """Get all rows from OTA Batch table.

        Returns:
            list: List of table row contents
        """
        logger.debug("Retrieving OTA Batch table data")
        table = TableSection(self.page)
        return table.get_rows()

    def get_batch_table_headers(self) -> list[str]:
        """Get headers from OTA Batch table.

        Returns:
            list: List of table headers
        """
        logger.debug("Retrieving OTA Batch table headers")
        table = TableSection(self.page)
        return table.get_headers()

    def get_batch_table_row_count(self) -> int:
        """Get row count from OTA Batch table.

        Returns:
            int: Number of rows in the table
        """
        logger.debug("Getting OTA Batch table row count")
        table = TableSection(self.page)
        return table.get_row_count()

    def is_batch_table_empty(self) -> bool:
        """Check if OTA Batch table is empty or has 'No Data Found' message.

        Returns:
            bool: True if table is empty, False otherwise
        """
        logger.debug("Checking if OTA Batch table is empty")
        table = TableSection(self.page)
        return table.has_no_data()

    def get_master_table_data(self) -> list[str]:
        """Get all rows from OTA Master table.

        Returns:
            list: List of table row contents
        """
        logger.debug("Retrieving OTA Master table data")
        table = TableSection(self.page)
        return table.get_rows()

    def get_master_table_headers(self) -> list[str]:
        """Get headers from OTA Master table.

        Returns:
            list: List of table headers
        """
        logger.debug("Retrieving OTA Master table headers")
        table = TableSection(self.page)
        return table.get_headers()

    def get_master_table_row_count(self) -> int:
        """Get row count from OTA Master table.

        Returns:
            int: Number of rows in the table
        """
        logger.debug("Getting OTA Master table row count")
        table = TableSection(self.page)
        return table.get_row_count()

    def is_master_table_empty(self) -> bool:
        """Check if OTA Master table is empty or has 'No Data Found' message.

        Returns:
            bool: True if table is empty, False otherwise
        """
        logger.debug("Checking if OTA Master table is empty")
        table = TableSection(self.page)
        return table.has_no_data()

    """ Add Ota Command Page"""

    def validate_add_ota_button_and_click(self) -> None:
        """Validate Add OTA Command button is visible and click it."""
        logger.debug("Validating Add OTA Command button visibility")
        add_ota_button = self.page.get_by_text(self.ADD_OTA_COMMAND_BUTTON)
        assert add_ota_button.is_visible(), "Add OTA Command button not visible"
        add_ota_button.click()

    def is_add_ota_command_button_visible(self) -> bool:
        """Check if Add OTA Command button is visible.

        Returns:
            bool: True if button is visible, False otherwise
        """
        logger.debug("Checking visibility of Add OTA Command button")
        add_ota_button = self.page.get_by_text(self.ADD_OTA_COMMAND_BUTTON)
        return add_ota_button.is_visible()

    def is_on_add_ota_command_page(self) -> str:
        """Get the page title from Add OTA Command page.

        Returns:
            str: The inner text of the Add OTA Command page title, or empty string if not found
        """
        logger.debug("Retrieving Add OTA Command page title")
        try:
            # Get page title text
            page_title = self.page.locator(self.ADD_OTA_COMMAND_PAGE_TITLE)
            if page_title.is_visible():
                title_text = page_title.inner_text()
                logger.debug("Add OTA Command page title: %s", title_text)
                return title_text
            else:
                logger.warning("Add OTA Command page title not visible")
                return ""
        except Exception as e:
            logger.warning("Error retrieving Add OTA Command page title: %s", str(e))
            return ""

    # Add OTA Command Form Validation Methods
    def are_add_ota_command_form_fields_visible(self) -> bool:
        """Check if all Add OTA Command form fields are visible.

        Returns:
            bool: True if all fields are visible, False otherwise
        """
        logger.debug("Checking visibility of Add OTA Command form fields")
        try:
            ota_name = self.page.locator(self.OTA_NAME_FIELD).is_visible()
            ota_command = self.page.locator(self.OTA_COMMAND_FIELD).is_visible()
            ota_type = self.page.locator(self.OTA_TYPE_DROPDOWN).is_visible()
            example = self.page.locator(self.EXAMPLE_FIELD).is_visible()
            input_required = self.page.locator(
                self.INPUT_FIELD_REQUIRED_DROPDOWN
            ).is_visible()
            submit_btn = self.page.locator(self.SUBMIT_BUTTON).is_visible()

            all_visible = (
                ota_name
                and ota_command
                and ota_type
                and example
                and input_required
                and submit_btn
            )
            logger.debug(
                "Form fields visibility - OTA Name: %s, OTA Command: %s, OTA Type: %s, "
                "Example: %s, Input Required: %s, Submit: %s",
                ota_name,
                ota_command,
                ota_type,
                example,
                input_required,
                submit_btn,
            )
            return all_visible
        except Exception as e:
            logger.warning("Error checking form fields visibility: %s", str(e))
            return False

    def fill_ota_name(self, name: str) -> None:
        """Fill OTA Name field.

        Args:
            name: Name to enter in OTA Name field
        """
        logger.debug("Filling OTA Name field with: %s", name)
        ota_name_field = self.page.locator(self.OTA_NAME_FIELD)
        ota_name_field.wait_for(state="visible")
        ota_name_field.fill(name)

    def fill_ota_command(self, command: str) -> None:
        """Fill OTA Command field.

        Args:
            command: Command to enter in OTA Command field
        """
        logger.debug("Filling OTA Command field with: %s", command)
        ota_command_field = self.page.locator(self.OTA_COMMAND_FIELD)
        ota_command_field.wait_for(state="visible")
        ota_command_field.fill(command)

    def select_ota_type(self, ota_type: str) -> None:
        """Select OTA Type from dropdown.

        Args:
            ota_type: OTA Type value to select
        """
        logger.debug("Selecting OTA Type: %s", ota_type)
        ota_type_dropdown = self.page.locator(self.OTA_TYPE_DROPDOWN)
        ota_type_dropdown.wait_for(state="visible")
        ota_type_dropdown.click()
        self.page.wait_for_timeout(500)
        # Select the option from dropdown using mat-option selector
        option_locator = self.page.locator(f"{self.MAT_OPTION}:has-text('{ota_type}')")
        option_locator.wait_for(state="visible")
        option_locator.click()

    def fill_example(self, example: str) -> None:
        """Fill Example field.

        Args:
            example: Example text to enter
        """
        logger.debug("Filling Example field with: %s", example)
        example_field = self.page.locator(self.EXAMPLE_FIELD)
        example_field.wait_for(state="visible")
        example_field.fill(example)

    def select_input_field_required(self, option: str) -> None:
        """Select Input Field Required dropdown option.

        Args:
            option: Option to select (e.g., 'Yes', 'No')
        """
        logger.debug("Selecting Input Field Required: %s", option)
        input_required_dropdown = self.page.locator(self.INPUT_FIELD_REQUIRED_DROPDOWN)
        input_required_dropdown.wait_for(state="visible")
        input_required_dropdown.click()
        self.page.wait_for_timeout(500)
        # Select the option from dropdown using mat-option selector
        option_locator = self.page.locator(f"{self.MAT_OPTION}:has-text('{option}')")
        option_locator.wait_for(state="visible")
        option_locator.click()

    def get_ota_name_value(self) -> str:
        """Get value from OTA Name field.

        Returns:
            str: Current value in OTA Name field
        """
        logger.debug("Retrieving OTA Name field value")
        ota_name_field = self.page.locator(self.OTA_NAME_FIELD)
        return ota_name_field.input_value()

    def get_ota_command_value(self) -> str:
        """Get value from OTA Command field.

        Returns:
            str: Current value in OTA Command field
        """
        logger.debug("Retrieving OTA Command field value")
        ota_command_field = self.page.locator(self.OTA_COMMAND_FIELD)
        return ota_command_field.input_value()

    def get_example_value(self) -> str:
        """Get value from Example field.

        Returns:
            str: Current value in Example field
        """
        logger.debug("Retrieving Example field value")
        example_field = self.page.locator(self.EXAMPLE_FIELD)
        return example_field.input_value()

    def click_submit_button(self) -> None:
        """Click the Submit button."""
        logger.debug("Clicking Submit button")
        submit_button = self.page.locator(self.SUBMIT_BUTTON)
        submit_button.wait_for(state="visible")
        submit_button.click()

    def is_submit_button_disabled(self) -> bool:
        """Check if Submit button is disabled.

        Returns:
            bool: True if submit button is disabled, False otherwise
        """
        logger.debug("Checking if Submit button is disabled")
        submit_button = self.page.locator(self.SUBMIT_BUTTON)
        submit_button.wait_for(state="visible")
        is_disabled = submit_button.is_disabled()
        logger.debug("Submit button disabled state: %s", is_disabled)
        return is_disabled

    def is_search_button_disabled(self) -> bool:
        """Check if Search button is disabled.

        Returns:
            bool: True if search button is disabled, False otherwise
        """
        logger.debug("Checking if Search button is disabled")
        search_button = self.page.locator(self.SEARCH_BUTTON)
        search_button.wait_for(state="visible")
        is_disabled = search_button.is_disabled()
        logger.debug("Search button disabled state: %s", is_disabled)
        return is_disabled

    def is_submit_button_enabled(self) -> bool:
        """Check if Submit button is enabled.

        Returns:
            bool: True if submit button is enabled, False otherwise
        """
        logger.debug("Checking if Submit button is enabled")
        submit_button = self.page.locator(self.SUBMIT_BUTTON)
        submit_button.wait_for(state="visible")
        is_enabled = not submit_button.is_disabled()
        logger.debug("Submit button enabled state: %s", is_enabled)
        return is_enabled

    """ Manual OTA Page Methods"""

    def go_to_manual_ota_page(self) -> None:
        """Navigate to Manual OTA page by clicking the button.

        Raises:
            Exception: If Manual OTA page button is not visible
        """
        logger.debug("Navigating to Manual OTA page")

        self.page.get_by_text("Manual OTA open_in_new").click()
        self.page.wait_for_url("**/manual-ota*")

    def is_manual_ota_button_visible(self) -> bool:
        """Check if Manual OTA button is visible.

        Returns:
            bool: True if Manual OTA button is visible, False otherwise
        """
        logger.debug("Checking visibility of Manual OTA button")
        manual_ota_button = self.page.get_by_text("Manual OTA open_in_new")
        return manual_ota_button.is_visible()

    def click_manual_ota_button(self) -> None:
        """Click the Manual OTA button."""
        logger.debug("Clicking Manual OTA button")
        manual_ota_button = self.page.get_by_text("Manual OTA open_in_new")
        manual_ota_button.wait_for(state="visible")
        manual_ota_button.click()

    def get_manual_ota_component_title(self) -> str:
        """Get the component title text from Manual OTA page.

        Returns:
            str: The component title text, or empty string if not found
        """
        logger.debug("Retrieving Manual OTA component title")
        try:
            component_title = self.page.locator("h6:has-text('Search Device')")
            if component_title.is_visible():
                title_text = component_title.inner_text()
                logger.debug("Manual OTA component title: %s", title_text)
                return title_text
            else:
                logger.warning("Manual OTA component title not visible")
                return ""
        except Exception as e:
            logger.warning("Error retrieving Manual OTA component title: %s", str(e))
            return ""

    def clear_imei_input(self) -> None:
        """Clear the IMEI input field on Manual OTA page."""
        logger.debug("Clearing IMEI input field")
        imei_input = self.page.locator("input[formcontrolname='imei']")
        imei_input.wait_for(state="visible")
        imei_input.fill("")

    def click_manual_ota_imei_search_button(self) -> None:
        """Click the Search button on Manual OTA page.

        Note: Uses force=True to click even when disabled, which is needed for validation testing.
        """
        logger.debug("Clicking Manual OTA Search button")
        search_button = self.page.locator("//button[@class='submit-button']")
        search_button.wait_for(state="visible")
        search_button.click(force=True)

    def get_imei_error_message(self, error) -> str:
        """Get the error message text related to IMEI input on Manual OTA page.

        Returns:
            str: The error message text, or empty string if not found
        """
        logger.debug("Retrieving IMEI error message")
        try:
            # Use get_by_text to avoid CSS selector escaping issues with apostrophes
            error_message = self.page.get_by_text(error, exact=True)
            if error_message.is_visible():
                message_text = error_message.inner_text().strip()
                logger.debug("IMEI error message: %s", message_text)
                return message_text
            else:
                logger.warning("IMEI error message not visible")
                return ""
        except Exception as e:
            logger.warning("Error retrieving IMEI error message: %s", str(e))
            return ""

    def fill_imei_input(self, imei: str) -> None:
        """Fill the IMEI input field on Manual OTA page.

        Args:
            imei: IMEI number to enter in the input field
        """
        logger.debug("Filling IMEI input field with: %s", imei)
        imei_input = self.page.locator("input[formcontrolname='imei']")
        imei_input.wait_for(state="visible")
        imei_input.fill(imei)

    def is_new_ota_button_visible(self) -> bool:
        """Check if New OTA button is visible on Manual OTA page.

        Returns:
            bool: True if New OTA button is visible, False otherwise
        """
        logger.debug("Checking visibility of New OTA button on Manual OTA page")
        try:
            # Try multiple locator strategies in order of preference
            locators = [
                ("button:has-text('New OTA')", "has-text selector"),
                (self.page.get_by_role("button", name="New OTA"), "by-role: New OTA"),
                ("//button[contains(text(), 'New OTA')]", "XPath with text"),
                (
                    self.page.get_by_text("New OTA add_circle"),
                    "by-text: New OTA add_circle",
                ),
            ]

            for locator, description in locators:
                try:
                    if isinstance(locator, str):
                        button = self.page.locator(locator)
                    else:
                        button = locator

                    # Wait for button to be visible with reasonable timeout
                    button.wait_for(state="visible", timeout=3000)
                    is_visible = button.is_visible()

                    if is_visible:
                        logger.info("New OTA button found using: %s", description)
                        return True
                    else:
                        logger.debug(
                            "Button found but not visible using: %s", description
                        )
                except Exception as e:
                    logger.debug("Locator '%s' failed: %s", description, str(e))
                    continue

            logger.warning("New OTA button not found with any locator strategy")
            return False

        except Exception as e:
            logger.error("Error checking New OTA button visibility: %s", str(e))
            return False
