from __future__ import annotations

from playwright.sync_api import Locator, Page

from utils.logger import get_logger

logger = get_logger(__name__)


class TableSection:
    def __init__(
        self,
        page: Page,
        table_selector: str = "div.component-body table",
        header_selector: str | None = None,
    ):
        self.page = page
        self.table_selector = table_selector
        self.header_selector = header_selector or f"{table_selector} thead th"

    def wait_for_table(self) -> Locator:
        table_locator = self.page.locator(self.table_selector)
        table_locator.wait_for(state="visible")
        return table_locator

    def get_headers(self) -> list[str]:
        headers_locator = self.page.locator(self.header_selector)
        headers_locator.first.wait_for(state="visible")
        count = headers_locator.count()
        headers = [headers_locator.nth(i).inner_text() for i in range(count)]
        logger.info("Table headers retrieved: %s", headers)
        return headers

    def get_rows(self, row_selector: str = "tbody tr") -> list[str]:
        table = self.wait_for_table()
        rows = table.locator(row_selector)
        values = [rows.nth(i).inner_text() for i in range(rows.count())]
        logger.info("Collected %s rows for selector %s", len(values), row_selector)
        return values
