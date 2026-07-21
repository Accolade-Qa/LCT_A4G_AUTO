import ast
import json
import time

from pages.atcu.atcu_tml_request_log_page import AtcuTmlRequestLogPage
from pages.common_utils.search import SearchHelper
from pages.common_utils.table_section import TableSection
from pages.common_utils.pagination import PaginationHelper
from utils.logger import get_logger
from pages.common_base_page import BasePage

logger = get_logger(__name__)


class AtcuAeplResponseLogPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.request_log = AtcuTmlRequestLogPage(page)
        logger.debug("Initialized AtcuAeplResponseLogPage")

    def get_title(self):
        title = self.page.locator(".page-title").text_content()
        logger.debug("AEPL Response Log page title retrieved: %s", title)
        return title

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

    def get_valid_request_response_by_api(self):
        logger.info("Fetching valid request-response pairs from AEPL Response Log API")

        payload, VIN, UIN, ICCID, ticket_number, data  = (
            self.request_log.get_tml_request_payload_by_api()
        )

        return payload, VIN, UIN, ICCID, ticket_number, data
    

    @staticmethod
    def _normalize_payload_value(payload):
        if isinstance(payload, str):
            value = payload.strip()
            if not value:
                return payload

            try:
                return json.loads(value)
            except json.JSONDecodeError:
                try:
                    return ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    return payload

        return payload

    def get_table_data_first_row(self):
        logger.info("Fetching first row data from AEPL Response Log table")

        table = TableSection(self.page)
        first_row_data = table.get_row_data(0)
        if isinstance(first_row_data, dict):
            first_row_data["PAYLOAD"] = self._normalize_payload_value(
                first_row_data.get("PAYLOAD")
            )
        logger.debug("Retrieved first row data: %s", first_row_data)
        return first_row_data

    def get_matching_row_for_api_data(
        self,
        expected_data: dict,
        max_attempts: int = 20,
        delay_seconds: int = 3,
    ):
        logger.info("Searching AEPL Response Log table for a row matching API data")

        expected_ticket = expected_data.get("TICKET_NO")
        expected_vin = expected_data.get("VIN_NO")
        expected_uin = expected_data.get("UIN_NO")
        expected_iccid = expected_data.get("ICCID")
        search_terms = expected_vin

        for attempt in range(max_attempts):
            if attempt > 0:
                logger.info(
                    "No matching AEPL row found on attempt %s. Reloading page and retrying...",
                    attempt,
                )
                self.page.reload()
                self.is_page_loaded()
                time.sleep(delay_seconds)
            else:
                self.page.wait_for_timeout(2000)

            try:
                pagination = PaginationHelper(self.page)
                total_pages = pagination.get_pagination_count()
            except Exception as exc:
                logger.warning("Pagination detection failed: %s", exc)
                total_pages = 1

            logger.info("Checking AEPL Response Log across %s page(s)", total_pages)

            for page_number in range(1, total_pages + 1):
                if page_number > 1:
                    next_button = self.page.locator(
                        "button:has(mat-icon:has-text('chevron_right'))"
                    )
                    if next_button.count() > 0 and not next_button.is_disabled():
                        next_button.click()
                        self.page.wait_for_timeout(1500)
                    else:
                        break

                table = TableSection(self.page)
                table_data = table.get_table_data()

                for row in table_data:
                    payload_value = self._normalize_payload_value(row.get("PAYLOAD"))
                    if not isinstance(payload_value, dict):
                        continue

                    if expected_ticket and payload_value.get("TICKET_NO") == expected_ticket:
                        matched_row = dict(row)
                        matched_row["PAYLOAD"] = payload_value
                        logger.info(
                            "Matched AEPL Response Log row by ticket number on page %s: %s",
                            page_number,
                            matched_row,
                        )
                        return matched_row

                    if expected_vin and payload_value.get("VIN_NO") == expected_vin:
                        matched_row = dict(row)
                        matched_row["PAYLOAD"] = payload_value
                        logger.info(
                            "Matched AEPL Response Log row by VIN on page %s: %s",
                            page_number,
                            matched_row,
                        )
                        return matched_row

                    if (
                        expected_iccid
                        and expected_uin
                        and payload_value.get("ICCID") == expected_iccid
                        and payload_value.get("UIN_NO") == expected_uin
                    ):
                        matched_row = dict(row)
                        matched_row["PAYLOAD"] = payload_value
                        logger.info(
                            "Matched AEPL Response Log row by shared ICCID/UIN on page %s: %s",
                            page_number,
                            matched_row,
                        )
                        return matched_row

            for search_term in search_terms:
                try:
                    search_result = self.search_logs(str(search_term))
                    if search_result.get("success") and search_result.get("results_found", 0) > 0:
                        logger.info(
                            "Search for '%s' returned results; re-reading table.",
                            search_term,
                        )
                        break
                except AssertionError as exc:
                    logger.warning("Search attempt for '%s' failed: %s", search_term, exc)

            if attempt < max_attempts - 1:
                time.sleep(delay_seconds)

        logger.warning("No matching AEPL Response Log row found for API data: %s", expected_data)
        return None