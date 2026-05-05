from __future__ import annotations

from typing import Sequence

from playwright.sync_api import Page

from utils.logger import get_logger

logger = get_logger(__name__)


class SearchHelper:
    def __init__(
        self,
        page: Page,
        input_selector: str = "//input[@placeholder='Search and Press Enter']",
        row_selector: str = "tr.ng-star-inserted",
    ):
        self.page = page
        self.input_selector = input_selector
        self.row_selector = row_selector

    def run_search(self, query: str) -> dict[str, Sequence[str] | int | bool | None]:
        result = {
            "success": True,
            "results_found": 0,
            "results": [],
            "error": None,
        }

        try:
            search_input = self.page.locator(self.input_selector)
            search_input.wait_for(state="visible")
            logger.info("Executing search for query '%s'", query)
            search_input.fill(query)
            search_input.press("Enter")
            self.page.wait_for_timeout(1000)

            rows = self.page.locator(self.row_selector)
            result["results_found"] = rows.count()

            for i in range(result["results_found"]):
                row_text = rows.nth(i).inner_text()
                result["results"].append(row_text)

            logger.info("%s rows found for query '%s'", result["results_found"], query)
        except Exception as exc:
            logger.exception("Search helper failed for query '%s': %s", query, exc)
            result["success"] = False
            result["error"] = str(exc)

        return result
