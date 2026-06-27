from pages.atcu.simple_atcu_page import SimpleAtcuPage


class TmlRequestLogPage(SimpleAtcuPage):
    def __init__(self, page, url: str):
        super().__init__(page, url, "tml-request-log", "TML")
