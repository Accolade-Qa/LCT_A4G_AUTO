from pages.common_utils.search import SearchHelper
from pages.common_utils.table_section import TableSection
from pages.common_utils.pagination import PaginationHelper
from utils.logger import get_logger
from pages.common_base_page import BasePage

logger = get_logger(__name__)

class AtcuAeplResponseLogPage(BasePage):
    """
    this page should mainly for validating the ticket response,
    and validate the data exactly on the ui.
    """

    def __init__(self, page):
        super().__init__(page)
        logger.debug("Initialized AtcuAeplResponseLogPage")

    def get_title(self):
        return super().get_title()

    def is_page_loaded(self):
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
            logger.debug("AEPL Response Log page loaded successfully.")
            return True
        except Exception as e:
            logger.error("AEPL Response Log page failed to load: %s", e)
            return False

    def search_logs(self, item_to_search):
        logger.info("Searching AEPL Response Log for '%s'", item_to_search)

        search = SearchHelper(self.page)
        result = search.run_search(item_to_search)

        logger.debug(
            "Search completed. Success=%s, Results Found=%s",
            result["success"],
            result["results_found"],
        )

        return result

    def get_table_headers(self):
        logger.info("Fetching AEPL Response Log table headers")

        table = TableSection(self.page)
        headers = table.get_headers()

        logger.debug("Retrieved table headers: %s", headers)

        return headers

    def validate_pagination(self):
        logger.info("Validating pagination on AEPL Response Log page")

        pagination = PaginationHelper(self.page)
        result = pagination.verify()

        logger.debug(
            "Pagination validation completed. Success=%s, Pages Visited=%s, Total Pages=%s",
            result["success"],
            result["pages_visited"],
            result["total_pages"],
        )

        return result