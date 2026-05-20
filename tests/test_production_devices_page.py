from config.config import (
    BASE_URL,
    USERNAME,
    PASSWORD,
    PRODUCTION_PAGE_URL,
    CREATE_PRODUCTION_URL,
    ADD_PRODUCTION_URL,
)

from playwright.sync_api import expect
from pages.production_devices_page import ProductionDevices

from pathlib import Path
from pages.login_page import LoginPage

TEST_DATA_DIR_PROD = Path(__file__).resolve().parents[1] / "test_data"


class TestProductionDevices:

    def _login_and_dashboard(self, page):
        login_page = LoginPage(page)
        login_page.load(BASE_URL)
        login_page.login(USERNAME, PASSWORD)

        return ProductionDevices(page)

    def test_go_to_prod(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        assert page.url == PRODUCTION_PAGE_URL

    def test_nav_list_visibility(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)

        assert production_page._nav_list_visibility(), "Navbar list is not visible"

    def test_is_PageTitle_Visible(self, page):
        production_page = self._login_and_dashboard(page)
        # production_page._is_PageTitle_Visible()

        assert production_page._is_PageTitle_Visible(), "Page Title is not visible"

    def test_manual_upload_btn_visibility(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)

        assert (
            production_page._manual_upload_btn_visibility()
        ), "Manual Upload button is not visible"

    def test_manual_upload_click(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._manual_upload_click()

    def test_create_prod_PageTitle(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)

        assert (
            production_page._create_prod_PageTitle()
        ), "Create production page title is not visible"

    def test_new_uid(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_uid()

    def test_new_imei(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_imei()

    def test_new_iccid(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_iccid()

    def test_new_model_name(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_model_name(value="Model Name")

    def test_new_mobile_no(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_mobile_no()

    def test__new_service_provider(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_service_provider()

    def test_new_alt_mob_no(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_alt_mob_no()

    def test_new_alt_ser_pro(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_alt_ser_pro()

    def test_new_firmware(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_firmware()

    def test_new_sim_vendor(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_sim_vendor()

    def test_new_boot_exp_date(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_boot_exp_date()

    def test_submit_button(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        # production_page._submit_button()
        submit_button_locator = page.get_by_text("Submit check_circle")
        assert not submit_button_locator.is_enabled()

    def test_new_device_flow(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(CREATE_PRODUCTION_URL)
        production_page._new_device_flow()

    def test_search_device(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._search_device()

    def test_search_device_2(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._search_device_2()

    def test_bulk_upload_btn_enability(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._bulk_upload_btn_enability()

    def test_click_bulk_btn(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._click_bulk_btn()

    def test_btn_enability(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(ADD_PRODUCTION_URL)
        production_page._btn_enability()

    def test_click_sample_btn(self, page):
        production_page = self._login_and_dashboard(page)

        production_page.go_to_prod(ADD_PRODUCTION_URL)

        download = production_page.click_sample_btn()

        assert production_page.is_sample_file_downloaded(
            download=download,
            expected_filename="Sample_Production_Sheet.xlsx"
        ), "Sample file validation failed"
        
    def test_upload_invalid_file(self, page): 
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(ADD_PRODUCTION_URL)
        upload_result = production_page.upload_invalid_file(
            str(TEST_DATA_DIR_PROD / "Invalid.xlsx")
        )
         
        assert production_page._check_file() and upload_result, "Add production page title is not visible"
        
        
    def test_upload_valid_file(self, page): 
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(ADD_PRODUCTION_URL)
        upload_result = production_page.upload_valid_file(
            str(TEST_DATA_DIR_PROD / "Uploaded.xlsx")
        )
        
        assert (
            production_page._check_file() and upload_result # true false str ???
        ), "Add production page title is not visible" 
        
    def test_upload_duplicate_file(self, page): 
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(ADD_PRODUCTION_URL)
        upload_result = production_page.upload_duplicate_file(
            str(TEST_DATA_DIR_PROD / "Duplicate.xlsx")
        )
        
        assert (
            production_page._check_file() and upload_result # true false str ???
        ), "Add production page title is not visible"    
        
    def test_search_device_3(self, page):
        production_page = self._login_and_dashboard(page)
        production_page.go_to_prod(PRODUCTION_PAGE_URL)
        production_page._search_device_2()     