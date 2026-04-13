from utils.logger import get_logger   # ✅ import logger

class BasePage:
    def __init__(self, page):
        self.page = page
        self.footer = page.locator("div.footer-col.footer-left")
        self.version =page.locator("body app-root app-footer span:nth-child(1)")

    def get_page_title(self):
        return self.page.title()

    def navigate_to(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def wait_for_text(self, text: str):
        return self.page.get_by_text(text, exact=True).wait_for(state="visible")
    
    # # 🔹 Highlight element with border
    # def highlight_element(self, locator):
    #     locator.evaluate("""
    #         element => {
    #             element.style.border = '3px solid red';
    #             element.style.backgroundColor = 'green';

    #             setTimeout(() => {
    #                 element.style.border = '';
    #                 element.style.backgroundColor = '';
    #             }, 1000);
    #         }
    #     """)
        
    #   # 🔥 Auto highlight on click
    # def click(self, locator):
    #     self.highlight_element(locator)
    #     locator.click()

    # # 🔥 Auto highlight on fill
    # def fill(self, locator, value):
    #     self.highlight_element(locator)
    #     locator.fill(value)