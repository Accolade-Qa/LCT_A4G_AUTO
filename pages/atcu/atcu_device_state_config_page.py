from utils.helpers import Helpers
from pages.common_base_page import BasePage
from pages.common_utils import SearchHelper, TableSection, PaginationHelper
from utils.logger import get_logger

logger = get_logger(__name__)

class AtcuDeviceStateConfigPage(BasePage):
    """
        This page is represents the state configuration of the atcu devices
    """
    def __init__(self, page):
        super().__init__(page)
        logger.debug("Initialized AtcuDeviceStateConfigPage with page: %s", page)

    def get_title(self):
        return super().get_title()

    def is_page_loaded(self):
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
            logger.debug("AtcuDeviceStateConfigPage loaded successfully.")
            return True
        except Exception as e:
            logger.error("AtcuDeviceStateConfigPage page failed to load: %s", e)
            return False

    def search_logs(self, item_to_search):
        logger.info("Searching AtcuDeviceStateConfigPage for '%s'", item_to_search)

        search = SearchHelper(self.page)
        result = search.run_search(item_to_search)

        logger.debug(
            "Search completed. Success=%s, Results Found=%s",
            result["success"],
            result["results_found"],
        )

        return result

    def get_table_headers(self):
        logger.info("Fetching AtcuDeviceStateConfigPage table headers")

        table = TableSection(self.page)
        headers = table.get_headers()

        logger.debug("Retrieved table headers: %s", headers)

        return headers

    def validate_pagination(self):
        logger.info("Validating pagination on AtcuDeviceStateConfigPage page")

        pagination = PaginationHelper(self.page)
        result = pagination.verify()

        logger.debug(
            "Pagination validation completed. Success=%s, Pages Visited=%s, Total Pages=%s",
            result["success"],
            result["pages_visited"],
            result["total_pages"],
        )

        return result