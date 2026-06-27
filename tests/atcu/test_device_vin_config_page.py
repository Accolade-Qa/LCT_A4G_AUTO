import pytest

from pages.atcu.device_vin_config_page import DeviceVinConfigPage


@pytest.mark.config
@pytest.mark.atcu
@pytest.mark.regression
class TestDeviceVinConfigPage:
    @pytest.mark.smoke
    def test_device_vin_config_page_loads(self, page, project_config, report_case):
        device_vin_config = DeviceVinConfigPage(
            page, project_config["device_vin_config_url"]
        )
        device_vin_config.load()

        loaded = device_vin_config.is_loaded()
        report_case(
            expected="Device VIN Config page should load",
            actual=f"url={page.url}",
            result="passed" if loaded else "failed",
            message="Validate ATCU Device VIN Config navigation",
        )
        assert loaded
