from utils.logger import get_logger

logger = get_logger(__name__)


class SimDataDetailsPage:
    def __init__(self, page):
        self.page = page
        logger.info("SimDataDetailsPage initialized with URL %s", page.url)

    def go_to_simbatchpage(self, url):
        logger.info("Navigating to SIM Data Details page: %s", url)
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        logger.debug("Navigation complete for SIM Data Details")

    def get_title(self):
        logger.info("Retrieving SIM data page title")
        locator = self.page.locator(".page-title")
        locator.wait_for(state="visible")
        title = locator.text_content()
        logger.info("Page title found: %s", title)
        return title

    def _get_button_by_text(self, text: str):
        logger.debug("Resolving button with text '%s'", text)
        locator = self.page.locator(f"button:has-text('{text}')")
        locator.wait_for(state="visible")
        return locator

    def is_manual_upload_button_visible(self):
        visible = self._get_button_by_text("Manual Upload").is_visible()
        logger.info("Manual Upload button visible: %s", visible)
        return visible

    def is_download_sample_button_visible(self):
        visible = self._get_button_by_text("Download Sample").is_visible()
        logger.info("Download Sample button visible: %s", visible)
        return visible

    def get_manual_upload_button_text(self):
        text = self._get_button_by_text("Manual Upload").text_content().strip()
        logger.info("Manual Upload button text: %s", text)
        return text

    def get_download_sample_button_text(self):
        text = self._get_button_by_text("Download Sample").text_content().strip()
        logger.info("Download Sample button text: %s", text)
        return text

    def get_upload_instruction_text(self):
        instruction_locator = self.page.get_by_text("Upload ICCID's to get SIM Data Details")
        instruction_locator.wait_for(state="visible")
        text = instruction_locator.text_content().strip()
        logger.info("Upload instruction text retrieved: %s", text)
        return text

    def get_iccid_upload_placeholder(self):
        locator = self.page.get_by_placeholder("Upload Device ICCID's*")
        locator.wait_for(state="visible")
        placeholder = locator.get_attribute("placeholder")
        logger.info("ICCID upload placeholder attribute: %s", placeholder)
        return placeholder

    def is_submit_button_disabled(self):
        submit_button = self.page.get_by_role("button", name="Submit")
        submit_button.wait_for(state="visible")
        disabled = submit_button.is_disabled()
        logger.info("Submit button initially disabled: %s", disabled)
        return disabled

    def click_manual_upload_button(self):
        manual_upload_button = self._get_button_by_text("Manual Upload")
        logger.info("Sending click to Manual Upload button")
        with self.page.expect_navigation(wait_until="networkidle"):
            manual_upload_button.click()

    def validate_blank_input_error_message(self):
        logger.info("Validating blank ICCID upload error text")
        iccid_input = self.page.get_by_role("textbox")
        iccid_input.wait_for(state="visible")
        iccid_input.click()
        canvas = self.page.locator("div.component-header")
        canvas.click()
        error_message = self.page.get_by_text("This field is required and can't be only spaces.")
        error_message.wait_for(state="visible")
        message = error_message.text_content().strip()
        logger.info("Blank input validation message: %s", message)
        return message
