from pathlib import Path

import pytest

from config.config import (
    ADD_PRODUCTION_URL,
    BASE_URL,
    CREATE_PRODUCTION_URL,
    PASSWORD,
    PRODUCTION_PAGE_URL,
    USERNAME,
)
from pages.login_page import LoginPage
from pages.production_devices_page import ProductionDevices
from utils.logger import get_logger

TEST_DATA_DIR_PROD = Path(__file__).resolve().parents[1] / "test_data"
logger = get_logger(__name__)


@pytest.mark.device
@pytest.mark.regression
class TestProductionDevices:
    def _login_and_dashboard(self, page):
        login_page = LoginPage(page)
        login_page.load(BASE_URL)
        login_page.login(USERNAME, PASSWORD)

        return ProductionDevices(page)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_go_to_prod(self, page, report_case):
        logger.info("Starting validation of Production Devices page navigation")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)

        actual_url = page.url
        logger.debug(
            "Production Devices URL check | expected=%s | actual=%s",
            PRODUCTION_PAGE_URL,
            actual_url,
        )

        report_case(
            expected=PRODUCTION_PAGE_URL,
            actual=actual_url,
            message="Validate Production Devices page navigation",
        )

        assert actual_url == PRODUCTION_PAGE_URL, (
            f"Expected URL '{PRODUCTION_PAGE_URL}', got '{actual_url}'"
        )
        logger.info("Successfully validated Production Devices page navigation")

    @pytest.mark.regression
    def test_nav_list_visibility(self, page, report_case):
        logger.info("Starting validation of Production navbar list visibility")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)

        is_visible = production_page._nav_list_visibility()
        logger.debug("Production navbar list visible: %s", is_visible)

        report_case(
            expected="Navbar list should be visible",
            actual=f"Navbar list visible: {is_visible}",
            message="Validate Production navbar list visibility",
        )

        assert is_visible, "Navbar list is not visible"
        logger.info("Successfully validated Production navbar list visibility")

    @pytest.mark.regression
    def test_is_PageTitle_Visible(self, page, report_case):
        logger.info("Starting validation of Production page title visibility")
        production_page = self._login_and_dashboard(page)

        is_visible = production_page._is_PageTitle_Visible()
        logger.debug("Production page title visible: %s", is_visible)

        report_case(
            expected="Page title should be visible",
            actual=f"Page title visible: {is_visible}",
            message="Validate Production page title visibility",
        )

        assert is_visible, "Page Title is not visible"
        logger.info("Successfully validated Production page title visibility")

    @pytest.mark.regression
    def test_manual_upload_btn_visibility(self, page, report_case):
        logger.info("Starting validation of Manual Upload button visibility")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)

        is_visible = production_page._manual_upload_btn_visibility()
        logger.debug("Manual Upload button visible: %s", is_visible)

        report_case(
            expected="Manual Upload button should be visible",
            actual=f"Manual Upload button visible: {is_visible}",
            message="Validate Manual Upload button visibility",
        )

        assert is_visible, "Manual Upload button is not visible"
        logger.info("Successfully validated Manual Upload button visibility")

    @pytest.mark.regression
    def test_manual_upload_click(self, page, report_case):
        logger.info("Starting validation of Manual Upload button click")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._manual_upload_click()

        actual_url = page.url
        logger.debug("Manual Upload click completed | current_url=%s", actual_url)

        report_case(
            expected="Manual Upload button click should complete",
            actual=f"Current URL after click: {actual_url}",
            message="Validate Manual Upload button click",
        )

        logger.info("Successfully validated Manual Upload button click")

    @pytest.mark.regression
    def test_create_prod_PageTitle(self, page, report_case):
        logger.info("Starting validation of Create Production page title")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)

        is_visible = production_page._create_prod_PageTitle()
        logger.debug("Create Production page title visible: %s", is_visible)

        report_case(
            expected="Create Production page title should be visible",
            actual=f"Create Production page title visible: {is_visible}",
            message="Validate Create Production page title",
        )

        assert is_visible, "Create production page title is not visible"
        logger.info("Successfully validated Create Production page title")

    @pytest.mark.regression
    def test_new_uid(self, page, report_case):
        logger.info("Starting validation of New UID input")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_uid()

        logger.debug("Completed New UID input validation")
        report_case(
            expected="New UID field should accept valid input",
            actual="New UID input validation completed",
            message="Validate New UID input",
        )

        logger.info("Successfully validated New UID input")

    @pytest.mark.regression
    def test_new_imei(self, page, report_case):
        logger.info("Starting validation of New IMEI input")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_imei()

        logger.debug("Completed New IMEI input validation")
        report_case(
            expected="New IMEI field should accept valid input",
            actual="New IMEI input validation completed",
            message="Validate New IMEI input",
        )

        logger.info("Successfully validated New IMEI input")

    @pytest.mark.regression
    def test_new_iccid(self, page, report_case):
        logger.info("Starting validation of New ICCID input")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_iccid()

        logger.debug("Completed New ICCID input validation")
        report_case(
            expected="New ICCID field should accept valid input",
            actual="New ICCID input validation completed",
            message="Validate New ICCID input",
        )

        logger.info("Successfully validated New ICCID input")

    @pytest.mark.regression
    def test_new_model_name(self, page, report_case):
        logger.info("Starting validation of New Model Name input")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_model_name(value="Model Name")

        logger.debug("Entered New Model Name value: %s", "Model Name")
        report_case(
            expected="New Model Name field should accept value 'Model Name'",
            actual="New Model Name value entered",
            message="Validate New Model Name input",
        )

        logger.info("Successfully validated New Model Name input")

    @pytest.mark.regression
    def test_new_mobile_no(self, page, report_case):
        logger.info("Starting validation of New Mobile Number input")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_mobile_no()

        logger.debug("Completed New Mobile Number input validation")
        report_case(
            expected="New Mobile Number field should accept valid input",
            actual="New Mobile Number input validation completed",
            message="Validate New Mobile Number input",
        )

        logger.info("Successfully validated New Mobile Number input")

    @pytest.mark.regression
    def test__new_service_provider(self, page, report_case):
        logger.info("Starting validation of New Service Provider input")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_service_provider()

        logger.debug("Completed New Service Provider input validation")
        report_case(
            expected="New Service Provider field should accept valid input",
            actual="New Service Provider input validation completed",
            message="Validate New Service Provider input",
        )

        logger.info("Successfully validated New Service Provider input")

    @pytest.mark.regression
    def test_new_alt_mob_no(self, page, report_case):
        logger.info("Starting validation of Alternate Mobile Number input")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_alt_mob_no()

        logger.debug("Completed Alternate Mobile Number input validation")
        report_case(
            expected="Alternate Mobile Number field should accept valid input",
            actual="Alternate Mobile Number input validation completed",
            message="Validate Alternate Mobile Number input",
        )

        logger.info("Successfully validated Alternate Mobile Number input")

    @pytest.mark.regression
    def test_new_alt_ser_pro(self, page, report_case):
        logger.info("Starting validation of Alternate Service Provider input")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_alt_ser_pro()

        logger.debug("Completed Alternate Service Provider input validation")
        report_case(
            expected="Alternate Service Provider field should accept valid input",
            actual="Alternate Service Provider input validation completed",
            message="Validate Alternate Service Provider input",
        )

        logger.info("Successfully validated Alternate Service Provider input")

    @pytest.mark.regression
    def test_new_firmware(self, page, report_case):
        logger.info("Starting validation of New Firmware input")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_firmware()

        logger.debug("Completed New Firmware input validation")
        report_case(
            expected="New Firmware field should accept valid input",
            actual="New Firmware input validation completed",
            message="Validate New Firmware input",
        )

        logger.info("Successfully validated New Firmware input")

    @pytest.mark.regression
    def test_new_sim_vendor(self, page, report_case):
        logger.info("Starting validation of New SIM Vendor input")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_sim_vendor()

        logger.debug("Completed New SIM Vendor input validation")
        report_case(
            expected="New SIM Vendor field should accept valid input",
            actual="New SIM Vendor input validation completed",
            message="Validate New SIM Vendor input",
        )

        logger.info("Successfully validated New SIM Vendor input")

    @pytest.mark.regression
    def test_new_boot_exp_date(self, page, report_case):
        logger.info("Starting validation of Boot Expiry Date input")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_boot_exp_date()

        logger.debug("Completed Boot Expiry Date input validation")
        report_case(
            expected="Boot Expiry Date field should accept valid input",
            actual="Boot Expiry Date input validation completed",
            message="Validate Boot Expiry Date input",
        )

        logger.info("Successfully validated Boot Expiry Date input")

    @pytest.mark.regression
    def test_submit_button(self, page, report_case):
        logger.info("Starting validation of disabled Production Submit button")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)

        submit_button_locator = page.get_by_text("Submit check_circle")
        is_enabled = submit_button_locator.is_enabled()
        logger.debug("Production Submit button enabled: %s", is_enabled)

        report_case(
            expected="Submit button should be disabled",
            actual=f"Submit button enabled: {is_enabled}",
            message="Validate disabled Production Submit button",
        )

        assert not is_enabled, "Submit button should be disabled"
        logger.info("Successfully validated disabled Production Submit button")

    @pytest.mark.regression
    def test_new_device_flow(self, page, report_case):
        logger.info("Starting validation of new device flow")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_device_flow()

        logger.debug("Completed new device flow")
        report_case(
            expected="New device flow should complete",
            actual="New device flow completed",
            message="Validate new device flow",
        )

        logger.info("Successfully validated new device flow")

    @pytest.mark.regression
    def test_search_device(self, page, report_case):
        logger.info("Starting validation of Production device search")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._search_device()

        logger.debug("Completed Production device search")
        report_case(
            expected="Production device search should complete",
            actual="Production device search completed",
            message="Validate Production device search",
        )

        logger.info("Successfully validated Production device search")

    @pytest.mark.regression
    def test_search_device_2(self, page, report_case):
        logger.info("Starting validation of alternate Production device search")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._search_device_2()

        logger.debug("Completed alternate Production device search")
        report_case(
            expected="Alternate Production device search should complete",
            actual="Alternate Production device search completed",
            message="Validate alternate Production device search",
        )

        logger.info("Successfully validated alternate Production device search")

    @pytest.mark.regression
    def test_bulk_upload_btn_enability(self, page, report_case):
        logger.info("Starting validation of Bulk Upload button enablement")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._bulk_upload_btn_enability()

        logger.debug("Completed Bulk Upload button enablement validation")
        report_case(
            expected="Bulk Upload button enablement should be validated",
            actual="Bulk Upload button enablement validation completed",
            message="Validate Bulk Upload button enablement",
        )

        logger.info("Successfully validated Bulk Upload button enablement")

    @pytest.mark.regression
    def test_click_bulk_btn(self, page, report_case):
        logger.info("Starting validation of Bulk Upload button click")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._click_bulk_btn()

        actual_url = page.url
        logger.debug("Bulk Upload click completed | current_url=%s", actual_url)

        report_case(
            expected="Bulk Upload button click should complete",
            actual=f"Current URL after click: {actual_url}",
            message="Validate Bulk Upload button click",
        )

        logger.info("Successfully validated Bulk Upload button click")

    @pytest.mark.regression
    def test_btn_enability(self, page, report_case):
        logger.info("Starting validation of Add Production button enablement")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(ADD_PRODUCTION_URL)
        production_page._btn_enability()

        logger.debug("Completed Add Production button enablement validation")
        report_case(
            expected="Add Production button enablement should be validated",
            actual="Add Production button enablement validation completed",
            message="Validate Add Production button enablement",
        )

        logger.info("Successfully validated Add Production button enablement")

    @pytest.mark.regression
    def test_click_sample_btn(self, page, report_case):
        logger.info("Starting validation of sample file download")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(ADD_PRODUCTION_URL)

        download = production_page.click_sample_btn()
        is_downloaded = production_page.is_sample_file_downloaded(
            download=download, expected_filename="Sample_Production_Sheet.xlsx"
        )
        logger.debug("Sample file downloaded successfully: %s", is_downloaded)

        report_case(
            expected="Sample_Production_Sheet.xlsx should be downloaded",
            actual=f"Sample file downloaded: {is_downloaded}",
            message="Validate sample file download",
        )

        assert is_downloaded, "Sample file validation failed"
        logger.info("Successfully validated sample file download")

    @pytest.mark.regression
    def test_upload_invalid_file(self, page, report_case):
        logger.info("Starting validation of invalid production file upload")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(ADD_PRODUCTION_URL)
        upload_result = production_page.upload_invalid_file(
            str(TEST_DATA_DIR_PROD / "Invalid.xlsx")
        )
        file_present = production_page._check_file()
        is_valid = file_present and upload_result

        logger.debug(
            "Invalid file upload check | file_present=%s | upload_result=%s",
            file_present,
            upload_result,
        )

        report_case(
            expected="Invalid file upload validation should complete",
            actual=f"File present: {file_present}, upload result: {upload_result}",
            message="Validate invalid production file upload",
        )

        assert is_valid, "Add production page title is not visible"
        logger.info("Successfully validated invalid production file upload")

    @pytest.mark.regression
    def test_upload_valid_file(self, page, report_case):
        logger.info("Starting validation of valid production file upload")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(ADD_PRODUCTION_URL)
        upload_result = production_page.upload_valid_file(
            str(TEST_DATA_DIR_PROD / "Uploaded.xlsx")
        )
        file_present = production_page._check_file()
        is_valid = file_present and upload_result

        logger.debug(
            "Valid file upload check | file_present=%s | upload_result=%s",
            file_present,
            upload_result,
        )

        report_case(
            expected="Valid file upload should complete",
            actual=f"File present: {file_present}, upload result: {upload_result}",
            message="Validate valid production file upload",
        )

        assert is_valid, "Add production page title is not visible"
        logger.info("Successfully validated valid production file upload")

    @pytest.mark.regression
    def test_upload_duplicate_file(self, page, report_case):
        logger.info("Starting validation of duplicate production file upload")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(ADD_PRODUCTION_URL)
        upload_result = production_page.upload_duplicate_file(
            str(TEST_DATA_DIR_PROD / "Duplicate.xlsx")
        )
        file_present = production_page._check_file()
        is_valid = file_present and upload_result

        logger.debug(
            "Duplicate file upload check | file_present=%s | upload_result=%s",
            file_present,
            upload_result,
        )

        report_case(
            expected="Duplicate file upload validation should complete",
            actual=f"File present: {file_present}, upload result: {upload_result}",
            message="Validate duplicate production file upload",
        )

        assert is_valid, "Add production page title is not visible"
        logger.info("Successfully validated duplicate production file upload")

    @pytest.mark.regression
    def test_search_device_3(self, page, report_case):
        logger.info("Starting validation of repeated Production device search")
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._search_device_2()

        logger.debug("Completed repeated Production device search")
        report_case(
            expected="Repeated Production device search should complete",
            actual="Repeated Production device search completed",
            message="Validate repeated Production device search",
        )

        logger.info("Successfully validated repeated Production device search")
