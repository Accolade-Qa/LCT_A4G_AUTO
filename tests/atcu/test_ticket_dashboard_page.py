import pytest

from pages.atcu.ticket_dashboard_page import TicketDashboardPage


@pytest.mark.ticket
@pytest.mark.atcu
@pytest.mark.regression
class TestTicketDashboardPage:
    @pytest.mark.smoke
    def test_ticket_dashboard_page_loads(self, page, project_config, report_case):
        ticket_dashboard = TicketDashboardPage(
            page, project_config["ticket_dashboard_url"]
        )
        ticket_dashboard.load()

        loaded = ticket_dashboard.is_loaded()
        report_case(
            expected="Ticket Dashboard page should load",
            actual=f"url={page.url}",
            result="passed" if loaded else "failed",
            message="Validate ATCU Ticket Dashboard navigation",
        )
        assert loaded
