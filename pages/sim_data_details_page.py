class SimDataDetailsPage:
    def __init__(self, page):
        self.page = page

    def go_to_simbatchpage(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def get_title(self):
        locator = self.page.locator(".page-title")
        locator.wait_for(state="visible")
        return locator.text_content()

    def _get_button_by_text(self, text: str):
        locator = self.page.locator(f"button:has-text('{text}')")
        locator.wait_for(state="visible")
        return locator

    def is_manual_upload_button_visible(self):
        return self._get_button_by_text("Manual Upload").is_visible()

    def is_download_sample_button_visible(self):
        return self._get_button_by_text("Download Sample").is_visible()

    def get_manual_upload_button_text(self):
        return self._get_button_by_text("Manual Upload").text_content().strip()

    def get_download_sample_button_text(self):
        return self._get_button_by_text("Download Sample").text_content().strip()

    def get_upload_instruction_text(self):
        instruction_locator = self.page.get_by_text("Upload ICCID's to get SIM Data Details")
        instruction_locator.wait_for(state="visible")
        return instruction_locator.text_content().strip()

    def get_iccid_upload_placeholder(self):
        locator = self.page.get_by_placeholder("Upload Device ICCID's*")
        locator.wait_for(state="visible")
        return locator.get_attribute("placeholder")

    def is_submit_button_disabled(self):
        submit_button = self.page.get_by_role("button", name="Submit")
        submit_button.wait_for(state="visible")
        return submit_button.is_disabled()

    def click_manual_upload_button(self):
        manual_upload_button = self._get_button_by_text("Manual Upload")
        with self.page.expect_navigation(wait_until="networkidle"):
            manual_upload_button.click()

    def validate_blank_input_error_message(self):
        iccid_input = self.page.get_by_role("textbox")
        iccid_input.wait_for(state="visible")
        iccid_input.click()
        canvas = self.page.locator("div.component-header")
        canvas.click()
        error_message = self.page.get_by_text("This field is required and can't be only spaces.")
        error_message.wait_for(state="visible")
        return error_message.text_content().strip()
