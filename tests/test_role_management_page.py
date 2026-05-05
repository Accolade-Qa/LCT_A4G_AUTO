from pages.common import TableSection, PaginationHelper
from utils.helpers import Helpers
from utils.logger import get_logger
from config.config import ROLE_MANAGEMENT_URL
import time

logger = get_logger(__name__)


class TestRoleManagementPage:

    def test_go_to_rolemanagementpage(self, page, role_management_page):
        logger.info("Navigating to Role Management page")
        role_management_page.go_to_rolemanagementpage(ROLE_MANAGEMENT_URL)

        assert (
            page.url == ROLE_MANAGEMENT_URL
        ), f"Expected URL to be '{ROLE_MANAGEMENT_URL}', got {page.url}"

    def test_role_management_page_elements(self, role_management_page):
        logger.info("Validating Role Management page elements")

        assert (
            role_management_page.is_page_loaded()
        ), "Role Management page did not load correctly"

        assert (
            role_management_page.is_add_role_button_visible()
        ), "Add Role button is not visible"

        assert role_management_page.is_role_table_visible(), "Role table is not visible"

        assert role_management_page.is_search_box_visible(), "Search box is not visible"

        logger.info("All Role Management page elements are present and visible")

    def test_add_Administrator_role(self, role_management_page):
        role_management_page.click_add_role()

        role_name = f"AdministratorTest{Helpers.generate_random_string(4)}"

        role_management_page.enter_role_name(role_name)
        role_management_page.select_role_type("Administrator")

        assert (
            not role_management_page.is_role_group_visible()
        ), "Role Group should NOT be visible for Administrator"

        role_management_page.select_permission("Dashboard", "select_all")

        role_management_page.enable_permission_group("Device Utility")
        role_management_page.select_sub_permission("Government Servers", "view")
        role_management_page.select_sub_permission("Government Servers", "create")

        role_management_page.click_save()

        # ✅ Wait + fetch message properly
        # message = role_management_page.get_success_message()

        # assert message == "Success", "Administrator role creation failed"

        # # ✅ Optional stability step
        # role_management_page.wait_for_snackbar_to_disappear()

    def test_add_manager_role_with_group(self, role_management_page):
        role_management_page.click_add_role()

        role_name = f"ManagerTest{Helpers.generate_random_string(4)}"

        role_management_page.enter_role_name(role_name)
        role_management_page.select_role_type("Manager")

        assert (
            role_management_page.is_role_group_visible()
        ), "Role Group should be visible for Manager"

        role_management_page.select_permission("Dashboard", "select_all")

        role_management_page.enable_permission_group("Device Utility")
        role_management_page.select_sub_permission("Government Servers", "view")
        role_management_page.select_sub_permission("Government Servers", "create")

        role_management_page.click_save()

    def test_manager_role_without_group(self, role_management_page):
        role_management_page.click_add_role()

        role_management_page.enter_role_name(
            f"ManagerNoGroup{Helpers.generate_random_string(4)}"
        )
        role_management_page.select_role_type("Manager")

        role_management_page.click_save()

        error = role_management_page.get_error_message()
        assert "Role Group is mandatory" in error

    def test_role_name_required(self, role_management_page):
        role_management_page.click_add_role()

        role_management_page.select_role_type("Administrator")
        role_management_page.click_save()

        error = role_management_page.get_input_box_error_message()
        assert " This field is mandatory." in error

    def test_invalid_role_name(self, role_management_page):
        role_management_page.click_add_role()

        role_management_page.enter_role_name("@@@###")
        role_management_page.select_role_type("Administrator")

        role_management_page.click_save()

        error = role_management_page.get_input_box_error_message()
        assert "Please enter a valid User Role." in error

    def test_select_all_permissions(self, role_management_page):
        role_management_page.click_add_role()

        role_name = f"FullAccess{Helpers.generate_random_string(4)}"

        role_management_page.enter_role_name(role_name)
        role_management_page.select_role_type("Administrator")

        role_management_page.select_all_permissions()
        role_management_page.click_save()

        assert (
            "Success" in role_management_page.get_success_message()
        ), "Select all permissions failed"

    def test_role_type_switch(self, role_management_page):
        role_management_page.click_add_role()

        role_management_page.select_role_type("Manager")
        assert role_management_page.is_role_group_visible()

        role_management_page.select_role_type("Administrator")
        assert not role_management_page.is_role_group_visible()

    def test_search_role(self, role_management_page):
        role_management_page.click_add_role()

        role_name = f"SearchTest{Helpers.generate_random_string(4)}"

        role_management_page.enter_role_name(role_name)
        role_management_page.select_role_type("Administrator")
        role_management_page.click_save()

        time.sleep(1)

        assert (
            "Success" in role_management_page.get_success_message()
        ), "Role creation failed for search test"

        # Wait for the new role to appear in the table
        time.sleep(1)

        assert (
            role_management_page.is_search_box_visible()
        ), "Search box is not visible for searching role"

        role_management_page.search_role(role_name)

        assert role_management_page.is_role_in_table(
            role_name
        ), f"Role '{role_name}' not found in search results"

    def test_table_data(self, role_management_page):
        logger.info("Validating role table data")

        assert role_management_page.is_role_table_visible(), "Role table is not visible"

        table_section = TableSection(role_management_page.page)
        row_count = table_section.get_row_count()

        # Handle empty table case
        if row_count == 0:
            logger.warning("No roles found in the table to validate data")
            assert table_section.has_no_data()
            return

        # Validate first row data
        first_row_data = role_management_page.get_table_row_data(0)

        assert (
            "Administrator" in first_row_data or "Manager" in first_row_data
        ), f"Unexpected role type in first row: {first_row_data}"

    def test_pagination_on_role_table(self, role_management_page):
        logger.info("Testing pagination on role table")

        pagination = PaginationHelper(
            role_management_page.page, content_selector="div.component-body table"
        )

        result = pagination.verify()

        logger.info(f"Pagination result: {result}")

        assert result["success"], f"Pagination failed: {result['error']}"
        assert result["total_pages"] >= 1

        # Optional: ensure multiple pages actually tested
        if result["total_pages"] > 1:
            assert len(result["pages_visited"]) > 1, "Pagination did not move forward"
