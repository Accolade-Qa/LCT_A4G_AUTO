from pages.atcu.simple_atcu_page import SimpleAtcuPage


class TicketDashboardPage(SimpleAtcuPage):
    def __init__(self, page, url: str):
        super().__init__(page, url, "ticket-dashboard", "Ticket")
