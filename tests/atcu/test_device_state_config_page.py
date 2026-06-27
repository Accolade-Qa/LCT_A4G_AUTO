import pytest

from pages.atcu.device_state_config_page import DeviceStateConfigPage


@pytest.mark.config
@pytest.mark.atcu
@pytest.mark.regression
class TestDeviceStateConfigPage:
    @pytest.mark.smoke
    def test_device_state_config_page_loads(self, page, project_config, report_case):
        device_state_config = DeviceStateConfigPage(
            page, project_config["device_state_config_url"]
        )
        device_state_config.load()

        loaded = device_state_config.is_loaded()
        report_case(
            expected="Device State Config page should load",
            actual=f"url={page.url}",
            result="passed" if loaded else "failed",
            message="Validate ATCU Device State Config navigation",
        )
        assert loaded
