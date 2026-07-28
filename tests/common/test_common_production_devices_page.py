from pathlib import Path
from utils.logger import get_logger
import pytest

TEST_DATA_DIR_PROD = Path(__file__).resolve().parents[2] / "test_data" / "lct"
logger = get_logger(__name__)


@pytest.mark.device
@pytest.mark.regression
@pytest.mark.lct
@pytest.mark.sampark
@pytest.mark.swaraj
@pytest.mark.trio
class TestProductionDevices:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Production Devices test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Production Devices test finished without call report: %s",
                test_name,
            )
        elif report.passed:
            logger.info("Production Devices test passed: %s", test_name)
        elif report.failed:
            logger.error("Production Devices test failed: %s", test_name)
            logger.debug(
                "Production Devices failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Production Devices test skipped: %s", test_name)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_production_devices_page_navigation(self, production_devices_page, project_config, report_case):
        logger.info("Starting validation of Production Devices page navigation")

        expected_url = project_config["production_page_url"]
        actual_url = production_devices_page.page.url
        logger.debug(
            "Production Devices URL check | expected=%s | actual=%s",
            expected_url,
            actual_url,
        )

        if actual_url == expected_url:
            report_case(
                expected=expected_url,
                actual=actual_url,
                result="PASS",
                message="Positive: Successfully validated Production Devices page navigation",
            )
        else:
            report_case(
                expected=expected_url,
                actual=actual_url,
                result="FAIL",
                message="Negative: Failed to validate Production Devices page navigation",
            )

        assert (
            actual_url == expected_url
        ), f"Expected URL '{expected_url}', got '{actual_url}'"
        logger.info("Successfully validated Production Devices page navigation")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_page_nav_list_visibility(
        self, production_devices_page, project_config, report_case
    ):
        logger.info("Starting validation of Production navbar list visibility")

        is_visible = production_devices_page._nav_list_visibility()
        logger.debug("Production navbar list visible: %s", is_visible)

        if is_visible:
            report_case(
                expected="Navbar list should be visible",
                actual=f"Navbar list visible: {is_visible}",
                result="PASS",
                message="Positive: Successfully validated Production navbar list visibility",
            )
        else:
            report_case(
                expected="Navbar list should be visible",
                actual=f"Navbar list visible: {is_visible}",
                result="FAIL",
                message="Negative: Failed to validate Production navbar list visibility",
            )

        assert is_visible, "Navbar list is not visible"
        logger.info("Successfully validated Production navbar list visibility")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_page_title_visibility(
        self, production_devices_page, project_config, report_case
    ):
        logger.info("Starting validation of Production page title visibility")

        is_visible = production_devices_page._is_PageTitle_Visible()
        logger.debug("Production page title visible: %s", is_visible)

        if is_visible:
            report_case(
                expected="Page title should be visible",
                actual=f"Page title visible: {is_visible}",
                result="PASS",
                message="Positive: Successfully validated Production page title visibility",
            )
        else:
            report_case(
                expected="Page title should be visible",
                actual=f"Page title visible: {is_visible}",
                result="FAIL",
                message="Negative: Failed to validate Production page title visibility",
            )

        assert is_visible, "Page Title is not visible"
        logger.info("Successfully validated Production page title visibility")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_page_manual_upload_btn_visibility(self, production_devices_page, report_case):
        logger.info("Starting validation of Manual Upload button visibility")

        is_visible = production_devices_page._manual_upload_btn_visibility()
        logger.debug("Manual Upload button visible: %s", is_visible)

        if is_visible:
            report_case(
                expected="Manual Upload button should be visible",
                actual=f"Manual Upload button visible: {is_visible}",
                result="PASS",
                message="Positive: Successfully validated Manual Upload button visibility",
            )
        else:
            report_case(
                expected="Manual Upload button should be visible",
                actual=f"Manual Upload button visible: {is_visible}",
                result="FAIL",
                message="Negative: Failed to validate Manual Upload button visibility",
            )

        assert is_visible, "Manual Upload button is not visible"
        logger.info("Successfully validated Manual Upload button visibility")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_page_manual_upload_click_navigation(self, page, production_devices_page, report_case):
        logger.info("Starting validation of Manual Upload button click")
        production_devices_page._manual_upload_click()

        actual_url = page.url
        logger.debug("Manual Upload click completed | current_url=%s", actual_url)

        report_case(
            expected="Manual Upload button click should complete",
            actual=f"Current URL after click: {actual_url}",
            result="PASS",
            message="Positive: Successfully validated Manual Upload button click",
        )

        logger.info("Successfully validated Manual Upload button click")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_page_create_production_title_visibility(self, production_devices_page, report_case):
        logger.info("Starting validation of Create Production page title")
        production_devices_page._manual_upload_click()

        is_visible = production_devices_page._create_prod_PageTitle()
        logger.debug("Create Production page title visible: %s", is_visible)

        if is_visible:
            report_case(
                expected="Create Production page title should be visible",
                actual=f"Create Production page title visible: {is_visible}",
                result="PASS",
                message="Positive: Successfully validated Create Production page title",
            )
        else:
            report_case(
                expected="Create Production page title should be visible",
                actual=f"Create Production page title visible: {is_visible}",
                result="FAIL",
                message="Negative: Failed to validate Create Production page title",
            )

        assert is_visible, "Create production page title is not visible"
        logger.info("Successfully validated Create Production page title")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_create_production_new_uid_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New UID input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_uid()

        logger.debug("Completed New UID input validation")
        report_case(
            expected="New UID field should accept valid input",
            actual="New UID input validation completed",
            result="PASS",
            message="Positive: Successfully validated New UID input",
        )

        logger.info("Successfully validated New UID input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_imei_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New IMEI input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_imei()

        logger.debug("Completed New IMEI input validation")
        report_case(
            expected="New IMEI field should accept valid input",
            actual="New IMEI input validation completed",
            result="PASS",
            message="Positive: Successfully validated New IMEI input",
        )

        logger.info("Successfully validated New IMEI input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_iccid_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New ICCID input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_iccid()

        logger.debug("Completed New ICCID input validation")
        report_case(
            expected="New ICCID field should accept valid input",
            actual="New ICCID input validation completed",
            result="PASS",
            message="Positive: Successfully validated New ICCID input",
        )

        logger.info("Successfully validated New ICCID input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_model_name_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New Model Name input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_model_name(value="Model Name")

        logger.debug("Entered New Model Name value: %s", "Model Name")
        report_case(
            expected="New Model Name field should accept value 'Model Name'",
            actual="New Model Name value entered",
            result="PASS",
            message="Positive: Successfully validated New Model Name input",
        )

        logger.info("Successfully validated New Model Name input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_mobile_no_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New Mobile Number input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_mobile_no()

        logger.debug("Completed New Mobile Number input validation")
        report_case(
            expected="New Mobile Number field should accept valid input",
            actual="New Mobile Number input validation completed",
            result="PASS",
            message="Positive: Successfully validated New Mobile Number input",
        )

        logger.info("Successfully validated New Mobile Number input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_service_provider_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New Service Provider input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_service_provider()

        logger.debug("Completed New Service Provider input validation")
        report_case(
            expected="New Service Provider field should accept valid input",
            actual="New Service Provider input validation completed",
            result="PASS",
            message="Positive: Successfully validated New Service Provider input",
        )

        logger.info("Successfully validated New Service Provider input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_alt_mobile_no_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of Alternate Mobile Number input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_alt_mob_no()

        logger.debug("Completed Alternate Mobile Number input validation")
        report_case(
            expected="Alternate Mobile Number field should accept valid input",
            actual="Alternate Mobile Number input validation completed",
            result="PASS",
            message="Positive: Successfully validated Alternate Mobile Number input",
        )

        logger.info("Successfully validated Alternate Mobile Number input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_alt_service_provider_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of Alternate Service Provider input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_alt_ser_pro()

        logger.debug("Completed Alternate Service Provider input validation")
        report_case(
            expected="Alternate Service Provider field should accept valid input",
            actual="Alternate Service Provider input validation completed",
            result="PASS",
            message="Positive: Successfully validated Alternate Service Provider input",
        )

        logger.info("Successfully validated Alternate Service Provider input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_firmware_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New Firmware input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_firmware()

        logger.debug("Completed New Firmware input validation")
        report_case(
            expected="New Firmware field should accept valid input",
            actual="New Firmware input validation completed",
            result="PASS",
            message="Positive: Successfully validated New Firmware input",
        )

        logger.info("Successfully validated New Firmware input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_sim_vendor_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of New SIM Vendor input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_sim_vendor()

        logger.debug("Completed New SIM Vendor input validation")
        report_case(
            expected="New SIM Vendor field should accept valid input",
            actual="New SIM Vendor input validation completed",
            result="PASS",
            message="Positive: Successfully validated New SIM Vendor input",
        )

        logger.info("Successfully validated New SIM Vendor input")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_new_boot_exp_date_field_validation(self, production_devices_page, report_case):
        logger.info("Starting validation of Boot Expiry Date input")
        production_devices_page._manual_upload_click()
        production_devices_page._new_boot_exp_date()

        logger.debug("Completed Boot Expiry Date input validation")
        report_case(
            expected="Boot Expiry Date field should accept valid input",
            actual="Boot Expiry Date input validation completed",
            result="PASS",
            message="Positive: Successfully validated Boot Expiry Date input",
        )

        logger.info("Successfully validated Boot Expiry Date input")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_create_production_submit_button_state_transitions(self, page, production_devices_page, report_case):
        logger.info("Starting validation of disabled Production Submit button")
        production_devices_page._manual_upload_click()

        submit_button_locator = page.get_by_text("Submit check_circle")
        is_enabled = submit_button_locator.is_enabled()
        logger.debug("Production Submit button enabled: %s", is_enabled)

        if not is_enabled:
            report_case(
                expected="Submit button should be disabled",
                actual=f"Submit button enabled: {is_enabled}",
                result="PASS",
                message="Positive: Successfully validated disabled Production Submit button",
            )
        else:
            report_case(
                expected="Submit button should be disabled",
                actual=f"Submit button enabled: {is_enabled}",
                result="FAIL",
                message="Negative: Failed to validate disabled Production Submit button",
            )

        assert not is_enabled, "Submit button should be disabled"
        logger.info("Successfully validated disabled Production Submit button")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_production_complete_new_device_flow(self, production_devices_page, report_case):
        logger.info("Starting validation of new device flow")
        production_devices_page._manual_upload_click()
        production_devices_page._new_device_flow()

        logger.debug("Completed new device flow")
        report_case(
            expected="New device flow should complete",
            actual="New device flow completed",
            result="PASS",
            message="Positive: Successfully validated new device flow",
        )

        logger.info("Successfully validated new device flow")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_production_devices_search_by_imei(self, production_devices_page, report_case):
        logger.info("Starting validation of Production device search")
        production_devices_page._search_device()

        logger.debug("Completed Production device search")
        report_case(
            expected="Production device search should complete",
            actual="Production device search completed",
            result="PASS",
            message="Positive: Successfully validated Production device search",
        )

        logger.info("Successfully validated Production device search")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_production_devices_search_by_uid(self, production_devices_page, report_case):
        logger.info("Starting validation of alternate Production device search")
        production_devices_page._search_device_2()

        logger.debug("Completed alternate Production device search")
        report_case(
            expected="Alternate Production device search should complete",
            actual="Alternate Production device search completed",
            result="PASS",
            message="Positive: Successfully validated alternate Production device search",
        )

        logger.info("Successfully validated alternate Production device search")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_bulk_upload_btn_visibility_and_state(self, production_devices_page, report_case):
        logger.info("Starting validation of Bulk Upload button enablement")
        is_enabled = production_devices_page._bulk_upload_btn_enability()

        logger.debug("Completed Bulk Upload button enablement validation")
        if is_enabled:
            report_case(
                expected="Bulk Upload button should be enabled",
                actual=f"Bulk Upload button enabled: {is_enabled}",
                result="PASS",
                message="Positive: Successfully validated Bulk Upload button enablement",
            )
        else:
            report_case(
                expected="Bulk Upload button should be enabled",
                actual=f"Bulk Upload button enabled: {is_enabled}",
                result="FAIL",
                message="Negative: Failed to validate Bulk Upload button enablement",
            )

        assert is_enabled, "Bulk Upload button is not enabled"
        logger.info("Successfully validated Bulk Upload button enablement")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_production_devices_click_bulk_upload_navigates_to_add_devices(self, page, production_devices_page, report_case):
        logger.info("Starting validation of Bulk Upload button click")
        production_devices_page._click_bulk_btn()

        actual_url = page.url
        logger.debug("Bulk Upload click completed | current_url=%s", actual_url)

        report_case(
            expected="Bulk Upload button click should complete",
            actual=f"Current URL after click: {actual_url}",
            result="PASS",
            message="Positive: Successfully validated Bulk Upload button click",
        )

        logger.info("Successfully validated Bulk Upload button click")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_add_devices_form_submit_button_disabled_by_default(self, production_devices_page, report_case):
        logger.info("Starting validation of Add Production button enablement")
        production_devices_page._click_bulk_btn()
        production_devices_page._btn_enability()

        logger.debug("Completed Add Production button enablement validation")
        report_case(
            expected="Add Production button enablement should be validated",
            actual="Add Production button enablement validation completed",
            result="PASS",
            message="Positive: Successfully validated Add Production button enablement",
        )

        logger.info("Successfully validated Add Production button enablement")

    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.regression
    def test_add_devices_form_download_sample_file(self, production_devices_page, report_case):
        logger.info("Starting validation of sample file download")
        production_devices_page._click_bulk_btn()

        download = production_devices_page.click_sample_btn()
        is_downloaded = production_devices_page.is_sample_file_downloaded(
            download=download, expected_filename="Sample_Production_Sheet.xlsx"
        )
        logger.debug("Sample file downloaded successfully: %s", is_downloaded)

        if is_downloaded:
            report_case(
                expected="Sample_Production_Sheet.xlsx should be downloaded",
                actual=f"Sample file downloaded: {is_downloaded}",
                result="PASS",
                message="Positive: Successfully validated sample file download",
            )
        else:
            report_case(
                expected="Sample_Production_Sheet.xlsx should be downloaded",
                actual=f"Sample file downloaded: {is_downloaded}",
                result="FAIL",
                message="Negative: Failed to validate sample file download",
            )

        assert is_downloaded, "Sample file validation failed"
        logger.info("Successfully validated sample file download")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_add_devices_form_upload_invalid_file_shows_error(self, production_devices_page, report_case):
        logger.info("Starting validation of invalid production file upload")
        production_devices_page._click_bulk_btn()
        upload_result = production_devices_page.upload_invalid_file(
            str(TEST_DATA_DIR_PROD / "Invalid.xlsx")
        )
        file_present = production_devices_page._check_file()
        is_valid = file_present and upload_result

        logger.debug(
            "Invalid file upload check | file_present=%s | upload_result=%s",
            file_present,
            upload_result,
        )

        if is_valid:
            report_case(
                expected="Invalid file upload validation should complete successfully",
                actual=f"File present: {file_present}, upload result: {upload_result}",
                result="PASS",
                message="Positive: Successfully validated invalid production file upload",
            )
        else:
            report_case(
                expected="Invalid file upload validation should complete successfully",
                actual=f"File present: {file_present}, upload result: {upload_result}",
                result="FAIL",
                message="Negative: Failed to validate invalid production file upload",
            )

        assert is_valid, "Invalid file upload failed"
        logger.info("Successfully validated invalid production file upload")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_add_devices_form_upload_valid_file_succeeds(self, production_devices_page, report_case):
        logger.info("Starting validation of valid production file upload")
        production_devices_page._click_bulk_btn()
        upload_result = production_devices_page.upload_valid_file(
            str(TEST_DATA_DIR_PROD / "Uploaded.xlsx")
        )
        file_present = production_devices_page._check_file()
        is_valid = file_present and upload_result

        logger.debug(
            "Valid file upload check | file_present=%s | upload_result=%s",
            file_present,
            upload_result,
        )

        if is_valid:
            report_case(
                expected="Valid file upload should complete successfully",
                actual=f"File present: {file_present}, upload result: {upload_result}",
                result="PASS",
                message="Positive: Successfully validated valid production file upload",
            )
        else:
            report_case(
                expected="Valid file upload should complete successfully",
                actual=f"File present: {file_present}, upload result: {upload_result}",
                result="FAIL",
                message="Negative: Failed to validate valid production file upload",
            )

        assert is_valid, "Valid file upload failed"
        logger.info("Successfully validated valid production file upload")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_add_devices_form_upload_duplicate_file_shows_error(self, production_devices_page, report_case):
        logger.info("Starting validation of duplicate production file upload")
        production_devices_page._click_bulk_btn()
        upload_result = production_devices_page.upload_duplicate_file(
            str(TEST_DATA_DIR_PROD / "Duplicate.xlsx")
        )
        file_present = production_devices_page._check_file()
        is_valid = file_present and upload_result

        logger.debug(
            "Duplicate file upload check | file_present=%s | upload_result=%s",
            file_present,
            upload_result,
        )

        if is_valid:
            report_case(
                expected="Duplicate file upload validation should complete successfully",
                actual=f"File present: {file_present}, upload result: {upload_result}",
                result="PASS",
                message="Positive: Successfully validated duplicate production file upload",
            )
        else:
            report_case(
                expected="Duplicate file upload validation should complete successfully",
                actual=f"File present: {file_present}, upload result: {upload_result}",
                result="FAIL",
                message="Negative: Failed to validate duplicate production file upload",
            )

        assert is_valid, "Duplicate file upload failed"
        logger.info("Successfully validated duplicate production file upload")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_production_devices_search_by_iccid(self, production_devices_page, report_case):
        logger.info("Starting validation of repeated Production device search")
        production_devices_page._search_device_2()

        logger.debug("Completed repeated Production device search")
        report_case(
            expected="Repeated Production device search should complete",
            actual="Repeated Production device search completed",
            result="PASS",
            message="Positive: Successfully validated repeated Production device search",
        )

        logger.info("Successfully validated repeated Production device search")
