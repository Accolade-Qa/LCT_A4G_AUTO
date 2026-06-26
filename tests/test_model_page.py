from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.model_page import DeviceModel
from utils.logger import get_logger
from config.config import MODEL_URL, CREATE_NEW_MODEL, UPDATE_MODEL

import pytest

logger = get_logger(__name__)


@pytest.mark.device
@pytest.mark.regression
class TestModelPage:
    def _login_and_dashboard(self, page, project_config=None):
        # Allow callers to omit project_config; fall back to config module values
        if project_config is None:
            from config import config as config_module

            project_config = {
                "base_url": config_module.BASE_URL,
                "username": config_module.USERNAME,
                "password": config_module.PASSWORD,
            }

        login_page = LoginPage(page)
        login_page.load(project_config["base_url"])
        login_page.login(project_config["username"], project_config["password"])

        return DeviceModel(page)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_go_to_model(self, model_page, project_config, report_case):
        logger.info("Starting validation of Model page navigation")

        expected_url = project_config["model_url"]
        actual_url = model_page.page.url
        logger.debug(
            "Model page URL check | expected=%s | actual=%s", expected_url, actual_url
        )

        report_case(
            expected=expected_url,
            actual=actual_url,
            message="Validate Model page navigation",
        )

        assert (
            actual_url == expected_url
        ), f"Expected URL '{expected_url}', got '{actual_url}'"
        logger.info("Successfully validated Model page navigation")

    @pytest.mark.regression
    def test_go_to_create_model(self, page, project_config, report_case):
        logger.info("Starting validation of Create Model page navigation")
        self._login_and_dashboard(page, project_config)
        model_page = DeviceModel(page)
        model_page.go_to_create_model(project_config["create_new_model"])

        actual_url = page.url
        expected_url = project_config["create_new_model"]
        logger.debug(
            "Create Model URL check | expected=%s | actual=%s",
            expected_url,
            actual_url,
        )

        report_case(
            expected=expected_url,
            actual=actual_url,
            message="Validate Create Model page navigation",
        )

        assert (
            actual_url == expected_url
        ), f"Expected URL '{expected_url}', got '{actual_url}'"
        logger.info("Successfully validated Create Model page navigation")

    @pytest.mark.regression
    def test_go_to_update_model(self, page, project_config, report_case):
        logger.info("Starting validation of Update Model page navigation")
        self._login_and_dashboard(page, project_config)
        model_page = DeviceModel(page)
        model_page.go_to_update_model(project_config["update_model"])

        actual_url = page.url
        expected_url = project_config["update_model"]
        logger.debug(
            "Update Model URL check | expected=%s | actual=%s",
            expected_url,
            actual_url,
        )

        report_case(
            expected=expected_url,
            actual=actual_url,
            message="Validate Update Model page navigation",
        )

        assert (
            actual_url == expected_url
        ), f"Expected URL '{expected_url}', got '{actual_url}'"
        logger.info("Successfully validated Update Model page navigation")

    @pytest.mark.regression
    def test_nav_list_visibility(self, model_page, project_config, report_case):
        logger.info("Starting validation of Model navigation list visibility")

        is_visible = model_page._nav_list_visibility()
        logger.debug("Model navigation list visible: %s", is_visible)

        report_case(
            expected="Navbar list should be visible",
            actual=f"Navbar list visible: {is_visible}",
            message="Validate Model navbar list visibility",
        )

        assert is_visible, "Navbar list is not visible"
        logger.info("Successfully validated Model navigation list visibility")

    @pytest.mark.regression
    def test_is_PageTitle_Visible(self, page, report_case):
        logger.info("Starting validation of Model page title visibility")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)

        is_visible = model_page._is_PageTitle_Visible()
        logger.debug("Model page title visible: %s", is_visible)

        report_case(
            expected="Page title should be visible",
            actual=f"Page title visible: {is_visible}",
            message="Validate Model page title visibility",
        )

        assert is_visible, "Page Title is not visible"
        logger.info("Successfully validated Model page title visibility")

    @pytest.mark.regression
    def test_create_model_visibility(self, page, report_case):
        logger.info("Starting validation of Create Model button visibility")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)

        is_visible = model_page._create_model_visibility()
        logger.debug("Create Model button visible/enabled: %s", is_visible)

        report_case(
            expected="Create Model button should be visible and enabled",
            actual=f"Create Model button visible/enabled: {is_visible}",
            message="Validate Create Model button availability",
        )

        assert is_visible, "Create Model button is not visible or enabled"
        logger.info("Successfully validated Create Model button visibility")

    @pytest.mark.regression
    def test_create_model_click(self, page, report_case):
        logger.info("Starting validation of Create Model button click")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)
        model_page._create_model_click()

        actual_url = page.url
        logger.debug("Create Model click completed | current_url=%s", actual_url)

        report_case(
            expected="Create Model button click should complete",
            actual=f"Current URL after click: {actual_url}",
            message="Validate Create Model button click",
        )

        logger.info("Successfully clicked Create Model button")

    @pytest.mark.regression
    def test_create_model_page_title(self, page, report_case):
        logger.info("Starting validation of Create Model page title")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)

        expected_title = "Create Device Model"
        actual_title = model_page._create_model_page_title()
        logger.debug(
            "Create Model title check | expected=%s | actual=%s",
            expected_title,
            actual_title,
        )

        report_case(
            expected=expected_title,
            actual=actual_title,
            message="Validate Create Model page title",
        )

        assert actual_title == expected_title, "Create Model Page Title not visible"
        logger.info("Successfully validated Create Model page title")

    @pytest.mark.regression
    def test_submit_button(self, page, report_case):
        logger.info("Starting validation of Create Model Submit button")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)

        is_enabled = model_page._submit_button()
        logger.debug("Create Model Submit button enabled: %s", is_enabled)

        report_case(
            expected="Submit button should be enabled",
            actual=f"Submit button enabled: {is_enabled}",
            message="Validate Create Model Submit button",
        )

        assert is_enabled, "Submit button is not enabled"
        logger.info("Successfully validated Create Model Submit button")

    @pytest.mark.regression
    def test_model_code(self, page, report_case):
        logger.info("Starting validation of Model Code input")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)

        model_code_locator = page.get_by_label("Model Code")
        expect(model_code_locator).to_be_visible()
        expect(model_code_locator).to_be_enabled()
        model_code_locator.fill("NewCode")

        actual_value = model_code_locator.input_value()
        logger.debug("Model Code field value after fill: %s", actual_value)

        report_case(
            expected="Model Code field should accept value 'NewCode'",
            actual=f"Model Code field value: '{actual_value}'",
            message="Validate Model Code input",
        )

        assert actual_value == "NewCode", f"Expected 'NewCode', got '{actual_value}'"
        logger.info("Successfully validated Model Code input")

    @pytest.mark.regression
    def test_model_name(self, page, report_case):
        logger.info("Starting validation of Model Name input")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)
        model_page._model_name("NewName")

        logger.debug("Entered Model Name value: %s", "NewName")
        report_case(
            expected="Model Name field should accept value 'NewName'",
            actual="Model Name value entered",
            message="Validate Model Name input",
        )

        logger.info("Successfully validated Model Name input")

    @pytest.mark.regression
    def test_model_seriel_sequence(self, page, report_case):
        logger.info("Starting validation of Model Serial Sequence input")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)
        model_page._model_seriel_sequence("NewSequence")

        logger.debug("Entered Model Serial Sequence value: %s", "NewSequence")
        report_case(
            expected="Model Serial Sequence field should accept value 'NewSequence'",
            actual="Model Serial Sequence value entered",
            message="Validate Model Serial Sequence input",
        )

        logger.info("Successfully validated Model Serial Sequence input")

    @pytest.mark.regression
    def test_hardware_version(self, page, report_case):
        logger.info("Starting validation of Hardware Version input")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)
        model_page._hardware_version("NewVersion")

        logger.debug("Entered Hardware Version value: %s", "NewVersion")
        report_case(
            expected="Hardware Version field should accept value 'NewVersion'",
            actual="Hardware Version value entered",
            message="Validate Hardware Version input",
        )

        logger.info("Successfully validated Hardware Version input")

    @pytest.mark.regression
    def test_submit_button_click(self, page, report_case):
        logger.info("Starting validation of disabled Submit button state")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(CREATE_NEW_MODEL)

        submit_button_locator = page.get_by_role("button", name="Submit check_circle")
        is_enabled = submit_button_locator.is_enabled()
        logger.debug("Submit button enabled state: %s", is_enabled)

        report_case(
            expected="Submit button should be disabled",
            actual=f"Submit button enabled: {is_enabled}",
            message="Validate disabled Submit button state",
        )

        assert not is_enabled, "Submit button should be disabled"
        logger.info("Successfully validated disabled Submit button state")

    @pytest.mark.regression
    def test_search_model(self, page, report_case):
        logger.info("Starting validation of Model search")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)
        model_page._search_model("NewCode")

        logger.debug("Executed Model search for keyword: %s", "NewCode")
        report_case(
            expected="Model search should execute for 'NewCode'",
            actual="Model search completed",
            message="Validate Model search",
        )

        logger.info("Successfully validated Model search")

    @pytest.mark.regression
    def test_view_icon(self, page, report_case):
        logger.info("Starting validation of Model view icon")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)
        model_page.view_icon()

        logger.debug("Clicked Model view icon")
        report_case(
            expected="Model view icon should be clickable",
            actual="Model view icon clicked",
            message="Validate Model view icon",
        )

        logger.info("Successfully validated Model view icon")

    @pytest.mark.regression
    def test_update_model_code(self, page, report_case):
        logger.info("Starting validation of Update Model Code input")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_update_model(UPDATE_MODEL)
        model_page.update_model_code("UpdatedCode")

        logger.debug("Entered updated Model Code value: %s", "UpdatedCode")
        report_case(
            expected="Update Model Code field should accept value 'UpdatedCode'",
            actual="Updated Model Code value entered",
            message="Validate Update Model Code input",
        )

        logger.info("Successfully validated Update Model Code input")

    @pytest.mark.regression
    def test_update_model_name(self, page, report_case):
        logger.info("Starting validation of Update Model Name input")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_update_model(UPDATE_MODEL)
        model_page.update_model_name("UpdatedName")

        logger.debug("Entered updated Model Name value: %s", "UpdatedName")
        report_case(
            expected="Update Model Name field should accept value 'UpdatedName'",
            actual="Updated Model Name value entered",
            message="Validate Update Model Name input",
        )

        logger.info("Successfully validated Update Model Name input")

    @pytest.mark.regression
    def test_update_model_seriel_sequence(self, page, report_case):
        logger.info("Starting validation of Update Model Serial Sequence input")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_update_model(UPDATE_MODEL)
        model_page.update_model_seriel_sequence("UpdatedSequence")

        logger.debug(
            "Entered updated Model Serial Sequence value: %s", "UpdatedSequence"
        )
        logger.debug(
            "Entered updated Model Serial Sequence value: %s", "UpdatedSequence"
        )
        report_case(
            expected="Update Model Serial Sequence field should accept value 'UpdatedSequence'",
            actual="Updated Model Serial Sequence value entered",
            message="Validate Update Model Serial Sequence input",
        )

        logger.info("Successfully validated Update Model Serial Sequence input")

    @pytest.mark.regression
    def test_update_hardware_version(self, page, report_case):
        logger.info("Starting validation of Update Hardware Version input")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_update_model(UPDATE_MODEL)
        model_page.update_hardware_version("UpdatedVersion")

        logger.debug("Entered updated Hardware Version value: %s", "UpdatedVersion")
        report_case(
            expected="Update Hardware Version field should accept value 'UpdatedVersion'",
            actual="Updated Hardware Version value entered",
            message="Validate Update Hardware Version input",
        )

        logger.info("Successfully validated Update Hardware Version input")

    @pytest.mark.regression
    def test_update_button_click(self, page, report_case):
        logger.info("Starting validation of Update button click")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_update_model(UPDATE_MODEL)
        model_page._update_button_click()

        logger.debug("Clicked Update button on Model page")
        report_case(
            expected="Update button click should complete",
            actual="Update button clicked",
            message="Validate Update button click",
        )

        logger.info("Successfully validated Update button click")

    @pytest.mark.regression
    def test_search_model_update(self, page, report_case):
        logger.info("Starting validation of updated Model search")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)
        model_page._search_model("updated")

        logger.debug("Executed Model search for keyword: %s", "updated")
        report_case(
            expected="Model search should execute for 'updated'",
            actual="Model search completed",
            message="Validate updated Model search",
        )

        logger.info("Successfully validated updated Model search")

    @pytest.mark.regression
    def test_get_updated_model_text(self, page, report_case):
        logger.info("Starting validation of updated Model text")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)

        expected_model_text = ["UpdatedCode"]
        actual_model_texts = []

        for text in expected_model_text:
            actual_model_text = model_page._get_updated_model_text(text)
            actual_model_texts.append(actual_model_text)
            logger.debug(
                "Updated Model text check | expected=%s | actual=%s",
                text,
                actual_model_text,
            )

        report_case(
            expected=expected_model_text,
            actual=actual_model_texts,
            message="Validate updated Model text",
        )

        assert (
            actual_model_texts == expected_model_text
        ), f"Expected model text {expected_model_text}, got {actual_model_texts}"
        assert (
            actual_model_texts == expected_model_text
        ), f"Expected model text {expected_model_text}, got {actual_model_texts}"
        logger.info("Successfully validated updated Model text")

    @pytest.mark.regression
    def test_delete_updated_model(self, page, report_case):
        logger.info("Starting validation of updated Model delete")
        self._login_and_dashboard(page)
        model_page = DeviceModel(page)
        model_page.go_to_model(MODEL_URL)
        model_page.delete_updated_model()

        logger.debug("Executed delete action for updated Model")
        report_case(
            expected="Updated Model delete action should complete",
            actual="Updated Model delete action completed",
            message="Validate updated Model delete",
        )

        logger.info("Successfully validated updated Model delete")
