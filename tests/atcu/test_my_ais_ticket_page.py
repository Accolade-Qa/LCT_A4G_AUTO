import pytest

from pages.atcu.my_ais_ticket_page import MyAisTicketPage


@pytest.mark.ticket
@pytest.mark.atcu
@pytest.mark.regression
class TestMyAisTicketPage:
    @pytest.mark.smoke
    def test_my_ais_ticket_page_loads(self, page, project_config, report_case):
        my_ais_ticket = MyAisTicketPage(page, project_config["my_ais_ticket_url"])
        my_ais_ticket.load()

        loaded = my_ais_ticket.is_loaded()
        report_case(
            expected="My AIS Ticket page should load",
            actual=f"url={page.url}",
            result="passed" if loaded else "failed",
            message="Validate ATCU My AIS Ticket navigation",
        )
        assert loaded
