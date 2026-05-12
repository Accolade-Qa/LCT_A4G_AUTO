from playwright.sync_api import expect

from pages.common import PaginationHelper, SearchHelper, TableSection

from utils.logger import get_logger

logger = get_logger(__name__)


class DashboardPage:
    def __init__(self, page):
        logger.debug("Initializing DashboardPage with page object")
        self.page = page
        logger.info("DashboardPage initialized for page %s", page.url)
        logger.debug("Setting up TableSection helper")
        self.table_section = TableSection(page)
        logger.debug("Setting up PaginationHelper")
        self.pagination_helper = PaginationHelper(page)
        logger.debug("Setting up SearchHelper")
        self.search_helper = SearchHelper(page)
        logger.info("All DashboardPage helpers initialized successfully")

    def go_to_dashboard(self, url):
        logger.info("Navigating to dashboard URL %s", url)

        logger.debug("Calling page.goto() with URL")

        self.page.goto(url)

        logger.debug("Dashboard goto complete, waiting for network idle")

        self.page.wait_for_load_state("networkidle")

        current_url = self.page.url

        logger.info("Successfully navigated to dashboard and page fully loaded")

        logger.debug("Current dashboard URL: %s", current_url)

        return current_url

    def _is_cards_visible(self):
        logger.info("Checking KPI card visibility")
        cards_locator = self.page.locator(".kpi-section.ng-star-inserted")
        cards_locator.wait_for(state="visible")
        visible = cards_locator.is_visible()
        logger.info("KPI cards visibility check result: %s", visible)
        return visible

    def _cards_parent(self):
        logger.debug("Retrieving cards parent container locator")
        cards_parent = self.page.locator("div.kpi-section.ng-star-inserted")
        logger.debug("Waiting for cards parent container to be visible")
        cards_parent.wait_for(state="visible")
        logger.debug("Cards parent container is now visible and ready")
        return cards_parent

    def _card_elements(self):
        logger.debug("Retrieving all card element locators")
        card_elements = self._cards_parent().locator(":scope > div")
        logger.debug("Card elements locator retrieved successfully")
        return card_elements

    def get_cards_count(self):
        count = self._card_elements().count()
        logger.info("Found %s dashboard cards", count)
        return count

    def get_card_element(self, index):
        logger.debug("Retrieving card element at index %s", index)
        card_element = self._card_elements().nth(index)
        logger.debug("Card element at index %s retrieved", index)
        return card_element

    def get_cards_title_text(self, index):
        logger.debug("Getting title for card index %s", index)
        card = self.get_card_element(index)
        card_title_locator = card.locator("div.kpi-details span").nth(0)
        card_title_locator.wait_for(state="visible")
        title = card_title_locator.inner_text()
        logger.info("Card index %s title text: %s", index, title)
        return title

    def get_cards_inner_count(self, index):
        logger.debug("Getting count for card index %s", index)
        card = self.get_card_element(index)
        card_count_locator = card.locator("div.kpi-details span").nth(1)
        card_count_locator.wait_for(state="visible")
        count_text = card_count_locator.inner_text()
        logger.info("Card index %s displayed count: %s", index, count_text)
        return count_text

    def _is_graph_visible(self):
        logger.info("Checking graph visibility")
        graph_locator = self.page.locator(".graph-section.ng-star-inserted")
        graph_locator.wait_for(state="visible")
        visible = graph_locator.is_visible()
        logger.info("Graph visibility result: %s", visible)
        return visible

    def get_graph_title(self, title):
        logger.debug("Querying graph title for '%s'", title)
        graph_title_locator = self.page.locator(f"h3:has-text('{title}')")
        graph_title_locator.wait_for(state="visible")
        text = graph_title_locator.inner_text()
        logger.info("Graph title text resolved: %s", text)
        return text

    def _is_table_visible(self):
        logger.info("Checking if dashboard table is visible")
        logger.debug("Retrieving table locator")
        table_locator = self.page.locator("//div[@class='component-body']//table")
        logger.debug("Waiting for table to be visible")
        table_locator.wait_for(state="visible")
        logger.debug("Table is now visible, checking visibility status")
        visible = table_locator.is_visible()
        logger.info("Dashboard table visibility result: %s", visible)
        return visible

    # def _is_buttons_visible(self):
    #     buttons_locator = self.page.get_by_role("button")
    #     buttons_locator.wait_for(state="visible")
    #     self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    #     return buttons_locator.is_visible()

    def get_table_title_after_card_click(self, title):
        logger.info("Attempting to click KPI card with title: %s", title)
        logger.debug("Building card locator filter for title: %s", title)
        card_locator = (
            self.page.locator(
                "div.kpi-section.ng-star-inserted div.kpi-details span.kpi-content"
            )
            .filter(has_text=title)
            .first
        )
        logger.debug("Waiting for card locator to be visible")
        card_locator.wait_for(state="visible")
        logger.debug("Card locator visible, clicking the card")
        card_locator.click()
        logger.info("Successfully clicked KPI card: %s", title)

        logger.debug("Retrieving table title locator")
        table_title_locator = self.page.locator(".component-title")
        logger.debug("Verifying table title contains expected text: %s", title)
        expect(table_title_locator).to_have_text(title, timeout=5000)
        logger.debug("Table title verification passed")
        real_title = table_title_locator.inner_text()
        logger.info("Table title after card click: %s", real_title)
        return real_title

    def check_export_button(self):
        logger.info("Verifying export button functionality")
        logger.debug("Retrieving export button locator")
        export_btn = self.page.locator("button:has-text('Export')")

        result = {"success": True, "error": None}

        try:
            logger.debug("Waiting for export button to be visible")
            export_btn.wait_for(state="visible", timeout=10000)
            logger.debug("Export button visible, scrolling into view if needed")
            export_btn.scroll_into_view_if_needed()
            logger.debug("Verifying export button is enabled")
            expect(export_btn).to_be_enabled(timeout=10000)
            logger.debug("Export button is enabled, clicking it")
            export_btn.click()
            logger.debug("Export button clicked, waiting for processing")
            self.page.wait_for_timeout(2000)
            logger.info("Export button verification completed successfully")

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            logger.exception("Export button verification failed: %s", e)

        return result

    def search_for_device(self, device):
        logger.info("Searching for device: %s", device)
        logger.debug("Delegating search to SearchHelper")
        search_result = self.search_helper.run_search(str(device))
        logger.info("Device search completed for: %s", device)
        return search_result

    def click_on_view_device_in_table(self, device):
        logger.info("Clicking view icon for device: %s", device)
        logger.debug("Building row locator for device: %s", device)
        row = self.page.locator(f"//tr[td[contains(text(), '{device}')]]")
        logger.debug("Waiting for device row to be visible")
        row.wait_for(state="visible")
        logger.debug("Device row is visible, retrieving view button locator")
        view_button = row.locator("button:has(mat-icon:has-text('visibility'))")
        logger.debug("Checking if view button exists for device: %s", device)
        if view_button.count() == 0:
            logger.error("View button not found for device: %s", device)
            raise Exception(f"View button not found for device {device}")
        logger.debug("View button found, clicking it")
        view_button.click()
        logger.info("Successfully clicked view button for device: %s", device)
