from pages.common_base_page import BasePage
from pages.common_utils import PaginationHelper, SearchHelper
from utils.logger import get_logger

logger = get_logger(__name__)


class AtcuModelPage(BasePage):
    # Main Page Locators (/device-model-list)
    PAGE_CONTAINER = "app-device-model-list"
    PAGE_TITLE = "span.page-title"
    COMPONENT_TITLE = ".component-title"
    ADD_MODEL_BTN = "button.primary-button:has-text('Add Device Model')"
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

    # Details Page Locators (/device-model-details)
    DETAILS_CONTAINER = "app-device-model-details"
    MODEL_NAME_INPUT = "input#modelName"
    MODEL_CODE_INPUT = "input#modelCode"
    HW_VERSION_INPUT = "input#hwVersion"
    SUBMIT_BTN = "button.submit-button"

    def __init__(self, page):
        super().__init__(page)
        logger.info("AtcuModelPage initialized")

    def is_page_loaded(self):
        logger.info("Checking if AtcuModelPage is loaded")
        try:
            self.page.locator(self.PAGE_CONTAINER).wait_for(
                state="visible", timeout=10000
            )
            is_vis = self.page.locator(self.PAGE_CONTAINER).is_visible()
            logger.info("AtcuModelPage load status: %s", is_vis)
            return is_vis
        except Exception as e:
            logger.error("AtcuModelPage load check failed: %s", e)
            return False

    def get_title(self):
        logger.info("Retrieving AtcuModelPage title")
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

    def is_add_device_model_button_visible(self):
        logger.info("Checking visibility of Add Device Model button")
        try:
            btn = self.page.locator(self.ADD_MODEL_BTN)
            return btn.is_visible() and "Add Device Model" in btn.text_content()
        except Exception:
            return False

    def click_add_device_model_button(self):
        logger.info("Clicking Add Device Model button")
        btn = self.page.locator(self.ADD_MODEL_BTN)
        btn.wait_for(state="visible", timeout=5000)
        btn.click()
        self.page.wait_for_load_state("networkidle")

    def search_model_list(self, search_term):
        logger.info("Searching Device Models list for term: %s", search_term)
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

    def clear_search_input(self):
        logger.info("Clearing search input field")
        input_loc = self.page.locator(self.SEARCH_INPUT).first
        input_loc.wait_for(state="visible", timeout=5000)
        input_loc.fill("")
        input_loc.press("Enter")
        try:
            btn = self.page.locator("button.search-btn, button:has(mat-icon:has-text('search'))").first
            if btn.is_visible():
                btn.click()
        except Exception:
            pass
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(1000)

    def get_table_headers(self):
        headers = []
        try:
            locators = self.page.locator(self.TABLE_HEADERS).all()
            headers = [loc.text_content().strip().upper() for loc in locators]
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

    def is_model_present_in_table(self, model_name_or_code, timeout=10000):
        logger.info("Checking if model '%s' is present in table", model_name_or_code)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{model_name_or_code}')]]")
            row_locator.wait_for(state="visible", timeout=timeout)
            is_vis = row_locator.is_visible()
            logger.info("Model '%s' present in table: %s", model_name_or_code, is_vis)
            return is_vis
        except Exception as e:
            logger.warning("Model '%s' not found in table within %s ms: %s", model_name_or_code, timeout, e)
            return False

    def is_view_button_visible_for_row(self, model_name):
        logger.info("Checking View button visibility for model: %s", model_name)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{model_name}')]]")
            view_btn = row_locator.locator("button.view-button, button:has(mat-icon:has-text('visibility'))").first
            return view_btn.is_visible()
        except Exception as e:
            logger.error("Failed to check View button visibility for '%s': %s", model_name, e)
            return False

    def click_view_button_for_row(self, model_name):
        logger.info("Clicking View button for model: %s", model_name)
        row_locator = self.page.locator(f"//tr[td[contains(text(), '{model_name}')]]")
        view_btn = row_locator.locator("button.view-button, button:has(mat-icon:has-text('visibility'))").first
        view_btn.wait_for(state="visible", timeout=5000)
        view_btn.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def is_delete_button_visible_for_row(self, model_name):
        logger.info("Checking Delete button visibility for model: %s", model_name)
        try:
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{model_name}')]]")
            delete_btn = row_locator.locator("button.delete-button, button:has(mat-icon:has-text('delete'))").first
            return delete_btn.is_visible()
        except Exception as e:
            logger.error("Failed to check Delete button visibility for '%s': %s", model_name, e)
            return False

    def click_delete_button_for_row(self, model_name):
        logger.info("Clicking Delete button for model: %s", model_name)

        def handle_dialog(dialog):
            logger.info("Accepting browser alert/confirm dialog: '%s'", dialog.message)
            dialog.accept()

        self.page.once("dialog", handle_dialog)

        row_locator = self.page.locator(f"//tr[td[contains(text(), '{model_name}')]]").first
        delete_btn = row_locator.locator("button.delete-button, button:has(mat-icon:has-text('delete'))").first
        delete_btn.wait_for(state="visible", timeout=5000)
        delete_btn.click()

        try:
            confirm_btn = self.page.locator(
                "button.swal2-confirm, .mat-mdc-dialog-actions button, button:has-text('Yes'), button:has-text('Confirm'), button:has-text('Delete')"
            ).first
            if confirm_btn.is_visible(timeout=2000):
                confirm_btn.click()
        except Exception:
            pass

        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(1000)

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
        logger.info("Validating pagination on Device Models page")
        pagination = PaginationHelper(
            self.page,
            page_input="input.page-input",
            next_button="button:has(mat-icon:has-text('chevron_right'))",
            prev_button="button:has(mat-icon:has-text('chevron_left'))",
            content_selector="table tbody tr",
        )
        result = pagination.verify()
        logger.debug("Pagination validation result: %s", result)
        return result

    # --- Add/Update Device Model Details Methods (/device-model-details) ---

    def is_details_page_loaded(self):
        logger.info("Checking if Device Model Details page is loaded")
        try:
            self.page.locator(self.DETAILS_CONTAINER).wait_for(
                state="visible", timeout=10000
            )
            return self.page.locator(self.DETAILS_CONTAINER).is_visible()
        except Exception as e:
            logger.error("Device Model Details page load check failed: %s", e)
            return False

    def get_details_page_title(self):
        try:
            loc = self.page.locator(self.PAGE_TITLE)
            loc.wait_for(state="visible", timeout=5000)
            return loc.text_content().strip()
        except Exception as e:
            logger.error("Failed to get details page title: %s", e)
            return ""

    def get_details_component_title(self):
        try:
            loc = self.page.locator(self.COMPONENT_TITLE).first
            loc.wait_for(state="visible", timeout=5000)
            return loc.text_content().strip()
        except Exception as e:
            logger.error("Failed to get details component title: %s", e)
            return ""

    def fill_create_model_form(self, model_name, model_code, hw_version):
        logger.info("Filling Create Model form: Name='%s', Code='%s', HW='%s'", model_name, model_code, hw_version)
        if model_name is not None:
            loc = self.page.locator(self.MODEL_NAME_INPUT)
            loc.fill(model_name)
            loc.dispatch_event("input")
            loc.dispatch_event("blur")
        if model_code is not None:
            loc = self.page.locator(self.MODEL_CODE_INPUT)
            loc.fill(model_code)
            loc.dispatch_event("input")
            loc.dispatch_event("blur")
        if hw_version is not None:
            loc = self.page.locator(self.HW_VERSION_INPUT)
            loc.fill(hw_version)
            loc.dispatch_event("input")
            loc.dispatch_event("blur")

    def is_submit_button_enabled(self):
        try:
            btn = self.page.locator(self.SUBMIT_BTN)
            return btn.is_enabled()
        except Exception:
            return False

    def click_submit_button(self):
        logger.info("Clicking Submit button on Create Model form")
        btn = self.page.locator(self.SUBMIT_BTN)
        btn.wait_for(state="visible", timeout=5000)
        btn.click()
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def get_toast_message(self, timeout=5000):
        logger.info("Waiting for toast notification")
        try:
            toast = self.page.locator(self.TOAST_MESSAGE)
            toast.wait_for(state="visible", timeout=timeout)
            return toast.text_content().strip()
        except Exception as e:
            logger.debug("No toast message displayed within %s ms: %s", timeout, e)
            return ""

    def get_form_input_values(self):
        try:
            m_name = self.page.locator(self.MODEL_NAME_INPUT).input_value()
            m_code = self.page.locator(self.MODEL_CODE_INPUT).input_value()
            hw_ver = self.page.locator(self.HW_VERSION_INPUT).input_value()
            return {"modelName": m_name, "modelCode": m_code, "hwVersion": hw_ver}
        except Exception as e:
            logger.error("Failed to get form input values: %s", e)
            return {}

    def get_row_details_by_model_name(self, model_name):
        logger.info("Getting row details for model: %s", model_name)
        try:
            headers = self.get_table_headers()
            row_locator = self.page.locator(f"//tr[td[contains(text(), '{model_name}')]]").first
            cells = [td.text_content().strip() for td in row_locator.locator("td").all()]
            row_dict = dict(zip(headers, cells)) if headers else cells
            logger.info("Row details for model '%s': %s", model_name, row_dict)
            return row_dict
        except Exception as e:
            logger.error("Failed to get row details for model '%s': %s", model_name, e)
            return {}

