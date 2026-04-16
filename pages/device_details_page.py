from pages.common import SearchHelper, TableSection
from utils.logger import get_logger


logger = get_logger(__name__)


class DeviceDetailsPage:
    def __init__(self, page):
        self.page = page
        self.search_helper = SearchHelper(page)
        self.table_section = TableSection(page)

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

    def is_device_details_page_buttons_are_visible(self):
        buttons = self.page.get_by_role("button")
        buttons.first.wait_for(state="visible")

        return all(buttons.nth(i).is_visible() for i in range(buttons.count()))

    def is_device_kpi_cards_visible(self):
        kpi_cards = self.page.locator(".kpi-card")
        kpi_cards.first.wait_for(state="visible")

        return all(kpi_cards.nth(i).is_visible() for i in range(kpi_cards.count()))

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

    def search_for_device(self, device):
        logger.info(f"Searching for device: {device}")
        return self.search_helper.run_search(str(device))

    def click_on_view_device_in_table(self, device):
        logger.info(f"Clicking view icon for device: {device}")

        row = self.page.locator(f"//tr[td[contains(text(), '{device}')]]")

        row.wait_for(state="visible")

        view_button = row.locator("button:has(mat-icon:has-text('visibility'))")

        if view_button.count() == 0:
            raise Exception(f"View button not found for device {device}")

        view_button.click()
