import os
import re

from playwright.sync_api import expect

from pages.common import PaginationHelper, SearchHelper, TableSection
from config.global_var import DOWNLOADS_PATH
from utils.logger import get_logger

logger = get_logger(__name__)


class DeviceDetailsPage:
    def __init__(self, page):
        self.page = page
        self.search_helper = SearchHelper(page)
        self.table_section = TableSection(page)
        self.pagination_helper = PaginationHelper(page)

    # ------------------ INTERNAL HELPERS ------------------

    def _login_packet_base(self):
        """
        Base locator for 'Last 50 Login Packets' component
        """
        return "//h6[text()='Last 50 Login Packets']/ancestor::div[contains(@class,'component-container')]"

    # ------------------ PAGINATION ------------------

    def set_pagination_for_login_packets(self):
        """
        Override pagination for specific component (Login Packets table)
        """
        self.pagination_helper = PaginationHelper(self.page)

    def get_login_packet_pagination(self):
        """
        Scoped pagination for Login Packets table
        """
        base = self._login_packet_base()

        return PaginationHelper(
            self.page,
            content_selector=f"{base}//table",
            page_input=f"{base}//input[contains(@class,'page-input')]",
            next_button=f"{base}//button[.//mat-icon[text()='chevron_right']]",
            prev_button=f"{base}//button[.//mat-icon[text()='chevron_left']]",
            total_pages_selector=f"{base}//span[contains(text(),'of')]",
        )

    # ------------------ NAVIGATION ------------------

    def go_to_device_details_page(self, url):
        logger.info("Navigating to Device Details page: %s", url)
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        logger.debug("Navigation complete for Device Details")

    def get_title(self):
        heading = self.page.get_by_role("heading", name="Device Details")
        heading.wait_for(state="visible")
        return heading.inner_text()

    def is_page_loaded(self):
        return (
            self.page.url.endswith("/device-details")
            and self.page.get_by_role("heading", name="Device Details").is_visible()
        )

    # ------------------ PAGE ELEMENTS ------------------

    def is_device_details_page_buttons_are_visible(self):
        buttons = self.page.get_by_role("button")
        buttons.first.wait_for(state="visible")

        return all(buttons.nth(i).is_visible() for i in range(buttons.count()))

    def is_device_kpi_cards_visible(self):
        kpi_cards = self.page.locator(".kpi-card")
        kpi_cards.first.wait_for(state="visible")

        return all(kpi_cards.nth(i).is_visible() for i in range(kpi_cards.count()))

    # ------------------ KPI CARDS ------------------

    def _is_cards_visible(self):
        logger.info("Checking KPI card visibility")
        cards_locator = self.page.locator(".kpi-details")
        cards_locator.wait_for(state="visible")
        visible = cards_locator.is_visible()
        logger.info("KPI cards visibility check result: %s", visible)
        return visible

    def _cards_parent(self):
        cards_parent = self.page.locator("div.kpi-section")
        cards_parent.wait_for(state="visible")
        logger.debug("Cards parent container ready")
        return cards_parent

    def _card_elements(self):
        return self._cards_parent().locator(":scope > div")

    def get_cards_count(self):
        count = self._card_elements().count()
        logger.info("Found %s dashboard cards", count)
        return count

    def get_card_element(self, index):
        return self._card_elements().nth(index)

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

    # ------------------ SEARCH ------------------

    def search_for_device(self, device):
        logger.info(f"Searching for device: {device}")
        return self.search_helper.run_search(str(device))

    # ------------------ TABLE ACTIONS ------------------

    def click_on_view_device_in_table(self, device):
        logger.info(f"Clicking view icon for device: {device}")

        row = self.page.locator(f"//tr[td[contains(text(), '{device}')]]")
        row.wait_for(state="visible")

        view_button = row.locator("button:has(mat-icon:has-text('visibility'))")

        if view_button.count() == 0:
            raise Exception(f"View button not found for device {device}")

        view_button.click()

    # ------------------ COMPONENT TITLES ------------------

    def get_table_component_title_text(self, index):
        logger.debug("Getting title for table component index %s", index)
        title_locator = self.page.locator(".component-title").nth(index)
        title_locator.wait_for(state="visible")
        title = title_locator.inner_text()
        logger.info("Table component index %s title text: %s", index, title)
        return title

    # ------------------ HEADERS ------------------

    def get_inside_table_headers_count(self):
        return self.page.locator(".component-body .header").count()

    def get_table_component_headers(self):
        logger.info("Getting headers for table component")

        headers_locator = self.page.locator(".component-body .header")
        headers_locator.first.wait_for(state="visible")

        headers = [
            headers_locator.nth(i).inner_text().strip()
            for i in range(headers_locator.count())
        ]

        logger.info("Table component headers: %s", headers)
        return headers

    # ------------------ LOGIN PACKET TABLE (FIXED) ------------------

    def get_login_packet_table_headers(self):
        """
        Scoped headers for Login Packet table
        """
        base = self._login_packet_base()

        headers = self.page.locator(f"{base}//thead//th")
        headers.first.wait_for(state="visible")

        return [
            headers.nth(i).inner_text().strip().upper() for i in range(headers.count())
        ]

    def get_device_details_table_data(self):
        """
        Scoped table data for Login Packet table
        """
        logger.info("Extracting login packet table data (row-wise)")

        # base = self._login_packet_base()
        # rows = self.page.locator(f"{base}//tbody//tr")

        rows = self.page.locator("tr.ng-star-inserted")
        rows.first.wait_for(state="visible", timeout=5000)

        table_data = []

        for i in range(rows.count()):
            row = rows.nth(i)
            cols = row.locator("td")

            row_data = [cols.nth(j).inner_text().strip() for j in range(cols.count())]

            # if i is zero or not gets anything then check the no data image is present
            if i == 0 and not row_data:
                self.table_section.has_no_data()
                logger.warning("No data found in login packet table")

            table_data.append(row_data)

        logger.info("Extracted table data: %s", table_data)
        return table_data

    # ------------------ EXPORT (FIXED) ------------------

    def check_export_button(self):
        """
        Scoped export button validation
        """
        base = self._login_packet_base()
        export_btn = self.page.locator(
            f"{base}//button[.//text()[contains(.,'Export')]]"
        )

        result = {"success": True, "error": None}

        logger.info("Verifying export button functionality")

        try:
            export_btn.wait_for(state="visible", timeout=10000)
            export_btn.scroll_into_view_if_needed()
            expect(export_btn).to_be_enabled(timeout=10000)

            export_btn.click()
            self.page.wait_for_timeout(2000)

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            logger.exception("Export button verification failed: %s", e)

        return result

    def click_export_button(self):
        """
        Clicks the export button and handles the download.
        Note: The button triggers an async download via backend API.
        """
        # Search for Export button directly on the page
        export_btn = self.page.locator("//button[contains(.,'Export')]")
        export_btn.wait_for(state="visible", timeout=10000)
        export_btn.scroll_into_view_if_needed()

        logger.info("Export button found and scrolled into view")

        # Start listening for the download before clicking
        # The backend may generate the file and trigger download
        with self.page.expect_download(timeout=60000) as download_info:
            # Also wait for any network activity to complete
            logger.info("Clicking export button")
            export_btn.click()
            # Wait a moment for the backend to process
            self.page.wait_for_load_state("networkidle", timeout=10000)
            logger.info("Export button clicked, waiting for download")

        download = download_info.value
        logger.info("Download captured: %s", download.suggested_filename)
        return download
