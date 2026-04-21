from config.config import MODEL_URL
from playwright.sync_api import expect
from .base_page import BasePage


class DeviceModel(BasePage):

    def __init__(self, page):
        self.page = page

    def go_to_model(self, url):
        self.page.goto(url)

    def go_to_create_model(self, url):
        self.page.goto(url)

    def go_to_update_model(self, url):
        self.page.goto(url)

    def _nav_list_visibility(self):
        nav_bar_locator = self.page.locator(".nav-list")
        nav_bar_locator.wait_for(state="visible")
        self.highlight(nav_bar_locator)
        return nav_bar_locator.is_enabled()

    def _is_PageTitle_Visible(self):
        page_title_locator = self.page.locator("span:has-text('Device Models')")
        page_title_locator.wait_for(state="visible")
        self.highlight(page_title_locator)
        return page_title_locator.is_visible()

    def _create_model_visibility(self):
        model_button_locator = self.page.get_by_text(
            "Add Device Model open_in_new", exact=True
        )
        model_button_locator.wait_for(state="visible")
        self.highlight(model_button_locator)
        return model_button_locator.is_visible()
        return model_button_locator.is_enabled()
        model_button_locator.click()

    def _create_model_click(self):
        model_button_locator = self.page.get_by_text(
            "Add Device Model open_in_new", exact=True
        )
        model_button_locator.wait_for(state="visible")
        self.highlight(model_button_locator)
        model_button_locator.click()

    def _create_model_page_title(self):
        page_title_locator = self.page.get_by_text("Create Device Model")
        page_title_locator.wait_for(state="visible")
        self.highlight(page_title_locator)
        assert page_title_locator.is_visible(), "Page title is not visible"

    def _submit_button(self):
        submit_button_locator = self.page.get_by_role("button")
        submit_button_locator.wait_for(state="visible")
        self.highlight(submit_button_locator)
        return submit_button_locator.is_enabled()

    def _model_code(self, code):
        model_code_locator = self.page.get_by_label("Model Code")
        model_code_locator.wait_for(state="visible")
        self.highlight(model_code_locator)
        expect(model_code_locator).to_be_visible()
        expect(model_code_locator).to_be_enabled()
        model_code_locator.fill(code)

    def _model_name(self, name):
        model_name_locator = self.page.get_by_label("Model Name")
        model_name_locator.wait_for(state="visible")
        self.highlight(model_name_locator)
        assert model_name_locator.is_visible()
        assert model_name_locator.is_enabled()
        model_name_locator.fill(name)

    def _model_seriel_sequence(self, sequence):
        model_sequence_locator = self.page.get_by_label("Model Serial Sequence")
        model_sequence_locator.wait_for(state="visible")
        self.highlight(model_sequence_locator)

        if model_sequence_locator.is_visible() and model_sequence_locator.is_enabled():
            model_sequence_locator.fill(sequence)
        else:
            raise AssertionError("Model Serial Sequence not found")

    def _hardware_version(self, version):
        hardware_version_locator = self.page.get_by_label("Hardware Version")
        hardware_version_locator.wait_for(state="visible")
        self.highlight(hardware_version_locator)
        if (
            hardware_version_locator.is_visible()
            and hardware_version_locator.is_enabled()
        ):
            hardware_version_locator.fill(version)
        else:
            raise AssertionError("Hardware Version not found")

    def _submit_button_click(self):
        submit_button_locator = self.page.get_by_role("button")
        submit_button_locator.wait_for(state="visible")
        self.highlight(submit_button_locator)

        if submit_button_locator.is_enabled():
            submit_button_locator.click()
        else:
            raise AssertionError("Submit button not enabled")

    def _search_model(self, model):
        search_field_locator = self.page.locator(
            "//input[@placeholder='Search and Press Enter']"
        )
        search_button_locator = self.page.locator(
            "button[class='search-btn'] mat-icon[role='img']"
        )
        search_field_locator.wait_for(state="visible")
        self.highlight(search_button_locator)
        if search_field_locator.is_enabled():
            search_field_locator.fill(model)
            search_button_locator.click()
        else:
            raise AssertionError("Search field not enabled")
        search_button_locator.click()

    def view_icon(self):
        view_icon_locator = self.page.locator(
            "//tbody/tr[1]/td[5]/div[1]/button[1]/mat-icon[1]"
        )
        view_icon_locator.wait_for(state="visible")
        self.highlight(view_icon_locator)
        if view_icon_locator.is_enabled():
            view_icon_locator.click()
        else:
            raise AssertionError("View Icon not enabled")

    def update_model_code(self, Updatecode):
        up_model_code_locator = self.page.get_by_placeholder("Model Code", exact=True)
        up_model_code_locator.wait_for(state="visible")
        self.highlight(up_model_code_locator)
        if up_model_code_locator.is_visible():
            up_model_code_locator.fill(Updatecode)
        else:
            raise AssertionError("Update Model Code not visible")

    def update_model_name(self, Updatename):
        up_model_name_locator = self.page.get_by_placeholder("Model Name", exact=True)
        up_model_name_locator.wait_for(state="visible")
        self.highlight(up_model_name_locator)
        if up_model_name_locator.is_visible():
            up_model_name_locator.fill(Updatename)
        else:
            raise AssertionError("Update Model Name not visible")

    def update_model_seriel_sequence(self, Updatesequence):
        up_model_sequence_locator = self.page.get_by_placeholder(
            "Model Serial Sequence", exact=True
        )
        up_model_sequence_locator.wait_for(state="visible")
        self.highlight(up_model_sequence_locator)
        if (
            up_model_sequence_locator.is_visible()
            and up_model_sequence_locator.is_enabled()
        ):
            up_model_sequence_locator.fill(Updatesequence)
        else:
            raise AssertionError("Update Model Sequence not visible")

    def update_hardware_version(self, Updateversion):
        up_hardware_version_locator = self.page.get_by_placeholder(
            "Hardware Version", exact=True
        )
        up_hardware_version_locator.wait_for(state="visible")
        self.highlight(up_hardware_version_locator)
        if (
            up_hardware_version_locator.is_visible()
            and up_hardware_version_locator.is_enabled()
        ):
            up_hardware_version_locator.fill(Updateversion)
        else:
            raise AssertionError("Update Hardware Version not visible")

    def _update_button_click(self):
        Update_button_locator = self.page.get_by_text("Update edit", exact=True)
        Update_button_locator.wait_for(state="visible")
        self.highlight(Update_button_locator)
        if Update_button_locator.is_enabled():
            Update_button_locator.click()
        else:
            raise AssertionError("Update button not enabled")

    def _search_model(self, model):
        search_field_locator = self.page.get_by_placeholder(
            "Search and Press Enter", exact=True
        )
        search_button_locator = self.page.locator(
            "button[class='search-btn'] mat-icon[role='img']"
        )
        search_field_locator.wait_for(state="visible")
        self.highlight(search_button_locator)
        if search_field_locator.is_visible() and search_button_locator.is_enabled():
            search_field_locator.fill(model)
            search_button_locator.click()

    def _get_updated_model_text(self, text):
        text_locator = self.page.get_by_text(text, exact=True)
        text_locator.wait_for(state="visible")
        self.highlight(text_locator)
        return text_locator.inner_text()

    def delete_updated_model(self):
        delete_icon_locator = self.page.locator("mat-icon", has_text="delete").first

        delete_icon_locator.wait_for(state="visible")
        self.highlight(delete_icon_locator)
        if delete_icon_locator.is_enabled():
            delete_icon_locator.click()
        else:
            raise AssertionError("Delete Icon not enabled")
