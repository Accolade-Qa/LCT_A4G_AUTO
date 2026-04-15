from utils.logger import get_logger

logger = get_logger(__name__)


class RoleGroupPage:
    def __init__(self, page):
        self.page = page

    def go_to_role_group_page(self, url):
        logger.info("Navigating to Role Group page: %s", url)
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        logger.info("Role Group page loaded")

    def get_title(self):
        logger.info("Retrieving Role Group page title")
        locator = self.page.locator(".page-title")
        locator.wait_for(state="visible")
        title = locator.text_content()
        logger.info("Page title found: %s", title)
        return title

    def is_page_loaded(self):
        logger.debug("Checking if Role Group page is loaded")
        return (
            self.page.url.endswith("/role-group")
            and self.page.locator(".page-title").is_visible()
        )

    def is_add_group_button_visible(self):
        logger.debug("Checking visibility of Add Group button")
        add_group = self.page.locator("button[class='primary-button ng-star-inserted']")
        return add_group.is_visible()

    def is_role_group_table_visible(self):
        logger.debug("Checking visibility of Role Group table")
        table = self.page.locator("//div[@class='component-body']")
        return table.is_visible()

    def is_search_box_visible(self):
        logger.debug("Checking visibility of Search box")
        search_box = self.page.get_by_placeholder("Search and Press Enter")
        return search_box.is_visible()

    def click_add_group(self):
        logger.info("Clicking Add New Group button")
        self.page.get_by_text("Add Group open_in_new", exact=True).click()

    def click_save(self):
        logger.info("Clicking Save button")
        self.page.get_by_role("button", name="Save").click()

    def get_success_message(self):
        logger.info("Waiting for success snackbar message")

        snackbar = self.page.locator(".mat-mdc-snack-bar-container")
        snackbar.wait_for(state="visible")

        message = snackbar.inner_text().strip()
        logger.info(f"Snackbar message: {message}")
        return message

    def enter_role_group_name(self, role_name):
        logger.info(f"Entering role group name: {role_name}")
        self.page.get_by_role("textbox", name="Group Name").fill(role_name)

    def get_component_title(self):
        logger.info("Retrieving component title")
        locator = self.page.locator(".component-title")
        locator.wait_for(state="visible")
        title = locator.text_content()
        logger.info("Component title found: %s", title)
        return title

    def get_input_box_error_message(self):
        logger.info("Retrieving input box error message")
        error_locator = self.page.locator("mat-error")
        if error_locator.is_visible():
            error_message = error_locator.text_content().strip()
            logger.info("Error message found: %s", error_message)
            return error_message
        logger.info("No error message visible")
        return None

    def get_created_at_values(self):
        rows = self.page.locator("div.component-body table tbody tr")
        return [
            rows.nth(i).locator("td").nth(1).inner_text().strip()
            for i in range(rows.count())
        ]
