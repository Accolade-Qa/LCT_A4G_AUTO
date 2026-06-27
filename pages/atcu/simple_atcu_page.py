from pages.base_page import BasePage


class SimpleAtcuPage(BasePage):
    """Generic page object for ATCU pages that only need navigation smoke checks."""

    def __init__(self, page, url: str, expected_path: str, title_text: str):
        super().__init__(page)
        self.url = url
        self.expected_path = expected_path
        self.title_text = title_text

    def load(self):
        self.navigate_to(self.url)

    def is_loaded(self) -> bool:
        self.page.wait_for_load_state("networkidle")
        return self.expected_path in self.page.url

    def has_page_text(self) -> bool:
        locator = self.page.get_by_text(self.title_text, exact=False).first
        try:
            locator.wait_for(state="visible", timeout=5000)
            return locator.is_visible()
        except Exception:
            return False
