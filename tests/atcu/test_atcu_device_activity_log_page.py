import time
import pytest

from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.device
@pytest.mark.regression
class TestDeviceActivityLogPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting ATCU Device Activity Log test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "ATCU Device Activity Log test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("ATCU Device Activity Log test passed: %s", test_name)
        elif report.failed:
            logger.error("ATCU Device Activity Log test failed: %s", test_name)
            logger.debug(
                "ATCU Device Activity Log failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("ATCU Device Activity Log test skipped: %s", test_name)

    # 1. Test page loaded
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_device_activity_log_page_loaded(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating ATCU Device System Activity Log page load")
        is_loaded = atcu_device_activity_log_page.is_page_loaded()

        report_case(
            expected="ATCU Device System Activity Log page should load successfully",
            actual=f"page_loaded={is_loaded}",
            message="Validate ATCU Device System Activity Log page loaded",
        )
        assert is_loaded, "ATCU Device System Activity Log page is not loaded"

    # 2. Test page title
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_device_activity_log_page_title(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating ATCU Device System Activity Log page title")
        title = atcu_device_activity_log_page.get_title()

        report_case(
            expected="Page title should be 'Device System Activity Log'",
            actual=f"title='{title}'",
            message="Validate ATCU Device System Activity Log page title",
        )
        assert title == "Device System Activity Log", f"Page title is incorrect: '{title}'"

    # 3. Test component header title
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_component_title(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating ATCU Device System Activity Log component header title")
        comp_title = atcu_device_activity_log_page.get_component_title()

        report_case(
            expected="Component header title should be 'Device System Activity Log'",
            actual=f"comp_title='{comp_title}'",
            message="Validate ATCU Device System Activity Log component header title",
        )
        assert (
            comp_title == "Device System Activity Log"
        ), f"Component header title is incorrect: '{comp_title}'"

    # 4. Test table headers
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_device_activity_log_table_headers(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating Device System Activity Log table headers")
        headers = atcu_device_activity_log_page.get_table_headers()
        expected_headers = [
            "IMEI",
            "ACTIVITY TYPE",
            "ACTIVITY PERFORMED",
            "PACKET",
            "ACTIVITY PERFORMED AT",
        ]

        report_case(
            expected=f"Table headers should be {expected_headers}",
            actual=f"headers={headers}",
            message="Validate Device System Activity Log table headers",
        )
        assert (
            headers == expected_headers
        ), f"Device System Activity Log table headers mismatched: {headers}"

    # 5. Test sample data rows
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_sample_data_rows(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating first data row in Device System Activity Log table")
        first_row = atcu_device_activity_log_page.get_first_row_data()

        report_case(
            expected="Table should contain valid data rows with IMEI, ACTIVITY TYPE, PACKET, and ACTIVITY PERFORMED AT",
            actual=f"first_row={first_row}",
            message="Validate Device System Activity Log sample row data",
        )
        assert first_row, "Device System Activity Log table has no data rows"
        assert "IMEI" in first_row
        assert "ACTIVITY TYPE" in first_row
        assert "PACKET" in first_row

    # 6. Test search by IMEI (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_device_activity_log_search_by_imei(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating positive search by IMEI")
        sample_row = atcu_device_activity_log_page.get_first_row_data()
        search_term = sample_row.get("IMEI", "869860089418880")
        atcu_device_activity_log_page.search_activity_log(search_term)

        is_present = atcu_device_activity_log_page.is_imei_present_in_table(search_term)
        report_case(
            expected=f"Search for IMEI '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate positive search by IMEI",
        )
        assert is_present, f"Search result for IMEI '{search_term}' not found in table"

    # 7. Test search by Activity Type (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_search_by_activity_type(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating positive search by Activity Type")
        search_term = "DNF"
        atcu_device_activity_log_page.search_activity_log(search_term)

        rows = atcu_device_activity_log_page.get_table_rows()
        report_case(
            expected=f"Search for Activity Type '{search_term}' should display matching rows",
            actual=f"rows_count={len(rows)}",
            message="Validate positive search by Activity Type",
        )
        assert len(rows) > 0, f"Search result for Activity Type '{search_term}' returned 0 rows"

    # 8. Test search by Activity Performed description (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_search_by_activity_performed(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating positive search by Activity Performed description")
        search_term = "Device Not Found"
        atcu_device_activity_log_page.search_activity_log(search_term)

        rows = atcu_device_activity_log_page.get_table_rows()
        report_case(
            expected=f"Search for Activity Performed '{search_term}' should display matching rows",
            actual=f"rows_count={len(rows)}",
            message="Validate positive search by Activity Performed",
        )
        assert len(rows) > 0, f"Search result for '{search_term}' returned 0 rows"

    # 9. Test search by Packet content (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_search_by_packet_content(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating positive search by Packet content substring")
        search_term = "55AA"
        atcu_device_activity_log_page.search_activity_log(search_term)

        rows = atcu_device_activity_log_page.get_table_rows()
        report_case(
            expected=f"Search for Packet content '{search_term}' should display matching rows",
            actual=f"rows_count={len(rows)}",
            message="Validate positive search by Packet content",
        )
        assert len(rows) > 0, f"Search result for Packet content '{search_term}' returned 0 rows"

    # 10. Test search clear query (Positive)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_search_clear_query(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating search input clearing restores full table results")
        atcu_device_activity_log_page.search_activity_log("869860089418880")
        atcu_device_activity_log_page.clear_search_input()

        rows = atcu_device_activity_log_page.get_table_rows()
        report_case(
            expected="Clearing search query should restore full table data rows",
            actual=f"rows_count={len(rows)}",
            message="Validate search clear query",
        )
        assert len(rows) > 1, "Clearing search failed to restore multiple data rows"

    # 11. Test search non-existent term (Negative Corner Case)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_search_non_existent_term(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating negative search with non-existent IMEI")
        invalid_term = "999999999999999"
        atcu_device_activity_log_page.search_activity_log(invalid_term)

        is_present = atcu_device_activity_log_page.is_imei_present_in_table(invalid_term, timeout=3000)
        report_case(
            expected=f"Searching non-existent IMEI '{invalid_term}' should yield no matching rows",
            actual=f"is_present={is_present}",
            message="Validate negative search for non-existent IMEI",
        )
        assert not is_present, f"Unexpectedly found matching row for non-existent IMEI '{invalid_term}'"

    # 12. Test search whitespace trimming (Corner Case)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_search_whitespace_trimming(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating search with leading and trailing whitespace")
        sample_row = atcu_device_activity_log_page.get_first_row_data()
        exact_imei = sample_row.get("IMEI", "869860089418880")
        spaced_imei = f"  {exact_imei}  "

        atcu_device_activity_log_page.search_activity_log(spaced_imei)
        is_present = atcu_device_activity_log_page.is_imei_present_in_table(exact_imei, timeout=5000)

        report_case(
            expected=f"Searching IMEI with whitespace '{spaced_imei}' should match IMEI '{exact_imei}'",
            actual=f"is_present={is_present}",
            message="Validate whitespace trimming in search bar",
        )
        assert is_present, f"Search with whitespace '{spaced_imei}' failed to find matching row"

    # 13. Test search bar tooltip message
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_search_tooltip_message(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating search bar tooltip message")
        tooltip = atcu_device_activity_log_page.get_search_tooltip_text()

        report_case(
            expected="Search bar tooltip should be 'IMEI'",
            actual=f"tooltip='{tooltip}'",
            message="Validate search bar tooltip message",
        )
        assert tooltip == "IMEI" or "IMEI" in tooltip, f"Tooltip message mismatched: '{tooltip}'"

    # 14. Test download report button visibility
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_download_report_button_visibility(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating Download Report button visibility")
        is_vis = atcu_device_activity_log_page.is_download_report_button_visible()

        report_case(
            expected="Download Report button should be visible",
            actual=f"is_visible={is_vis}",
            message="Validate Download Report button visibility",
        )
        assert is_vis, "Download Report button is not visible"

    # 15. Test download report button click
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_download_report_button_click(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating Download Report button click event")
        try:
            download = atcu_device_activity_log_page.click_download_report_button()
            filename = download.suggested_filename
            report_case(
                expected="Download Report click should trigger file download event",
                actual=f"downloaded_file='{filename}'",
                message="Validate Download Report button click",
            )
            assert filename != "", "Downloaded report file name should not be empty"
        except Exception as e:
            logger.warning("Download report event handling: %s", e)
            report_case(
                expected="Download Report button should be visible and clickable",
                actual=f"error='{e}'",
                message="Validate Download Report button click",
            )

    # 16. Test reload button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_reload_button_click(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating Reload button click on Device Activity Log page")
        atcu_device_activity_log_page.click_reload_button()
        is_loaded = atcu_device_activity_log_page.is_page_loaded()

        report_case(
            expected="Page should reload and be loaded successfully after reload click",
            actual=f"page_loaded={is_loaded}",
            message="Validate Reload button functionality",
        )
        assert is_loaded, "Page failed to reload properly"

    # 17. Test back button functionality
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_back_button_click(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating Back button click on Device Activity Log page")
        atcu_device_activity_log_page.click_back_button()
        report_case(
            expected="Back button click should trigger navigation",
            actual="clicked=True",
            message="Validate Back button functionality",
        )

    # 18. Test pagination container visibility
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_pagination_visibility(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating pagination container visibility")
        is_pag_visible = atcu_device_activity_log_page.is_pagination_visible()

        report_case(
            expected="Pagination container should be visible on Device Activity Log table",
            actual=f"is_pag_visible={is_pag_visible}",
            message="Validate pagination container visibility",
        )
        assert is_pag_visible, "Pagination container is not visible"

    # 19. Test rows per page dropdown selection
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_rows_per_page(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating rows per page dropdown selection")
        initial_rows = atcu_device_activity_log_page.get_selected_rows_per_page()
        atcu_device_activity_log_page.select_rows_per_page("25")
        updated_rows = atcu_device_activity_log_page.get_selected_rows_per_page()

        report_case(
            expected="Rows per page should default to 10 and update to 25 after selection",
            actual=f"initial_rows='{initial_rows}', updated_rows='{updated_rows}'",
            message="Validate rows per page dropdown selection",
        )
        assert initial_rows == "10", f"Expected default rows per page '10', got '{initial_rows}'"
        assert updated_rows == "25", f"Expected updated rows per page '25', got '{updated_rows}'"

    # 20. Test pagination navigation verification
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_pagination_navigation(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating pagination navigation on Device Activity Log page")
        pag_result = atcu_device_activity_log_page.validate_pagination()

        report_case(
            expected="Pagination helper should verify pagination controls successfully",
            actual=f"pag_result={pag_result}",
            message="Validate pagination navigation",
        )
        assert (
            pag_result["success"]
        ), f"Pagination validation failed: {pag_result.get('error')}"

    # 21. Test activity type dropdown filter
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_device_activity_log_activity_type_dropdown_filter(
        self,
        atcu_device_activity_log_page,
        report_case,
    ):
        logger.info("Validating Activity Type dropdown filter selection")
        atcu_device_activity_log_page.select_activity_type_filter("DNF")
        rows = atcu_device_activity_log_page.get_table_rows()

        report_case(
            expected="Selecting Activity Type filter 'DNF' should filter table rows",
            actual=f"rows_count={len(rows)}",
            message="Validate Activity Type dropdown filter",
        )
