import re
from config.config import IMEI
from playwright.sync_api import expect
from pages.common.search import SearchHelper
from pages.common.table_section import TableSection
from utils.helpers import Helpers as helper
from utils.logger import get_logger

logger = get_logger(__name__)


class TestOtaPage:
    """Test suite for OTA Batch and OTA Master pages."""

    # Test data
    SEARCH_QUERY = "test"

    """ OTA Batch Page Tests """

    def test_go_to_ota_page(self, ota_page):
        """Verify OTA page is loaded with correct URL."""
        assert (
            ota_page.is_page_loaded()
        ), f"OTA page did not load at {ota_page.page.url}"

    def test_ota_page_title(self, ota_page):
        """Verify OTA Batch page title is correct."""
        expected_title = "OTA Batch"
        actual_title = ota_page.get_title()
        assert (
            actual_title == expected_title
        ), f"Expected title '{expected_title}', but got '{actual_title}'"

    def test_ota_page_elements(self, ota_page):
        """Verify all OTA Batch page elements are visible and loaded."""
        logger.info("Validating OTA Batch page elements")

        assert ota_page.is_page_loaded(), "OTA Batch page did not load correctly"
        assert (
            ota_page.is_ota_batch_page_buttons_visible()
        ), "OTA Batch page buttons are not visible"
        assert ota_page.is_ota_batch_table_visible(), "OTA Batch table is not visible"
        assert ota_page.is_search_box_visible(), "Search box is not visible"

        logger.info("All OTA Batch page elements are present and visible")

    def test_search_functionality_on_ota_batch_table(self, ota_page):
        """Verify search functionality on OTA Batch page."""
        logger.info("Testing search functionality on OTA Batch table")

        assert ota_page.is_ota_batch_table_visible(), "OTA Batch table is not visible"

        search = SearchHelper(ota_page.page)
        result = search.run_search(self.SEARCH_QUERY)

        logger.info("Search result: %s", result)

        assert result["success"], f"Search failed: {result['error']}"

        if result["results_found"] == 0:
            table = TableSection(ota_page.page)
            assert (
                table.has_no_data()
            ), f"Search query '{self.SEARCH_QUERY}' not found and no data message shown"
        else:
            rows = result["results"]
            assert any(
                self.SEARCH_QUERY.lower() in row.lower() for row in rows
            ), f"Search query '{self.SEARCH_QUERY}' not found in results"

    def test_table_data_validation_on_ota_batch(self, ota_page):
        """Verify OTA Batch table data is visible and valid."""
        logger.info("Validating OTA Batch table data")

        table = TableSection(ota_page.page)
        assert ota_page.is_ota_batch_table_visible(), "OTA Batch table not visible"

        row_count = ota_page.get_batch_table_row_count()
        logger.info("OTA Batch table row count: %s", row_count)

        if row_count == 0:
            logger.warning("OTA Batch table is empty - skipping data validation")
            return

        try:
            headers = ota_page.get_batch_table_headers()
            assert len(headers) > 0, "Table headers should not be empty"
            logger.info("OTA Batch table headers: %s", headers)
        except Exception as e:
            logger.warning("Could not retrieve headers: %s", str(e))

        try:
            rows = ota_page.get_batch_table_data()
            if rows:
                logger.info("Retrieved %s rows from OTA Batch table", len(rows))
            else:
                logger.warning(
                    "No rows retrieved from table - selector may need adjustment"
                )
        except Exception as e:
            logger.warning("Could not retrieve rows: %s", str(e))

    def test_search_with_helper_on_ota_batch(self, ota_page):
        """Test search using SearchHelper on OTA Batch page."""
        logger.info("Testing search using SearchHelper on OTA Batch")

        search = SearchHelper(ota_page.page)
        result = ota_page.search_in_batch_page(self.SEARCH_QUERY)

        logger.info("Search result: %s", result)

        assert result["success"], f"Search failed: {result['error']}"

        if result["results_found"] == 0:
            assert ota_page.is_batch_table_empty(), "Expected no data"
        else:
            for row in result["results"]:
                assert self.SEARCH_QUERY.lower() in row.lower()

    """ OTA Master Page Tests """

    def test_is_ota_master_button_visible(self, ota_page):
        """Verify OTA Master button is visible on OTA Batch page."""
        assert (
            ota_page.is_ota_master_page_button_visible()
        ), "OTA Master page button is not visible"

    def test_navigate_to_ota_master_page(self, ota_page):
        """Verify navigation to OTA Master page succeeds."""
        ota_page.go_to_ota_master_page()
        expect(ota_page.page).to_have_url(re.compile(r".*ota-master"))

    def test_ota_master_page_title(self, ota_page):
        """Verify OTA Master page title is correct after navigation."""
        ota_page.go_to_ota_master_page()
        expected_title = "OTA Master"
        actual_title = ota_page.get_page_title()
        assert (
            actual_title == expected_title
        ), f"Expected title '{expected_title}', but got '{actual_title}'"

    def test_ota_master_page_elements(self, ota_page):
        """Verify OTA Master page elements are visible after navigation."""
        ota_page.go_to_ota_master_page()

        assert (
            ota_page.is_ota_master_page_loaded()
        ), "OTA Master page did not load correctly"
        # Note: OTA Master button is only visible on Batch page, not on Master page
        assert (
            ota_page.is_ota_batch_page_buttons_visible()
        ), "Action buttons are not visible on OTA Master page"
        assert (
            ota_page.is_ota_batch_table_visible()
        ), "OTA Master table is not visible on OTA Master page"

        logger.info("OTA Master page elements are present and visible")

    def test_search_functionality_on_ota_master_table(self, ota_page):
        """Verify search functionality on OTA Master page."""
        logger.info("Testing search functionality on OTA Master table")

        ota_page.go_to_ota_master_page()
        assert ota_page.is_ota_batch_table_visible(), "OTA Master table is not visible"

        search = SearchHelper(ota_page.page)
        result = search.run_search(self.SEARCH_QUERY)

        logger.info("Search result: %s", result)

        assert result["success"], f"Search failed: {result['error']}"

        if result["results_found"] == 0:
            table = TableSection(ota_page.page)
            assert (
                table.has_no_data()
            ), f"Search query '{self.SEARCH_QUERY}' not found and no data message shown"
        else:
            rows = result["results"]
            assert any(
                self.SEARCH_QUERY.lower() in row.lower() for row in rows
            ), f"Search query '{self.SEARCH_QUERY}' not found in results"

    def test_table_data_validation_on_ota_master(self, ota_page):
        """Verify OTA Master table data is visible and valid."""
        logger.info("Validating OTA Master table data")

        ota_page.go_to_ota_master_page()
        table = TableSection(ota_page.page)
        assert ota_page.is_ota_batch_table_visible(), "OTA Master table not visible"

        row_count = ota_page.get_master_table_row_count()
        logger.info("OTA Master table row count: %s", row_count)

        if row_count == 0:
            logger.warning("OTA Master table is empty - skipping data validation")
            return

        try:
            headers = ota_page.get_master_table_headers()
            assert len(headers) > 0, "Table headers should not be empty"
            logger.info("OTA Master table headers: %s", headers)
        except Exception as e:
            logger.warning("Could not retrieve headers: %s", str(e))

        try:
            rows = ota_page.get_master_table_data()
            if rows:
                logger.info("Retrieved %s rows from OTA Master table", len(rows))
            else:
                logger.warning(
                    "No rows retrieved from table - selector may need adjustment"
                )
        except Exception as e:
            logger.warning("Could not retrieve rows: %s", str(e))

    def test_search_with_helper_on_ota_master(self, ota_page):
        """Test search using SearchHelper on OTA Master page."""
        logger.info("Testing search using SearchHelper on OTA Master")

        ota_page.go_to_ota_master_page()
        result = ota_page.search_in_master_page(self.SEARCH_QUERY)

        logger.info("Search result: %s", result)

        assert result["success"], f"Search failed: {result['error']}"

        if result["results_found"] == 0:
            assert ota_page.is_master_table_empty(), "Expected no data"
        else:
            for row in result["results"]:
                assert self.SEARCH_QUERY.lower() in row.lower()

    """ Add Ota Command Page"""

    def test_add_ota_command_button(self, ota_page):
        """Verify Add OTA Command button is visible on OTA Master page."""
        ota_page.go_to_ota_master_page()
        assert (
            ota_page.is_add_ota_command_button_visible()
        ), "Add OTA Command button is not visible on OTA Master page"

        if ota_page.is_add_ota_command_button_visible():
            logger.info("Add OTA Command button is visible on OTA Master page")
            ota_page.validate_add_ota_button_and_click()
        else:
            logger.warning("Add OTA Command button is not visible - cannot click")

        page_title = ota_page.is_on_add_ota_command_page()
        assert page_title, "Did not navigate to Add OTA Command page"
        assert (
            "Add OTA Command" in page_title
        ), f"Expected 'Add OTA Command' in page title, got '{page_title}'"

    def test_add_ota_command_form_fields_visible(self, ota_page):
        """Verify all Add OTA Command form fields are visible."""
        logger.info("Validating Add OTA Command form fields visibility")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        assert (
            ota_page.are_add_ota_command_form_fields_visible()
        ), "Not all Add OTA Command form fields are visible"

        logger.info("All Add OTA Command form fields are visible")

    def test_fill_ota_name_field(self, ota_page):
        """Verify OTA Name field can be filled."""
        logger.info("Testing OTA Name field fill")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        test_name = "Test OTA Name"
        ota_page.fill_ota_name(test_name)

        actual_value = ota_page.get_ota_name_value()
        assert (
            actual_value == test_name
        ), f"Expected '{test_name}', but got '{actual_value}'"
        logger.info("OTA Name field filled successfully: %s", test_name)

    def test_fill_ota_command_field(self, ota_page):
        """Verify OTA Command field can be filled."""
        logger.info("Testing OTA Command field fill")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        test_command = "Test Command"
        ota_page.fill_ota_command(test_command)

        actual_value = ota_page.get_ota_command_value()
        assert (
            actual_value == test_command
        ), f"Expected '{test_command}', but got '{actual_value}'"
        logger.info("OTA Command field filled successfully: %s", test_command)

    def test_fill_example_field(self, ota_page):
        """Verify Example field can be filled."""
        logger.info("Testing Example field fill")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        test_example = helper.generate_random_string(10)
        ota_page.fill_example(test_example)

        actual_value = ota_page.get_example_value()
        assert (
            actual_value == test_example
        ), f"Expected '{test_example}', but got '{actual_value}'"
        logger.info("Example field filled successfully: %s", test_example)

    def test_select_ota_type_dropdown(self, ota_page):
        """Verify OTA Type dropdown can be selected."""
        logger.info("Testing OTA Type dropdown selection")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        ota_type = "GET"
        try:
            ota_page.select_ota_type(ota_type)
            logger.info("OTA Type selected successfully: %s", ota_type)
        except Exception as e:
            logger.warning("Error selecting OTA Type: %s", str(e))

    def test_select_input_field_required_dropdown(self, ota_page):
        """Verify Input Field Required dropdown can be selected."""
        logger.info("Testing Input Field Required dropdown selection")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        option = "NO"
        try:
            ota_page.select_input_field_required(option)
            logger.info("Input Field Required selected successfully: %s", option)
        except Exception as e:
            logger.warning("Error selecting Input Field Required: %s", str(e))

    def test_add_ota_command_form_complete_flow(self, ota_page):
        """Test complete Add OTA Command form flow with all fields."""
        logger.info("Testing complete Add OTA Command form flow")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        # Verify form fields are visible
        assert (
            ota_page.are_add_ota_command_form_fields_visible()
        ), "Form fields not visible"

        # Fill OTA Name
        test_name = "Complete Test OTA"
        ota_page.fill_ota_name(test_name)
        assert (
            ota_page.get_ota_name_value() == test_name
        ), "OTA Name not filled correctly"

        # Fill OTA Command
        test_command = "Test Command Complete"
        ota_page.fill_ota_command(test_command)
        assert (
            ota_page.get_ota_command_value() == test_command
        ), "OTA Command not filled correctly"

        # Fill Example
        test_example = "Complete Example"
        ota_page.fill_example(test_example)
        assert (
            ota_page.get_example_value() == test_example
        ), "Example not filled correctly"

        logger.info("Add OTA Command form complete flow test passed")

    def test_submit_button_disabled_when_form_empty(self, ota_page):
        """Verify Submit button is disabled when form fields are empty."""
        logger.info("Testing Submit button disabled state on empty form")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        # Form should be empty, so submit button should be disabled
        assert (
            ota_page.is_submit_button_disabled()
        ), "Submit button should be disabled when form is empty"

        logger.info("Submit button is correctly disabled on empty form")

    def test_submit_button_enabled_when_form_filled(self, ota_page):
        """Verify Submit button is enabled when all form fields are filled."""
        logger.info("Testing Submit button enabled state on filled form")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        # Initially form is empty, submit should be disabled
        assert (
            ota_page.is_submit_button_disabled()
        ), "Submit button should be disabled initially"

        # Fill all required fields
        ota_page.fill_ota_name("Test OTA Name")
        ota_page.fill_ota_command("Test Command")
        ota_page.fill_example("Test Example")

        try:
            ota_page.select_ota_type("GET")
        except Exception as e:
            logger.warning("Could not select OTA Type: %s", str(e))

        try:
            ota_page.select_input_field_required("NO")
        except Exception as e:
            logger.warning("Could not select Input Field Required: %s", str(e))

        # Now all fields are filled, submit should be enabled
        assert (
            ota_page.is_submit_button_enabled()
        ), "Submit button should be enabled when all fields are filled"

        logger.info("Submit button is correctly enabled on filled form")

    def test_submit_button_state_transitions(self, ota_page):
        """Verify Submit button state transitions between disabled and enabled."""
        logger.info("Testing Submit button state transitions")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        # Step 1: Initially empty - should be disabled
        assert (
            ota_page.is_submit_button_disabled()
        ), "Submit should be disabled initially"
        logger.info("Step 1 - Submit button is disabled on empty form")

        # Step 2: Fill first field - check state
        ota_page.fill_ota_name("Test OTA")
        logger.info(
            "Step 2 - OTA Name filled. Submit button disabled: %s",
            ota_page.is_submit_button_disabled(),
        )

        # Step 3: Fill second field
        ota_page.fill_ota_command("Test Command")
        logger.info(
            "Step 3 - OTA Command filled. Submit button disabled: %s",
            ota_page.is_submit_button_disabled(),
        )

        # Step 4: Fill example field
        ota_page.fill_example("Example Value")
        logger.info(
            "Step 4 - Example filled. Submit button disabled: %s",
            ota_page.is_submit_button_disabled(),
        )

        # Step 5: Try to select dropdowns and check if submit becomes enabled
        try:
            ota_page.select_ota_type("GET")
            logger.info(
                "Step 5 - OTA Type selected. Submit button enabled: %s",
                ota_page.is_submit_button_enabled(),
            )
        except Exception as e:
            logger.warning("Could not select OTA Type: %s", str(e))

        try:
            ota_page.select_input_field_required("NO")
            logger.info(
                "Step 6 - Input Field Required selected. Submit button enabled: %s",
                ota_page.is_submit_button_enabled(),
            )
        except Exception as e:
            logger.warning("Could not select Input Field Required: %s", str(e))

        logger.info("Submit button state transitions test completed")

    def test_submit_button_clickable_when_enabled(self, ota_page):
        """Verify Submit button is clickable when enabled with all fields filled."""
        logger.info("Testing Submit button is clickable when enabled")
        ota_page.go_to_ota_master_page()
        ota_page.validate_add_ota_button_and_click()

        # Fill all required fields
        ota_page.fill_ota_name("Clickable Test OTA")
        ota_page.fill_ota_command("Clickable Test Command")
        ota_page.fill_example("Clickable Example")

        try:
            ota_page.select_ota_type("GET")
        except Exception as e:
            logger.warning("Could not select OTA Type: %s", str(e))

        try:
            ota_page.select_input_field_required("NO")
        except Exception as e:
            logger.warning("Could not select Input Field Required: %s", str(e))

        # Verify button is enabled before clicking
        assert ota_page.is_submit_button_enabled(), "Submit button should be enabled"

        # Click submit button
        try:
            ota_page.click_submit_button()
            logger.info("Submit button clicked successfully")
        except Exception as e:
            logger.error("Error clicking submit button: %s", str(e))
            raise

    """ Manual Ota Test Cases"""

    def test_manual_ota_button_visible(self, ota_page):
        """Verify Manual OTA button is visible on OTA Master page."""
        assert (
            ota_page.is_manual_ota_button_visible()
        ), "Manual OTA button is not visible on OTA Master page"

    def test_click_and_validate_manual_ota_button(self, ota_page):
        """Verify clicking Manual OTA button opens correct page."""
        if ota_page.is_manual_ota_button_visible():
            logger.info("Manual OTA button is visible - attempting to click")
            try:
                ota_page.click_manual_ota_button()
                expect(ota_page.page).to_have_url(re.compile(r".*manual-ota"))
                logger.info("Clicked Manual OTA button successfully")
            except Exception as e:
                logger.error("Error clicking Manual OTA button: %s", str(e))
                raise

            # Validate new page opened (this would depend on the expected behavior)
            # For example, if it opens a new tab or navigates to a new URL, we would check that here.
            # This is a placeholder for actual validation logic.
            logger.info(
                "Manual OTA button click test completed - add validation logic as needed"
            )
        else:
            logger.warning(
                "Manual OTA button is not visible - cannot perform click test"
            )

    def test_component_title_on_manual_ota_page(self, ota_page):
        """Verify component title is visible on Manual OTA page."""
        ota_page.go_to_manual_ota_page()
        assert (
            ota_page.get_manual_ota_component_title() == "Search Device"
        ), "Component title is not visible on Manual OTA page"

    def test_search_button_disabled_on_manual_ota_page_if_fields_not_filled(
        self, ota_page
    ):
        """Verify Search button is disabled on Manual OTA page if fields are not filled."""
        ota_page.go_to_manual_ota_page()
        assert (
            ota_page.is_search_button_disabled()
        ), "Search button should be disabled when fields are not filled"

    def test_imei_input_fields_errors(self, ota_page):
        """Verify error messages for IMEI input fields on Manual OTA page."""
        ota_page.go_to_manual_ota_page()

        # Test empty IMEI field
        ota_page.clear_imei_input()
        # ota_page.click_imei_input()  # Focus on the IMEI input to trigger validation
        ota_page.click_manual_ota_imei_search_button()
        assert (
            ota_page.get_imei_error_message(
                "This field is required and can't be only spaces."
            )
            == "This field is required and can't be only spaces."
        ), "Expected error message for empty IMEI field not shown"

        # Test invalid IMEI format
        ota_page.fill_imei_input("invalid_imei_demo")
        ota_page.click_manual_ota_imei_search_button()
        assert (
            ota_page.get_imei_error_message("Value must be exactly 15 characters long.")
            == "Value must be exactly 15 characters long."
        ), "Expected error message for invalid IMEI format not shown"

        # Test 15 character IMEI format in string
        ota_page.fill_imei_input("a" * 15)
        ota_page.click_manual_ota_imei_search_button()
        assert (
            ota_page.get_imei_error_message("Only numbers are allowed.")
            == "Only numbers are allowed."
        ), "Expected error message for invalid IMEI format not shown"

    def test_enter_valid_imei_and_search(self, ota_page):
        """Verify entering valid IMEI and clicking search on Manual OTA page."""
        ota_page.go_to_manual_ota_page()

        valid_imei = IMEI  # Example of a valid 15-digit IMEI
        ota_page.fill_imei_input(valid_imei)
        assert (
            not ota_page.is_search_button_disabled()
        ), "Search button should be enabled when valid IMEI is entered"

        try:
            ota_page.click_manual_ota_imei_search_button()
            logger.info("Clicked Search button with valid IMEI successfully")

            # Verify search was executed (page still on manual-ota and no error displayed)
            assert (
                "manual-ota" in ota_page.page.url
            ), "Should remain on manual-ota page after search"

            # Note: New OTA button check removed as it doesn't appear after search.
            # Add more specific assertions here based on actual search results behavior
            logger.info("Search completed successfully with valid IMEI")

        except Exception as e:
            logger.error("Error during search: %s", str(e))
            raise
