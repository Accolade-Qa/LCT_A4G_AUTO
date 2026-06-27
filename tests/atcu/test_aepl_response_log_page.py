import pytest

from pages.atcu.aepl_response_log_page import AeplResponseLogPage


@pytest.mark.log
@pytest.mark.atcu
@pytest.mark.regression
class TestAeplResponseLogPage:
    @pytest.mark.smoke
    def test_aepl_response_log_page_loads(self, page, project_config, report_case):
        aepl_response_log = AeplResponseLogPage(
            page, project_config["aepl_response_log_url"]
        )
        aepl_response_log.load()

        loaded = aepl_response_log.is_loaded()
        report_case(
            expected="AEPL Response Log page should load",
            actual=f"url={page.url}",
            result="passed" if loaded else "failed",
            message="Validate ATCU AEPL Response Log navigation",
        )
        assert loaded
