from __future__ import annotations

from playwright.sync_api import Locator, Page

from utils.logger import get_logger

logger = get_logger(__name__)


class TableSection:
    def __init__(
        self,
        page: Page,
        table_selector: str | Locator = "div.component-body table",
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

        headers = [
            headers_locator.nth(i).inner_text().strip()
            for i in range(headers_locator.count())
        ]

        logger.info("Table headers retrieved: %s", headers)
        return headers

    def get_rows(self, row_selector: str = "tbody tr") -> list[str]:
        table = self.wait_for_table()
        rows = table.locator(row_selector)

        values = [rows.nth(i).inner_text().strip() for i in range(rows.count())]

        logger.info("Collected %s rows for selector %s", len(values), row_selector)
        return values

    def has_no_data(self) -> bool:
        """
        Detect 'No Data Found' state
        """

        no_data_text = self.page.locator(f"{self.table_selector} >> text=No Data Found")

        if no_data_text.count() > 0:
            return no_data_text.first.is_visible()

        return self.page.locator(
            f"{self.table_selector} img[alt='No Data Found']"
        ).is_visible()

    def get_row_count(self) -> int:
        rows = self.page.locator(f"{self.table_selector} tbody tr")
        return rows.count()

    def validate_table_data(
        self,
        expected_list: list,
        iccid_key: str = "iccid",
    ):
        """
        Generic reusable validator
        """

        if expected_list:
            row_count = self.get_row_count()

            assert row_count > 0, "Expected data but table is empty"

            ui_text = self.page.locator(self.table_selector).inner_text()

            expected_iccids = [item.get(iccid_key) for item in expected_list]

            for iccid in expected_iccids:
                assert iccid in ui_text, f"{iccid} not found in UI table"

        else:
            assert self.has_no_data(), "Expected 'No Data Found' but table has data"

    def get_table_data(self) -> list[dict[str, str]]:
        """
        Returns complete table data in row-wise dictionary format

        Example:
        [
            {
                "ICCID": "12345",
                "Status": "Active"
            },
            {
                "ICCID": "67890",
                "Status": "Inactive"
            }
        ]
        """

        table = self.wait_for_table()
        headers = self.get_headers()

        rows = table.locator("tbody tr")

        table_data = []

        for i in range(rows.count()):
            cells = rows.nth(i).locator("td")

            row_dict = {
                headers[j]: cells.nth(j).inner_text().strip()
                for j in range(cells.count())
            }

            table_data.append(row_dict)

        logger.info("Extracted table data: %s", table_data)

        return table_data

    def get_row_data(self, row_index: int) -> dict[str, str]:
        """
        Returns data of a specific row index

        Example:
        {
            "ICCID": "12345",
            "Status": "Active"
        }
        """

        table = self.wait_for_table()
        headers = self.get_headers()

        rows = table.locator("tbody tr")

        total_rows = rows.count()

        if row_index >= total_rows:
            raise IndexError(
                f"Row index {row_index} out of range. Total rows: {total_rows}"
            )

        cells = rows.nth(row_index).locator("td")

        row_data = {
            headers[j]: cells.nth(j).inner_text().strip() for j in range(cells.count())
        }

        logger.info("Extracted row data at index %s: %s", row_index, row_data)

        return row_data
