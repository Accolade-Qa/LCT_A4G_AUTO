import pytest

from pages.atcu.status_update_log_page import StatusUpdateLogPage


@pytest.mark.log
@pytest.mark.atcu
@pytest.mark.regression
class TestStatusUpdateLogPage:
    @pytest.mark.smoke
    def test_status_update_log_page_loads(self, page, project_config, report_case):
        status_update_log = StatusUpdateLogPage(
            page, project_config["status_update_log_url"]
        )
        status_update_log.load()

        loaded = status_update_log.is_loaded()
        report_case(
            expected="Status Update Log page should load",
            actual=f"url={page.url}",
            result="passed" if loaded else "failed",
            message="Validate ATCU Status Update Log navigation",
        )
        assert loaded
