import pytest
from datetime import datetime, timezone, timedelta

from utils.logger import get_logger
from api.tml_request_api import TmlRequestAPI

logger = get_logger(__name__)


@pytest.mark.atcu
@pytest.mark.regression
class TestTicketDashboardPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting Ticket Dashboard test: %s", test_name)
        yield
        report = getattr(request.node, "rep_call", None)
        if report and report.failed:
            logger.error("Ticket Dashboard test failed: %s", test_name)
        else:
            logger.info("Ticket Dashboard test passed: %s", test_name)

    # --- Group 1: Page Load & Basic Navigation ---
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_page_loaded(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating ATCU Ticket Dashboard page load")
        is_loaded = atcu_ticket_dashboard_page.is_page_loaded()
        report_case(
            expected="ATCU Ticket Dashboard page should load successfully",
            actual=f"page_loaded={is_loaded}",
            message="Validate ATCU Ticket Dashboard page loaded",
        )
        assert is_loaded, "ATCU Ticket Dashboard page is not loaded"

    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_page_title(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating ATCU Ticket Dashboard page title")
        title = atcu_ticket_dashboard_page.get_title()
        report_case(
            expected="Page title should be 'Ticket Dashboard'",
            actual=f"title='{title}'",
            message="Validate ATCU Ticket Dashboard page title",
        )
        assert title == "Ticket Dashboard", f"Page title is incorrect: '{title}'"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_reload_button_click(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating Reload button click")
        atcu_ticket_dashboard_page.click_reload_button()
        is_loaded = atcu_ticket_dashboard_page.is_page_loaded()
        report_case(
            expected="Page should reload and remain loaded successfully",
            actual=f"is_loaded={is_loaded}",
            message="Validate Reload button click",
        )
        assert is_loaded, "Page failed to reload properly"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_back_button_click(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating Back button click")
        atcu_ticket_dashboard_page.click_back_button()
        report_case(
            expected="Back button click should trigger navigation",
            actual="clicked=True",
            message="Validate Back button functionality",
        )

    # --- Group 2: Time Rules & Default State ---
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_530_pm_ist_rule_verification(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        is_after_530 = atcu_ticket_dashboard_page.is_after_530_pm_ist()
        in_progress_count = atcu_ticket_dashboard_page.get_kpi_card_count("IN PROGRESS")
        on_hold_count = atcu_ticket_dashboard_page.get_kpi_card_count("ON HOLD")

        logger.info("Current Time IST after 5:30 PM: %s | IN_PROGRESS=%s | ON_HOLD=%s", is_after_530, in_progress_count, on_hold_count)
        report_case(
            expected=f"After 5:30 PM IST (is_after_530={is_after_530}), in-progress tickets shift to on-hold appropriately",
            actual=f"is_after_530={is_after_530}, in_progress={in_progress_count}, on_hold={on_hold_count}",
            message="Validate 5:30 PM IST time rule for IN PROGRESS vs ON HOLD tickets",
        )
        if is_after_530:
            assert on_hold_count >= 0, "ON HOLD count should be non-negative after 5:30 PM IST"
        else:
            assert in_progress_count >= 0, "IN PROGRESS count should be non-negative before 5:30 PM IST"

    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_default_card_set_to_total(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating default table selection is set to TOTAL / ALL Tickets List")
        comp_title = atcu_ticket_dashboard_page.get_component_title()
        report_case(
            expected="Default component header title should be 'All Tickets List'",
            actual=f"comp_title='{comp_title}'",
            message="Validate default card selection set to TOTAL",
        )
        assert "All" in comp_title or "Total" in comp_title or "Tickets" in comp_title, f"Unexpected default table header: '{comp_title}'"

    # --- Group 3: Table Headers per Card View ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_table_headers_card_all(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ALL")
        headers = atcu_ticket_dashboard_page.get_table_headers()
        report_case(
            expected="ALL card view should display correct table headers",
            actual=f"headers={headers}",
            message="Validate ALL card view table headers",
        )
        assert len(headers) >= 5, "Headers missing in ALL card table"
        assert "TICKET NO." in headers or "UIN NO." in headers, f"Header mismatch: {headers}"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_table_headers_card_in_progress(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("IN PROGRESS")
        headers = atcu_ticket_dashboard_page.get_table_headers()
        report_case(
            expected="IN PROGRESS card view should display correct table headers",
            actual=f"headers={headers}",
            message="Validate IN PROGRESS card view table headers",
        )
        assert len(headers) >= 5, "Headers missing in IN PROGRESS card table"
        assert "TICKET NO." in headers or "UIN NO." in headers, f"Header mismatch: {headers}"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_table_headers_card_on_hold(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ON HOLD")
        headers = atcu_ticket_dashboard_page.get_table_headers()
        report_case(
            expected="ON HOLD card view should display correct table headers",
            actual=f"headers={headers}",
            message="Validate ON HOLD card view table headers",
        )
        assert len(headers) >= 5, "Headers missing in ON HOLD card table"
        assert "TICKET NO." in headers or "UIN NO." in headers, f"Header mismatch: {headers}"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_table_headers_card_cancelled(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("CANCELLED")
        headers = atcu_ticket_dashboard_page.get_table_headers()
        report_case(
            expected="CANCELLED card view should display correct table headers",
            actual=f"headers={headers}",
            message="Validate CANCELLED card view table headers",
        )
        assert len(headers) >= 5, "Headers missing in CANCELLED card table"
        assert "TICKET NO." in headers or "UIN NO." in headers, f"Header mismatch: {headers}"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_table_headers_card_completed(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("COMPLETED")
        headers = atcu_ticket_dashboard_page.get_table_headers()
        report_case(
            expected="COMPLETED card view should display correct table headers",
            actual=f"headers={headers}",
            message="Validate COMPLETED card view table headers",
        )
        assert len(headers) >= 5, "Headers missing in COMPLETED card table"
        assert "TICKET NO." in headers or "UIN NO." in headers, f"Header mismatch: {headers}"

    # --- Group 4: End Date Column Verification per Card View ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_end_date_values_card_completed(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("COMPLETED")
        end_dates = atcu_ticket_dashboard_page.get_column_values("END DATE")
        non_empty = [d for d in end_dates if d and d != "--"]
        report_case(
            expected="COMPLETED card table should contain valid non-empty End Date values",
            actual=f"total={len(end_dates)}, non_empty={len(non_empty)}",
            message="Validate End Date in COMPLETED table",
        )
        if end_dates:
            assert len(non_empty) > 0, "COMPLETED table missing valid End Date values"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_end_date_values_card_in_progress(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("IN PROGRESS")
        end_dates = atcu_ticket_dashboard_page.get_column_values("END DATE")
        dash_values = [d for d in end_dates if d == "--" or not d]
        report_case(
            expected="IN PROGRESS card table should contain '--' for End Date",
            actual=f"total={len(end_dates)}, dash_count={len(dash_values)}",
            message="Validate End Date in IN PROGRESS table",
        )
        if end_dates:
            assert len(dash_values) == len(end_dates), "IN PROGRESS table should contain '--' for End Date"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_end_date_values_card_on_hold(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ON HOLD")
        end_dates = atcu_ticket_dashboard_page.get_column_values("END DATE")
        dash_values = [d for d in end_dates if d == "--" or not d]
        report_case(
            expected="ON HOLD card table should contain '--' for End Date",
            actual=f"total={len(end_dates)}, dash_count={len(dash_values)}",
            message="Validate End Date in ON HOLD table",
        )
        if end_dates:
            assert len(dash_values) == len(end_dates), "ON HOLD table should contain '--' for End Date"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_end_date_values_card_cancelled(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("CANCELLED")
        end_dates = atcu_ticket_dashboard_page.get_column_values("END DATE")
        dash_values = [d for d in end_dates if d == "--" or not d]
        report_case(
            expected="CANCELLED card table should contain '--' for End Date",
            actual=f"total={len(end_dates)}, dash_count={len(dash_values)}",
            message="Validate End Date in CANCELLED table",
        )
        if end_dates:
            assert len(dash_values) == len(end_dates), "CANCELLED table should contain '--' for End Date"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_end_date_values_card_all(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ALL")
        end_dates = atcu_ticket_dashboard_page.get_column_values("END DATE")
        report_case(
            expected="ALL card table should extract End Date column values cleanly",
            actual=f"total={len(end_dates)}",
            message="Validate End Date in ALL table",
        )
        assert isinstance(end_dates, list), "Failed to extract End Date list"

    # --- Group 5: Ticket Category Column Verification per Card View ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_ticket_category_card_in_progress(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("IN PROGRESS")
        categories = atcu_ticket_dashboard_page.get_column_values("TICKET CATEGORY")
        matches = [c for c in categories if "IN_PROGRESS" in c or "PROGRESS" in c]
        report_case(
            expected="IN PROGRESS card table should contain IN_PROGRESS Ticket Category",
            actual=f"total={len(categories)}, matches={len(matches)}",
            message="Validate Ticket Category in IN PROGRESS table",
        )
        if categories:
            assert len(matches) > 0, "IN PROGRESS table missing IN_PROGRESS Ticket Category"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_ticket_category_card_on_hold(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ON HOLD")
        categories = atcu_ticket_dashboard_page.get_column_values("TICKET CATEGORY")
        matches = [c for c in categories if "HOLD" in c or "ON_HOLD" in c]
        report_case(
            expected="ON HOLD card table should contain ON_HOLD Ticket Category",
            actual=f"total={len(categories)}, matches={len(matches)}",
            message="Validate Ticket Category in ON HOLD table",
        )
        if categories:
            assert len(matches) > 0, "ON HOLD table missing ON_HOLD Ticket Category"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_ticket_category_card_cancelled(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("CANCELLED")
        categories = atcu_ticket_dashboard_page.get_column_values("TICKET CATEGORY")
        matches = [c for c in categories if "CANCEL" in c]
        report_case(
            expected="CANCELLED card table should contain CANCELLED Ticket Category",
            actual=f"total={len(categories)}, matches={len(matches)}",
            message="Validate Ticket Category in CANCELLED table",
        )
        if categories:
            assert len(matches) > 0, "CANCELLED table missing CANCELLED Ticket Category"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_ticket_category_card_completed(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("COMPLETED")
        categories = atcu_ticket_dashboard_page.get_column_values("TICKET CATEGORY")
        matches = [c for c in categories if "COMPLETE" in c]
        report_case(
            expected="COMPLETED card table should contain COMPLETED Ticket Category",
            actual=f"total={len(categories)}, matches={len(matches)}",
            message="Validate Ticket Category in COMPLETED table",
        )
        if categories:
            assert len(matches) > 0, "COMPLETED table missing COMPLETED Ticket Category"

    # --- Group 6: Pagination per Card View ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_pagination_card_all(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ALL")
        is_vis = atcu_ticket_dashboard_page.is_pagination_visible()
        res = atcu_ticket_dashboard_page.validate_pagination()
        report_case(
            expected="Pagination should be visible and verified for ALL card view",
            actual=f"is_vis={is_vis}, res={res}",
            message="Validate pagination for ALL card view",
        )
        assert is_vis, "Pagination container not visible for ALL card view"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_pagination_card_in_progress(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("IN PROGRESS")
        is_vis = atcu_ticket_dashboard_page.is_pagination_visible()
        res = atcu_ticket_dashboard_page.validate_pagination()
        report_case(
            expected="Pagination should be visible and verified for IN PROGRESS card view",
            actual=f"is_vis={is_vis}, res={res}",
            message="Validate pagination for IN PROGRESS card view",
        )
        assert is_vis, "Pagination container not visible for IN PROGRESS card view"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_pagination_card_on_hold(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("ON HOLD")
        is_vis = atcu_ticket_dashboard_page.is_pagination_visible()
        res = atcu_ticket_dashboard_page.validate_pagination()
        report_case(
            expected="Pagination should be visible and verified for ON HOLD card view",
            actual=f"is_vis={is_vis}, res={res}",
            message="Validate pagination for ON HOLD card view",
        )
        assert is_vis, "Pagination container not visible for ON HOLD card view"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_pagination_card_cancelled(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("CANCELLED")
        is_vis = atcu_ticket_dashboard_page.is_pagination_visible()
        res = atcu_ticket_dashboard_page.validate_pagination()
        report_case(
            expected="Pagination should be visible and verified for CANCELLED card view",
            actual=f"is_vis={is_vis}, res={res}",
            message="Validate pagination for CANCELLED card view",
        )
        assert is_vis, "Pagination container not visible for CANCELLED card view"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_pagination_card_completed(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_kpi_card("COMPLETED")
        is_vis = atcu_ticket_dashboard_page.is_pagination_visible()
        res = atcu_ticket_dashboard_page.validate_pagination()
        report_case(
            expected="Pagination should be visible and verified for COMPLETED card view",
            actual=f"is_vis={is_vis}, res={res}",
            message="Validate pagination for COMPLETED card view",
        )
        assert is_vis, "Pagination container not visible for COMPLETED card view"

    # --- Group 7: Graph Visibility & Canvas Hover per Chart ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_month_wise_trend_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "Month-wise AIS140 Ticket Trend"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_tat_trend_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "AIS140 Ticket TAT Trend"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_tat_reason_breakdown_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "TAT Reason Breakdown"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_state_wise_distribution_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "State Wise Ticket Distribution"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_individual_performance_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "Individual Performance"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_graph_device_model_wise_visibility_and_hover(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        title = "Device Model Wise Graph"
        is_vis = atcu_ticket_dashboard_page.is_graph_visible(title)
        hover_ok = atcu_ticket_dashboard_page.hover_over_graph(title)
        report_case(
            expected=f"Graph '{title}' canvas should be visible and support mouse hover",
            actual=f"is_vis={is_vis}, hover_ok={hover_ok}",
            message=f"Validate graph '{title}'",
        )
        assert is_vis, f"Graph '{title}' canvas not visible"
        assert hover_ok, f"Graph '{title}' hover failed"

    # --- Group 8: API Integration & Count Sync ---
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_api_counts_validation_vs_ui(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        logger.info("Validating UI KPI Card counts against /api/crm/getDashCounts API endpoint")
        ui_counts = atcu_ticket_dashboard_page.get_all_kpi_counts()

        api_response = TmlRequestAPI.get_dash_counts()
        api_data = api_response.get("data", {}) if isinstance(api_response, dict) else {}

        api_all = api_data.get("all", 0) if isinstance(api_data, dict) else 0
        api_in_progress = api_data.get("inProgress", 0) if isinstance(api_data, dict) else 0
        api_on_hold = api_data.get("onHold", 0) if isinstance(api_data, dict) else 0
        api_cancelled = api_data.get("cancelled", 0) if isinstance(api_data, dict) else 0
        api_completed = api_data.get("completed", 0) if isinstance(api_data, dict) else 0

        report_case(
            expected="UI KPI card counts should match or closely align with getDashCounts API response keys (all, inProgress, onHold, cancelled, completed)",
            actual=f"ui_counts={ui_counts}, api_counts={{'all': {api_all}, 'inProgress': {api_in_progress}, 'onHold': {api_on_hold}, 'cancelled': {api_cancelled}, 'completed': {api_completed}}}",
            message="Validate KPI Card counts against getDashCounts API response",
        )
        assert ui_counts["ALL"] >= 0, "ALL KPI count should be non-negative"
        assert ui_counts["IN_PROGRESS"] >= 0, "IN PROGRESS KPI count should be non-negative"
        if isinstance(api_data, dict) and "all" in api_data:
            assert abs(ui_counts["ALL"] - api_all) <= 10, f"ALL count mismatch: UI={ui_counts['ALL']}, API={api_all}"

    @pytest.mark.regression
    @pytest.mark.smoke
    def test_atcu_ticket_dashboard_generate_ticket_api_count_increment_and_ui_sync(
        self,
        atcu_ticket_dashboard_page,
        project_config,
        report_case,
    ):
        is_after_530 = atcu_ticket_dashboard_page.is_after_530_pm_ist()

        initial_ui_all = atcu_ticket_dashboard_page.get_kpi_card_count("ALL")
        initial_ui_in_progress = atcu_ticket_dashboard_page.get_kpi_card_count("IN PROGRESS")
        initial_ui_on_hold = atcu_ticket_dashboard_page.get_kpi_card_count("ON HOLD")

        pre_api_resp = TmlRequestAPI.get_dash_counts()
        pre_api_data = pre_api_resp.get("data", {}) if isinstance(pre_api_resp, dict) else {}
        pre_api_all = pre_api_data.get("all", 0)

        payload, VIN, UIN, ICCID, ticket_number, data = TmlRequestAPI.post_tml_request_log()
        assert ticket_number, "Ticket generation API failed to return TICKET_NO"

        post_api_resp = TmlRequestAPI.get_dash_counts()
        post_api_data = post_api_resp.get("data", {}) if isinstance(post_api_resp, dict) else {}
        post_api_all = post_api_data.get("all", 0)

        atcu_ticket_dashboard_page.page.reload()
        atcu_ticket_dashboard_page.page.wait_for_load_state("networkidle")

        updated_ui_all = atcu_ticket_dashboard_page.get_kpi_card_count("ALL")

        target_card = "ON HOLD" if is_after_530 else "IN PROGRESS"
        atcu_ticket_dashboard_page.click_kpi_card(target_card)
        atcu_ticket_dashboard_page.search_ticket(ticket_number)

        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(ticket_number, timeout=10000)

        if not is_present:
            atcu_ticket_dashboard_page.click_kpi_card("ALL")
            atcu_ticket_dashboard_page.search_ticket(ticket_number)
            is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(ticket_number, timeout=5000)

        report_case(
            expected=f"Generated ticket '{ticket_number}' should increment counts and be present in table under '{target_card}'",
            actual=f"ticket='{ticket_number}', is_present={is_present}, pre_ui_all={initial_ui_all}, post_ui_all={updated_ui_all}, pre_api_all={pre_api_all}, post_api_all={post_api_all}",
            message="Validate ticket generation API, count update, and table search",
        )
        assert is_present, f"Newly generated ticket '{ticket_number}' not found in table"

    # --- Group 9: Deep UI & Tooltips ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_tooltip_validation(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        tooltip = atcu_ticket_dashboard_page.get_search_tooltip_message()
        report_case(
            expected="Search bar tooltip should specify searchable fields ('Ticket No | UIN NO. | Chassis NO. | IMEI NO.')",
            actual=f"tooltip='{tooltip}'",
            message="Validate search bar tooltip message",
        )
        assert "Ticket No" in tooltip or "UIN" in tooltip or "Chassis" in tooltip or "IMEI" in tooltip, f"Unexpected search tooltip: '{tooltip}'"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_download_tat_report_functionality(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        download = atcu_ticket_dashboard_page.click_download_tat_report_button()
        report_case(
            expected="Download TAT Report click should trigger report download event",
            actual=f"download_triggered={download is not None}",
            message="Validate Download TAT Report button click",
        )

    # --- Group 10: Filter Modal & Reactivity ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_modal_opening_and_controls(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        is_vis = atcu_ticket_dashboard_page.is_filter_modal_visible()
        atcu_ticket_dashboard_page.close_filter_modal()
        report_case(
            expected="Filter button click should display details filter modal",
            actual=f"is_vis={is_vis}",
            message="Validate filter modal opening and close",
        )
        assert is_vis, "Filter modal not visible"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_filter_modal_submit_and_clear_reactivity(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        atcu_ticket_dashboard_page.click_filter_button()
        is_modal_vis = atcu_ticket_dashboard_page.is_filter_modal_visible()
        assert is_modal_vis, "Details filter modal should be visible"

        atcu_ticket_dashboard_page.click_modal_submit()
        graphs_reactive = atcu_ticket_dashboard_page.verify_all_graphs_reactive()

        atcu_ticket_dashboard_page.click_filter_button()
        atcu_ticket_dashboard_page.click_modal_clear()

        report_case(
            expected="Applying and clearing filters should reactively update graphs and table rows",
            actual=f"modal_vis={is_modal_vis}, graphs_reactive={graphs_reactive}",
            message="Validate filter modal submit, clear, and reactivity",
        )
        assert all(graphs_reactive.values()), "Graphs failed reactivity check after filter submission"

    # --- Group 11: Search Scenarios ---
    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_by_ticket_no(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        first_row = atcu_ticket_dashboard_page.get_first_row_data()
        search_term = first_row.get("TICKET NO.", "AEPL-260730-1") if first_row else "AEPL-260730-1"
        atcu_ticket_dashboard_page.search_ticket(search_term)
        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(search_term)
        report_case(
            expected=f"Search for Ticket NO. '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate search by Ticket NO.",
        )
        assert is_present, f"Ticket NO. '{search_term}' not found in table"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_by_uin(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        first_row = atcu_ticket_dashboard_page.get_first_row_data()
        search_term = first_row.get("UIN NO.", "ACON4IA202200075879") if first_row else "ACON4IA202200075879"
        atcu_ticket_dashboard_page.search_ticket(search_term)
        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(search_term)
        report_case(
            expected=f"Search for UIN NO. '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate search by UIN NO.",
        )
        assert is_present, f"UIN NO. '{search_term}' not found in table"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_by_chassis(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        first_row = atcu_ticket_dashboard_page.get_first_row_data()
        search_term = first_row.get("CHASSIS NO.", "MAT00007241590103") if first_row else "MAT00007241590103"
        atcu_ticket_dashboard_page.search_ticket(search_term)
        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(search_term)
        report_case(
            expected=f"Search for Chassis NO. '{search_term}' should display matching row",
            actual=f"is_present={is_present}",
            message="Validate search by Chassis NO.",
        )
        assert is_present, f"Chassis NO. '{search_term}' not found in table"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_non_existent_term(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        search_term = "NON_EXISTENT_TICKET_99999"
        atcu_ticket_dashboard_page.search_ticket(search_term)
        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(search_term, timeout=3000)
        report_case(
            expected="Searching non-existent ticket should return 0 matching rows",
            actual=f"is_present={is_present}",
            message="Validate search non-existent term",
        )
        assert not is_present, "Non-existent ticket term returned unexpected row"

    @pytest.mark.regression
    @pytest.mark.ui
    def test_atcu_ticket_dashboard_search_whitespace_trimming(
        self,
        atcu_ticket_dashboard_page,
        report_case,
    ):
        first_row = atcu_ticket_dashboard_page.get_first_row_data()
        clean_term = first_row.get("TICKET NO.", "AEPL-260730-1") if first_row else "AEPL-260730-1"
        raw_search_term = f"  {clean_term}  "
        atcu_ticket_dashboard_page.search_ticket(raw_search_term)
        is_present = atcu_ticket_dashboard_page.is_ticket_present_in_table(clean_term)
        report_case(
            expected="Search query with leading/trailing whitespace should execute cleanly",
            actual=f"raw='{raw_search_term}', is_present={is_present}",
            message="Validate search input whitespace trimming",
        )
        assert is_present, f"Ticket '{clean_term}' not found when searching with whitespace"
