from pandas.plotting import table

from pages.common.table_section import TableSection
from utils.logger import get_logger
from pages.base_page import BasePage

logger = get_logger(__name__)


class GovtServerPage(BasePage):
    def __init__(self, page):
        self.page = page

    def get_page_title(self):
        """Get the title of the Government Server page"""
        title = super().get_title()
        logger.debug("Retrieved Government Server page title: %s", title)
        return title

    def get_table_headers(self):
        """Get the headers of the table on the Government Server page"""
        table = TableSection(self.page)
        if table.has_no_data():
            logger.warning(
                "Government Server table has no data, cannot retrieve headers"
            )
            return []

        headers = table.get_headers()
        logger.debug("Retrieved Government Server table headers: %s", headers)
        return headers
