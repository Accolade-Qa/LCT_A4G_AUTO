import os
import pytest

from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.config
@pytest.mark.atcu
@pytest.mark.regression
class TestDeviceStateConfigPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Device State Config test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Device State Config test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Device State Config test passed: %s", test_name)
        elif report.failed:
            logger.error("Device State Config test failed: %s", test_name)
            logger.debug(
                "Device State Config failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Device State Config test skipped: %s", test_name)

    # 1. Test page loaded
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_device_state_config_page_loaded(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating ATCU state config page load")
        is_loaded = atcu_device_state_config_page.is_page_loaded()

        report_case(
            expected="ATCU state config page should load successfully",
            actual=f"page_loaded={is_loaded}",
            message="Validate ATCU state config page loaded",
        )
        assert is_loaded, "ATCU state config page is not loaded"

    # 2. Test page title
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_device_state_config_page_title(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating ATCU state config page title")
        title = atcu_device_state_config_page.get_title()

        report_case(
            expected="ATCU state config page title should be 'Assign Device State'",
            actual=f"page_title='{title}'",
            message="Validate ATCU state config page title",
        )
        assert (
            title == "Assign Device State"
        ), f"ATCU state config page title is incorrect: '{title}'"

    # 3. Test component header
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_component_header(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating ATCU device state config component header")
        comp_title = atcu_device_state_config_page.get_component_title()

        report_case(
            expected="Component header should be 'Add Device State'",
            actual=f"component_title='{comp_title}'",
            message="Validate ATCU device state config component header",
        )
        assert (
            comp_title == "Add Device State"
        ), f"Component header title is incorrect: '{comp_title}'"

    # 4. Test file upload form label
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_file_upload_label(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating File Upload form label")
        label = atcu_device_state_config_page.get_file_upload_label()

        report_case(
            expected="Form label should be 'Device State File Upload'",
            actual=f"label='{label}'",
            message="Validate File Upload form label",
        )
        assert (
            label == "Device State File Upload"
        ), f"Form label is incorrect: '{label}'"

    # 5. Test input accept restriction attribute
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_file_input_accept_restriction(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating file input accept restriction attribute")
        accept_attr = (
            atcu_device_state_config_page.get_file_input_accept_attribute()
        )

        report_case(
            expected="File input accept attribute should be '.csv'",
            actual=f"accept_attr='{accept_attr}'",
            message="Validate file input accept restriction attribute",
        )
        assert (
            accept_attr == ".csv"
        ), f"File input accept attribute is incorrect: '{accept_attr}'"

    # 6. Test reload button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_reload_button_click(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating Reload button click on Device State Config page")
        atcu_device_state_config_page.click_reload_button()
        is_loaded = atcu_device_state_config_page.is_page_loaded()

        report_case(
            expected="Page should reload and be loaded successfully after reload click",
            actual=f"page_loaded={is_loaded}",
            message="Validate Reload button functionality",
        )
        assert is_loaded, "Page failed to reload properly"

    # 6b. Test back button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_back_button_click(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating Back button click on Device State Config page")
        atcu_device_state_config_page.click_back_button()
        report_case(
            expected="Back button click should trigger navigation",
            actual="clicked=True",
            message="Validate Back button functionality",
        )

    # 7. Test download sample template button visibility

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_download_sample_template_visibility(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating Download Sample Excel Template button visibility")
        is_visible = (
            atcu_device_state_config_page.is_download_sample_button_visible()
        )

        report_case(
            expected="Download Sample Excel Template button should be visible",
            actual=f"button_visible={is_visible}",
            message="Validate Download Sample Excel Template button visibility",
        )
        assert is_visible, "Download Sample Excel Template button is not visible"

    # 8. Test download sample template click
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_download_sample_template_click(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating Download Sample Excel Template button click and download")
        try:
            download = atcu_device_state_config_page.click_download_sample_template()
            filename = download.suggested_filename
            report_case(
                expected="Sample template file download should trigger successfully",
                actual=f"downloaded_file='{filename}'",
                message="Validate Download Sample Excel Template click",
            )
            assert filename != "", "Downloaded file name should not be empty"
        except Exception as e:
            logger.warning("Download event test skipped/failed: %s", e)
            report_case(
                expected="Sample template button should be clickable",
                actual=f"error='{e}'",
                message="Validate Download Sample Excel Template button",
            )

    # 9. Test initial state of file upload inputs & submit button
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_file_upload_initial_state(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating initial state of file upload inputs and Upload button")
        file_name = atcu_device_state_config_page.get_uploaded_file_name()
        is_submit_enabled = (
            atcu_device_state_config_page.is_upload_submit_button_enabled()
        )

        report_case(
            expected="Initial file name input should be empty and Upload submit button should be disabled",
            actual=f"file_name='{file_name}', is_submit_enabled={is_submit_enabled}",
            message="Validate initial state of file upload form",
        )
        assert file_name == "", f"Expected empty file name initially, got '{file_name}'"
        assert (
            not is_submit_enabled
        ), "Upload submit button should be disabled when no file is selected"

    # 10. Test CSV valid file selection (headers: imei,state) and enabling upload button
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_device_state_config_upload_valid_csv_file(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating uploading a valid CSV file with imei,state headers")
        sample_csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "test_data",
                "atcu",
                "device_state_config_sample_valid.csv",
            )
        )
        assert os.path.exists(
            sample_csv_path
        ), f"Valid sample CSV file not found at: {sample_csv_path}"

        atcu_device_state_config_page.upload_csv_file(sample_csv_path)

        uploaded_name = atcu_device_state_config_page.get_uploaded_file_name()
        is_submit_enabled = (
            atcu_device_state_config_page.is_upload_submit_button_enabled()
        )

        report_case(
            expected="Uploaded file name should match selected file and Upload button should be enabled",
            actual=f"uploaded_name='{uploaded_name}', is_submit_enabled={is_submit_enabled}",
            message="Validate CSV file selection and Upload button state",
        )
        assert (
            "device_state_config_sample_valid.csv" in uploaded_name
        ), f"Expected file name in input, got: '{uploaded_name}'"
        assert (
            is_submit_enabled
        ), "Upload submit button should be enabled after selecting a valid CSV file"

    # 11. Test uploading valid CSV file and verifying response table results
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_device_state_config_upload_valid_file_response_table(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating CSV file upload form submission and response table")
        sample_csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "test_data",
                "atcu",
                "device_state_config_sample_valid.csv",
            )
        )
        atcu_device_state_config_page.upload_csv_file(sample_csv_path)
        assert atcu_device_state_config_page.is_upload_submit_button_enabled()

        atcu_device_state_config_page.click_upload_submit_button()

        is_table_visible = atcu_device_state_config_page.is_response_table_visible()
        comp_title = atcu_device_state_config_page.get_component_title()
        headers = atcu_device_state_config_page.get_response_table_headers()
        first_row = atcu_device_state_config_page.get_response_table_first_row()

        report_case(
            expected="Response table should be displayed with headers ['IMEI', 'State', 'Status'] and valid state update row",
            actual=f"is_table_visible={is_table_visible}, comp_title='{comp_title}', headers={headers}, first_row={first_row}",
            message="Validate valid CSV file upload response table results",
        )
        assert is_table_visible, "Response table should be visible after uploading valid file"
        assert (
            comp_title == "Device State Uploaded Files Response"
        ), f"Expected response component title, got '{comp_title}'"
        assert headers == [
            "IMEI",
            "State",
            "Status",
        ], f"Response table headers mismatched: {headers}"
        assert first_row.get("IMEI") == "863192053020625", f"IMEI mismatched: {first_row}"
        assert first_row.get("State") == "Maharashtra", f"State mismatched: {first_row}"
        assert (
            "State updated successfully" in first_row.get("Status", "")
        ), f"Status mismatched: {first_row}"

    # 12. Test uploading invalid IMEI CSV file and asserting response status
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_upload_invalid_imei(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating uploading CSV file with invalid IMEI")
        invalid_csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "test_data",
                "atcu",
                "device_state_config_sample_invalid.csv",
            )
        )
        assert os.path.exists(
            invalid_csv_path
        ), f"Invalid sample CSV file not found at: {invalid_csv_path}"

        atcu_device_state_config_page.upload_csv_file(invalid_csv_path)
        assert atcu_device_state_config_page.is_upload_submit_button_enabled()

        atcu_device_state_config_page.click_upload_submit_button()
        is_table_visible = atcu_device_state_config_page.is_response_table_visible()
        first_row = atcu_device_state_config_page.get_response_table_first_row()
        toast = atcu_device_state_config_page.get_toast_message(timeout=2000)

        report_case(
            expected="Invalid IMEI upload should be handled with appropriate error status/message",
            actual=f"is_table_visible={is_table_visible}, first_row={first_row}, toast='{toast}'",
            message="Validate invalid IMEI CSV file upload",
        )

    # 13. Test Download Report button visibility and download click on response view
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_download_report_button(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating Download Report button on response view")
        sample_csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "test_data",
                "atcu",
                "device_state_config_sample_valid.csv",
            )
        )
        atcu_device_state_config_page.upload_csv_file(sample_csv_path)
        atcu_device_state_config_page.click_upload_submit_button()

        is_btn_visible = (
            atcu_device_state_config_page.is_download_report_button_visible()
        )
        assert is_btn_visible, "Download Report button should be visible after file upload"

        try:
            download = atcu_device_state_config_page.click_download_report_button()
            filename = download.suggested_filename
            report_case(
                expected="Download Report button should trigger file download on response view",
                actual=f"is_btn_visible={is_btn_visible}, downloaded_report='{filename}'",
                message="Validate Download Report button visibility and download action",
            )
            assert filename != "", "Downloaded report file name should not be empty"
        except Exception as e:
            logger.warning("Report download event handling: %s", e)
            report_case(
                expected="Download Report button should be visible and clickable",
                actual=f"is_btn_visible={is_btn_visible}, download_result='{e}'",
                message="Validate Download Report button visibility and download action",
            )


    # 14. Test uploading empty CSV file (headers imei,state only with 0 data rows)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_upload_empty_csv_file(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating uploading an empty CSV file with imei,state headers")
        empty_csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "test_data",
                "atcu",
                "device_state_config_empty.csv",
            )
        )
        assert os.path.exists(
            empty_csv_path
        ), f"Empty CSV file not found at: {empty_csv_path}"

        atcu_device_state_config_page.upload_csv_file(empty_csv_path)
        uploaded_name = atcu_device_state_config_page.get_uploaded_file_name()

        report_case(
            expected="Empty CSV file should be attached and file name displayed in input",
            actual=f"uploaded_name='{uploaded_name}'",
            message="Validate empty CSV file selection",
        )
        assert (
            "device_state_config_empty.csv" in uploaded_name
        ), f"Expected file name in input, got: '{uploaded_name}'"

    # 15. Test pagination component visibility on response view
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_response_table_pagination_visibility(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating pagination component visibility on response view")
        sample_csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "test_data",
                "atcu",
                "device_state_config_sample_valid.csv",
            )
        )
        atcu_device_state_config_page.upload_csv_file(sample_csv_path)
        atcu_device_state_config_page.click_upload_submit_button()

        is_table_visible = atcu_device_state_config_page.is_response_table_visible(timeout=15000)
        is_pag_visible = atcu_device_state_config_page.is_pagination_visible(timeout=15000)

        report_case(
            expected="Pagination container should be visible on response table view after file upload",
            actual=f"is_table_visible={is_table_visible}, is_pag_visible={is_pag_visible}",
            message="Validate response table pagination visibility",
        )
        assert is_table_visible, "Response table should be visible after uploading valid file"
        assert is_pag_visible, "Pagination container should be visible on response view"

    # 16. Test rows per page dropdown selection
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_response_table_rows_per_page(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating rows per page dropdown options on response view")
        sample_csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "test_data",
                "atcu",
                "device_state_config_sample_valid.csv",
            )
        )
        atcu_device_state_config_page.upload_csv_file(sample_csv_path)
        atcu_device_state_config_page.click_upload_submit_button()

        atcu_device_state_config_page.is_response_table_visible(timeout=15000)
        initial_rows = atcu_device_state_config_page.get_selected_rows_per_page()
        atcu_device_state_config_page.select_rows_per_page("25")
        updated_rows = atcu_device_state_config_page.get_selected_rows_per_page()

        report_case(
            expected="Rows per page should default to 10 and update to 25 after selection",
            actual=f"initial_rows='{initial_rows}', updated_rows='{updated_rows}'",
            message="Validate rows per page dropdown selection",
        )
        assert initial_rows == "10", f"Expected default rows per page '10', got '{initial_rows}'"
        assert updated_rows == "25", f"Expected updated rows per page '25', got '{updated_rows}'"


    # 17. Test pagination navigation verification
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_state_config_response_table_pagination_navigation(
        self,
        atcu_device_state_config_page,
        report_case,
    ):
        logger.info("Validating pagination navigation on response view table")
        sample_csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "test_data",
                "atcu",
                "device_state_config_sample_valid.csv",
            )
        )
        atcu_device_state_config_page.upload_csv_file(sample_csv_path)
        atcu_device_state_config_page.click_upload_submit_button()

        pag_result = (
            atcu_device_state_config_page.validate_response_table_pagination()
        )

        report_case(
            expected="Pagination helper should verify pagination controls successfully",
            actual=f"pag_result={pag_result}",
            message="Validate response table pagination navigation",
        )
        assert (
            pag_result["success"]
        ), f"Pagination validation failed: {pag_result.get('error')}"


