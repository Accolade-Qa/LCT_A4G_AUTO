from config.config import (
    BASE_URL,
    MODEL_URL,
    PASSWORD,
    USERNAME,
    CREATE_NEW_MODEL,
    UPDATE_MODEL,
)
from playwright.sync_api import expect

# from pages.api import model_api
from pages.model_page import DeviceModel
from pages.login_page import LoginPage


class TestModel:

    def _login_and_dashboard(self, page):
        login_page = LoginPage(page)
        login_page.load(BASE_URL)
        login_page.login(USERNAME, PASSWORD)

        return DeviceModel(page)

    def test_go_to_model(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)

    def test_go_to_create_model(self, page):
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_create_model(CREATE_NEW_MODEL)
        assert page.url == CREATE_NEW_MODEL

    def test_go_to_update_model(self, page):
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_update_model(UPDATE_MODEL)
        assert page.url == UPDATE_MODEL

    def test_nav_list_visibility(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)

        assert model_page._nav_list_visibility(), "Navbar list is not visible"

    def test_is_PageTitle_Visible(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)

        assert model_page._is_PageTitle_Visible(), "Page Title is not visible"

    def test_create_model_visibility(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)

        return (
            model_page._create_model_visibility()
        ), "Create Model button is not visible or enabled"

    def test_create_model_click(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)
        model_page._create_model_click()

    def test_create_model_page_title(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)
        return (
            model_page._create_model_page_title() == "Create Device Model"
        ), "Create Model Page Title not visible"

    def test_submit_button(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)
        return model_page._submit_button(), "Submit button is not enabled"

    def test_model_code(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)
        # model_code_locator = self.page.get_by_label("Model Code")
        model_code_locator = page.get_by_label("Model Code")
        expect(model_code_locator).to_be_visible()
        expect(model_code_locator).to_be_enabled()
        model_code_locator.fill("NewCode")

    def test_model_name(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)
        model_page._model_name("NewName")
        # assert model_page._model_name(), "Model Name is not visible"

    def test_model_seriel_sequence(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)
        model_page._model_seriel_sequence("NewSequence")

    def test_hardware_version(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)
        model_page._hardware_version("NewVersion")

    def test_submit_button_click(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)

        submit_button_locator = page.get_by_text("Submit check_circle", exact=True)
        assert not submit_button_locator.is_enabled()

    def test_search_model(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)
        model_page._search_model("NewCode")

    def test_view_icon(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)
        model_page.view_icon()

    def test_update_model_code(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_update_model(UPDATE_MODEL)
        model_page.update_model_code("UpdatedCode")

    def test_update_model_name(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_update_model(UPDATE_MODEL)
        model_page.update_model_name("UpdatedName")

    def test_update_model_seriel_sequence(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_update_model(UPDATE_MODEL)
        model_page.update_model_seriel_sequence("UpdatedSequence")

    def test_update_hardware_version(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_update_model(UPDATE_MODEL)
        model_page.update_hardware_version("UpdatedVersion")

    def test_update_button_click(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_update_model(UPDATE_MODEL)
        model_page._update_button_click()

    def test_search_model_update(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)
        model_page._search_model("updated")

    def test_get_updated_model_text(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)
        
        expected_model_text = ["UpdatedCode"]

        for text in expected_model_text:
            actual_model_text = model_page._get_updated_model_text(text)
            assert actual_model_text == text, \
                f"expected model text '{text}', got '{actual_model_text}'"

    def test_delete_updated_model(self, page):
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)
        model_page.delete_updated_model()
