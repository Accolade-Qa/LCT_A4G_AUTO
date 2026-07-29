from pages.common_base_page import BasePage
from pages.common_utils import PaginationHelper
from utils.logger import get_logger

logger = get_logger(__name__)


class AtcuDeviceVinConfigPage(BasePage):
    # Locators
    PAGE_CONTAINER = "app-device-vin-config"
    PAGE_TITLE = "span.page-title"
    COMPONENT_TITLE = ".component-title"
    FORM_LABEL = "label.form-label"
    FILE_INPUT = "input[type='file'][accept='.csv']"
    FILE_NAME_INPUT = "input[formcontrolname='fileName']"
    ATTACH_FILE_BTN = "button.upload-btn"
    DOWNLOAD_SAMPLE_BTN = "button.primary-button"
    UPLOAD_SUBMIT_BTN = "button.edit-button"
    BACK_BTN = ".back-button"
    RELOAD_BTN = ".reload-button"
    TOAST_MESSAGE = ".mat-mdc-snack-bar-label, simple-snack-bar, [data-sonner-toast]"

    # Response View Locators
    RESPONSE_TABLE = ".component-body table"
    RESPONSE_TABLE_HEADERS = ".component-body table thead th"
    RESPONSE_TABLE_ROWS = ".component-body table tbody tr"
    DOWNLOAD_REPORT_BTN = "button.primary-button"

    def __init__(self, page):
        super().__init__(page)
        logger.info("AtcuDeviceVinConfigPage initialized")

    def is_page_loaded(self):
        logger.info("Checking if AtcuDeviceVinConfigPage is loaded")
        try:
            self.page.locator(self.PAGE_CONTAINER).wait_for(
                state="visible", timeout=10000
            )
            is_vis = self.page.locator(self.PAGE_CONTAINER).is_visible()
            logger.info("AtcuDeviceVinConfigPage load status: %s", is_vis)
            return is_vis
        except Exception as e:
            logger.error("AtcuDeviceVinConfigPage load check failed: %s", e)
            return False

    def get_title(self):
        logger.info("Retrieving AtcuDeviceVinConfigPage title")
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

    def get_file_upload_label(self):
        logger.info("Retrieving file upload form label")
        try:
            loc = self.page.locator(self.FORM_LABEL).first
            loc.wait_for(state="visible", timeout=5000)
            text = loc.text_content().strip()
            logger.info("Form label text: '%s'", text)
            return text
        except Exception as e:
            logger.error("Failed to get form label: %s", e)
            return ""

    def get_file_input_accept_attribute(self):
        logger.info("Checking file input accept restriction attribute")
        try:
            accept_val = self.page.locator(self.FILE_INPUT).get_attribute("accept")
            logger.info("File input accept attribute value: '%s'", accept_val)
            return accept_val
        except Exception as e:
            logger.error("Failed to get accept attribute: %s", e)
            return ""

    def click_back_button(self):
        logger.info("Clicking Back button")
        self.page.locator(self.BACK_BTN).click()

    def click_reload_button(self):
        logger.info("Clicking Reload button")
        self.page.locator(self.RELOAD_BTN).click()
        self.page.wait_for_load_state("networkidle")

    def is_download_sample_button_visible(self):
        logger.info("Checking visibility of Download Sample Excel Template button")
        try:
            btn = self.page.locator(self.DOWNLOAD_SAMPLE_BTN)
            return btn.is_visible() and "Download Sample Excel Template" in btn.text_content()
        except Exception:
            return False

    def click_download_sample_template(self):
        logger.info("Clicking Download Sample Excel Template button")
        with self.page.expect_download() as download_info:
            self.page.locator(self.DOWNLOAD_SAMPLE_BTN).click()
        download = download_info.value
        logger.info("Downloaded sample template: %s", download.suggested_filename)
        return download

    def get_uploaded_file_name(self):
        logger.info("Retrieving uploaded file name text value")
        try:
            val = self.page.locator(self.FILE_NAME_INPUT).input_value()
            logger.info("File name input value: '%s'", val)
            return val
        except Exception as e:
            logger.error("Failed to get file name input value: %s", e)
            return ""

    def is_upload_submit_button_enabled(self):
        logger.info("Checking if Upload submit button is enabled")
        try:
            btn = self.page.locator(self.UPLOAD_SUBMIT_BTN)
            enabled = btn.is_enabled()
            logger.info("Upload submit button enabled state: %s", enabled)
            return enabled
        except Exception as e:
            logger.error("Failed to check Upload submit button state: %s", e)
            return False

    def upload_csv_file(self, file_path):
        logger.info("Uploading CSV file: %s", file_path)
        self.page.locator(self.FILE_INPUT).set_input_files(file_path)
        self.page.wait_for_timeout(500)
        logger.info("File successfully attached to file input")

    def click_upload_submit_button(self):
        logger.info("Clicking Upload submit button")
        btn = self.page.locator(self.UPLOAD_SUBMIT_BTN)
        btn.wait_for(state="visible", timeout=5000)
        btn.click()

    def get_toast_message(self, timeout=5000):
        logger.info("Waiting for toast notification")
        try:
            toast = self.page.locator(self.TOAST_MESSAGE)
            toast.wait_for(state="visible", timeout=timeout)
            text = toast.text_content().strip()
            logger.info("Toast notification text: '%s'", text)
            return text
        except Exception as e:
            logger.debug("No toast message displayed within %s ms: %s", timeout, e)
            return ""

    def is_response_table_visible(self, timeout=15000):
        logger.info("Checking if uploaded files response table is visible")
        try:
            self.page.locator(self.RESPONSE_TABLE).wait_for(
                state="visible", timeout=timeout
            )
            return True
        except Exception as e:
            logger.debug("Response table not visible within %s ms: %s", timeout, e)
            return False

    def get_response_table_headers(self):
        headers = []
        try:
            locators = self.page.locator(self.RESPONSE_TABLE_HEADERS).all()
            headers = [loc.text_content().strip() for loc in locators]
            logger.debug("Retrieved response table headers: %s", headers)
        except Exception as e:
            logger.error("Failed to get response table headers: %s", e)
        return headers

    def get_response_table_rows(self):
        rows_data = []
        try:
            headers = self.get_response_table_headers()
            row_elements = self.page.locator(self.RESPONSE_TABLE_ROWS).all()
            for row in row_elements:
                cells = [cell.text_content().strip() for cell in row.locator("td").all()]
                if cells:
                    row_dict = dict(zip(headers, cells)) if headers else cells
                    rows_data.append(row_dict)
            logger.debug("Retrieved %s response table rows: %s", len(rows_data), rows_data)
        except Exception as e:
            logger.error("Failed to get response table rows: %s", e)
        return rows_data

    def get_response_table_first_row(self):
        rows = self.get_response_table_rows()
        return rows[0] if rows else {}

    def is_download_report_button_visible(self):
        try:
            btn = self.page.locator(self.DOWNLOAD_REPORT_BTN)
            return btn.is_visible() and "Download Report" in btn.text_content()
        except Exception:
            return False

    def click_download_report_button(self):
        logger.info("Clicking Download Report button")
        with self.page.expect_download() as download_info:
            self.page.locator(self.DOWNLOAD_REPORT_BTN).click()
        download = download_info.value
        logger.info("Downloaded report file: %s", download.suggested_filename)
        return download

    def is_pagination_visible(self, timeout=15000):
        try:
            self.is_response_table_visible(timeout=timeout)
            loc = self.page.locator(
                "app-common-component-pagination, .pagination-container, .rows-per-page"
            )
            loc.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception as e:
            logger.error("Pagination container not visible within %s ms: %s", timeout, e)
            return False

    def get_selected_rows_per_page(self):
        try:
            loc = self.page.locator("select#rowsSelect")
            loc.wait_for(state="visible", timeout=15000)
            val = loc.input_value()
            logger.debug("Current rows per page selected: %s", val)
            return val
        except Exception as e:
            logger.error("Failed to get rows per page: %s", e)
            return ""

    def select_rows_per_page(self, option_value):
        logger.info("Selecting %s rows per page", option_value)
        loc = self.page.locator("select#rowsSelect")
        loc.wait_for(state="visible", timeout=15000)
        loc.select_option(str(option_value))

    def validate_response_table_pagination(self):
        logger.info("Validating response table pagination")
        self.is_response_table_visible(timeout=15000)
        pagination = PaginationHelper(
            self.page,
            page_input="input.page-input",
            next_button="button:has(mat-icon:has-text('chevron_right'))",
            prev_button="button:has(mat-icon:has-text('chevron_left'))",
            content_selector="table tbody tr",
        )
        result = pagination.verify()
        logger.debug("Response table pagination validation result: %s", result)
        return result
