import re
import pytest
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.auth
@pytest.mark.critical
@pytest.mark.regression
class TestLoginPage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        """Automatically log test lifecycle events"""
        test_name = request.node.name
        logger.info("Starting Login Page test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug("Login Page test finished without call report: %s", test_name)
        elif report.passed:
            logger.info("Login Page test passed: %s", test_name)
        elif report.failed:
            logger.error("Login Page test failed: %s", test_name)
            logger.debug(
                "Login Page failure details for %s: %s",
                test_name,
                report.longrepr,
            )
        elif report.skipped:
            logger.warning("Login Page test skipped: %s", test_name)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_with_valid_credentials(
        self,
        login_page,
        project_config,
        test_data,
        report_case,
    ):
        """Validate successful login with valid username and password"""
        logger.info("Starting validation of login with valid credentials")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_url = project_config["dashboard_url"]
        logger.debug("Expected dashboard URL: %s", expected_url)

        logger.debug(
            "Submitting login credentials for user: %s",
            project_config["username"],
        )
        login_page.login(
            project_config["username"],
            project_config["password"],
        )

        login_page.page.wait_for_url("**/device-dashboard-page", timeout=60000)

        actual_url = login_page.page.url

        assert project_config["username"] == test_data.get(
            "login_user"
        ), "Configured username should match project login user"
        assert (
            project_config["dashboard_url"] in actual_url
        ), f"Expected dashboard URL to contain {project_config['dashboard_url']}, got {actual_url}"

        logger.debug(
            "Login URL check | expected=%s | actual=%s",
            expected_url,
            actual_url,
        )

        report_case(
            expected=expected_url,
            actual=actual_url,
            message="Validate successful navigation to dashboard after login",
        )

        logger.info("Comparing expected and actual URLs after login")

        assert actual_url == expected_url, (
            f"Expected to navigate to '{expected_url}' after login, "
            f"but got '{actual_url}'"
        )

        logger.info("Login validation with valid credentials completed successfully")

    @pytest.mark.regression
    def test_login_with_invalid_credentials(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate error message when logging in with invalid credentials"""
        logger.info("Starting validation of login with invalid credentials")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_error_message = "Minimum 6 characters required"

        logger.debug(
            "Submitting invalid credentials | username=%s | password=%s",
            project_config["invalid_username"],
            project_config["invalid_password"],
        )
        actual_error_message = (
            login_page.login_with_invalid_credentials(
                project_config["invalid_username"],
                project_config["invalid_password"],
            )
            .strip()
            .lower()
            .rstrip(".")
        )

        expected_error_normalized = expected_error_message.strip().lower().rstrip(".")

        logger.debug(
            "Invalid login error message check | expected=%s | actual=%s",
            expected_error_normalized,
            actual_error_message,
        )

        report_case(
            expected=expected_error_normalized,
            actual=actual_error_message,
            message="Validate error message for invalid credentials",
        )

        logger.info("Comparing expected and actual error messages")

        assert actual_error_message == expected_error_normalized, (
            f"Expected error message '{expected_error_normalized}', "
            f"but got '{actual_error_message}'"
        )

        logger.info("Invalid credentials validation completed successfully")

    @pytest.mark.regression
    def test_login_with_username_only(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate error message when logging in with username only"""
        logger.info("Starting validation of login with username only")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_error_message = "minimum 6 characters required"

        logger.debug(
            "Submitting username only: %s",
            project_config["username"],
        )
        error_message = login_page.login_with_usernameonly(project_config["username"])

        logger.debug("Received error message: %s", error_message)
        assert error_message != "", "Error message should not be empty"

        actual_error_normalized = error_message.strip().lower().rstrip(".")

        logger.debug(
            "Username only error message check | expected=%s | actual=%s",
            expected_error_message,
            actual_error_normalized,
        )

        report_case(
            expected=expected_error_message,
            actual=actual_error_normalized,
            message="Validate error message for username only",
        )

        logger.info("Comparing expected and actual error messages")

        assert actual_error_normalized == expected_error_message, (
            f"Expected error message '{expected_error_message}', "
            f"but got '{actual_error_normalized}'"
        )

        logger.info("Username only validation completed successfully")

    @pytest.mark.regression
    def test_login_with_password_only(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate error message when logging in with password only"""
        logger.info("Starting validation of login with password only")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_error_message = "This field is required and can't be only spaces."

        logger.debug("Submitting password only with username field as spaces")
        error_message = login_page.login_with_passwordonly(
            " ",
            project_config["password"],
        )

        logger.debug("Received error message: %s", error_message)
        assert error_message != "", "Error message should not be empty"

        actual_error = error_message.strip().lower().rstrip(".")
        expected_error = expected_error_message.strip().lower().rstrip(".")

        logger.debug(
            "Password only error message check | expected=%s | actual=%s",
            expected_error,
            actual_error,
        )

        report_case(
            expected=expected_error,
            actual=actual_error,
            message="Validate error message for password only",
        )

        logger.info("Comparing expected and actual error messages")

        assert actual_error == expected_error, (
            f"Expected error message '{expected_error}', " f"but got '{actual_error}'"
        )

        logger.info("Password only validation completed successfully")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_page_title_is_correct(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate that the login page title is correct"""
        logger.info("Starting validation of login page title")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_title = project_config["page_title"]
        logger.debug("Expected page title: %s", expected_title)

        logger.debug("Verifying page title")
        actual_title = login_page.verify_page_title(expected_title)

        actual_title_normalized = actual_title.strip().lower()
        expected_title_normalized = expected_title.strip().lower()

        logger.debug(
            "Page title check | expected=%s | actual=%s",
            expected_title_normalized,
            actual_title_normalized,
        )

        report_case(
            expected=expected_title_normalized,
            actual=actual_title_normalized,
            message="Validate login page title",
        )

        logger.info("Comparing expected and actual page titles")

        assert actual_title_normalized == expected_title_normalized, (
            f"Expected page title '{expected_title}', " f"but got '{actual_title}'"
        )

        logger.info("Page title validation completed successfully")

    @pytest.mark.regression
    def test_login_with_long_username_and_short_password(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate error messages when logging in with long username and short password"""
        logger.info(
            "Starting validation of login with long username and short password"
        )

        expected_errors = [
            "Please enter a valid Email ID.",
            "Minimum 6 characters required.",
        ]
        logger.debug("Expected error messages: %s", expected_errors)

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        logger.debug(
            "Submitting invalid credentials | username=shitalaccolade | password=ABCD"
        )
        login_page.login("shitalaccolade", "ABCD")

        logger.debug("Retrieving error messages from page")
        actual_errors = login_page.get_error_message()

        logger.debug(
            "Error messages retrieved | count=%s | errors=%s",
            len(actual_errors),
            actual_errors,
        )

        expected_errors_str = ", ".join(expected_errors)
        actual_errors_str = (
            ", ".join(actual_errors) if actual_errors else "No error message"
        )

        logger.debug(
            "Long username/short password error check | expected=%s | actual=%s",
            expected_errors_str,
            actual_errors_str,
        )

        report_case(
            expected=expected_errors_str,
            actual=actual_errors_str,
            message="Validate error messages for long username and short password",
        )

        logger.info("Comparing expected and actual error messages")

        assert sorted(actual_errors) == sorted(expected_errors), (
            f"Expected error messages {expected_errors}, " f"but got {actual_errors}"
        )

        logger.info(
            "Long username and short password validation completed successfully"
        )

    @pytest.mark.regression
    def test_login_with_short_username_and_short_password(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate error messages when logging in with short username and short password"""
        logger.info(
            "Starting validation of login with short username and short password"
        )

        expected_errors = [
            "Please enter a valid Email ID.",
            "Minimum 6 characters required.",
        ]
        logger.debug("Expected error messages: %s", expected_errors)

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        logger.debug("Submitting invalid credentials | username=shital | password=ABCD")
        login_page.login("shital", "ABCD")

        logger.debug("Retrieving error messages from page")
        actual_errors = login_page.get_error_message()

        logger.debug(
            "Error messages retrieved | count=%s | errors=%s",
            len(actual_errors),
            actual_errors,
        )

        expected_errors_str = ", ".join(expected_errors)
        actual_errors_str = (
            ", ".join(actual_errors) if actual_errors else "No error message"
        )

        logger.debug(
            "Short username/short password error check | expected=%s | actual=%s",
            expected_errors_str,
            actual_errors_str,
        )

        report_case(
            expected=expected_errors_str,
            actual=actual_errors_str,
            message="Validate error messages for short username and short password",
        )

        logger.info("Comparing expected and actual error messages")

        assert sorted(actual_errors) == sorted(expected_errors), (
            f"Expected error messages {expected_errors}, " f"but got {actual_errors}"
        )

        logger.info(
            "Short username and short password validation completed successfully"
        )

    @pytest.mark.regression
    def test_footer_links_are_present(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate that footer links are present on the login page"""
        logger.info("Starting validation of footer links presence")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        expected_links = ["Accolade Electronics Pvt. Ltd."]
        logger.debug("Expected footer links: %s", expected_links)

        logger.debug("Verifying footer links")
        actual_links = login_page.verify_footer_links_present()

        logger.debug(
            "Footer links retrieved | count=%s | links=%s",
            len(actual_links),
            actual_links,
        )

        expected_links_str = ", ".join(expected_links)
        actual_links_str = ", ".join(actual_links) if actual_links else "No links found"

        logger.debug(
            "Footer links check | expected=%s | actual=%s",
            expected_links_str,
            actual_links_str,
        )

        report_case(
            expected=expected_links_str,
            actual=actual_links_str,
            message="Validate footer links presence",
        )

        logger.info("Comparing expected and actual footer links")

        # Validate all expected links are present
        links_found = all(
            any(exp.lower() in link.lower() for link in actual_links)
            for exp in expected_links
        )

        assert (
            links_found
        ), f"Expected footer links {expected_links} not found in {actual_links}"

        logger.info("Footer links presence validation completed successfully")

    @pytest.mark.regression
    def test_footer_links_are_clickable(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate that footer links are clickable on the login page"""
        logger.info("Starting validation of footer links clickability")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        logger.debug("Verifying footer links clickability")
        results = login_page.verify_footer_links_clickable()

        logger.debug(
            "Footer links clickability check | total=%s | results=%s",
            len(results),
            results,
        )

        all_clickable = all(link["clickable"] for link in results)
        expected_result = "All footer links should be clickable"
        actual_result = ", ".join(
            [f"{link['text']}: {link['clickable']}" for link in results]
        )

        logger.debug(
            "Footer links clickability check | expected=%s | actual=%s",
            expected_result,
            actual_result,
        )

        report_case(
            expected=expected_result,
            actual=actual_result,
            message="Validate footer links are clickable",
        )

        logger.info("Validating all footer links are clickable")

        assert all_clickable, (
            f"Expected all footer links to be clickable, " f"but got: {actual_result}"
        )

        logger.info("Footer links clickability validation completed successfully")

    @pytest.mark.regression
    def test_footer_contains_current_year(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate that footer contains the current year"""
        logger.info("Starting validation of footer year")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        logger.debug("Verifying footer year")
        footer_text, current_year = login_page.verify_footer_year()

        logger.debug(
            "Footer year check | footer_text=%s | current_year=%s",
            footer_text,
            current_year,
        )

        expected_year_presence = f"Footer should contain year {current_year}"
        actual_footer_text = footer_text

        year_found = current_year in footer_text

        logger.debug(
            "Footer year check | expected=%s | actual=%s",
            expected_year_presence,
            actual_footer_text,
        )

        report_case(
            expected=expected_year_presence,
            actual=actual_footer_text,
            message="Validate footer contains current year",
        )

        logger.info("Comparing footer text with expected year")

        assert year_found, (
            f"Expected year {current_year} to be found in footer text, "
            f"but got: {footer_text}"
        )

        logger.info("Footer year validation completed successfully")

    @pytest.mark.regression
    def test_build_version_format_is_valid(
        self,
        login_page,
        project_config,
        report_case,
    ):
        """Validate that build version is in valid format (X.Y.Z)"""
        logger.info("Starting validation of build version format")

        logger.debug("Loading base URL: %s", project_config["base_url"])
        login_page.load(project_config["base_url"])

        logger.debug("Retrieving build version from page")
        version = login_page.get_build_version()

        logger.debug("Retrieved build version: %s", version)

        expected_format = "Build version should be in format X.Y.Z"

        not_empty = version is not None and version != ""
        valid_format = bool(re.search(r"\d+\.\d+\.\d+", version))

        logger.debug(
            "Build version validation | not_empty=%s | valid_format=%s",
            not_empty,
            valid_format,
        )

        report_case(
            expected=expected_format,
            actual=version,
            message="Validate build version format",
        )

        logger.info("Comparing build version format with expected pattern")

        assert not_empty, "Build version should not be empty"

        assert valid_format, (
            f"Expected build version in format X.Y.Z, " f"but got: {version}"
        )

        logger.info("Build version format validation completed successfully")
