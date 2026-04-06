class BasePage:
    def __init__(self, page):
        self.page = page

    def get_page_title(self):
        return self.page.title()
    
    def get_title(self):
        # page.locator(".page-title")
        locator = self.page.locator(".page-title")
        locator.wait_for(state="visible")
        return locator.text_content()

    def navigate_to(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def wait_for_text(self, text: str):
        locator = self.page.get_by_text(text, exact=True)
        locator.wait_for(state="visible")
        return locator
