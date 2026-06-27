from config.config import API_BASE_URL, ROLE_MANAGEMENT_URL, API_PASSWORD, API_USERNAME
from pages.api.api_client import APIClient
from pages.common_utils import TableSection, PaginationHelper
from utils.helpers import Helpers
from utils.logger import get_logger
import time
import pytest

logger = get_logger(__name__)


@pytest.mark.critical
@pytest.mark.regression
@pytest.mark.atcu
@pytest.mark.lct
@pytest.mark.sampark
@pytest.mark.swaraj
@pytest.mark.trio
class TestRoleManagementPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Role Management test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Role Management test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Role Management test passed: %s", test_name)
        elif report.failed:
            logger.error("Role Management test failed: %s", test_name)
            logger.debug(
                "Role Management failure details for %s: %s", test_name, report.longrepr
            )
        elif report.skipped:
            logger.warning("Role Management test skipped: %s", test_name)

    """" Test for deleting roles from the role management page. """

    def test_delete_role_management_roles(self, role_management_page):
        """Test deleting a role permission."""

        logger.info("Testing delete role permission functionality")

        if "sampark-qa" in API_BASE_URL:
            endpoint = "/api/roles/getRoles?page=0&size=1000&search=&userRole="
        else:
            endpoint = "/roles/getRoles?page=0&size=1000&search=&userRole="

        # first call get all item i.e. roles by get all roles count from the role management page
        response = APIClient.send_request(
            role_management_page.page,
            API_BASE_URL,
            API_USERNAME,
            API_PASSWORD,
            "GET",
            endpoint,
        )
        total_roles = response.get("totalItems", 0)

        for i in range(1, total_roles + 1):
            if "sampark-qa" in API_BASE_URL:
                endpoint = f"/api/roles/deleteRole?roleId={i}"
            else:
                endpoint = f"/roles/deleteRole?roleId={i}"

            try:
                response = APIClient.send_request(
                    role_management_page.page,
                    API_BASE_URL,
                    API_USERNAME,
                    API_PASSWORD,
                    "DELETE",
                    endpoint,
                )

                assert (
                    response.get("message") == "Success"
                ), f"Failed to delete permission for role group {i}"

                logger.info("Deleted role group %s successfully", i)

            except Exception as e:

                error_message = str(e)

                if (
                    "Cannot delete role: Role is assigned to one or more users."
                    in error_message
                ):
                    logger.warning(
                        "Cannot delete role group %s: Role is assigned to users",
                        i,
                    )
                    continue

                logger.error(
                    "Unexpected error while deleting role group %s: %s",
                    i,
                    error_message,
                )
                raise

        logger.info("Delete role management test completed")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_role_management_page_navigates_correctly(
        self, page, role_management_page, report_case
    ):
        logger.info("Navigating to Role Management page")
        role_management_page.go_to_rolemanagementpage(ROLE_MANAGEMENT_URL)
        logger.debug(
            "Role Management URL check | expected=%s | actual=%s",
            ROLE_MANAGEMENT_URL,
            page.url,
        )
        report_case(expected=ROLE_MANAGEMENT_URL, actual=page.url)

        assert (
            page.url == ROLE_MANAGEMENT_URL
        ), f"Expected URL to be '{ROLE_MANAGEMENT_URL}', got {page.url}"

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_role_management_page_all_elements_are_visible(
        self, role_management_page, report_case
    ):
        logger.info("Validating Role Management page elements")

        page_loaded = role_management_page.is_page_loaded()
        add_role_visible = role_management_page.is_add_role_button_visible()
        table_visible = role_management_page.is_role_table_visible()
        search_visible = role_management_page.is_search_box_visible()
        report_case(
            expected="Page loaded=True, Add Role visible=True, table visible=True, search visible=True",
            actual=(
                f"Page loaded={page_loaded}, Add Role visible={add_role_visible}, "
                f"table visible={table_visible}, search visible={search_visible}"
            ),
        )

        assert page_loaded, "Role Management page did not load correctly"

        assert add_role_visible, "Add Role button is not visible"

        assert table_visible, "Role table is not visible"

        assert search_visible, "Search box is not visible"

        logger.info("All Role Management page elements are present and visible")

    @pytest.mark.regression
    def test_role_management_page_form_creates_administrator_role(
        self, role_management_page, report_case
    ):
        logger.info("Creating Administrator role")
        role_management_page.click_add_role()

        role_name = f"AdministratorTest{Helpers.generate_random_string(4)}"
        logger.debug("Generated Administrator role name: %s", role_name)

        role_management_page.enter_role_name(role_name)
        role_management_page.select_role_type("Administrator")
        logger.debug("Selected role type: Administrator")

        role_group_visible = role_management_page.is_role_group_visible()
        report_case(
            expected="Role Group visible=False for Administrator role",
            actual=f"Role name={role_name}, role group visible={role_group_visible}",
        )
        assert (
            not role_group_visible
        ), "Role Group should NOT be visible for Administrator"
        logger.debug("Role group field hidden for Administrator as expected")

        role_management_page.select_permission("Dashboard", "select_all")
        logger.debug("Selected Dashboard select_all permission")

        role_management_page.enable_permission_group("Device Utility")
        role_management_page.select_sub_permission("Government Servers", "view")
        role_management_page.select_sub_permission("Government Servers", "create")
        logger.debug("Selected Device Utility government server permissions")

        role_management_page.click_save()
        logger.info("Submitted Administrator role creation form: %s", role_name)

    @pytest.mark.regression
    def test_role_management_page_form_creates_manager_role_with_group(
        self, role_management_page, report_case
    ):
        logger.info("Creating Manager role with group")
        role_management_page.click_add_role()

        role_name = f"ManagerTest{Helpers.generate_random_string(4)}"
        logger.debug("Generated Manager role name: %s", role_name)

        role_management_page.enter_role_name(role_name)
        role_management_page.select_role_type("Manager")
        role_management_page.select_role_group("Software")
        logger.debug("Selected role type Manager and role group Software")

        role_group_visible = role_management_page.is_role_group_visible()
        report_case(
            expected="Role Group visible=True for Manager role",
            actual=f"Role name={role_name}, role group visible={role_group_visible}",
        )
        assert role_group_visible, "Role Group should be visible for Manager"

        role_management_page.select_permission("Dashboard", "select_all")

        role_management_page.enable_permission_group("Device Utility")

        # Select sub-permissions only if they are not disabled
        if not role_management_page.is_sub_permission_disabled(
            "Government Servers", "view"
        ):
            role_management_page.select_sub_permission("Government Servers", "view")

        if not role_management_page.is_sub_permission_disabled(
            "Government Servers", "create"
        ):
            role_management_page.select_sub_permission("Government Servers", "create")

        role_management_page.click_save()
        logger.info("Submitted Manager role creation form: %s", role_name)

    @pytest.mark.regression
    def test_role_management_page_form_creates_manager_role_without_group(
        self, role_management_page, report_case
    ):
        logger.info("Validating Manager role requires role group")
        role_management_page.click_add_role()

        role_name = f"ManagerNoGroup{Helpers.generate_random_string(4)}"
        logger.debug("Generated Manager role without group name: %s", role_name)
        role_management_page.enter_role_name(role_name)
        role_management_page.select_role_type("Manager")

        role_management_page.click_save()

        error = role_management_page.get_error_message()
        logger.debug("Role group mandatory error text: %s", error)
        report_case(expected="Role Group is mandatory", actual=error)
        assert "Role Group is mandatory" in error

    @pytest.mark.regression
    def test_role_management_page_form_shows_error_when_role_name_empty(
        self, role_management_page, report_case
    ):
        logger.info("Validating role name required error")
        role_management_page.click_add_role()

        role_management_page.select_role_type("Administrator")
        role_management_page.click_save()

        error = role_management_page.get_input_box_error_message()
        logger.debug("Role name required error text: %s", error)
        report_case(expected=" This field is mandatory.", actual=error)
        assert " This field is mandatory." in error

    @pytest.mark.regression
    def test_role_management_page_form_shows_error_for_invalid_role_name(
        self, role_management_page, report_case
    ):
        logger.info("Validating invalid role name error")
        role_management_page.click_add_role()

        role_management_page.enter_role_name("@@@###")
        role_management_page.select_role_type("Administrator")

        role_management_page.click_save()

        error = role_management_page.get_input_box_error_message()
        logger.debug("Invalid role name error text: %s", error)
        report_case(expected="Please enter a valid User Role.", actual=error)
        assert "Please enter a valid User Role." in error

    @pytest.mark.regression
    def test_role_management_page_form_allows_selecting_all_permissions(
        self, role_management_page, report_case
    ):
        logger.info("Creating Administrator role with all permissions selected")
        role_management_page.click_add_role()

        role_name = f"FullAccess{Helpers.generate_random_string(4)}"
        logger.debug("Generated full access role name: %s", role_name)

        role_management_page.enter_role_name(role_name)
        role_management_page.select_role_type("Administrator")

        role_management_page.select_all_permissions()
        logger.debug("Selected all permissions")
        role_management_page.click_save()

        success_message = role_management_page.get_success_message()
        logger.debug("Select all permissions success message: %s", success_message)
        report_case(expected="Success", actual=success_message)
        assert "Success" in success_message, "Select all permissions failed"

    @pytest.mark.regression
    def test_role_management_page_form_role_type_toggle_works(
        self, role_management_page, report_case
    ):
        logger.info("Validating role group visibility when switching role type")
        role_management_page.click_add_role()

        role_management_page.select_role_type("Manager")
        logger.debug("Selected Manager role type")
        manager_group_visible = role_management_page.is_role_group_visible()
        assert manager_group_visible

        role_management_page.select_role_type("Administrator")
        logger.debug("Selected Administrator role type")
        admin_group_visible = role_management_page.is_role_group_visible()
        report_case(
            expected="Manager role group visible=True, Administrator role group visible=False",
            actual=(
                f"Manager role group visible={manager_group_visible}, "
                f"Administrator role group visible={admin_group_visible}"
            ),
        )
        assert not admin_group_visible

    @pytest.mark.regression
    def test_role_management_page_table_search_finds_roles(
        self, role_management_page, report_case
    ):
        logger.info("Creating and searching role")
        role_management_page.click_add_role()

        role_name = f"SearchTest{Helpers.generate_random_string(4)}"
        logger.debug("Generated searchable role name: %s", role_name)

        role_management_page.enter_role_name(role_name)
        role_management_page.select_role_type("Administrator")
        role_management_page.click_save()

        time.sleep(1)

        success_message = role_management_page.get_success_message()
        logger.debug("Role creation success message: %s", success_message)
        assert "Success" in success_message, "Role creation failed for search test"

        assert (
            role_management_page.is_search_box_visible()
        ), "Search box is not visible for searching role"

        role_management_page.search_role(role_name)
        logger.debug("Executed role search for: %s", role_name)

        role_found = role_management_page.is_role_in_table(role_name)
        report_case(
            expected=f"Role '{role_name}' should be found in search results",
            actual=f"success_message={success_message}, role_found={role_found}",
        )
        assert role_found, f"Role '{role_name}' not found in search results"

    @pytest.mark.regression
    def test_role_management_page_table_displays_valid_role_data(
        self, role_management_page, report_case
    ):
        logger.info("Validating role table data")

        assert role_management_page.is_role_table_visible(), "Role table is not visible"

        table_section = TableSection(role_management_page.page)
        row_count = table_section.get_row_count()
        logger.debug("Role Management table row count: %s", row_count)

        # Handle empty table case
        if row_count == 0:
            logger.warning("No roles found in the table to validate data")
            report_case(
                expected="No data message should be visible", actual="Row count=0"
            )
            assert table_section.has_no_data()
            return

        # Validate first row data
        first_row_data = role_management_page.get_table_row_data(0)
        logger.debug("Role Management first row data: %s", first_row_data)
        report_case(
            expected="First row should contain Administrator or Manager role type",
            actual=first_row_data,
        )

        assert (
            "Administrator" in first_row_data or "Manager" in first_row_data
        ), f"Unexpected role type in first row: {first_row_data}"

    @pytest.mark.regression
    def test_role_management_page_table_pagination_navigates_across_pages(
        self, role_management_page, report_case
    ):
        logger.info("Testing pagination on role table")

        pagination = PaginationHelper(
            role_management_page.page, content_selector="div.component-body table"
        )

        result = pagination.verify()

        logger.info("Pagination result: %s", result)
        logger.debug("Role Management pagination raw result: %s", result)
        report_case(
            expected="Pagination success=True and total pages >= 1",
            actual=result,
            message=result.get("error", ""),
        )

        assert result["success"], f"Pagination failed: {result['error']}"
        assert result["total_pages"] >= 1

        # Optional: ensure multiple pages actually tested
        if result["total_pages"] > 1:
            assert len(result["pages_visited"]) > 1, "Pagination did not move forward"
