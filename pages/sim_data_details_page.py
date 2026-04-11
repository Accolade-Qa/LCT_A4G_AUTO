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

    def validate_20_characters_error_message(self):
        logger.info("Validating ICCID length error message")
        iccid_input = self.page.get_by_role("textbox")
        iccid_input.wait_for(state="visible")
        iccid_input.fill("123456789")  # Input less than 20 characters
        canvas = self.page.locator("div.component-header")
        canvas.click()
        error_message = self.page.get_by_text("Value must be exactly 20 characters long.")
        error_message.wait_for(state="visible")
        message = error_message.text_content().strip()
        logger.info("ICCID length validation message: %s", message)
        return message
    
    def enter_valid_iccid(self, iccid):
        logger.info("Entering valid ICCID: %s", iccid)
        iccid_input = self.page.get_by_role("textbox")
        iccid_input.wait_for(state="visible")
        iccid_input.fill(iccid)
        canvas = self.page.locator("div.component-header")
        canvas.click()
        
    def click_submit_button(self):
        logger.info("Clicking Submit button")
        submit_button = self.page.get_by_role("button", name="Submit")
        submit_button.wait_for(state="visible")
        submit_button.click()
        
    def is_results_table_visible(self):
        logger.info("Checking if results table is visible or not")
        table_locator = self.page.locator("//div[@class='component-container ng-star-inserted']")
        table_locator.wait_for(state="visible")
        visible = table_locator.is_visible()
        logger.info("Results table visible: %s", visible)
        return visible
    
    def get_results_table_component_header(self):
        logger.info("Retrieving results table component header text")
        header_locator = self.page.locator("div[class='component-container ng-star-inserted'] h6[class='component-title']")
        header_locator.wait_for(state="visible")
        header_text = header_locator.text_content().strip()
        logger.info("Results table component header text: %s", header_text)
        return header_text
    
    def get_table_headers(self):
        headers_locator = self.page.locator("div.component-body table thead th")
        headers_locator.first.wait_for(state="visible")
        headers_count = headers_locator.count()
        headers = [headers_locator.nth(i).inner_text() for i in range(headers_count)]
        logger.info("Retrieved table headers: %s", headers)
        return headers
    
    def check_pagination(self):
        PAGE_INPUT = "input.page-input"
        NEXT_BUTTON = "button:has(mat-icon:has-text('chevron_right'))"
        PREV_BUTTON = "button:has(mat-icon:has-text('chevron_left'))"
        CONTENT_CONTAINER = "table"

        result = {
            "success": True,
            "pages_visited": [],
            "total_pages": 0,
            "error": None
        }

        try:
            logger.info("Starting pagination verification")

            self.page.wait_for_selector(PAGE_INPUT)
            self.page.wait_for_selector(CONTENT_CONTAINER)

            current_page = int(self.page.locator(PAGE_INPUT).input_value())
            result["pages_visited"].append(current_page)

            # 🔥 Detect total pages (if visible like "1 / 10")
            try:
                pagination_text = self.page.locator("text=/\\d+\\s*/\\s*\\d+/").inner_text()
                total_pages = int(pagination_text.split("/")[-1].strip())
            except:
                total_pages = 1  # fallback if not available

            result["total_pages"] = total_pages

            print(f"Total pages detected: {total_pages}")

            # ✅ If only 1 page → exit early
            if total_pages <= 1:
                print("Only one page found. Skipping pagination.")
                return result

            visited_pages = set([current_page])

            # 🔥 Limit to 5 pages max
            max_steps = min(5, total_pages - current_page)

            # ========================
            # 👉 FORWARD NAVIGATION
            # ========================
            for _ in range(max_steps):
                prev_content = self.page.locator(CONTENT_CONTAINER).inner_text()

                next_btn = self.page.locator(NEXT_BUTTON)

                if next_btn.is_disabled():
                    print("Reached last page early.")
                    break

                next_btn.click()

                self.page.wait_for_function(
                    """(prev) => {
                        const el = document.querySelector('input.page-input');
                        return el && el.value != prev;
                    }""",
                    arg=str(current_page)
                )

                new_page = int(self.page.locator(PAGE_INPUT).input_value())

                if new_page in visited_pages:
                    print("Loop detected.")
                    break

                # Validate increment
                if new_page != current_page + 1:
                    result["success"] = False
                    result["error"] = f"Forward pagination issue: {current_page} -> {new_page}"
                    return result

                new_content = self.page.locator(CONTENT_CONTAINER).inner_text()

                if prev_content == new_content:
                    result["success"] = False
                    result["error"] = "Content did not change on next page"
                    return result

                visited_pages.add(new_page)
                result["pages_visited"].append(new_page)
                current_page = new_page

            # ========================
            # 👉 BACKWARD NAVIGATION
            # ========================
            for _ in range(len(result["pages_visited"]) - 1):
                prev_btn = self.page.locator(PREV_BUTTON)

                if prev_btn.is_disabled():
                    print("Reached first page.")
                    break

                prev_content = self.page.locator(CONTENT_CONTAINER).inner_text()

                prev_btn.click()

                self.page.wait_for_function(
                    """(prev) => {
                        const el = document.querySelector('input.page-input');
                        return el && el.value != prev;
                    }""",
                    arg=str(current_page)
                )

                new_page = int(self.page.locator(PAGE_INPUT).input_value())

                # Validate decrement
                if new_page != current_page - 1:
                    result["success"] = False
                    result["error"] = f"Backward pagination issue: {current_page} -> {new_page}"
                    return result

                new_content = self.page.locator(CONTENT_CONTAINER).inner_text()

                if prev_content == new_content:
                    result["success"] = False
                    result["error"] = "Content did not change on previous page"
                    return result

                result["pages_visited"].append(new_page)
                current_page = new_page

            logger.info("Pagination visited pages: %s", result["pages_visited"])

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            logger.exception("Pagination check failed: %s", e)

        print("\nPagination test completed.")
        return result