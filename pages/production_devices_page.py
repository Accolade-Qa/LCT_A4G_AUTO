from config.config import PRODUCTION_PAGE_URL
from playwright.sync_api import expect
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class ProductionDevices(BasePage):

    def __init__(self, page):
        self.page = page

    def go_to_prod(self, url):
        self.page.goto(url)

    def _nav_list_visibility(self):
        nav_bar_locator = self.page.locator(".nav-list")
        nav_bar_locator.wait_for(state="visible")
        self.highlight(nav_bar_locator)
        self.page.wait_for_timeout(5000)
        return nav_bar_locator.is_enabled()
        

    def _is_PageTitle_Visible(self):
        self.page.goto(PRODUCTION_PAGE_URL)
        page_title_locator = self.page.locator(":text-is('Production Device')")
        page_title_locator.wait_for(state="visible")
        self.highlight(page_title_locator)
        self.page.wait_for_timeout(5000)
        return page_title_locator.is_visible()

    def _manual_upload_btn_visibility(self):
        manual_btn_locator = self.page.get_by_text(
            "Manual Upload open_in_new", exact=True
        )
        manual_btn_locator.wait_for(state="visible")
        self.highlight(manual_btn_locator)
        self.page.wait_for_timeout(5000)
        return manual_btn_locator.is_visible()

    def _manual_upload_click(self):
        manual_btn_locator = self.page.get_by_text(
            "Manual Upload open_in_new", exact=True
        )
        manual_btn_locator.wait_for(state="visible")
        self.highlight(manual_btn_locator)
        self.page.wait_for_timeout(5000)
        manual_btn_locator.click()

    def _create_prod_PageTitle(self):
        create_title_locator = self.page.get_by_text(
            "Create Production Device", exact=True
        )
        create_title_locator.wait_for(state="visible")
        self.highlight(create_title_locator)
        self.page.wait_for_timeout(5000)
        return create_title_locator.is_visible()

    def _uid_visibility(self):
        uid_locator = self.page.get_by_label("UID", exact=True)
        uid_locator.wait_for(state="visible")
        self.highlight(uid_locator)
        self.page.wait_for_timeout(5000)
        return uid_locator.is_visible()

    def _new_uid(self):
        uid_locator = self.page.get_by_label("UID", exact=True)
        uid_locator.wait_for(state="visible")
        self.highlight(uid_locator)
        uid_locator.fill("NewUID")
        uid_locator.click()
        self.page.wait_for_timeout(5000)

    def _new_imei(self):
        imei_locator = self.page.get_by_placeholder("IMEI", exact=True)
        imei_locator.wait_for(state="visible")
        self.highlight(imei_locator)
        imei_locator.fill("NewIMEI")
        self.page.wait_for_timeout(5000)

    def _new_iccid(self):
        iccid_locator = self.page.get_by_placeholder("ICCID", exact=True)
        iccid_locator.wait_for(state="visible")
        self.highlight(iccid_locator)
        iccid_locator.fill("NewICCID")
        self.page.wait_for_timeout(5000)

    def _new_model_name(self, value):
        dropdown = self.page.get_by_role("combobox")
        dropdown.wait_for(state="visible")
        self.highlight(dropdown)
        logger.info(f"Selecting role type: {value}")

        # Click mat-select dropdown
        self.page.get_by_role("combobox").click()

        # Wait for dropdown options panel
        self.page.locator("mat-option").first.wait_for()

        # Click the option
        self.page.get_by_text(value, exact=True).click()
        self.page.wait_for_timeout(5000)

    def _new_mobile_no(self):
        mobile_locator = self.page.get_by_placeholder("Mobile Number", exact=True)
        mobile_locator.wait_for(state="visible")
        self.highlight(mobile_locator)
        mobile_locator.fill("918273645512345")
        self.page.wait_for_timeout(5000)

    def _new_service_provider(self):
        ser_pro_locator = self.page.get_by_label("Service Provider", exact=True)
        ser_pro_locator.wait_for(state="visible")
        self.highlight(ser_pro_locator)
        ser_pro_locator.fill("Airtel")
        self.page.wait_for_timeout(5000)

    def _new_alt_mob_no(self):
        alt_mob_locator = self.page.get_by_label("Alt Mobile No", exact=True)
        alt_mob_locator.wait_for(state="visible")
        self.highlight(alt_mob_locator)
        alt_mob_locator.fill("9182736455")
        self.page.wait_for_timeout(5000)

    def _new_alt_ser_pro(self):
        alt_ser_pro_locator = self.page.get_by_label("Alt Service Provider", exact=True)
        alt_ser_pro_locator.wait_for(state="visible")
        self.highlight(alt_ser_pro_locator)
        alt_ser_pro_locator.fill("BSNL")
        self.page.wait_for_timeout(5000)

    def _new_firmware(self):
        firmware_locator = self.page.get_by_label("Firmware", exact=True)
        firmware_locator.wait_for(state="visible")
        self.highlight(firmware_locator)
        firmware_locator.fill("1.0.0")
        self.page.wait_for_timeout(5000)

    def _new_sim_vendor(self):
        sim_vendor_locator = self.page.get_by_label("SIM Vendor", exact=True)

        sim_vendor_locator.evaluate(
            "element => element.scrollIntoView({block: 'center'})"
        )
        self.page.wait_for_timeout(10000)
        sim_vendor_locator.wait_for(state="visible")
        self.highlight(sim_vendor_locator)
        sim_vendor_locator.fill("Sensorise")
        self.page.wait_for_timeout(5000)

    def _new_boot_exp_date(self):

        boot_exp_locator = self.page.get_by_role("button", name="Open calendar")

        boot_exp_locator.click()

        next_month = self.page.get_by_role("button", name="Next month")

        next_month.wait_for(state="visible")
        next_month.click()

        date = self.page.get_by_role("gridcell", name="15")

        date.wait_for(state="visible")
        date.click()
        self.page.wait_for_timeout(5000)
       
    def _submit_button(self):
        submit_button_locator = self.page.get_by_role("button")
        submit_button_locator.wait_for(state="visible")
        self.highlight(submit_button_locator)

        if submit_button_locator.is_enabled():
            submit_button_locator.click()
        else:
            raise AssertionError("Submit button not enabled")
       
    # def _create_device_flow(self):
           
       
       
       
       
       
       

    def _bulk_upload_btn_visibility(self):
        bulk_btn_locator = self.page.get_by_text("Bulk Upload open_in_new", exact=True)
        bulk_btn_locator.wait_for(state="visible")
        self.highlight(bulk_btn_locator)
        return bulk_btn_locator.is_visible()
