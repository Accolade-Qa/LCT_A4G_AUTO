from pages.atcu.simple_atcu_page import SimpleAtcuPage


class AeplResponseLogPage(SimpleAtcuPage):
    def __init__(self, page, url: str):
        super().__init__(page, url, "aepl-response-log", "AEPL")
