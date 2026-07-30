from pages.common_base_page import BasePage
from pages.common_utils import PaginationHelper, SearchHelper
from utils.logger import get_logger

logger = get_logger(__name__)


class AtcuDealerFotaPage(BasePage):
    # Locators for Dealer FOTA Main Page (/dealer-fota)
    PAGE_CONTAINER = "app-dealer-fota"
    PAGE_TITLE = "span.page-title"
    COMPONENT_TITLE = ".component-title"
    ADD_APPROVED_FILE_BTN = "button.primary-button:has-text('Add Approved File')"
    DOWNLOAD_DETAILS_BTN = "button.primary-button:has-text('Download Dealer FOTA Details')"
    SEARCH_INPUT = "input[formcontrolname='searchInput']"
    SEARCH_BTN = "button.search-btn"
    TABLE = ".component-body table"
    TABLE_HEADERS = ".component-body table thead th"
    TABLE_ROWS = ".component-body table tbody tr"
    PAGINATION_CONTAINER = "app-common-component-pagination, .pagination-container"
    ROWS_SELECT = "select#rowsSelect"
    BACK_BTN = ".back-button"
    RELOAD_BTN = ".reload-button"
    TOAST_MESSAGE = ".mat-mdc-snack-bar-label, simple-snack-bar, [data-sonner-toast]"

    # Locators for Approved Files Sub-Page (/dealer-fota-approved-files)
    APPROVED_FILES_CONTAINER = "app-dealer-fota-approved-files"
    ADD_FILE_INPUT = "input#fileName"
    SUBMIT_BTN = "button.submit-button"
    FILE_NAME_LIST_HEADERS = "app-dealer-fota-approved-files table thead th"
    FILE_NAME_LIST_ROWS = "app-dealer-fota-approved-files table tbody tr"

    def __init__(self, page):
        super().__init__(page)
        logger.info("AtcuDealerFotaPage initialized")

    def is_page_loaded(self):
        logger.info("Checking if AtcuDealerFotaPage is loaded")
        try:
            self.page.locator(self.PAGE_CONTAINER).wait_for(
                state="visible", timeout=10000
            )
            is_vis = self.page.locator(self.PAGE_CONTAINER).is_visible()
            logger.info("AtcuDealerFotaPage load status: %s", is_vis)
            return is_vis
        except Exception as e:
            logger.error("AtcuDealerFotaPage load check failed: %s", e)
            return False

    def get_title(self):
        logger.info("Retrieving AtcuDealerFotaPage title")
        try:
            title_loc = self.page.locator(self.PAGE_TITLE)
            title_loc.wait_for(state="visible", timeout=5000)
            text = title_loc.text_content().strip()
            logger.info("Page title text: '%s'", text)
            return text
        except Exception as e:
            logger.error("Failed to get page title: %s", e)
            return ""

    def get_component_title(self):
        logger.info("Retrieving component header title")
        try:
            loc = self.page.locator(self.COMPONENT_TITLE).first
            loc.wait_for(state="visible", timeout=5000)
            text = loc.text_content().strip()
            logger.info("Component header title: '%s'", text)
            return text
        except Exception as e:
            logger.error("Failed to get component title: %s", e)
            return ""

    def click_back_button(self):
        logger.info("Clicking Back button")
        self.page.locator(self.BACK_BTN).click()

    def click_reload_button(self):
        logger.info("Clicking Reload button")
        self.page.locator(self.RELOAD_BTN).click()
        self.page.wait_for_load_state("networkidle")

    def is_add_approved_file_button_visible(self):
        logger.info("Checking visibility of Add Approved File button")
        try:
            btn = self.page.locator(self.ADD_APPROVED_FILE_BTN)
            return btn.is_visible() and "Add Approved File" in btn.text_content()
        except Exception:
            return False

    def click_add_approved_file_button(self):
        logger.info("Clicking Add Approved File button")
        btn = self.page.locator(self.ADD_APPROVED_FILE_BTN)
        btn.wait_for(state="visible", timeout=5000)
        btn.click()
        self.page.wait_for_load_state("networkidle")

    def is_download_details_button_visible(self):
        logger.info("Checking visibility of Download Dealer FOTA Details button")
        try:
            btn = self.page.locator(self.DOWNLOAD_DETAILS_BTN)
            return btn.is_visible() and "Download Dealer FOTA Details" in btn.text_content()
        except Exception:
            return False

    def click_download_details_button(self):
        logger.info("Clicking Download Dealer FOTA Details button")
        with self.page.expect_download() as download_info:
            self.page.locator(self.DOWNLOAD_DETAILS_BTN).click()
        download = download_info.value
        logger.info("Downloaded details file: %s", download.suggested_filename)
        return download

    def search_dealer_fota_list(self, search_term):
        logger.info("Searching Dealer FOTA list for term: %s", search_term)
        try:
            input_loc = self.page.locator(self.SEARCH_INPUT).first
            input_loc.wait_for(state="visible", timeout=10000)
            input_loc.fill(str(search_term))
            input_loc.press("Enter")
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            logger.warning("Direct search input fill fallback to SearchHelper: %s", e)
            search_helper = SearchHelper(self.page)
            search_helper.run_search(str(search_term))

    def get_table_headers(self):
        headers = []
        try:
            locators = self.page.locator(self.TABLE_HEADERS).all()
            headers = [loc.text_content().strip() for loc in locators]
            logger.debug("Retrieved table headers: %s", headers)
        except Exception as e:
            logger.error("Failed to get table headers: %s", e)
        return headers

    def get_table_rows(self):
        rows_data = []
        try:
            headers = self.get_table_headers()
            row_elements = self.page.locator(self.TABLE_ROWS).all()
            for row in row_elements:
                cells = [cell.text_content().strip() for cell in row.locator("td").all()]
                if cells:
                    row_dict = dict(zip(headers, cells)) if headers else cells
                    rows_data.append(row_dict)
            logger.debug("Retrieved %s table rows: %s", len(rows_data), rows_data)
        except Exception as e:
            logger.error("Failed to get table rows: %s", e)
        return rows_data

    def get_first_row_data(self):
        rows = self.get_table_rows()
        return rows[0] if rows else {}

    def is_device_present_in_table(self, uin_or_vin, timeout=10000):
        logger.info("Checking if device with UIN/VIN '%s' is present in table", uin_or_vin)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{uin_or_vin}')]][1]")
            row_locator.wait_for(state="visible", timeout=timeout)
            is_vis = row_locator.is_visible()
            logger.info("Device '%s' present in table: %s", uin_or_vin, is_vis)
            return is_vis
        except Exception as e:
            logger.warning("Device '%s' not found in table within %s ms: %s", uin_or_vin, timeout, e)
            return False

    def is_pagination_visible(self, timeout=10000):
        try:
            loc = self.page.locator(self.PAGINATION_CONTAINER)
            loc.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception as e:
            logger.error("Pagination container not visible within %s ms: %s", timeout, e)
            return False

    def get_selected_rows_per_page(self):
        try:
            loc = self.page.locator(self.ROWS_SELECT)
            loc.wait_for(state="visible", timeout=10000)
            val = loc.input_value()
            logger.debug("Current rows per page selected: %s", val)
            return val
        except Exception as e:
            logger.error("Failed to get rows per page: %s", e)
            return ""

    def select_rows_per_page(self, option_value):
        logger.info("Selecting %s rows per page", option_value)
        loc = self.page.locator(self.ROWS_SELECT)
        loc.wait_for(state="visible", timeout=10000)
        loc.select_option(str(option_value))

    def validate_pagination(self):
        logger.info("Validating pagination on Dealer FOTA page")
        pagination = PaginationHelper(
            self.page,
            page_input="input.page-input",
            next_button="button:has(mat-icon:has-text('chevron_right'))",
            prev_button="button:has(mat-icon:has-text('chevron_left'))",
            # content_selector="table tbody tr",
        )
        result = pagination.verify()
        logger.debug("Pagination validation result: %s", result)
        return result

    # --- Approved Files Page Methods (/dealer-fota-approved-files) ---

    def is_approved_files_page_loaded(self):
        logger.info("Checking if Approved Files page is loaded")
        try:
            self.page.locator(self.APPROVED_FILES_CONTAINER).wait_for(
                state="visible", timeout=10000
            )
            return self.page.locator(self.APPROVED_FILES_CONTAINER).is_visible()
        except Exception as e:
            logger.error("Approved Files page load check failed: %s", e)
            return False

    def get_approved_files_page_title(self):
        try:
            loc = self.page.locator(self.PAGE_TITLE)
            loc.wait_for(state="visible", timeout=5000)
            return loc.text_content().strip()
        except Exception as e:
            logger.error("Failed to get approved files page title: %s", e)
            return ""

    def enter_file_name_in_add_file_form(self, file_name):
        logger.info("Entering file name '%s' in Add File form", file_name)
        input_loc = self.page.locator(self.ADD_FILE_INPUT)
        input_loc.wait_for(state="visible", timeout=5000)
        input_loc.fill(file_name)

    def is_submit_button_enabled(self):
        try:
            btn = self.page.locator(self.SUBMIT_BTN)
            return btn.is_enabled()
        except Exception:
            return False

    def click_submit_file_name(self):
        logger.info("Clicking Submit button on Add File form")
        btn = self.page.locator(self.SUBMIT_BTN)
        btn.wait_for(state="visible", timeout=5000)
        btn.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(1000)

    def get_file_name_list_headers(self):
        headers = []
        try:
            locators = self.page.locator(self.FILE_NAME_LIST_HEADERS).all()
            headers = [loc.text_content().strip() for loc in locators]
            logger.debug("Retrieved File Name List headers: %s", headers)
        except Exception as e:
            logger.error("Failed to get File Name List headers: %s", e)
        return headers

    def is_file_name_present_in_list(self, file_name, timeout=5000):
        logger.info("Checking if file name '%s' is present in File Name List", file_name)
        try:
            row_loc = self.page.locator(f"//tr[td[contains(text(), '{file_name}')]]").first
            row_loc.wait_for(state="visible", timeout=timeout)
            return row_loc.is_visible()
        except Exception:
            return False

    def is_approved_files_pagination_visible(self, timeout=10000):
        logger.info("Checking pagination visibility on Approved Files page")
        try:
            loc = self.page.locator("app-dealer-fota-approved-files app-common-component-pagination, app-dealer-fota-approved-files .pagination-container")
            loc.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception as e:
            logger.error("Approved Files pagination container not visible within %s ms: %s", timeout, e)
            return False

    def validate_approved_files_pagination(self):
        logger.info("Validating pagination on Approved Files page")
        pagination = PaginationHelper(
            self.page,
            page_input="app-dealer-fota-approved-files input.page-input",
            next_button="app-dealer-fota-approved-files button:has(mat-icon:has-text('chevron_right'))",
            prev_button="app-dealer-fota-approved-files button:has(mat-icon:has-text('chevron_left'))",
            content_selector="app-dealer-fota-approved-files table tbody tr",
        )
        result = pagination.verify()
        logger.debug("Approved Files pagination validation result: %s", result)
        return result

    def search_approved_file_name(self, search_term):
        logger.info("Searching Approved Files table for term: %s", search_term)
        try:
            input_loc = self.page.locator("app-dealer-fota-approved-files input[formcontrolname='searchInput']").first
            input_loc.wait_for(state="visible", timeout=10000)
            input_loc.fill(str(search_term))
            input_loc.press("Enter")
            self.page.wait_for_load_state("networkidle", timeout=10000)
            self.page.wait_for_timeout(500)
        except Exception as e:
            logger.warning("Direct search input fill fallback on Approved Files page: %s", e)
            search_helper = SearchHelper(self.page)
            search_helper.run_search(str(search_term))

    def is_delete_button_visible_for_row(self, file_name):
        logger.info("Checking Delete button visibility for file: %s", file_name)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{file_name}')]]").first
            delete_btn = row_locator.locator("button.delete-button, button:has(mat-icon:has-text('delete'))").first
            return delete_btn.is_visible()
        except Exception as e:
            logger.error("Failed to check Delete button visibility for '%s': %s", file_name, e)
            return False

    def is_delete_button_enabled_for_row(self, file_name):
        logger.info("Checking Delete button enablement for file: %s", file_name)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{file_name}')]]").first
            delete_btn = row_locator.locator("button.delete-button, button:has(mat-icon:has-text('delete'))").first
            return delete_btn.is_enabled()
        except Exception as e:
            logger.error("Failed to check Delete button enablement for '%s': %s", file_name, e)
            return False

    def click_delete_button_for_file_name(self, file_name):
        logger.info("Clicking Delete button for file: %s", file_name)

        def handle_dialog(dialog):
            logger.info("Accepting browser alert/confirm dialog: '%s'", dialog.message)
            dialog.accept()

        self.page.once("dialog", handle_dialog)

        row_locator = self.page.locator(f"//tr[td[contains(text(), '{file_name}')]]").first
        delete_btn = row_locator.locator("button.delete-button, button:has(mat-icon:has-text('delete'))").first
        delete_btn.wait_for(state="visible", timeout=5000)
        delete_btn.click()

        # Handle modal confirmation dialog if present
        try:
            confirm_btn = self.page.locator(
                "button.swal2-confirm, .mat-mdc-dialog-actions button, button:has-text('Yes'), button:has-text('Confirm'), button:has-text('Delete')"
            ).first
            if confirm_btn.is_visible(timeout=2000):
                confirm_btn.click()
                logger.info("Clicked modal delete confirmation button")
        except Exception:
            pass

        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(1000)




