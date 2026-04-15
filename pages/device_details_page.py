from utils.logger import get_logger


logger = get_logger(__name__)


class DeviceDetailsPage:
    def __init__(self, page):
        self.page = page

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
