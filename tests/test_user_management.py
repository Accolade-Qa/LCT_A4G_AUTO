from utils.logger import get_logger

# from pages.base_page import BasePage
from pages.user_management import UserManagementPage
from pages.login_page import LoginPage

import pytest
from config.config import (
    BASE_URL,
    USER_MANAGEMENT_URL,
    PASSWORD,
    USERNAME,
)

logger = get_logger(__name__)


class TestUsermanagement:

    def _login_and_dashboard(self, page):
        login_page = LoginPage(page)
        login_page.load(BASE_URL)
        login_page.login(USERNAME, PASSWORD)

        return UserManagementPage(page)

    def test_go_to_user(self, page, report_case):
        logger.info("Starting validation of User Management page navigation")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)

        actual_url = page.url
        logger.debug(
            "User Management URL check | expected=%s | actual=%s",
            USER_MANAGEMENT_URL,
            actual_url,
        )

        report_case(
            expected=USER_MANAGEMENT_URL,
            actual=actual_url,
            message="Validate User Management page navigation",
        )

        assert (
            actual_url == USER_MANAGEMENT_URL
        ), f"Expected URL '{USER_MANAGEMENT_URL}', got '{actual_url}'"
        logger.info("Successfully validated User Management page navigation")

    def test_user_management_nav_list_enability(
        self, user_management, report_case, page
    ):
        logger.info("Testing navbar list enability on user management page")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        enabled = user_management._nav_list_enability()
        report_case(expected=False, actual=enabled)
        logger.info("Navbar list enability result: %s", enabled)
        assert enabled, "Navbar list is not enabled"
        logger.info("Navbar list enability test passed successfully")

    def test_user_management_is_PageTitle_Visible(
        self, user_management, report_case, page
    ):
        logger.info("Testing page title visibility on user management page")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        expected_title = "User Management"
        actual_title = user_management.get_title()
        logger.info(
            "Expected page title: '%s', Actual page title: '%s'",
            expected_title,
            actual_title,
        )

        report_case(expected=expected_title, actual=actual_title)
        assert (
            actual_title == expected_title
        ), f"Expected title to be '{expected_title}', got '{actual_title}'"
        logger.info("Page title visibility test passed successfully")

    def test_user_management_element_enability(
        self, user_management, report_case, page
    ):
        logger.info("Testing element enability on user management page")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        ele_enabled = user_management._element_enability()

        report_case(expected=True, actual=ele_enabled)
        logger.info("Element enability result: %s", ele_enabled)

        assert ele_enabled, "Elements not enabled"
        logger.info("Element enability test passed successfully")

    def test_user_management_click_add_user(self, user_management, page):
        logger.info("Testinng click add user functionality")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        user_management._click_add_user()
        logger.info("Clicked add user button successfully")

    def test_usermanagement_user_type_drop(self, user_management, report_case, page):
        logger.info("Starting test: User type dropdown validation")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        error_msg = user_management.user_type_drop()
        logger.debug("User type dropdown validation result: %s", error_msg)
        error_text = user_management.page.locator("#mat-select-value-1:visible")
        visible = error_text.text_content()

        report_case(
            expected="This field is mandatory.",
            actual=visible,
            result="Pass" if visible == "This field is mandatory." else "Fail",
            message="Validate user type dropdown error message",
        )
        logger.info("Verifying user type dropdown validation message")
        assert (
            error_msg["result_drop_text"] == "This field is mandatory."
        ), f"Expected error message to be 'This field is mandatory.', got '{error_msg["result_drop_text"]}'"
        logger.info("User type dropdown validation test passed")

    def test_first_name_field(self, user_management, report_case, page):
        logger.info("Starting test: First name field validation")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        result = user_management.first_name_field()
        logger.debug("First name field validation results: %s", result)
        validations = {
            "name_blank_text": {
                "expected": "This field is required and can't be empty.",
                "message": "Validate blank first name field",
            },
            "name_num_text": {
                "expected": "Only alphabets and spaces are allowed.",
                "message": "Validate numeric input in first name field",
            },
            "name_sp_char_text": {
                "expected": "Only alphabets and spaces are allowed.",
                "message": "Validate special characters in first name field",
            },
            "name_space_text": {
                "expected": "This field is required and can't be only spaces.",
                "message": "Validate spaces-only first name field",
            },
            "name_char_space_text": {
                "expected": "Remove leading or trailing spaces.",
                "message": "Validate leading/trailing spaces in first name field",
            },
        }

        for key, data in validations.items():
            logger.info("Verifying validation message for: %s", key)
            actual = result[key]
            logger.debug("Expected: %s | Actual: %s", data["expected"], actual)
        report_case(expected=data["expected"], actual=actual, message=data["message"])

        assert actual == data["expected"]
        logger.info("First name field validation test passed")

    def test_last_name_field(self, user_management, report_case, page):
        logger.info("Starting test: Last name field validation")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        result = user_management.last_name_field()
        logger.debug("Last name field validation results: %s", result)
        validations = {
            "last_name_blank_text": {
                "expected": "This field is required and can't be empty.",
                "message": "Validate blank last name field",
            },
            "last_name_num_text": {
                "expected": "Only alphabets and spaces are allowed.",
                "message": "Validate numeric input in last name field",
            },
            "last_name_sp_char_text": {
                "expected": "Only alphabets and spaces are allowed.",
                "message": "Validate special characters in last name field",
            },
            "last_name_space_text": {
                "expected": "This field is required and can't be only spaces.",
                "message": "Validate spaces-only last name field",
            },
            "last_name_char_space_text": {
                "expected": "Remove leading or trailing spaces.",
                "message": "Validate leading/trailing spaces in last name field",
            },
        }

        for key, data in validations.items():
            logger.info("Verifying validation message for: %s", key)
            actual = result[key]
            logger.debug("Expected: %s | Actual: %s", data["expected"], actual)
        report_case(expected=data["expected"], actual=actual, message=data["message"])

        assert actual == data["expected"]
        logger.info("Last name field validation test passed")

    def test_email_field(self, user_management, report_case, page):
        logger.info("Starting test: Email field validation")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        result = user_management.email_field()
        logger.debug("Email field validation results: %s", result)
        validations = {
            "email_blank_text": {
                "expected": "This field is required and can't be empty.",
                "message": "Validate blank email field",
            },
            "email_num_text": {
                "expected": "Please enter a valid Email ID.",
                "message": "Validate numeric input in email field",
            },
            "email_sp_char_text": {
                "expected": "Please enter a valid Email ID.",
                "message": "Validate special characters in email field",
            },
            "email_space_text": {
                "expected": "This field is required and can't be only spaces.",
                "message": "Validate spaces-only email field",
            },
            "email_char_space_text": {
                "expected": "Please enter a valid Email ID.",
                "message": "Validate leading/trailing spaces in email field",
            },
        }

        for key, data in validations.items():
            logger.info("Verifying validation message for: %s", key)
            actual = result[key]
            logger.debug("Expected: %s | Actual: %s", data["expected"], actual)
        report_case(expected=data["expected"], actual=actual, message=data["message"])

        assert actual == data["expected"]
        logger.info("Email field validation test passed")

    def test_mob_no_field(self, user_management, report_case, page):

        logger.info("Starting test: Mobile number field validation")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        result = user_management.mob_no_field()
        logger.debug("Mobile number field validation results: %s", result)
        validations = {
            "mob_blank_text": {
                "expected": "Mobile number is required.",
                "message": "Validate blank mobile number field",
            },
            "mob_num_text": {
                "expected": "Enter a valid mobile number.",
                "message": "Validate numeric input in mobile number field",
            },
            "mob_sp_char_text": {
                "expected": "Enter a valid mobile number.",
                "message": "Validate special characters in mobile number field",
            },
            "mob_space_text": {
                "expected": "Mobile number is required.",
                "message": "Validate spaces-only mobile number field",
            },
            "mob_char_space_text": {
                "expected": "Enter a valid mobile number.",
                "message": "Validate leading/trailing spaces in mobile number field",
            },
        }

        for key, data in validations.items():
            logger.info("Verifying validation message for: %s", key)
            actual = result[key]
            logger.debug("Expected: %s | Actual: %s", data["expected"], actual)
        report_case(expected=data["expected"], actual=actual, message=data["message"])

        assert actual == data["expected"]
        logger.info("Mobile number field validation test passed")

    def test_country_field(self, user_management, report_case, page):

        logger.info("Starting test: Country field validation")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        result = user_management.country_field()
        logger.debug("Country field validation results: %s", result)
        validations = {
            "con_blank_text": {
                "expected": "This field is required and can't be empty.",
                "message": "Validate blank country field",
            },
            "con_num_text": {
                "expected": "Only alphabets and spaces are allowed.",
                "message": "Validate numeric input in country field",
            },
            "con_sp_char_text": {
                "expected": "Only alphabets and spaces are allowed.",
                "message": "Validate special characters in country field",
            },
            "con_space_text": {
                "expected": "This field is required and can't be only spaces.",
                "message": "Validate spaces-only country field",
            },
            "con_char_space_text": {
                "expected": "Remove leading or trailing spaces.",
                "message": "Validate leading/trailing spaces in country field",
            },
        }

        for key, data in validations.items():

            logger.info("Verifying validation message for: %s", key)

            actual = result[key]
            logger.debug("Expected: %s | Actual: %s", data["expected"], actual)

        report_case(expected=data["expected"], actual=actual, message=data["message"])

        assert actual == data["expected"]

        logger.info("Country field validation test passed")

    def test_state_field(self, user_management, report_case, page):

        logger.info("Starting test: State field validation")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        result = user_management.state_field()

        logger.debug("State field validation results: %s", result)

        validations = {
            "state_blank_text": {
                "expected": "This field is required and can't be empty.",
                "message": "Validate blank state field",
            },
            "state_num_text": {
                "expected": "Only alphabets and spaces are allowed.",
                "message": "Validate numeric input in state field",
            },
            "state_sp_char_text": {
                "expected": "Only alphabets and spaces are allowed.",
                "message": "Validate special characters in state field",
            },
            "state_space_text": {
                "expected": "This field is required and can't be only spaces.",
                "message": "Validate spaces-only state field",
            },
            "state_char_space_text": {
                "expected": "Remove leading or trailing spaces.",
                "message": "Validate leading/trailing spaces in state field",
            },
        }

        for key, data in validations.items():

            logger.info("Verifying validation message for: %s", key)

            actual = result[key]

        logger.debug("Expected: %s | Actual: %s", data["expected"], actual)

        report_case(expected=data["expected"], actual=actual, message=data["message"])

        assert actual == data["expected"]

        logger.info("State field validation test passed")

    def test_usermanagement_status_field(self, user_management, report_case, page):

        logger.info("Starting test: User management status field validation")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        error_msg = user_management.status_field()

        logger.debug("Status field validation result: %s", error_msg)

        error_text = user_management.page.locator("#mat-select-value-1:visible")

        visible = error_text.text_content().strip()

        logger.debug("Captured dropdown text: %s", visible)

        report_case(
            expected="This field is mandatory.",
            actual=visible,
            result="Pass" if visible == "This field is mandatory." else "Fail",
            message="Validate user type dropdown error message",
        )

        logger.info("Verifying status field validation message")

        assert (
            error_msg["status_locator_text"]
            == "This field is required and can't be empty."
        ), (
            "Expected error message to be "
            "'This field is required and can't be empty.', "
            f"got '{error_msg['status_locator_text']}'"
        )

        logger.info("Status field validation test passed")

    def test_usermanagement_new_flow(self, user_management, report_case, page):
        logger.info("Starting test: Test usermanagement new flow.")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        user_management.new_flow()
        logger.info("Completed usermanagement new flow, validating results.")
        toast = user_management.page.locator(
            "//div[contains(@class,'mat-mdc-snack-bar-label mdc-snackbar__label')]"
        )
        toast_text = toast.text_content().strip()

        report_case(
            expected="Data Fetched Successfully",
            actual=toast_text,
            result="Pass" if toast_text == "Data Fetched Successfully" else "Fail",
            message="Validate new user flow",
        )
        logger.info(f"Toast message after new user flow: '{toast_text}'")
        assert (
            toast_text == "Data Fetched Successfully"
        ), f"Expected toast message to be 'Data Fetched Successfully', got '{toast_text}'"

    def test_usermanagement_update_flow(self, user_management, report_case, page):

        logger.info("Starting Test: Test user management update flow")
        user_page = self._login_and_dashboard(page)
        user_page.go_to_user(USER_MANAGEMENT_URL)
        user_management.update_flow()
        logger.info("Completed usermanagement new flow, validating results.")
        toast = user_management.page.locator(
            "//div[contains(@class,'mat-mdc-snack-bar-label mdc-snackbar__label')]"
        )
        toast_text = toast.text_content().strip()

        report_case(
            expected="Data Fetched Successfully",
            actual=toast_text,
            result=(
                "Pass"
                if toast_text == "Data Fetched Successfully"
                else "Fail"
            ),
            message="Validate new user flow",
        )
        logger.info(f"Toast message after update user flow: '{toast_text}'")
        assert (
            toast_text == "Data Fetched Successfully"
        ), f"Expected toast message to be 'Data Fetched Successfully', got '{toast_text}'"
