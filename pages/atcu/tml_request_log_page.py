from config.config import TICKET_PASSWORD
from utils.logger import get_logger
from pages.base_page import BasePage
from pages.api.tml_request_api import TmlRequestApi
from pages.common_utils import SearchHelper, TableSection, PaginationHelper

logger = get_logger(__name__)


class TmlRequestLogPage(BasePage):
    """
    this page should mainly for validating the ticket request,
    and validate the data exactly on the ui.
    """

    def __init__(self, page):
        super().__init__(page)
        logger.debug("Initialized OtaPage")

    def get_title(self):
        return super().get_title()

    def is_page_loaded(self):
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
            logger.debug("TML Request Log page loaded successfully.")
            return True
        except Exception as e:
            logger.error("TML Request Log page failed to load: %s", e)
            return False

    def search_logs(self, item_to_search):
        logger.info("Searching TML Request Log for '%s'", item_to_search)

        search = SearchHelper(self.page)
        result = search.run_search(item_to_search)

        logger.debug(
            "Search completed. Success=%s, Results Found=%s",
            result["success"],
            result["results_found"],
        )

        return result

    def get_table_headers(self):
        logger.info("Fetching TML Request Log table headers")

        table = TableSection(self.page)
        headers = table.get_headers()

        logger.debug("Retrieved table headers: %s", headers)

        return headers

    def validate_pagination(self):
        logger.info("Validating pagination on TML Request Log page")

        pagination = PaginationHelper(self.page)
        result = pagination.verify()

        logger.debug(
            "Pagination validation completed. Success=%s, Pages Visited=%s, Total Pages=%s",
            result["success"],
            result["pages_visited"],
            result["total_pages"],
        )

        return result

    def get_tml_request_payload_by_ui(self) -> list[str]:
        """
        Returns all payload values from the TML Request Log table.
        """

        logger.info("Fetching payload values from the TML Request Log table")

        table = TableSection(self.page)
        table_data = table.get_table_data()

        payloads = [row.get("PAYLOAD", "").strip() for row in table_data]

        logger.debug("Retrieved %s payload(s): %s", len(payloads), payloads)

        return payloads

    def get_tml_request_payload_by_api(self):
        """
        Returns the payload values from the TML Request Log API.
        """

        logger.info("Fetching payload values from the TML Request Log API")

        tml_request_api = TmlRequestApi()
        payload, VIN, UIN, ICCID, ticket_number = tml_request_api.post_tml_request_log(
            self.page
        )

        logger.debug(
            "Retrieved payload from API: %s, VIN: %s, UIN: %s, ICCID: %s, Ticket Number: %s",
            payload,
            VIN,
            UIN,
            ICCID,
            ticket_number,
        )

        return payload, VIN, UIN, ICCID, ticket_number
