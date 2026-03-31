class BasePage:
    def __init__(self, page):
        self.page = page

    def get_page_title(self):
        return self.page.title()

    def navigate_to(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def wait_for_text(self, text: str):
        return self.page.get_by_text(text, exact=True).wait_for(state="visible")