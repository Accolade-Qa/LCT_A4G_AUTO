from config.config import SIM_DATA_DETAILS_URL
from utils.logger import get_logger

logger = get_logger(__name__)


class TestSimBatchDataDetails:
    def test_go_to_simbatchpage(self, page, sim_data_details_page):
        logger.info("Navigating to SIM Data Details page")
        sim_data_details_page.go_to_simbatchpage(SIM_DATA_DETAILS_URL)
        assert page.url == SIM_DATA_DETAILS_URL, f"Expected URL to be '{SIM_DATA_DETAILS_URL}', got {page.url}"

    def test_simbatchpage_title(self, sim_data_details_page):
        logger.info("Asserting SIM Data Details title")
        sim_data_details_page.go_to_simbatchpage(SIM_DATA_DETAILS_URL)
        expected_title = "Sensorise SIM Data Details"
        actual_title = sim_data_details_page.get_title()
        assert actual_title == expected_title, f"Expected title to be '{expected_title}', got '{actual_title}'"

    def test_manual_upload_and_download_buttons(self, sim_data_details_page):
        logger.info("Validating manual upload and download buttons")
        assert sim_data_details_page.is_manual_upload_button_visible(), "Manual Upload button should be visible"
        assert sim_data_details_page.is_download_sample_button_visible(), "Download Sample button should be visible"
        manual_button_text = sim_data_details_page.get_manual_upload_button_text()
        download_button_text = sim_data_details_page.get_download_sample_button_text()
        assert "Manual Upload" in manual_button_text, "Manual Upload button text mismatch"
        assert "Download Sample" in download_button_text, "Download Sample button text mismatch"

    def test_upload_instruction_and_placeholder(self, sim_data_details_page):
        logger.info("Checking upload instruction and placeholder copy")
        expected_instruction = "Upload ICCID's to get SIM Data Details"
        assert sim_data_details_page.get_upload_instruction_text() == expected_instruction, "Upload instruction text mismatch"
        # placeholder = sim_data_details_page.get_iccid_upload_placeholder()
        # assert "ICCID" in (placeholder or ""), "ICCID placeholder should mention ICCID"

    def test_submit_button_initial_state(self, sim_data_details_page):
        logger.info("Verifying submit button is disabled before upload")
        assert sim_data_details_page.is_submit_button_disabled(), "Submit button should be disabled before upload"

    def test_manual_button_click_opens_manual_upload_page(self, sim_data_details_page):
        logger.info("Opening manual upload page")
        sim_data_details_page.click_manual_upload_button()
        assert (
            "sensorise-sim-manual-upload" in sim_data_details_page.page.url
        ), f"Expected manual upload URL fragment in '{sim_data_details_page.page.url}'"

    def test_manual_upload_blank_input_error(self, sim_data_details_page):
        logger.info("Validating blank input error message on manual upload form")
        expected_error_message = "This field is required and can't be only spaces."
        sim_data_details_page.click_manual_upload_button()
        actual_error_message = sim_data_details_page.validate_blank_input_error_message()
        assert (
            actual_error_message == expected_error_message
        ), f"Expected error message to be '{expected_error_message}', got '{actual_error_message}'"

    def test_manual_upload_20_characters_error(self, sim_data_details_page):
        '''this error is for the less than 20 and more thann 20 characters'''
        logger.info("Checking error message for input exceeding 20 characters")
        expected_error_message = "Value must be exactly 20 characters long."
        sim_data_details_page.click_manual_upload_button()
        actual_error_message = sim_data_details_page.validate_20_characters_error_message()
        assert (
            actual_error_message == expected_error_message
        ), f"Expected error message to be '{expected_error_message}', got '{actual_error_message}'"
        
    def test_submit_button_enabled_after_valid_input(self, sim_data_details_page):
        logger.info("Ensuring submit button is enabled after valid input")
        sim_data_details_page.click_manual_upload_button()
        sim_data_details_page.enter_valid_iccid("89916450244842405755")  # Example valid ICCID
        assert not sim_data_details_page.is_submit_button_disabled(), "Submit button should be enabled after valid input"
        
        
    def test_click_on_submit_is_opening_the_table(self, sim_data_details_page):
        logger.info("Testing that clicking submit opens the results table")
        sim_data_details_page.click_manual_upload_button()
        sim_data_details_page.enter_valid_iccid("89916450244842405755")  # Example valid ICCID
        sim_data_details_page.click_submit_button()
        assert sim_data_details_page.is_results_table_visible(), "Results table should be visible after submitting valid ICCID"
        
    def test_is_table_component_header_visible_and_correct(self, sim_data_details_page):
        logger.info("Verifying results table header is visible and correct")
        sim_data_details_page.click_manual_upload_button()
        sim_data_details_page.enter_valid_iccid("89916450244842405755")  # Example valid ICCID
        sim_data_details_page.click_submit_button()
        expected_header = "Uploaded ICCID's Sensorise SIM Details List" # Example expected headers
        actual_headers = sim_data_details_page.get_results_table_component_header()
        assert actual_headers == expected_header, f"Expected table headers to be {expected_header}, got {actual_headers}"
        
        
    def test_table_headers(self, sim_data_details_page):
        logger.info("Validating table headers")
        sim_data_details_page.click_manual_upload_button()
        sim_data_details_page.enter_valid_iccid("89916450244842405755")  # Example valid ICCID
        sim_data_details_page.click_submit_button()
        # ['ICCID', 'CARD STATE', 'CARD STATUS', 'PRIMARY TSP', 'FALLBACK TSP', 'PRIMARY STATUS', 'PRIMARY MSISDN', 'FALLBACK STATUS', 'FALLBACK MSISDN', 'ACTIVE PROFILES', 'CARD EXPIRY DATE', 'PRODUCT NAME', 'IS RSU REQUIRED', 'IS IMSI REQUIRED', 'ACTIVE SR NUMBER']
        expected_headers = ["ICCID", "CARD STATE", "CARD STATUS", "PRIMARY TSP", "FALLBACK TSP", "PRIMARY STATUS", "PRIMARY MSISDN", "FALLBACK STATUS", "FALLBACK MSISDN", "ACTIVE PROFILES", "CARD EXPIRY DATE", "PRODUCT NAME", "IS RSU REQUIRED", "IS IMSI REQUIRED", "ACTIVE SR NUMBER"]
        actual_headers = sim_data_details_page.get_table_headers()
        print(f"Actual headers: {actual_headers}")
        assert actual_headers == expected_headers, f"Expected table headers {expected_headers}, got {actual_headers}"
        
    def test_pagination(self, sim_data_details_page):
        logger.info("Executing pagination workflow")
        sim_data_details_page.click_manual_upload_button()
        sim_data_details_page.enter_valid_iccid("89916450244842405755")  # Example valid ICCID
        sim_data_details_page.click_submit_button()
        sim_data_details_page.page.wait_for_timeout(2000)  # Wait for table to load before checking pagination
        result = sim_data_details_page.check_pagination()
        assert result["success"], f"Pagination failed: {result['error']}"
        assert result["total_pages"] > 1, "Pagination did not move beyond first page"
        assert result["pages_visited"] == sorted(result["pages_visited"]), "Pages not in order"