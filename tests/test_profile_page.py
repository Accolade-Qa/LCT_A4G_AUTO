from utils.logger import get_logger
import pytest
from pages.api.api_client import APIClient

logger = get_logger(__name__)


class TestProfilePage:
    @pytest.fixture(autouse=True)
    def log_test_case(self, request):
        test_name = request.node.name
        logger.info("Starting profile page test: %s", test_name)
        logger.debug("Executing test node: %s", request.node.nodeid)
        yield
        report = getattr(request.node, "rep_call", None)
        if report is None:
            logger.debug(
                "Profile page test finished without call report: %s", test_name
            )
        elif report.passed:
            logger.info("Profile page test passed: %s", test_name)
        elif report.failed:
            logger.error("Profile page test failed: %s", test_name)
            logger.debug(
                "Profile page failure details for %s: %s", test_name, report.longrepr
            )
        elif report.skipped:
            logger.warning("Profile page test skipped: %s", test_name)

    def test_login_data(self, profile_page):
        """Test fetching login data using API client."""
        logger.info("Testing login data retrieval from ProfilePage")
        try:
            login_data = profile_page.get_login_data()

            # login data should not be none
            assert login_data is not None, "Login data should not be None"

            # login data should be a dict and contain expected keys
            assert isinstance(login_data, dict), "Login data should be a dictionary"

            # basic assertions on login data keys
            ## id should be int type and not empty
            assert isinstance(
                login_data.get("id"), int
            ), "Login data 'id' should be an integer"
            assert (
                login_data.get("id") != 0
            ), "Login data 'id' should not be empty or zero"
            assert "id" in login_data, "Login data should contain 'id'"

            ## full name should be string type and not empty
            assert isinstance(
                login_data.get("fullName"), str
            ), "Login data 'fullName' should be a string"
            assert login_data.get(
                "fullName"
            ), "Login data 'fullName' should not be empty"
            assert "fullName" in login_data, "Login data should contain 'fullName'"

            assert "leadName" in login_data, "Login data should contain 'leadName'"
            assert "roleType" in login_data, "Login data should contain 'roleType'"
            assert "userRole" in login_data, "Login data should contain 'userRole'"
            assert (
                "userPermission" in login_data
            ), "Login data should contain 'permissions'"

            ## assert on permission obj count should be 16
            assert (
                len(login_data["userPermission"]) == 16
            ), "Permissions should contain 16 items"

            # assert on if roletyp is super admin then user have all permission with view, create, update, delete and count should be 16
            if login_data.get("roleType") == "SUPER_ADMIN":
                permissions = login_data.get("userPermission", [])
                assert len(permissions) == 16, "SUPER_ADMIN should have 16 permissions"
                for perm in permissions:
                    assert (
                        perm.get("view") is True
                    ), "SUPER_ADMIN should have view permission"
                    assert (
                        perm.get("create") is True
                    ), "SUPER_ADMIN should have create permission"
                    assert (
                        perm.get("update") is True
                    ), "SUPER_ADMIN should have update permission"
                    assert (
                        perm.get("delete") is True
                    ), "SUPER_ADMIN should have delete permission"

            logger.info("Login data retrieval test passed")
        except AssertionError as e:
            logger.error("Assertion error during login data test: %s", str(e))
            raise
        except Exception as e:
            logger.error("Unexpected error during login data test: %s", str(e))
            raise
