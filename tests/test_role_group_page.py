from utils.helpers import Helpers
from pages.common import TableSection, PaginationHelper, SearchHelper
from utils.logger import get_logger
import re
from datetime import datetime

logger = get_logger(__name__)


class TestRoleGroupPage:
    group = f"Test{Helpers.generate_random_string(4)}"

    def test_role_group_page_title(self, role_group_page):
        logger.info("Testing Role Group page title")
        title = role_group_page.get_title()
        assert (
            title == "Group Management"
        ), f"Expected page title 'Group Management', but got '{title}'"

    def test_role_group_page_elements(self, role_group_page):
        logger.info("Testing Role Group page elements")
        assert (
            role_group_page.is_page_loaded()
        ), "Role Group page did not load correctly"

        assert (
            role_group_page.is_add_group_button_visible()
        ), "Add Group button is not visible"

        assert (
            role_group_page.is_role_group_table_visible()
        ), "Role Group table is not visible"

        assert role_group_page.is_search_box_visible(), "Search box is not visible"

        logger.info("All Role Group page elements are present and visible")

    def test_go_to_add_group_page_and_validate(self, role_group_page):
        logger.info("Testing navigation to Add Group page")

        if role_group_page.is_add_group_button_visible():
            role_group_page.click_add_group()

        assert role_group_page.page.url.endswith(
            "/role-group"
        ), f"Expected URL to end with '/role-group', but got '{role_group_page.page.url}'"

        assert (
            role_group_page.get_component_title() == "Add Group"
        ), "Add Group page did not load correctly"

    def test_input_box_errors_on_different_inputs(self, role_group_page):
        logger.info("Testing input box errors on different inputs")

        role_group_page.click_add_group()

        # Test empty input
        role_group_page.enter_role_group_name("")
        role_group_page.click_save()
        error_message = role_group_page.get_input_box_error_message()
        assert (
            error_message == "This field is required and can't be empty."
        ), f"Expected error message 'Group Name is required', but got '{error_message}'"

        # Test input with only spaces
        role_group_page.enter_role_group_name("   ")
        role_group_page.click_save()
        error_message = role_group_page.get_input_box_error_message()
        assert (
            error_message == "This field is required and can't be only spaces."
        ), f"Expected error message 'Group Name is required', but got '{error_message}'"

        # Test special characters
        role_group_page.enter_role_group_name("@#$%^&*")
        role_group_page.click_save()
        error_message = role_group_page.get_input_box_error_message()
        assert (
            error_message == "Only alphabets and spaces are allowed."
        ), f"Expected error message 'Group Name is required', but got '{error_message}'"

        # Test valid input
        role_group_page.enter_role_group_name(self.group)
        role_group_page.click_save()
        error_message = role_group_page.get_input_box_error_message()
        assert error_message is None, f"Unexpected error message '{error_message}'"
        assert (
            "Success" in role_group_page.get_success_message()
        ), "Expected success message not found"

    def test_search_functionality_on_role_group_table(self, role_group_page):
        logger.info("Testing search functionality on Role Group table")

        assert (
            role_group_page.is_role_group_table_visible()
        ), "Role Group table is not visible"

        # Search for the group created in previous test
        role_group_page.page.get_by_placeholder("Search and Press Enter").fill(
            self.group
        )
        role_group_page.page.keyboard.press("Enter")

        # Wait for search results to load
        role_group_page.page.wait_for_timeout(1000)

        # Check if the group is found in the table
        table = TableSection(role_group_page.page)
        rows = table.get_rows()
        assert any(
            self.group in row for row in rows
        ), f"Group '{self.group}' not found in search results"

    def test_table_data_validation(self, role_group_page):
        logger.info("Validating Role Group table data")

        table = TableSection(role_group_page.page)

        assert role_group_page.is_role_group_table_visible()

        row_count = table.get_row_count()

        if row_count == 0:
            logger.warning("Table is empty")
            assert table.has_no_data()
            return

        rows = table.get_rows()
        assert len(rows) > 0

        logger.info(f"First row data: {rows[0]}")
        assert any(
            keyword in rows[0] for keyword in ["Admin", "Manager", "Test", "Software"]
        ), f"Unexpected row data: {rows[0]}"

    def test_search_with_helper(self, role_group_page):
        logger.info("Testing search using SearchHelper")

        search = SearchHelper(role_group_page.page)

        result = search.run_search(self.group)

        logger.info(f"Search result: {result}")

        assert result["success"], f"Search failed: {result['error']}"

        if result["results_found"] == 0:
            table = TableSection(role_group_page.page)
            assert table.has_no_data()
        else:
            for row in result["results"]:
                assert self.group.lower() in row.lower()

    def test_pagination_on_role_group_table(self, role_group_page):
        logger.info("Testing pagination on Role Group table")

        # Check if pagination elements exist
        page_input = role_group_page.page.locator("input.page-input")
        next_button = role_group_page.page.locator(
            "button:has(mat-icon:has-text('chevron_right'))"
        )

        if page_input.count() > 0 and next_button.count() > 0:
            assert page_input.is_visible(), "Pagination input not visible"
            assert next_button.is_visible(), "Next button not visible"
            logger.info("Pagination elements are present")
        else:
            logger.info("No pagination elements found, assuming single page")

    def test_search_and_validate_table_data(self, role_group_page):
        logger.info("Testing search + table validation")

        search = SearchHelper(role_group_page.page)
        table = TableSection(role_group_page.page)

        result = search.run_search(self.group)

        assert result["success"]

        if result["results_found"] == 0:
            assert table.has_no_data()
        else:
            rows = table.get_rows()
            for row in rows:
                assert self.group.lower() in row.lower()

    def test_table_headers(self, role_group_page):
        logger.info("Validating table headers")

        table = TableSection(role_group_page.page)

        headers = table.get_headers()

        expected_headers = ["GROUP NAME", "CREATED AT", "ACTION"]

        for header in expected_headers:
            assert header in headers, f"{header} not found in table headers"

    def test_created_at_not_future(self, role_group_page):
        logger.info("Validating 'Created At' is not a future date")

        from datetime import datetime

        rows = role_group_page.page.locator("div.component-body table tbody tr")
        today = datetime.today()

        for i in range(rows.count()):
            created_at = rows.nth(i).locator("td").nth(1).inner_text().strip()
            date_obj = datetime.strptime(created_at, "%d/%m/%Y")

            assert date_obj <= today, f"Future date found: {created_at}"

    def test_created_at_sorted(self, role_group_page):
        logger.info("Validating 'Created At' column sorting")

        rows = role_group_page.page.locator("div.component-body table tbody tr")
        row_count = rows.count()

        dates = []

        for i in range(row_count):
            created_at = rows.nth(i).locator("td").nth(1).inner_text().strip()
            date_obj = datetime.strptime(created_at, "%d/%m/%Y")
            dates.append(date_obj)

        # ✅ Check ascending order (oldest first)
        assert dates == sorted(dates), "Dates are not sorted in ascending order"

    def test_created_at_column_format(self, role_group_page):
        logger.info("Validating 'Created At' column format")

        table = TableSection(role_group_page.page)

        rows = role_group_page.page.locator("div.component-body table tbody tr")
        row_count = rows.count()

        assert row_count > 0, "Table is empty"

        date_pattern = re.compile(r"\d{2}/\d{2}/\d{4}")

        for i in range(row_count):
            created_at = rows.nth(i).locator("td").nth(1).inner_text().strip()

            # ✅ Check format
            assert date_pattern.match(created_at), f"Invalid date format: {created_at}"

            # ✅ Check valid date
            try:
                datetime.strptime(created_at, "%d/%m/%Y")
            except ValueError:
                assert False, f"Invalid date value: {created_at}"
