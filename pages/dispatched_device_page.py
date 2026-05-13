from utils.logger import get_logger
from pages.common.table_section import TableSection

logger = get_logger(__name__)


class DispatchedDevicePage:
    def __init__(self, page):
        logger.debug("Initializing Dispatched Devices Page with page object")
        self.page = page
        logger.info("DispatchedDevicePage initialized successfully")

    def go_to_dispatcheddevicepage(self, url):
        logger.info("Navigating to Dispatched Device page: %s", url)
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        logger.info("Navigation to Dispatched Device page completed: %s", url)

    def is_page_loaded(self):
        logger.debug("Checking if Dispatched Device page is loaded")
        return self.page.url.endswith("/dispatched-devices")

    def is_manual_upload_button_visible(self):
        logger.debug("Checking visibility of Manual Upload button")
        manual_upload = self.page.locator("//div[@class='page-header']//button[1]")
        return manual_upload.is_visible()

    def is_bulk_upload_button_visible(self):
        logger.debug("Checking visibility of Bulk Upload button")
        bulk_upload = self.page.locator("//div[@class='page-header']//button[2]")
        return bulk_upload.is_visible()

    def is_checkbox_visible(self):
        logger.debug("Checking visibility of checkbox in Dispatched Device page")
        checkbox = self.page.locator("span:has-text('Select Customer')")
        return checkbox.is_visible()

    def is_view_actions_button_visible(self):
        logger.debug("Checking visibility of View Actions button")
        view_actions = (
            self.page.locator("mat-icon").filter(has_text="visibility").last()
        )
        return view_actions.is_visible()

    def is_delete_action_button_visible(self):
        logger.debug("Checking visibility of Delete Action button")
        delete_action = self.page.locator("mat-icon").filter(has_text="delete").last()
        return delete_action.is_visible()

    def is_dispatched_device_table_visible(self):
        logger.debug("Checking visibility of Dispatched Device table")
        table = self.page.locator("//div[@class='component-body']")
        return table.is_visible()

    def is_search_box_visible(self):
        logger.debug("Checking visibility of Search box")
        search_box = self.page.get_by_placeholder("Search and Press Enter")
        return search_box.is_visible()

    def get_table_headers(self):
        logger.debug("Retrieving table headers from Dispatched Device page")
        table = TableSection(self.page)
        headers = table.get_headers()
        logger.info("Table headers retrieved: %s", headers)
        return headers
