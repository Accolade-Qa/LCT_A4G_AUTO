from config.config import SIM_DATA_DETAILS_URL

class TestSimBatchDataDetails:
    def test_go_to_simbatchpage(self, page, sim_data_details_page):
        sim_data_details_page.go_to_simbatchpage(SIM_DATA_DETAILS_URL)
        assert page.url == SIM_DATA_DETAILS_URL, f"Expected URL to be '{SIM_DATA_DETAILS_URL}', got {page.url}"

    def test_simbatchpage_title(self, sim_data_details_page):
        sim_data_details_page.go_to_simbatchpage(SIM_DATA_DETAILS_URL)
        expected_title = "Sensorise SIM Data Details"
        actual_title = sim_data_details_page.get_title()
        assert actual_title == expected_title, f"Expected title to be '{expected_title}', got '{actual_title}'"

    def test_manual_upload_and_download_buttons(self, sim_data_details_page):
        assert sim_data_details_page.is_manual_upload_button_visible(), "Manual Upload button should be visible"
        assert sim_data_details_page.is_download_sample_button_visible(), "Download Sample button should be visible"
        manual_button_text = sim_data_details_page.get_manual_upload_button_text()
        download_button_text = sim_data_details_page.get_download_sample_button_text()
        assert "Manual Upload" in manual_button_text, "Manual Upload button text mismatch"
        assert "Download Sample" in download_button_text, "Download Sample button text mismatch"

    def test_upload_instruction_and_placeholder(self, sim_data_details_page):
        expected_instruction = "Upload ICCID's to get SIM Data Details"
        assert sim_data_details_page.get_upload_instruction_text() == expected_instruction, "Upload instruction text mismatch"
        # placeholder = sim_data_details_page.get_iccid_upload_placeholder()
        # assert "ICCID" in (placeholder or ""), "ICCID placeholder should mention ICCID"

    def test_submit_button_initial_state(self, sim_data_details_page):
        assert sim_data_details_page.is_submit_button_disabled(), "Submit button should be disabled before upload"

    def test_manual_button_click_opens_manual_upload_page(self, sim_data_details_page):
        sim_data_details_page.click_manual_upload_button()
        assert (
            "sensorise-sim-manual-upload" in sim_data_details_page.page.url
        ), f"Expected manual upload URL fragment in '{sim_data_details_page.page.url}'"

    def test_manual_upload_blank_input_error(self, sim_data_details_page):
        expected_error_message = "This field is required and can't be only spaces."
        sim_data_details_page.click_manual_upload_button()
        actual_error_message = sim_data_details_page.validate_blank_input_error_message()
        assert (
            actual_error_message == expected_error_message
        ), f"Expected error message to be '{expected_error_message}', got '{actual_error_message}'"
