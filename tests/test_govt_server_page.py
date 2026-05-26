import pytest
from config.config import GOVERNMENT_SERVERS_URL
from pages.common.pagination import PaginationHelper
from pages.common.search import SearchHelper
from utils.logger import get_logger
from pages.common.table_section import TableSection
from pages.api.government_server_api import GovtServerAPI

logger = get_logger(__name__)


@pytest.mark.device
@pytest.mark.regression
class TestGovtServerPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        """Automatically log test lifecycle events"""
        test_name = request.node.name
        logger.info("Starting Government Server test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Government Server test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Government Server test passed: %s", test_name)
        elif report.failed:
            logger.error("Government Server test failed: %s", test_name)
            logger.debug(
                "Government Server failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Government Server test skipped: %s", test_name)

    @pytest.mark.smoke
    def test_govt_server_page_title_is_correct(self, govt_server_page, report_case):
        """Verify the title of the Government Server page"""
        logger.info("Verifying Government Server page title")

        expected_title = "Government Server"
        logger.debug("Expected page title: %s", expected_title)

        actual_title = govt_server_page.get_page_title()
        logger.debug(
            "Government Server page title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=expected_title,
            actual=actual_title,
            message="Validate Government Server page title",
        )

        assert (
            expected_title in actual_title
        ), f"Expected title '{expected_title}' to be in '{actual_title}'"
        logger.info("Government Server page title verified successfully")

    def test_govt_server_page_table_headers(self, govt_server_page, report_case):
        """Verify the table headers on the Government Server page"""
        logger.info("Verifying Government Server table headers")

        expected_headers = [
            "STATE NAME",
            "STATE CODE",
            "STATE ENABLE OTA COMMAND",
            "STATE PRIMARY IP:PORT",
            "STATE SECONDARY IP:PORT",
            "ACTION",
        ]
        logger.debug("Expected table headers: %s", expected_headers)

        actual_headers = govt_server_page.get_table_headers()
        logger.debug(
            "Government Server table headers check | expected=%s | actual=%s",
            expected_headers,
            actual_headers,
        )

        report_case(
            expected=str(expected_headers),
            actual=str(actual_headers),
            message="Validate Government Server table headers",
        )

        assert (
            actual_headers == expected_headers
        ), f"Expected headers {expected_headers}, but got {actual_headers}"

        logger.info("Government Server table headers verified successfully")

    def test_govt_server_page_table_no_data(self, govt_server_page, report_case):
        """Verify the 'No Data Found' state of the table on the Government Server page"""
        logger.info("Verifying 'No Data Found' state of Government Server table")

        expected_no_data = False
        logger.debug("Expected: Table should have no data")

        actual_has_no_data = govt_server_page.get_table_headers() == []
        logger.debug(
            "Government Server table no data check | expected=%s | actual=%s",
            expected_no_data,
            actual_has_no_data,
        )

        report_case(
            expected=expected_no_data,
            actual=actual_has_no_data,
            message="Validate 'No Data Found' state for Government Server table",
        )

        assert (
            actual_has_no_data == expected_no_data
        ), "Expected 'No Data Found' state, but data was present"
        logger.info(
            "'No Data Found' state verified successfully for Government Server table"
        )

    def test_govt_server_page_table_row_count(self, govt_server_page, report_case):
        """Verify Government Server table has rows"""

        logger.info("Verifying row count of Government Server table")

        table = TableSection(govt_server_page.page)
        actual_row_count = table.get_row_count()

        logger.debug(
            "Government Server table row count: %s",
            actual_row_count,
        )

        report_case(
            expected="Row count > 0",
            actual=actual_row_count,
            message="Validate Government Server table contains rows",
        )

        assert (
            actual_row_count > 0
        ), f"Expected row count greater than 0, but got {actual_row_count}"

        logger.info(
            "Government Server table contains %s rows",
            actual_row_count,
        )

    def test_govt_server_page_table_data_validation(
        self, govt_server_page, report_case
    ):
        """Verify the data in the Government Server table matches expected values"""
        logger.info("Validating data in Government Server table")

        expected_data = [
            {
                "STATE NAME": "Auto FOTA",
                "STATE CODE": "AF",
                "STATE ENABLE OTA COMMAND": "--",
                "STATE PRIMARY IP:PORT": "--:--",
                "STATE SECONDARY IP:PORT": "--:--",
                "ACTION": "visibility\ndelete",
            }
        ]

        table = TableSection(govt_server_page.page)
        actual_row_data = table.get_row_data(0)
        logger.debug(
            "Government Server table row data validation | expected=%s | actual=%s",
            expected_data[0],
            actual_row_data,
        )
        report_case(
            expected=str(expected_data[0]),
            actual=str(actual_row_data),
            message="Validate data of first row in Government Server table",
        )
        assert (
            actual_row_data == expected_data[0]
        ), f"Expected row data {expected_data[0]}, but got {actual_row_data}"
        logger.info(
            "Data in Government Server table validated successfully for first row"
        )

    def test_govt_server_page_search_functionality(self, govt_server_page, report_case):
        """Verify the search functionality of the Government Server table"""
        logger.info("Verifying search functionality of Government Server table")

        search_query = "Auto FOTA"

        search_helper = SearchHelper(govt_server_page.page)
        search_result = search_helper.run_search(search_query)
        logger.debug(
            "Government Server table search result for query '%s': %s",
            search_query,
            search_result,
        )
        report_case(
            expected=f"At least 1 result containing '{search_query}'",
            actual=f"{search_result['results_found']} results found",
            message="Validate search functionality of Government Server table",
        )
        assert search_result[
            "success"
        ], f"Search failed with error: {search_result['error']}"
        assert (
            search_result["results_found"] > 0
        ), f"Expected at least 1 search result for query '{search_query}', but found none"
        assert any(
            search_query in result for result in search_result["results"]
        ), f"Expected search results to contain '{search_query}', but got {search_result['results']}"
        logger.info(
            "Search functionality of Government Server table verified successfully for query '%s'",
            search_query,
        )

    def test_govt_server_page_table_action_buttons(self, govt_server_page, report_case):
        """Verify the presence of action buttons in the Government Server table"""
        logger.info("Verifying action buttons in Government Server table")

        table = TableSection(govt_server_page.page)
        action_buttons = table.get_action_buttons(
            1
        )  # this should be 1 cause 0 th row is headers row
        expected_buttons = ["visibility", "delete"]

        logger.debug(
            "Government Server table action buttons check | expected=%s | actual=%s",
            expected_buttons,
            action_buttons,
        )

        report_case(
            expected=str(expected_buttons),
            actual=str(action_buttons),
            message="Validate presence of action buttons in Government Server table",
        )

        assert set(action_buttons) == set(
            expected_buttons
        ), f"Expected action buttons {expected_buttons}, but got {action_buttons}"
        logger.info(
            "Action buttons in Government Server table verified successfully for first row"
        )

    def test_govt_server_page_pagination_validations(
        self, govt_server_page, report_case
    ):
        """Verify pagination controls of the Government Server table"""
        logger.info("Verifying pagination controls of Government Server table")
        pagination = PaginationHelper(govt_server_page.page)
        pagination_result = pagination.verify(include_backward=True)
        logger.debug(
            "Government Server table pagination verification result: %s",
            pagination_result,
        )
        report_case(
            expected="Pagination should work correctly in both directions",
            actual=str(pagination_result),
            message="Validate pagination controls of Government Server table",
        )
        assert pagination_result[
            "success"
        ], f"Pagination verification failed: {pagination_result['error']}"
        if pagination_result["total_pages"] > 1:
            assert len(pagination_result["pages_visited"]) > 1, (
                "Expected to visit multiple pages during pagination verification, "
                "but only one page was visited"
            )
        else:
            logger.info(
                "Only one page available in pagination. Navigation validation skipped."
            )
        logger.info(
            "Pagination controls of Government Server table verified successfully, pages visited: %s",
            pagination_result["pages_visited"],
        )

    """ test add goverment server page test """

    @pytest.mark.smoke
    def test_govt_server_page_add_government_button_is_visible_and_enable(
        self, govt_server_page, report_case
    ):
        """Verify the presence of Add Government Server button in Government Server page"""
        logger.info(
            "Verifying presence of Add Government Server button in Government Server page"
        )
        is_visible, is_enabled = (
            govt_server_page.is_add_govt_server_button_visible_and_enabled()
        )

        logger.debug(
            "Add Government Server button visibility: %s, enabled state: %s",
            is_visible,
            is_enabled,
        )

        report_case(
            expected="Add Government Server button should be visible and enabled",
            actual=f"Visible: {is_visible}, Enabled: {is_enabled}",
            message="Validate presence and state of Add Government Server button",
        )

        assert is_visible, "Expected 'Add Government Server' button to be visible"
        assert is_enabled, "Expected 'Add Government Server' button to be enabled"

        logger.info(
            "Presence and state of Add Government Server button verified successfully"
        )

    def test_govt_server_page_click_add_gov_server_btn_and_validate_title(
        self, govt_server_page, report_case
    ):
        """Verify clicking Add Government Server button navigates to correct page"""
        logger.info(
            "Verifying navigation after clicking 'Add Government Server' button"
        )
        govt_server_page.click_add_govt_server_button()
        expected_title = "Add Government Servers"
        actual_title = govt_server_page.get_page_title()

        logger.debug(
            "Add Government Server page title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=expected_title,
            actual=actual_title,
            message="Validate navigation to Add Government Server page and its title",
        )

        assert (
            expected_title in actual_title
        ), f"Expected title '{expected_title}' to be in '{actual_title}' after clicking 'Add Government Server' button"

        logger.info(
            "Navigation to Add Government Server page and its title verified successfully"
        )

    def test_govt_server_page_validate_component_title(
        self, govt_server_page, report_case
    ):
        """Verify the component title on the Government Server page"""
        logger.info("Verifying component title on Government Server page")

        govt_server_page.click_add_govt_server_button()
        expected_component_title = "Government Servers Details"
        actual_component_title = govt_server_page.get_component_title()

        logger.debug(
            "Government Server component title check | expected=%s | actual=%s",
            expected_component_title,
            actual_component_title,
        )

        report_case(
            expected=expected_component_title,
            actual=actual_component_title,
            message="Validate component title on Government Server page",
        )

        assert (
            expected_component_title in actual_component_title
        ), f"Expected component title '{expected_component_title}' to be in '{actual_component_title}'"
        logger.info("Component title on Government Server page verified successfully")

    def test_govt_server_page_validate_all_input_enabled_and_editable(
        self, govt_server_page, report_case
    ):
        """Verify all input fields on Add Government Server page are enabled and editable"""
        logger.info(
            "Verifying all input fields on Add Government Server page are enabled and editable"
        )
        govt_server_page.click_add_govt_server_button()

        govt_input_fields = govt_server_page.get_input_fields_locators().items()

        for field, locator in govt_input_fields:
            is_visible = locator.is_visible()
            is_enabled = locator.is_enabled()

            logger.debug(
                "Input field '%s' visibility: %s, enabled state: %s",
                field,
                is_visible,
                is_enabled,
            )

            report_case(
                expected=f"Input field '{field}' should be visible and enabled",
                actual=f"Visible: {is_visible}, Enabled: {is_enabled}",
                message=f"Validate presence and state of input field '{field}' on Add Government Server page",
            )

            assert is_visible, f"Expected input field '{field}' to be visible"
            assert is_enabled, f"Expected input field '{field}' to be enabled"

    def test_govt_server_page_validate_input_fields_accept_text_except_port_and_ip(
        self, govt_server_page, report_case
    ):
        """Verify all input fields accept entered text values"""

        logger.info(
            "Verifying all input fields on Add Government Server page accept entered values"
        )

        govt_server_page.click_add_govt_server_button()

        govt_input_fields = govt_server_page.get_input_fields_locators().items()

        for field, locator in govt_input_fields:

            if "ip" in field.lower() or "port" in field.lower():
                test_input = "InvalidInput"
            else:
                test_input = "TestInput"

            locator.fill(test_input)

            actual_value = locator.input_value()

            logger.debug(
                "Input field '%s' acceptance check | test input: '%s' | actual value: '%s'",
                field,
                test_input,
                actual_value,
            )

            report_case(
                expected=f"Input field '{field}' should accept entered input",
                actual=f"Actual value after input: '{actual_value}'",
                message=f"Validate input acceptance for field '{field}'",
            )

            assert (
                actual_value == test_input
            ), f"Expected input field '{field}' to accept entered input"

    def test_govt_server_page_validate_input_fields_accept_valid_ip_and_port(
        self, govt_server_page, report_case
    ):
        """Verify IP and port input fields on Add Government Server page accept valid input"""
        logger.info(
            "Verifying IP and port input fields on Add Government Server page accept valid input"
        )
        govt_server_page.click_add_govt_server_button()

        govt_input_fields = govt_server_page.get_input_fields_locators().items()

        for field, locator in govt_input_fields:
            if "gov_ip1" in field or "gov_ip2" in field:
                test_input = "192.168.1.1"
            elif "port1" in field or "port2" in field:
                test_input = "8080"
            else:
                continue

            locator.fill(test_input)
            actual_value = locator.input_value()

            logger.debug(
                "Input field '%s' validation check | test input: '%s' | actual value: '%s'",
                field,
                test_input,
                actual_value,
            )

            report_case(
                expected=f"Input field '{field}' should accept valid input",
                actual=f"Actual value after input: '{actual_value}'",
                message=f"Validate valid input acceptance for field '{field}' on Add Government Server page",
            )

            assert (
                actual_value == test_input
            ), f"Expected input field '{field}' to accept valid input, but it did not"

    def test_govt_server_page_validate_error_messages_on_invalid_inputs(
        self, govt_server_page, report_case
    ):
        """Verify validation error messages for invalid inputs on Add Government Server page"""

        logger.info(
            "Verifying validation error messages for invalid inputs on Add Government Server page"
        )

        invalid_test_data = govt_server_page.get_valid_invalid_inputs_for_field()

        for field_name, field_test_data in invalid_test_data.items():

            for invalid_input, expected_error_message in field_test_data:

                logger.info(
                    "Validating field '%s' with invalid input '%s'",
                    field_name,
                    invalid_input,
                )

                # Navigate fresh every iteration
                govt_server_page.page.goto(GOVERNMENT_SERVERS_URL)

                govt_server_page.page.wait_for_load_state("networkidle")

                govt_server_page.click_add_govt_server_button()

                input_fields = govt_server_page.get_input_fields_locators()

                locator = input_fields[field_name]

                # Fill invalid input
                locator.fill(str(invalid_input))

                # Trigger validation
                govt_server_page.click_submit_button()

                govt_server_page.page.wait_for_timeout(1000)

                actual_error_message = govt_server_page.get_error_message_from_field(
                    field_name
                )

                logger.debug(
                    "Field: %s | Invalid Input: '%s' | Expected Error: '%s' | Actual Error: '%s'",
                    field_name,
                    invalid_input,
                    expected_error_message,
                    actual_error_message,
                )

                report_case(
                    expected=f"Error message should be '{expected_error_message}'",
                    actual=f"Actual error message: '{actual_error_message}'",
                    message=(
                        f"Validate error message for invalid input "
                        f"'{invalid_input}' in field '{field_name}'"
                    ),
                )

                assert (
                    actual_error_message is not None
                ), f"No error message displayed for field '{field_name}'"

                assert actual_error_message == expected_error_message, (
                    f"Expected error message '{expected_error_message}' "
                    f"but got '{actual_error_message}' "
                    f"for field '{field_name}'"
                )

    def test_govt_server_page_validate_submit_button_disabled_on_blank_form(
        self, govt_server_page, report_case
    ):
        """Verify Submit button is disabled when form is blank"""

        logger.info(
            "Verifying Submit button is disabled when Add Government Server form is blank"
        )

        govt_server_page.click_add_govt_server_button()

        submit_button_enabled = govt_server_page.is_submit_button_enabled()

        logger.debug(
            "Submit button enabled state on blank form: %s",
            submit_button_enabled,
        )

        report_case(
            expected="Submit button should be disabled on blank form",
            actual=f"Submit button enabled state: {submit_button_enabled}",
            message="Validate Submit button disabled state on blank form",
        )

        assert submit_button_enabled is False, "Submit button is enabled on blank form"

    def test_govt_server_page_validate_submit_button_disabled_on_invalid_inputs(
        self, govt_server_page, report_case
    ):
        """Verify Submit button is disabled on invalid inputs"""

        logger.info("Verifying Submit button is disabled on invalid inputs")

        govt_server_page.click_add_govt_server_button()

        input_fields = govt_server_page.get_input_fields_locators()

        invalid_test_data = govt_server_page.get_valid_invalid_inputs_for_field()

        for field_name, field_test_data in invalid_test_data.items():

            locator = input_fields[field_name]

            invalid_input, _ = field_test_data[0]

            locator.fill(str(invalid_input))

            locator.blur()

        submit_button_enabled = govt_server_page.is_submit_button_enabled()

        logger.debug(
            "Submit button enabled state on invalid inputs: %s",
            submit_button_enabled,
        )

        report_case(
            expected="Submit button should be disabled on invalid inputs",
            actual=f"Submit button enabled state: {submit_button_enabled}",
            message="Validate Submit button disabled state on invalid inputs",
        )

        assert (
            submit_button_enabled is False
        ), "Submit button is enabled on invalid inputs"

    def test_govt_server_page_validate_submit_button_enabled_on_valid_inputs(
        self, govt_server_page, report_case
    ):
        """Verify Submit button is enabled on valid inputs"""

        logger.info("Verifying Submit button is enabled on valid inputs")

        govt_server_page.click_add_govt_server_button()

        input_fields = govt_server_page.get_input_fields_locators()

        valid_test_data = govt_server_page.enter_valid_input_for_field()

        for field_name, valid_input in valid_test_data.items():

            locator = input_fields[field_name]

            locator.fill(str(valid_input))

            actual_value = locator.input_value()

            logger.debug(
                "Field '%s' | Valid Input: '%s' | Actual Value: '%s'",
                field_name,
                valid_input,
                actual_value,
            )

            report_case(
                expected=f"Field '{field_name}' should accept valid input",
                actual=f"Actual value after input: '{actual_value}'",
                message=f"Validate valid input acceptance for field '{field_name}'",
            )

            assert actual_value == str(
                valid_input
            ), f"Field '{field_name}' did not accept valid input"

        submit_button_enabled = govt_server_page.is_submit_button_enabled()

        logger.debug(
            "Submit button enabled state on valid inputs: %s",
            submit_button_enabled,
        )

        report_case(
            expected="Submit button should be enabled on valid inputs",
            actual=f"Submit button enabled state: {submit_button_enabled}",
            message="Validate Submit button enabled state on valid inputs",
        )

        assert (
            submit_button_enabled is True
        ), "Submit button is not enabled on valid inputs"

    def test_govt_server_page_validate_success_message_on_valid_form_submission(
        self, govt_server_page, report_case
    ):
        """Verify success message is displayed after successful form submission"""

        logger.info("Verifying success message after successful form submission")

        govt_server_page.click_add_govt_server_button()

        input_fields = govt_server_page.get_input_fields_locators()

        valid_test_data = govt_server_page.enter_valid_input_for_field()

        for field_name, valid_input in valid_test_data.items():

            locator = input_fields[field_name]

            locator.fill(str(valid_input))

        submit_button_enabled = govt_server_page.is_submit_button_enabled()

        logger.debug(
            "Submit button enabled state before submission: %s",
            submit_button_enabled,
        )

        assert (
            submit_button_enabled is True
        ), "Submit button is not enabled before submission"

        govt_server_page.click_submit_button()

        actual_success_message = govt_server_page.get_success_message()

        expected_success_message = "Data Fetched Successfully"

        logger.debug(
            "Expected Success Message: '%s' | Actual Success Message: '%s'",
            expected_success_message,
            actual_success_message,
        )

        report_case(
            expected=f"Success message should be '{expected_success_message}'",
            actual=f"Actual success message: '{actual_success_message}'",
            message="Validate success message after successful form submission",
        )

        assert expected_success_message in actual_success_message, (
            f"Expected success message '{expected_success_message}' "
            f"but got '{actual_success_message}'"
        )

    ##### API Validation of firmware master with oc and d firmware types.  #####
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_validating_all_api_of_firmwares(self, govt_server_page):
        all_firmwares = GovtServerAPI.getAllFirmware(govt_server_page.page)
        # logger.info(f"all firmwares -> ", all_firmwares)
        total_firmware_count = len(all_firmwares)

        oc_firmwares = GovtServerAPI.get_oc_firmwares(govt_server_page.page)
        # logger.info(f"oc firmwares -> ", oc_firmwares)
        oc_firmware_count = len(oc_firmwares)

        d_firmwares = GovtServerAPI.get_d_firmwares(govt_server_page.page)
        # logger.info(f"d firmwares -> ", d_firmwares)
        d_firmware_count = len(d_firmwares)

        assert (
            total_firmware_count == oc_firmware_count + d_firmware_count
        ), "Total count is mismatched"

        # ---------------- OC Firmware Validation ---------------- #

        all_oc_firmware_data = [
            {"id": firmware["id"], "fileName": firmware["fileName"]}
            for firmware in all_firmwares
            if firmware.get("firmwareType") == "OC"
        ]

        oc_firmware_data = [
            {"id": firmware["id"], "fileName": firmware["fileName"]}
            for firmware in oc_firmwares
        ]

        logger.info(f"OC firmware data from all firmware API -> {all_oc_firmware_data}")
        logger.info(f"OC firmware data from OC firmware API -> {oc_firmware_data}")

        assert sorted(all_oc_firmware_data, key=lambda x: x["id"]) == sorted(
            oc_firmware_data, key=lambda x: x["id"]
        ), (
            f"Mismatch found in OC firmware data.\n"
            f"From all firmware API: {all_oc_firmware_data}\n"
            f"From OC firmware API: {oc_firmware_data}"
        )

        # ---------------- D Firmware Validation ---------------- #

        all_d_firmware_data = [
            {"id": firmware["id"], "fileName": firmware["fileName"]}
            for firmware in all_firmwares
            if firmware.get("firmwareType") == "D"
        ]

        d_firmware_data = [
            {"id": firmware["id"], "fileName": firmware["fileName"]}
            for firmware in d_firmwares
        ]

        logger.info(f"D firmware data from all firmware API -> {all_d_firmware_data}")
        logger.info(f"D firmware data from D firmware API -> {d_firmware_data}")

        assert sorted(all_d_firmware_data, key=lambda x: x["id"]) == sorted(
            d_firmware_data, key=lambda x: x["id"]
        ), (
            f"Mismatch found in D firmware data.\n"
            f"From all firmware API: {all_d_firmware_data}\n"
            f"From D firmware API: {d_firmware_data}"
        )

    @pytest.mark.smoke
    def test_govt_server_page_view_button_is_enabled_for_searched_server(
        self, govt_server_page, report_case
    ):
        """Verify view button is enabled and clickable for searched server"""

        logger.info("Verifying view button is enabled for searched server")

        response = govt_server_page.search_server("Shital")

        logger.debug("Search response: %s", response)

        assert response["success"] is True, "Search operation was not successful"

        assert (
            response["results_found"] == 1
        ), f"Expected 1 result but found {response['results_found']}"

        view_button = govt_server_page.get_view_button()

        logger.debug("Checking visibility of view button")

        assert view_button.is_visible(), "View button is not visible"

        logger.debug("Checking enabled state of view button")

        assert view_button.is_enabled(), "View button is not enabled"

        report_case(
            expected="View button should be visible and enabled",
            actual=(
                f"View button visible: {view_button.is_visible()}, "
                f"enabled: {view_button.is_enabled()}"
            ),
            message="Validate view button state for searched server",
        )

        govt_server_page.click_view_button()

        current_url = govt_server_page.page.url

        logger.debug(
            "Current URL after clicking view button: %s",
            current_url,
        )

        assert (
            current_url is not None and current_url != ""
        ), "Navigation did not happen after clicking view button"

    @pytest.mark.smoke
    def test_govt_server_page_validate_page_title_after_view_button_clicked(
        self, govt_server_page, report_case
    ):
        """Verify page title after clicking view button"""

        logger.info("Verifying page title after clicking view button")

        response = govt_server_page.search_server("Shital")

        logger.debug("Search response: %s", response)

        assert response["success"] is True, "Search operation was not successful"

        assert (
            response["results_found"] == 1
        ), f"Expected 1 result but found {response['results_found']}"

        view_button = govt_server_page.get_view_button()

        logger.debug("Checking visibility of view button")

        assert view_button.is_visible(), "View button is not visible"

        logger.debug("Checking enabled state of view button")

        assert view_button.is_enabled(), "View button is not enabled"

        govt_server_page.click_view_button()

        actual_page_title = govt_server_page.get_page_title_on_view_page()

        expected_page_title = "View/Update Government Servers"

        logger.debug(
            "Expected page title: '%s' | Actual page title: '%s'",
            expected_page_title,
            actual_page_title,
        )

        report_case(
            expected=(f"Page title should be " f"'{expected_page_title}'"),
            actual=(f"Actual page title: " f"'{actual_page_title}'"),
            message=("Validate page title after " "clicking view button"),
        )

        assert expected_page_title == actual_page_title, (
            f"Expected page title "
            f"'{expected_page_title}' "
            f"but got '{actual_page_title}'"
        )

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_govt_server_page_validate_input_fields_with_actual_api_data(
        self, govt_server_page, report_case
    ):
        """Validate UI input field data with actual API response data"""

        logger.info("Validating UI input field data with API response")

        response, _, _ = GovtServerAPI.get_state_server_details_by_id(
            govt_server_page.page
        )

        logger.info(
            "Response after hitting the API: %s",
            response,
        )

        assert response, "API response data is empty"

        api_data = response

        searched_response = govt_server_page.search_server("Shital")

        logger.debug(
            "Search response: %s",
            searched_response,
        )

        assert (
            searched_response["success"] is True
        ), "Search operation was not successful"

        assert searched_response["results_found"] == 1, (
            f"Expected 1 search result but got " f"{searched_response['results_found']}"
        )

        govt_server_page.click_view_button()

        govt_server_page.page.wait_for_load_state("networkidle")

        input_fields = govt_server_page.get_input_fields_locators()

        field_mapping = {
            "state": "state",
            "stateCode": "stateCode",
            "govtIp1": "govtIp1",
            "port1": "port1",
            "govtIp2": "govtIp2",
            "port2": "port2",
            "stateEnable": "stateEnable",
        }

        for ui_field, api_key in field_mapping.items():

            locator = input_fields[ui_field]

            locator.wait_for(state="visible")

            actual_ui_value = locator.input_value().strip()

            expected_api_value = str(api_data.get(api_key, "")).strip()

            logger.debug(
                "Validating field '%s' | " "Expected: '%s' | Actual: '%s'",
                ui_field,
                expected_api_value,
                actual_ui_value,
            )

            report_case(
                expected=(f"{ui_field} value should be " f"'{expected_api_value}'"),
                actual=(f"Actual {ui_field} value is " f"'{actual_ui_value}'"),
                message=(f"Validate {ui_field} field value " f"with API response"),
            )

            assert expected_api_value == actual_ui_value, (
                f"Mismatch found for field "
                f"'{ui_field}'. "
                f"Expected '{expected_api_value}' "
                f"but got '{actual_ui_value}'"
            )
