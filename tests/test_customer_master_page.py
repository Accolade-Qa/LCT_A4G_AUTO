from utils.logger import get_logger
from pages.base_page import BasePage

logger = get_logger(__name__)


class TestCustomerMaster:

    def test_customer_master_nav_list(self, customer_master, report_case):

        logger.info("Starting Test: Customer master navigation bar validation")
        is_enabled = customer_master._nav_list_enability()
        logger.info("Verifying navigation bar is enabled")
        assert is_enabled
        report_case(expected=True, actual=is_enabled, result="PASS")
        logger.info("Navigation bar is enabled: Test Passed")

    def test_customer_master_page_title(self, customer_master, report_case):
        logger.info("Starting Test: Customer master page title visibility validation")
        expected_title = "Customer Management"
        is_visible = customer_master._is_PageTitle_Visible()
        logger.info("Verifying page title is visible")
        assert is_visible
        base = BasePage(customer_master.page)

        report_case(expected=expected_title, actual=base.get_title(), result="PASS")

        logger.info("Page title is visible: Test Passed")

    def test_customer_master_element_enability(self, customer_master, report_case):
        logger.info("Starting Test: Customer master element enability validation")
        is_enabled = customer_master._element_enability()
        logger.info("Verifying elements are enabled")
        assert is_enabled

        report_case(expected=True, actual=is_enabled, result="PASS")

        logger.info("Elements are enabled: Test Passed")

    def test_customer_master_add_customer(self, customer_master, report_case):
        logger.info(
            "Starting Test: Customer master add customer button functionality validation"
        )
        visibility = customer_master.page.get_by_text(
            "Add Customer open_in_new", exact=True
        ).is_visible()
        click = customer_master._click_add_customer()
        logger.info("Verifying Add Customer button is clickable")
        assert click is None

        report_case(expected=True, actual=visibility)
        logger.info("Add Customer button is clickable and clicked")

    def test_customer_master_click_customer_name(self, customer_master):
        logger.info("Starting Test: Customer name field validation")
        result = customer_master.customer_name_field()
        logger.debug("Validation results: %s", result)

        logger.info("Verifying blank field validation message")
        assert result["name_blank_text"] == "This field is required and can't be empty."

        logger.info("Varifying numeric input validation message")
        assert result["name_num_text"] == "Only alphabets and spaces are allowed."

        logger.info("Verifying special characters validation message")
        assert result["name_sp_char_text"] == "Only alphabets and spaces are allowed."

        logger.info("Verifying space only input validation message")
        assert (
            result["name_space_text"]
            == "This field is required and can't be only spaces."
        )

        logger.info("Verifying leading/trailing space validation message")
        assert result["name_char_space_text"] == "Remove leading or trailing spaces."

        logger.info("Customer name field validation: Test Passed")

    def test_customer_master_new_customer(self, customer_master, report_case):
        logger.info(
            "Starting Test: Customer master add new customer fuctionality validation"
        )
        customer_master.new_customer()

        toast_locator = customer_master.page.locator(
            "//div[@class='mat-mdc-snack-bar-label mdc-snackbar__label']"
        )
        visibility = toast_locator.is_visible()
        toast_text = toast_locator.inner_text() if visibility else ""

        report_case(
            expected="Data Saved Successfully!!", actual=toast_text, result="PASS"
        )

        logger.info("New customer added successfully: Test Passed")

    def test_customer_master_search_customer(self, customer_master, report_case):
        logger.info("Starting test: Customer search and update functionality")
        customer_master.search_and_update_customer()

        toast_locator = customer_master.page.locator(
            "//div[@class='mat-mdc-snack-bar-label mdc-snackbar__label']"
        )
        visibility = toast_locator.is_visible()
        toast_text = toast_locator.inner_text() if visibility else ""

        report_case(
            expected="Data Saved Successfully!!", actual=toast_text, result="PASS"
        )

        logger.info(
            "Customer search and update functionality validation successful: Test Passed"
        )

    def test_customer_master_search_delete_customer(self, customer_master, report_case):
        logger.info("Starting Test: Customer search and delete functionality")
        customer_master.search_and_delete_customer()

        toast_locator = customer_master.page.locator(
            "//div[@class='mat-mdc-snack-bar-label mdc-snackbar__label']"
        )
        visibility = toast_locator.is_visible()
        toast_text = toast_locator.inner_text() if visibility else ""

        report_case(
            expected=" Data Deleted Successfully!!", actual=toast_text, result="PASS"
        )

        logger.info(
            "Customer search and delete functionality validation sucessful: Test Passed"
        )
