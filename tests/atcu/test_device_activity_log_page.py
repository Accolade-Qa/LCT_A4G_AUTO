import pytest

from pages.atcu.device_activity_log_page import DeviceActivityLogPage


@pytest.mark.log
@pytest.mark.atcu
@pytest.mark.regression
class TestDeviceActivityLogPage:
    @pytest.mark.smoke
    def test_device_activity_log_page_loads(self, page, project_config, report_case):
        device_activity_log = DeviceActivityLogPage(
            page, project_config["device_activity_log_url"]
        )
        device_activity_log.load()

        loaded = device_activity_log.is_loaded()
        report_case(
            expected="Device Activity Log page should load",
            actual=f"url={page.url}",
            result="passed" if loaded else "failed",
            message="Validate ATCU Device Activity Log navigation",
        )
        assert loaded
