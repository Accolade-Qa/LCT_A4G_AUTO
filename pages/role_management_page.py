from pytest_playwright.pytest_playwright import page

from utils.logger import get_logger

logger = get_logger(__name__)


class RoleManagementPage:
    def __init__(self, page):
        self.page = page

    def go_to_rolemanagementpage(self, url):
        logger.info("Navigating to Role Management page: %s", url)
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        logger.debug("Navigation complete for Role Management")

    def is_page_loaded(self):
        logger.debug("Checking if Role Management page is loaded")
        return self.page.url.endswith("/user-role")

    def is_add_role_button_visible(self):
        logger.debug("Checking visibility of Add Role button")
        add_role = self.page.locator("button[class='primary-button ng-star-inserted']")
        return add_role.is_visible()

    def is_role_table_visible(self):
        logger.debug("Checking visibility of Role table")
        table = self.page.locator("//div[@class='component-body']")
        return table.is_visible()

    def is_search_box_visible(self):
        logger.debug("Checking visibility of Search box")
        search_box = self.page.get_by_placeholder("Search and Press Enter")
        return search_box.is_visible()

    def click_add_role(self):
        logger.info("Clicking Add New Role button")
        self.page.get_by_text("Add Role open_in_new", exact=True).click()

    def enter_role_name(self, role_name):
        logger.info(f"Entering role name: {role_name}")
        self.page.get_by_role("textbox", name="Role Name").fill(role_name)

    def select_role_type(self, role_type):
        logger.info(f"Selecting role type: {role_type}")

        # Click mat-select dropdown
        self.page.locator("mat-select[formcontrolname='roleType']").click()

        # Wait for dropdown options panel
        self.page.locator("mat-option").first.wait_for()

        # Click the option
        self.page.get_by_text(role_type, exact=True).click()

    def is_role_group_visible(self):
        logger.debug("Checking Role Group visibility")
        return self.page.locator("mat-select[formcontrolname='roleGroup']").is_visible()

    def select_role_group(self, group):
        logger.info(f"Selecting role group: {group}")

        self.page.locator("mat-select[formcontrolname='roleGroup']").click()
        self.page.locator("mat-option").first.wait_for()

        self.page.locator(f"mat-option:has-text('{group}')").click()

    def click_save(self):
        logger.info("Clicking Save button")
        self.page.locator(".submit-button.ng-star-inserted").click()

    def get_error_message(self):
        logger.debug("Fetching error message")
        return self.page.locator("simple-snack-bar").inner_text()

    def get_input_box_error_message(self):
        logger.debug(f"Fetching error message for input field:")
        error_locator = self.page.locator("mat-error")
        return error_locator.inner_text()

    def select_permission(self, page_name, permission_type):
        logger.info(f"Selecting {permission_type} permission for {page_name}")

        permission_map = {
            "select_all": 1,
            "view": 2,
            "create": 3,
            "update": 4,
            "delete": 5,
        }

        col_index = permission_map.get(permission_type.lower())

        if not col_index:
            raise ValueError(f"Invalid permission type: {permission_type}")

        checkbox = self.page.locator(
            f"//tr[td//strong[text()='{page_name}']]/td[{col_index + 1}]//input[@type='checkbox']"
        )

        checkbox.check()

    def select_all_permissions(self):
        self.page.locator("#mat-mdc-checkbox-1-input").check()

    def get_success_message(self):
        logger.info("Waiting for success snackbar message")

        snackbar = self.page.locator(".mat-mdc-snack-bar-container")
        snackbar.wait_for(state="visible")

        message = snackbar.inner_text().strip()
        logger.info(f"Snackbar message: {message}")
        return message

    def wait_for_snackbar_to_disappear(self):
        snackbar = self.page.locator("div.mat-mdc-snack-bar-label")

        try:
            snackbar.wait_for(state="hidden", timeout=5000)
        except:
            pass  # ignore if already gone

    def is_sub_permission_disabled(self, sub_name, permission_type):
        permission_map = {
            "view": 2,
            "create": 3,
            "update": 4,
            "delete": 5,
        }

        col_index = permission_map[permission_type.lower()]

        checkbox = self.page.locator(
            f"//tr[td[contains(text(),'{sub_name}')]]/td[{col_index + 1}]//input"
        )

        return checkbox.is_disabled()

    def is_sub_permission_disabled(self, sub_name, permission_type):
        permission_map = {
            "view": 2,
            "create": 3,
            "update": 4,
            "delete": 5,
        }

        col_index = permission_map[permission_type.lower()]

        checkbox = self.page.locator(
            f"//tr[td[contains(text(),'{sub_name}')]]/td[{col_index + 1}]//input"
        )

        return checkbox.is_disabled()

    def select_sub_permission(self, sub_name, permission_type):
        logger.info(f"Selecting {permission_type} for {sub_name}")

        permission_map = {
            "view": 2,
            "create": 3,
            "update": 4,
            "delete": 5,
        }

        col_index = permission_map[permission_type.lower()]

        row = self.page.locator(f"//tr[td[contains(text(),'{sub_name}')]]")

        checkbox = row.locator(f"td:nth-child({col_index + 1}) input")

        checkbox.scroll_into_view_if_needed()
        checkbox.check(force=True)

    def enable_permission_group(self, page_name):
        logger.info(f"Enabling permission group: {page_name}")

        row = self.page.locator(f"//tr[td//strong[text()='{page_name}']]")

        # Main checkbox = first checkbox column (Select All)
        checkbox = row.locator("td:nth-child(2) input")

        checkbox.scroll_into_view_if_needed()
        checkbox.check(force=True)

    def search_role(self, role_name):
        logger.info(f"Searching for role: {role_name}")

        search_box = self.page.get_by_placeholder("Search and Press Enter")
        search_box.fill(role_name)
        search_box.press("Enter")

    def is_role_in_table(self, role_name):
        logger.info(f"Checking if role '{role_name}' is in the table")

        # Wait for potential search results to load
        self.page.wait_for_timeout(1000)

        role_locator = self.page.locator(f"//td[contains(text(), '{role_name}')]")
        return role_locator.is_visible()

    def get_table_row_data(self, index: int) -> str:
        row = self.page.locator("div.component-body table tbody tr").nth(index)
        return row.inner_text().strip()
