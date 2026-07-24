from utils.logger import get_logger
from pages.common_base_page import BasePage
from config.config import CUSTOMER_MASTER_URL

import pytest

logger = get_logger(__name__)

@pytest.mark.lct
@pytest.mark.sampark
@pytest.mark.swaraj
@pytest.mark.trio
class TestCustomerMaster:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting SIM Batch Data Details test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "SIM Batch Data Details test finished without call report: %s",
                test_name,
            )
        elif report.passed:
            logger.info("SIM Batch Data Details test passed: %s", test_name)
        elif report.failed:
            logger.error("SIM Batch Data Details test failed: %s", test_name)
            logger.debug(
                "SIM Batch Data Details failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("SIM Batch Data Details test skipped: %s", test_name)

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_page_navigation(self, customer_master, report_case):
        logger.info("Starting validation of Customer master page navigation")
        # wait for page to load and network idle
        customer_master.page.wait_for_load_state("networkidle")
        actual_url = customer_master.page.url
        logger.debug(
            "Customer master URL check | expected=%s | actual=%s",
            CUSTOMER_MASTER_URL,
            actual_url,
        )

        report_case(
            expected=CUSTOMER_MASTER_URL,
            actual=actual_url,
            message="Validate Customer master page navigation",
        )

        assert (
            actual_url == CUSTOMER_MASTER_URL
        ), f"Expected URL '{CUSTOMER_MASTER_URL}', got '{actual_url}'"
        logger.info("Successfully validated Customer Master page navigation")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_nav_list(self, customer_master, report_case):
        logger.info("Starting Test: Customer master navigation bar validation")

        is_enabled = customer_master._nav_list_enability()
        logger.info("Verifying navigation bar is enabled")

        if is_enabled:
            assert is_enabled, "The customer master navigation list failed"
            report_case(
                expected=True,
                actual=is_enabled,
                result="PASS",
                message="Validate Customer master nav list",
            )
            logger.info("Navigation bar is enabled: Test Passed")
        else:
            assert not is_enabled, "The customer master navigation list failed"
            report_case(
                expected=False,
                actual=is_enabled,
                result="FAIL",
                message="Validate Customer master nav list",
            )
            logger.info("Navigation bar is disabled: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_page_title(self, customer_master, report_case):
        logger.info("Starting Test: Customer master page title visibility validation")

        expected_title = "Customer Management"
        is_visible = customer_master._is_PageTitle_Visible()
        logger.info("Verifying page title is visible")
        base = BasePage(customer_master.page)

        if is_visible:
            assert is_visible, f"{expected_title} should be visible on the page"
            report_case(
                expected=expected_title,
                actual=base.get_title(),
                result="PASS",
                message="Validate Customer master page title",
            )
        else:
            assert not is_visible, f"{expected_title} should not be visible on the page"
            report_case(
                expected=expected_title,
                actual=base.get_title(),
                result="FAIL",
                message="Validate Customer master page title",
            )
        logger.info("Page title is visible: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_element_enability(
        self, customer_master, report_case
    ):
        logger.info("Starting Test: Customer master element enability validation")

        is_enabled = customer_master._element_enability()
        logger.info("Verifying elements are enabled")
        assert is_enabled

        if is_enabled: 
            report_case(
                expected=True,
                actual=is_enabled,
                result="PASS",
                message="Validate Customer master element enability",
            )

        else:
            report_case(
                expected=False,
                actual=is_enabled,
                result="FAIL",
                message="Validation of customer master element failed"
            )

        logger.info("Elements are enabled: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_add_customer(self, customer_master, report_case):
        logger.info(
            "Starting Test: Customer master add customer button functionality validation"
        )

        visibility = customer_master.page.get_by_text(
            "Add Customer", exact=True
        ).is_visible()
        click = customer_master._click_add_customer()
        logger.info("Verifying Add Customer button is clickable")
        assert click is None

        if visibility:
            report_case(
                expected=True,
                actual=visibility,
                result="PASS",
                message="Validate Customer master add customer",
            )
        else:
            report_case(
                expected=True,
                actual=visibility,
                result="FAIL",
                message="Validate Customer master add customer",
            )
        logger.info("Add Customer button is clickable and clicked")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_click_customer_name(
        self, customer_master, report_case
    ):
        logger.info("Starting Test: Customer name field validation")

        result = customer_master.customer_name_field()
        logger.debug("Validation results: %s", result)

        expected = {
            "name_blank_text": "This field is required and can't be empty.",
            "name_num_text": "Only alphabets and spaces are allowed.",
            "name_sp_char_text": "Only alphabets and spaces are allowed.",
            "name_space_text": "This field is required and can't be only spaces.",
            "name_char_space_text": "Remove leading or trailing spaces.",
        }

        actual = {
            "name_blank_text": result["name_blank_text"],
            "name_num_text": result["name_num_text"],
            "name_sp_char_text": result["name_sp_char_text"],
            "name_space_text": result["name_space_text"],
            "name_char_space_text": result["name_char_space_text"],
        }

        logger.info("Verifying Customer Name field validation messages")

        # Assertions
        assert actual["name_blank_text"] == expected["name_blank_text"]
        assert actual["name_num_text"] == expected["name_num_text"]
        assert actual["name_sp_char_text"] == expected["name_sp_char_text"]
        assert actual["name_space_text"] == expected["name_space_text"]
        assert actual["name_char_space_text"] == expected["name_char_space_text"]

        # Conditional reporting
        if actual == expected:
            report_case(
                expected=expected,
                actual=actual,
                result="PASS",
                message="Validate Customer master customer name field validation messages",
            )
        else:
            report_case(
                expected=expected,
                actual=actual,
                result="FAIL",
                message="Validate Customer master customer name field validation messages",
            )

        logger.info("Customer name field validation: Test Passed")

    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_customer_master_add_update_delete_flow(self, customer_master, report_case):
        logger.info("Starting Test: Customer Master add, update, and delete complete flow")
        # ----------------- Step 1: Add New Customer -----------------
        logger.info("Step 1: Adding new customer")
        customer_master.new_customer()

        toast_locator = customer_master.page.locator(
            "xpath=(//div[@class='mat-mdc-snack-bar-label mdc-snackbar__label'])[last()]"
        )
        toast_locator.wait_for(state="visible", timeout=5000)
        toast_text = toast_locator.inner_text().strip()
        expected_add_text = "Data Saved Successfully!!"

        if toast_text == expected_add_text:
            report_case(
                expected=expected_add_text,
                actual=toast_text,
                result="PASS",
                message="Validate Customer master new customer creation",
            )
        else:
            report_case(
                expected=expected_add_text,
                actual=toast_text,
                result="FAIL",
                message="Validate Customer master new customer creation",
            )
        assert toast_text == expected_add_text, f"Failed to add customer. Got: '{toast_text}'"
        logger.info("New customer added successfully: Step Passed")

        # Wait for the add toast to disappear to prevent overlapping with next toast
        toast_locator.wait_for(state="hidden", timeout=5000)

        # ----------------- Step 2: Search and Update Customer -----------------
        logger.info("Step 2: Searching and updating customer")
        customer_master.search_and_update_customer()

        toast_locator.wait_for(state="visible", timeout=5000)
        toast_text = toast_locator.inner_text().strip()
        expected_update_text = "Data Saved Successfully!!"

        if toast_text == expected_update_text:
            report_case(
                expected=expected_update_text,
                actual=toast_text,
                result="PASS",
                message="Validate Customer master search & update",
            )
        else:
            report_case(
                expected=expected_update_text,
                actual=toast_text,
                result="FAIL",
                message="Validate Customer master search & update",
            )
        assert toast_text == expected_update_text, f"Failed to update customer. Got: '{toast_text}'"
        logger.info("Customer updated successfully: Step Passed")

        # Wait for the update toast to disappear to prevent overlapping with next toast
        toast_locator.wait_for(state="hidden", timeout=5000)

        # ----------------- Step 3: Search and Delete Customer -----------------
        logger.info("Step 3: Searching and deleting customer")
        customer_master.search_and_delete_customer()

        toast_locator.wait_for(state="visible", timeout=5000)
        toast_text = toast_locator.inner_text().strip()
        expected_delete_text = "Data Deleted Successfully!!"

        if toast_text == expected_delete_text:
            report_case(
                expected=expected_delete_text,
                actual=toast_text,
                result="PASS",
                message="Validate Customer master search & delete",
            )
        else:
            report_case(
                expected=expected_delete_text,
                actual=toast_text,
                result="FAIL",
                message="Validate Customer master search & delete",
            )
        assert toast_text == expected_delete_text, f"Failed to delete customer. Got: '{toast_text}'"
        logger.info("Customer deleted successfully: Step Passed")

    # Validate table headers
    # Validate table data 
    # Validate table data with no data message
    # Validate pagination
    


    # Have to test the whole flow like add customer, then validate into the list of customers, then validate the whole list of customers in various places,
    # then, come back to customer master page and then update one customer that is added earlier, then again test that will changes on those locations, then 
    # delete it.. and finally cross check on the list that is deleted successfully. 
    # for this we have to use multi window concept to go back and forth into tabs or windows to check and validate 
    ''' customers dropdown list appears of these places 
        1. On dashboard
        2. On dispatch device page - here i have dropdown on table header and a coloumn in the dispatch device list
        3. On dispatched device - manual upload page 
    '''