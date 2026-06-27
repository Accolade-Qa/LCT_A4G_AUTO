import pytest

from pages.atcu.fota_page import FotaPage


@pytest.mark.atcu
@pytest.mark.regression
class TestFotaPage:
    @pytest.mark.smoke
    def test_fota_page_loads(self, page, project_config, report_case):
        fota = FotaPage(page, project_config["fota_url"])
        fota.load()

        loaded = fota.is_loaded()
        report_case(
            expected="FOTA page should load",
            actual=f"url={page.url}",
            result="passed" if loaded else "failed",
            message="Validate ATCU FOTA navigation",
        )
        assert loaded
