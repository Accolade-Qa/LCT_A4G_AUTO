from playwright.sync_api import expect


class DashboardPage:
    def __init__(self, page):
        self.page = page
        
    def go_to_dashboard(self, url):
        self.page.goto(url)
    
    def _is_cards_visible(self):
        cards_locator = self.page.locator(".kpi-section.ng-star-inserted")
        cards_locator.wait_for(state="visible")
        return cards_locator.is_visible()
    
    def _cards_parent(self):
        cards_parent = self.page.locator("div.kpi-section.ng-star-inserted")
        cards_parent.wait_for(state="visible")
        return cards_parent

    def _card_elements(self):
        return self._cards_parent().locator(":scope > div")

    def get_cards_count(self):
        return self._card_elements().count()

    def get_card_element(self, index):
        return self._card_elements().nth(index)
    
    def get_cards_title_text(self, index):
        card = self.get_card_element(index)
        card_title_locator = card.locator("div.kpi-details span").nth(0)
        card_title_locator.wait_for(state="visible")
        return card_title_locator.inner_text()
    
    def get_cards_inner_count(self, index):
        card = self.get_card_element(index)
        card_count_locator = card.locator("div.kpi-details span").nth(1)
        card_count_locator.wait_for(state="visible")
        return card_count_locator.inner_text()
    
    def _is_graph_visible(self):
        graph_locator = self.page.locator(".graph-section.ng-star-inserted")
        graph_locator.wait_for(state="visible")
        return graph_locator.is_visible()
    
    def get_graph_title(self, title):
        graph_title_locator = self.page.locator(f"h3:has-text('{title}')")
        graph_title_locator.wait_for(state="visible")
        return graph_title_locator.inner_text()
    
    def _is_table_visible(self):
        table_locator = self.page.locator("//div[@class='component-body']//table")
        table_locator.wait_for(state="visible")
        return table_locator.is_visible()
    
    # def _is_buttons_visible(self):
    #     buttons_locator = self.page.get_by_role("button")
    #     buttons_locator.wait_for(state="visible")
    #     self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    #     return buttons_locator.is_visible()
    
    def get_table_title_after_card_click(self, title):
        card_locator = (
            self.page
            .locator("div.kpi-section.ng-star-inserted div.kpi-details span.kpi-content")
            .filter(has_text=title)
            .first
        )
        card_locator.wait_for(state="visible")
        card_locator.click()

        table_title_locator = self.page.locator(".component-title")
        expect(table_title_locator).to_have_text(title, timeout=5000)
        return table_title_locator.inner_text()
      
    def check_pagination(self):
        PAGE_INPUT = "input.page-input"
        NEXT_BUTTON = "button:has(mat-icon:has-text('chevron_right'))"
        CONTENT_CONTAINER = "table"  

        result = {
            "success": True,
            "pages_visited": [],
            "total_pages": 0,
            "error": None
        }

        try:
            self.page.wait_for_selector(PAGE_INPUT)
            self.page.wait_for_selector(CONTENT_CONTAINER)

            print("Pagination detected")

            visited_pages = set()

            while True:
                current_page = self.page.locator(PAGE_INPUT).input_value()
                print(f"\nCurrent page: {current_page}")

                # Prevent infinite loop
                if current_page in visited_pages:
                    print("Loop detected. Stopping.")
                    break

                visited_pages.add(current_page)
                result["pages_visited"].append(int(current_page))

                prev_content = self.page.locator(CONTENT_CONTAINER).inner_text()

                next_btn = self.page.locator(NEXT_BUTTON)

                if next_btn.count() == 0:
                    result["success"] = False
                    result["error"] = "Next button not found"
                    break

                if next_btn.is_disabled():
                    print("Reached last page.")
                    break

                print("Clicking Next...")
                next_btn.scroll_into_view_if_needed()
                next_btn.click()

                # Wait for page number change
                self.page.wait_for_function(
                    """(prev) => {
                        const el = document.querySelector('input.page-input');
                        return el && el.value !== prev;
                    }""",
                    arg=current_page
                )

                new_page = self.page.locator(PAGE_INPUT).input_value()

                # Validate page increment
                if int(new_page) != int(current_page) + 1:
                    result["success"] = False
                    result["error"] = f"Page did not increment correctly: {current_page} -> {new_page}"
                    break

                self.page.wait_for_timeout(500)

                new_content = self.page.locator(CONTENT_CONTAINER).inner_text()

                if prev_content == new_content:
                    result["success"] = False
                    result["error"] = "Content did not change after pagination"
                    break

            result["total_pages"] = len(result["pages_visited"])

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)

        print("\nPagination test completed.")
        return result


    def check_export_button(self):
        export_btn = self.page.get_by_text("Export download")

        result = {
            "success": True,
            "file_downloaded": False,
            "file_format": None,
            "error": None
        }

        try:
            export_btn.wait_for(state="visible")

            with self.page.expect_download() as download_info:
                export_btn.click()

            download = download_info.value

            result["file_downloaded"] = True
            result["file_format"] = download.suggested_filename.split(".")[-1]

            if result["file_format"] != "csv":
                result["success"] = False
                result["error"] = f"Expected file format 'csv', got '{result['file_format']}'"

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)

        return result