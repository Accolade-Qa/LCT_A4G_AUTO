from pages.atcu.simple_atcu_page import SimpleAtcuPage


class MyAisTicketPage(SimpleAtcuPage):
    def __init__(self, page, url: str):
        super().__init__(page, url, "my-ais-ticket", "Ticket")
