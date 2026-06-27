import pytest

from pages.atcu.tml_request_log_page import TmlRequestLogPage


@pytest.mark.log
@pytest.mark.atcu
@pytest.mark.regression
class TestTmlRequestLogPage:
    @pytest.mark.smoke
    def test_tml_request_log_page_loads(self, page, project_config, report_case):
        tml_request_log = TmlRequestLogPage(
            page, project_config["tml_request_log_url"]
        )
        tml_request_log.load()

        loaded = tml_request_log.is_loaded()
        report_case(
            expected="TML Request Log page should load",
            actual=f"url={page.url}",
            result="passed" if loaded else "failed",
            message="Validate ATCU TML Request Log navigation",
        )
        assert loaded
