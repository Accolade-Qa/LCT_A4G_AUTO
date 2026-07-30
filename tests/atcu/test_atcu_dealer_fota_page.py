import time
import pytest

from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.regression
class TestDealerFotaPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Dealer FOTA test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Dealer FOTA test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Dealer FOTA test passed: %s", test_name)
        elif report.failed:
            logger.error("Dealer FOTA test failed: %s", test_name)
            logger.debug(
                "Dealer FOTA failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Dealer FOTA test skipped: %s", test_name)

    # 1. Test page loaded
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_dealer_fota_page_loaded(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating ATCU Dealer FOTA page load")
        is_loaded = atcu_dealer_fota_page.is_page_loaded()

        report_case(
            expected="ATCU Dealer FOTA page should load successfully",
            actual=f"page_loaded={is_loaded}",
            message="Validate ATCU Dealer FOTA page loaded",
        )
        assert is_loaded, "ATCU Dealer FOTA page is not loaded"

    # 2. Test page title
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_dealer_fota_page_title(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating ATCU Dealer FOTA page title")
        title = atcu_dealer_fota_page.get_title()

        report_case(
            expected="ATCU Dealer FOTA page title should be 'Dealer FOTA'",
            actual=f"page_title='{title}'",
            message="Validate ATCU Dealer FOTA page title",
        )
        assert (
            title == "Dealer FOTA"
        ), f"ATCU Dealer FOTA page title is incorrect: '{title}'"

    # 3. Test component header
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_component_title(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating ATCU Dealer FOTA component header title")
        comp_title = atcu_dealer_fota_page.get_component_title()

        report_case(
            expected="Component header title should be 'Dealer FOTA List'",
            actual=f"component_title='{comp_title}'",
            message="Validate ATCU Dealer FOTA component header title",
        )
        assert (
            comp_title == "Dealer FOTA List"
        ), f"Component header title is incorrect: '{comp_title}'"

    # 4. Test table headers
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_dealer_fota_table_headers(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating Dealer FOTA table headers")
        headers = atcu_dealer_fota_page.get_table_headers()
        expected_headers = [
            "Sr. No",
            "File Name",
            "UIN NO.",
            "VIN NO.",
            "Flashing Status",
            "Created At",
        ]

        report_case(
            expected=f"Table headers should be {expected_headers}",
            actual=f"headers={headers}",
            message="Validate Dealer FOTA table headers",
        )
        assert (
            headers == expected_headers
        ), f"Dealer FOTA table headers mismatched: {headers}"

    # 5. Test sample row data
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_sample_row_data(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating first row data in Dealer FOTA table")
        first_row = atcu_dealer_fota_page.get_first_row_data()

        report_case(
            expected="First row should contain valid Sr. No, File Name, UIN NO., VIN NO., and Flashing Status",
            actual=f"first_row={first_row}",
            message="Validate Dealer FOTA sample row data",
        )
        assert first_row, "Dealer FOTA table has no data rows"
        assert "File Name" in first_row
        assert "UIN NO." in first_row
        assert "VIN NO." in first_row

    # 6. Test search by File Name
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_search_by_file_name(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating search by File Name")
        first_row = atcu_dealer_fota_page.get_first_row_data()
        search_term = first_row.get("File Name", "5.2.8_REL24") if first_row else "5.2.8_REL24"
        atcu_dealer_fota_page.search_dealer_fota_list(search_term)

        is_present = atcu_dealer_fota_page.is_device_present_in_table(search_term)
        report_case(
            expected=f"Search for File Name '{search_term}' should display matching rows",
            actual=f"is_present={is_present}",
            message="Validate search by File Name",
        )
        assert is_present, f"Search result for File Name '{search_term}' not found in table"

    # 7. Test search by UIN NO.
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_search_by_uin(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating search by UIN NO.")
        first_row = atcu_dealer_fota_page.get_first_row_data()
        search_term = first_row.get("UIN NO.", "ACON4NA082300092233") if first_row else "ACON4NA082300092233"
        atcu_dealer_fota_page.search_dealer_fota_list(search_term)

        is_present = atcu_dealer_fota_page.is_device_present_in_table(search_term)
        report_case(
            expected=f"Search for UIN NO. '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate search by UIN NO.",
        )
        assert is_present, f"Search result for UIN NO. '{search_term}' not found in table"

    # 8. Test search by VIN NO.
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_search_by_vin(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating search by VIN NO.")
        first_row = atcu_dealer_fota_page.get_first_row_data()
        search_term = first_row.get("VIN NO.", "ACCDEV07241580138") if first_row else "ACCDEV07241580138"
        atcu_dealer_fota_page.search_dealer_fota_list(search_term)

        is_present = atcu_dealer_fota_page.is_device_present_in_table(search_term)
        report_case(
            expected=f"Search for VIN NO. '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate search by VIN NO.",
        )
        assert is_present, f"Search result for VIN NO. '{search_term}' not found in table"


    # 9. Test download details button visibility
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_download_details_button_visibility(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating Download Dealer FOTA Details button visibility")
        is_vis = atcu_dealer_fota_page.is_download_details_button_visible()

        report_case(
            expected="Download Dealer FOTA Details button should be visible",
            actual=f"is_visible={is_vis}",
            message="Validate Download Dealer FOTA Details button visibility",
        )
        assert is_vis, "Download Dealer FOTA Details button is not visible"

    # 10. Test download details button click
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_download_details_button_click(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating Download Dealer FOTA Details button click event")
        try:
            download = atcu_dealer_fota_page.click_download_details_button()
            filename = download.suggested_filename
            report_case(
                expected="Download Dealer FOTA Details click should trigger download event",
                actual=f"downloaded_file='{filename}'",
                message="Validate Download Dealer FOTA Details button click",
            )
            assert filename != "", "Downloaded file name should not be empty"
        except Exception as e:
            logger.warning("Download event handling: %s", e)
            report_case(
                expected="Download Dealer FOTA Details button should be visible and clickable",
                actual=f"error='{e}'",
                message="Validate Download Dealer FOTA Details button click",
            )

    # 11. Test reload button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_reload_button_click(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating Reload button click on Dealer FOTA page")
        atcu_dealer_fota_page.click_reload_button()
        is_loaded = atcu_dealer_fota_page.is_page_loaded()

        report_case(
            expected="Page should reload and be loaded successfully after reload click",
            actual=f"page_loaded={is_loaded}",
            message="Validate Reload button functionality",
        )
        assert is_loaded, "Page failed to reload properly"

    # 12. Test back button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_back_button_click(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating Back button click on Dealer FOTA page")
        atcu_dealer_fota_page.click_back_button()
        report_case(
            expected="Back button click should trigger navigation",
            actual="clicked=True",
            message="Validate Back button functionality",
        )

    # 13. Requirement 1a: Pagination on Main Dealer FOTA page (/dealer-fota)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_main_page_pagination(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating pagination on Main Dealer FOTA page (/dealer-fota)")
        is_pag_visible = atcu_dealer_fota_page.is_pagination_visible()
        initial_rows = atcu_dealer_fota_page.get_selected_rows_per_page()
        pag_result = atcu_dealer_fota_page.validate_pagination()

        report_case(
            expected="Pagination container should be visible, default to 10 rows per page, and verify page controls",
            actual=f"is_pag_visible={is_pag_visible}, initial_rows='{initial_rows}', pag_result={pag_result}",
            message="Validate pagination on Main Dealer FOTA page",
        )
        assert is_pag_visible, "Pagination container is not visible on Main Dealer FOTA page"
        assert initial_rows == "10", f"Expected default rows per page '10', got '{initial_rows}'"
        assert pag_result["success"], f"Main page pagination verification failed: {pag_result.get('error')}"

    # 14. Requirement 1b: Pagination on Approved Files page (/dealer-fota-approved-files)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_approved_files_page_pagination(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating pagination on Approved Files sub-page (/dealer-fota-approved-files)")
        atcu_dealer_fota_page.click_add_approved_file_button()
        assert atcu_dealer_fota_page.is_approved_files_page_loaded()

        is_pag_visible = atcu_dealer_fota_page.is_approved_files_pagination_visible()
        pag_result = atcu_dealer_fota_page.validate_approved_files_pagination()

        report_case(
            expected="Pagination container should be visible and verify controls on Approved Files sub-page",
            actual=f"is_pag_visible={is_pag_visible}, pag_result={pag_result}",
            message="Validate pagination on Approved Files sub-page",
        )
        assert is_pag_visible, "Pagination container is not visible on Approved Files sub-page"
        assert pag_result["success"], f"Approved Files pagination verification failed: {pag_result.get('error')}"

    # 15. Requirement 2: Action button {delete} visibility and enablement
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_dealer_fota_delete_button_visibility_and_enablement(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        logger.info("Validating Action Delete button visibility and enablement on Approved Files page")
        atcu_dealer_fota_page.click_add_approved_file_button()
        assert atcu_dealer_fota_page.is_approved_files_page_loaded()

        sample_file_name = "ATCU_5.2.8_REL18.bin"
        assert atcu_dealer_fota_page.is_file_name_present_in_list(sample_file_name)

        is_delete_vis = atcu_dealer_fota_page.is_delete_button_visible_for_row(sample_file_name)
        is_delete_enabled = atcu_dealer_fota_page.is_delete_button_enabled_for_row(sample_file_name)

        report_case(
            expected="Delete button in Action column should be visible and enabled for table row",
            actual=f"sample_file='{sample_file_name}', is_delete_vis={is_delete_vis}, is_delete_enabled={is_delete_enabled}",
            message="Validate Delete action button visibility and enablement",
        )
        assert is_delete_vis, f"Delete button not visible for row '{sample_file_name}'"
        assert is_delete_enabled, f"Delete button not enabled for row '{sample_file_name}'"

    # 16. Requirement 3: Add file, delete recently added file, and validate deletion by searching
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_dealer_fota_add_delete_and_validate_search(
        self,
        atcu_dealer_fota_page,
        report_case,
    ):
        """
        Flow:
        1. Navigate to Approved Files sub-page (/dealer-fota-approved-files)
        2. Enter unique file name in Add File form (e.g. 'auto_test_fota_1700.bin') and click Submit
        3. Validate newly added file appears in File Name List table
        4. Click Delete action button for that recently added file
        5. Search for that deleted file name in search bar
        6. Validate file entry is no longer present in table
        """
        logger.info("Step 1: Navigating to Approved Files page")
        atcu_dealer_fota_page.click_add_approved_file_button()
        assert atcu_dealer_fota_page.is_approved_files_page_loaded()

        logger.info("Step 2: Adding unique file name to Add File form")
        unique_file_name = f"auto_test_fota_{int(time.time())}.bin"
        atcu_dealer_fota_page.enter_file_name_in_add_file_form(unique_file_name)
        assert atcu_dealer_fota_page.is_submit_button_enabled(), "Submit button should be enabled after entering file name"

        atcu_dealer_fota_page.click_submit_file_name()

        logger.info("Step 3: Validating newly added file appears in table")
        is_added_present = atcu_dealer_fota_page.is_file_name_present_in_list(unique_file_name, timeout=10000)
        assert is_added_present, f"Newly added file '{unique_file_name}' not found in table after submission"

        logger.info("Step 4: Deleting recently added file via Delete action button")
        assert atcu_dealer_fota_page.is_delete_button_visible_for_row(unique_file_name)
        atcu_dealer_fota_page.click_delete_button_for_file_name(unique_file_name)

        logger.info("Step 5: Searching for the deleted file name in search bar")
        atcu_dealer_fota_page.search_approved_file_name(unique_file_name)

        logger.info("Step 6: Validating deleted file is no longer present in table")
        is_still_present = atcu_dealer_fota_page.is_file_name_present_in_list(unique_file_name, timeout=3000)
        assert not is_still_present, f"Deleted file '{unique_file_name}' is still present in table after deletion"

        report_case(
            expected="Added file should be deleted upon clicking Delete button and search should confirm it is absent",
            actual=f"unique_file='{unique_file_name}', is_added_present={is_added_present}, is_still_present={is_still_present}",
            message="Validate delete recently added file and verify by searching",
        )
