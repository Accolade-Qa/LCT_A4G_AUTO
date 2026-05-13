from pages.common.table_section import TableSection
from pages.common.pagination import PaginationHelper
from pages.common.search import SearchHelper
from utils.logger import get_logger
from config.config import DISPATCHED_DEVICE_URL, IMEI
import pytest
from pages.base_page import BasePage
from pages.api.customer_details import CustomerDetailsAPI

logger = get_logger(__name__)


class TestDispatchedDevicePage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Dispatched Device test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Dispatched Device test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Dispatched Device test passed: %s", test_name)
        elif report.failed:
            logger.error("Dispatched Device test failed: %s", test_name)
            logger.debug(
                "Dispatched Device failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Dispatched Device test skipped: %s", test_name)

    def test_dispatched_device_page(self, dispatched_device_page, report_case):
        logger.info("Starting validation of Dispatched Device page URL")

        actual_url = dispatched_device_page.page.url

        logger.debug(
            "Dispatched Device URL check | expected=%s | actual=%s",
            DISPATCHED_DEVICE_URL,
            actual_url,
        )

        report_case(
            expected=DISPATCHED_DEVICE_URL,
            actual=actual_url,
        )

        logger.info("Comparing expected and actual page URLs")

        assert actual_url == DISPATCHED_DEVICE_URL, (
            f"Expected URL to be '{DISPATCHED_DEVICE_URL}', " f"got '{actual_url}'"
        )

        logger.info("Dispatched Device page URL validated successfully")

    """ Dispatched Device Page Test Cases """

    def test_dispatched_device_page_title(self, dispatched_device_page, report_case):
        logger.info("Starting validation of Dispatched Device page title")

        expected_title = "Dispatched Devices"

        logger.debug("Expected page title: %s", expected_title)

        logger.debug("Fetching actual page title")
        base = BasePage(dispatched_device_page.page)
        actual_title = base.get_title()

        logger.debug(
            "Dispatched Device page title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=expected_title,
            actual=actual_title,
        )

        logger.info("Comparing expected and actual page titles")

        assert actual_title == expected_title, (
            f"Expected page title to be '{expected_title}', " f"got '{actual_title}'"
        )

        logger.info("Dispatched Device page title validated successfully")

    def test_dispatched_device_page_elements(self, dispatched_device_page, report_case):
        logger.info("Starting validation of Dispatched Device page elements")

        logger.debug("Checking visibility of page elements")

        elements_checks = {
            "Manual Upload button": (
                dispatched_device_page.is_manual_upload_button_visible()
            ),
            "Bulk Upload button": (
                dispatched_device_page.is_bulk_upload_button_visible()
            ),
            "Checkbox": dispatched_device_page.is_checkbox_visible(),
            # "View Actions button": (
            #     dispatched_device_page.is_view_actions_button_visible()
            # ),
            # "Delete Action button": (
            #     dispatched_device_page.is_delete_action_button_visible()
            # ),
            "Dispatched Device table": (
                dispatched_device_page.is_dispatched_device_table_visible()
            ),
            "Search box": dispatched_device_page.is_search_box_visible(),
        }

        logger.info(
            "Total elements configured for validation: %s",
            len(elements_checks),
        )

        for element_name, is_visible in elements_checks.items():
            logger.info("Validating visibility of element: %s", element_name)

            logger.debug(
                "%s visibility check | expected=True | actual=%s",
                element_name,
                is_visible,
            )

            report_case(
                expected=True,
                actual=is_visible,
                message=f"{element_name} visibility",
            )

            assert is_visible, (
                f"Expected {element_name} to be visible " f"on Dispatched Device page"
            )

            logger.info(
                "%s visibility validated successfully",
                element_name,
            )

        logger.info("All Dispatched Device page elements validated successfully")

    def test_component_title_dispatched_device_page(
        self, dispatched_device_page, report_case
    ):
        logger.info("Starting validation of Dispatched Device component title")

        base_page = BasePage(dispatched_device_page.page)

        expected_title = "Dispatched Device List"

        logger.debug("Expected component title: %s", expected_title)

        logger.debug("Fetching actual component title from page")
        actual_title = base_page.get_component_title()

        logger.debug(
            "Dispatched Device component title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=expected_title,
            actual=actual_title,
        )

        logger.info("Comparing expected and actual component titles")

        assert actual_title == expected_title, (
            f"Expected component title to be '{expected_title}', "
            f"got '{actual_title}'"
        )

        logger.info("Dispatched Device component title validated successfully")

    def test_table_headers_dispatched_device_page(
        self, dispatched_device_page, report_case
    ):
        logger.info("Starting validation of Dispatched Device table headers")

        expected_headers = [
            "UID",
            "IMEI",
            "ICCID",
            "MODEL NAME",
            "CUSTOMER NAME",
            "ACTION",
        ]

        logger.debug("Expected table headers: %s", expected_headers)

        logger.debug("Fetching actual table headers from Dispatched Device page")
        actual_headers = dispatched_device_page.get_table_headers()

        logger.debug(
            "Dispatched Device table headers check | expected=%s | actual=%s",
            expected_headers,
            actual_headers,
        )

        logger.info(
            "Validating total number of table headers | expected=%s | actual=%s",
            len(expected_headers),
            len(actual_headers),
        )

        report_case(
            expected=expected_headers,
            actual=actual_headers,
        )

        logger.info("Comparing expected and actual table headers")

        assert actual_headers == expected_headers, (
            f"Expected table headers to be {expected_headers}, " f"got {actual_headers}"
        )

        logger.info("Dispatched Device table headers validated successfully")

    def test_table_data_dispatched_device_page(
        self, dispatched_device_page, report_case
    ):
        logger.info("Starting validation of Dispatched Device table data")

        table = TableSection(dispatched_device_page.page)

        logger.debug("Fetching table data from Dispatched Device page")
        table_data = table.get_table_data()

        logger.debug(
            "Dispatched Device table data extracted successfully | rows=%s | data=%s",
            len(table_data),
            table_data,
        )

        report_case(expected="Valid table data", actual=table_data)

        logger.info("Validating table data structure")
        assert isinstance(
            table_data, list
        ), "Expected table data to be a list of dictionaries"

        logger.info("Total rows received for validation: %s", len(table_data))

        for index, row in enumerate(table_data, start=1):
            logger.info("Validating row %s", index)
            logger.debug("Row %s data: %s", index, row)

            assert isinstance(
                row, dict
            ), f"Expected row {index} data to be a dictionary"

            logger.debug("Checking mandatory keys in row %s", index)

            assert "IMEI" in row, "Expected 'IMEI' key in row data"
            assert "ICCID" in row, "Expected 'ICCID' key in row data"
            assert "UID" in row, "Expected 'UID' key in row data"
            assert "MODEL NAME" in row, "Expected 'MODEL NAME' key in row data"
            assert "CUSTOMER NAME" in row, "Expected 'CUSTOMER NAME' key in row data"
            assert "ACTION" in row, "Expected 'ACTION' key in row data"

            logger.debug("Validating IMEI value in row %s: %s", index, row["IMEI"])

            # IMEI should be of digits and length is 14 or 15
            assert row["IMEI"].isdigit() and len(row["IMEI"]) in [
                14,
                15,
            ], (
                f"Expected IMEI to be a 14 or 15 digit number, " f"got {row['IMEI']}"
            )

            logger.debug("Validating ICCID value in row %s: %s", index, row["ICCID"])

            # ICCID should be of digits and length is 19 or 20
            assert row["ICCID"].isdigit() and len(row["ICCID"]) in [
                19,
                20,
            ], (
                f"Expected ICCID to be a 19 or 20 digit number, " f"got {row['ICCID']}"
            )

            logger.debug("Validating UID value in row %s: %s", index, row["UID"])

            # UID is of alphanumeric and length is 19
            assert row["UID"].isalnum() and len(row["UID"]) == 19, (
                f"Expected UID to be a 19 character alphanumeric string, "
                f"got {row['UID']}"
            )

            logger.debug(
                "Validating MODEL NAME value in row %s: %s",
                index,
                row["MODEL NAME"],
            )

            # Model name should be non-empty string
            assert (
                isinstance(row["MODEL NAME"], str) and row["MODEL NAME"].strip() != ""
            ), (
                f"Expected MODEL NAME to be a non-empty string, "
                f"got '{row['MODEL NAME']}'"
            )

            logger.debug(
                "Validating CUSTOMER NAME value in row %s: %s",
                index,
                row["CUSTOMER NAME"],
            )

            # Customer name should be non-empty string
            assert (
                isinstance(row["CUSTOMER NAME"], str)
                and row["CUSTOMER NAME"].strip() != ""
            ), (
                f"Expected CUSTOMER NAME to be a non-empty string, "
                f"got '{row['CUSTOMER NAME']}'"
            )

            logger.debug(
                "Validating ACTION value in row %s: %s",
                index,
                row["ACTION"],
            )

            # ACTION should be non-empty
            assert row["ACTION"].strip() != "", (
                f"Expected ACTION to be a non-empty value, " f"got '{row['ACTION']}'"
            )

            logger.info("Row %s validated successfully", index)

        logger.info("Dispatched Device table data validation completed successfully")

    def test_no_data_message_dispatched_device_page_if_no_data(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of 'No Data Found' message on Dispatched Device page"
        )

        table = TableSection(dispatched_device_page.page)

        logger.debug("Checking row count in Dispatched Device table")
        row_count = table.get_row_count()

        logger.info("Dispatched Device table row count: %s", row_count)

        logger.debug("Checking presence of 'No Data Found' message")
        actual_has_no_data = table.has_no_data()

        expected_has_no_data = row_count == 0

        logger.debug(
            "Dispatched Device no data message check | expected=%s | actual=%s",
            expected_has_no_data,
            actual_has_no_data,
        )

        report_case(
            expected=expected_has_no_data,
            actual=actual_has_no_data,
        )

        logger.debug(
            "Validating actual_has_no_data type | value=%s | type=%s",
            actual_has_no_data,
            type(actual_has_no_data).__name__,
        )

        assert isinstance(actual_has_no_data, bool), (
            "Expected actual_has_no_data to be a boolean value "
            "indicating presence of 'No Data Found' message"
        )

        if expected_has_no_data:
            logger.info(
                "Table is empty, validating 'No Data Found' message is displayed"
            )

            assert actual_has_no_data, (
                "Expected 'No Data Found' message to be displayed "
                "when table is empty"
            )

            logger.info(
                "'No Data Found' message displayed successfully for empty table"
            )

        else:
            logger.info(
                "Table contains data, 'No Data Found' message validation skipped"
            )

        logger.info(
            "Completed validation of 'No Data Found' message on Dispatched Device page"
        )

    def test_select_customer_checkbox_dispatched_device_page(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Select Customer dropdown values "
            "on Dispatched Device page"
        )

        logger.debug("Fetching customer list from API")

        listofcust = CustomerDetailsAPI._fetch_customer_details_from_api(
            dispatched_device_page.page
        )

        # All added because on ui dropdown first option is All and then followed by customer list from api
        listofcust.insert(0, "All")

        logger.info(
            "Customer list fetched successfully from API | total customers=%s",
            len(listofcust),
        )

        logger.debug("Customer list fetched from API: %s", listofcust)

        logger.debug("Fetching customer list from Select Customer dropdown")

        actual_customers = dispatched_device_page.get_customer_list()

        logger.info(
            "Customer list fetched successfully from UI dropdown | total customers=%s",
            len(actual_customers),
        )

        logger.debug(
            "Customer list fetched from UI dropdown: %s",
            actual_customers,
        )

        report_case(
            expected=listofcust,
            actual=actual_customers,
            message="Validate Select Customer dropdown values",
        )

        logger.info("Comparing customer list fetched from API with UI dropdown values")

        assert actual_customers == listofcust, (
            f"Expected customer list {listofcust}, " f"but got {actual_customers}"
        )

        logger.info("Select Customer dropdown values validated successfully")

    # test select dropdown one by one and validate the table data with if no data then with no data found message
    def test_select_customer_dropdown_values_dispatched_device_page(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Select Customer dropdown functionality "
            "on Dispatched Device page"
        )

        logger.debug("Fetching customer list from API")

        listofcust = CustomerDetailsAPI._fetch_customer_details_from_api(
            dispatched_device_page.page
        )

        # All added because on ui dropdown first option is All and then followed by customer list from api
        listofcust.insert(0, "All")

        logger.info(
            "Customer list fetched successfully from API | total customers=%s",
            len(listofcust),
        )

        logger.debug("Customer list fetched from API: %s", listofcust)

        for customer in listofcust:
            logger.info("Validating Select Customer dropdown value: %s", customer)

            dispatched_device_page.select_customer(customer)

            table = TableSection(dispatched_device_page.page)

            logger.debug(
                "Fetching table data for customer '%s' from Dispatched Device page",
                customer,
            )
            table_data = table.get_table_data()

            logger.debug(
                "Table data for customer '%s' extracted successfully | rows=%s | data=%s",
                customer,
                len(table_data),
                table_data,
            )

            expected_data_description = (
                f"Valid table data for customer '{customer}'"
                if table_data
                else "No Data Found message"
            )

            report_case(
                expected=expected_data_description,
                actual=table_data if table_data else "No Data Found",
                message=f"Validate table data for Select Customer '{customer}'",
            )

            if table_data:
                assert isinstance(
                    table_data, list
                ), f"Expected table data to be a list of dictionaries for customer '{customer}'"

                logger.info(
                    "Total rows received for validation for customer '%s': %s",
                    customer,
                    len(table_data),
                )

                for index, row in enumerate(table_data, start=1):
                    logger.info("Validating row %s for customer '%s'", index, customer)
                    logger.debug("Row %s data: %s", index, row)

                    assert isinstance(
                        row, dict
                    ), f"Expected row {index} data to be a dictionary for customer '{customer}'"

                    # Additional validations for row structure and content can be added here

                    logger.info(
                        "Row %s validated successfully for customer '%s'",
                        index,
                        customer,
                    )

    # Test the search functionality by entering a value in search box and validating the table data with that value if no data then with no data found message
    def test_search_functionality_dispatched_device_page(
        self, dispatched_device_page, report_case
    ):
        logger.info(
            "Starting validation of Search functionality on Dispatched Device page"
        )

        search_value = IMEI

        logger.debug("Entering search value '%s' in Search box", search_value)

        search_helper = SearchHelper(dispatched_device_page.page)
        result = search_helper.run_search(search_value)
        logger.debug(
            "Search results for query '%s': %s",
            search_value,
            result,
        )
        expected_result_description = (
            f"Search results containing '{search_value}'"
            if result["results_found"] > 0
            else "No Data Found message"
        )
        report_case(
            expected=expected_result_description,
            actual=(
                result["results"] if result["results_found"] > 0 else "No Data Found"
            ),
            message=f"Validate search results for query '{search_value}'",
        )
        if result["results_found"] > 0:
            assert result["success"], f"Search failed: {result['error']}"

            for row in result["results"]:
                assert (
                    search_value in row
                ), f"Expected search value '{search_value}' to be present in row: {row}"

            logger.info(
                "Search functionality validated successfully with %s results found",
                result["results_found"],
            )
        else:
            assert result["success"], f"Search failed: {result['error']}"

            logger.info(
                "Search functionality validated successfully with no results found"
            )

    ## Pagination test case should be added
    def test_pagination_dispatched_device_page(
        self, dispatched_device_page, report_case
    ):
        logger.info("Starting validation of pagination on Dispatched Device page")

        pagination_helper = PaginationHelper(
            page=dispatched_device_page.page,
            # page_input="input[aria-label='Page number']",
            # content_selector="//div[@class='component-body']",
            # total_pages_selector="//div[@class='pagination-info']",
            max_forward_steps=5,
        )

        result = pagination_helper.verify()

        logger.debug(
            "Pagination verification result: %s",
            result,
        )

        report_case(
            expected="Pagination works correctly across pages",
            actual=result,
        )

        assert result[
            "success"
        ], f"Pagination verification failed: {result.get('error', 'Unknown error')}"

        logger.info("Pagination on Dispatched Device page validated successfully")
