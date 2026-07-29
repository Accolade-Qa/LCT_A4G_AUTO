from utils.logger import get_logger
from .api_client import APIClient
from config.config import API_BASE_URL, API_USERNAME, API_PASSWORD

logger = get_logger(__name__)


class RoleManagementAPI(APIClient):
    """API client for role management operations."""

    @staticmethod
    def get_roles(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """Fetch all roles from API.

        Args:
            page: Playwright page object with request context.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            dict: API response payload containing roles data and totalItems count.
        """
        if "sampark-qa" in api_base_url or api_base_url.rstrip("/").endswith(
            "sampark-qa.accoladeelectronics.com"
        ):
            endpoint = "/api/roles/getRoles?page=0&size=1000&search=&userRole="
        else:
            endpoint = "/roles/getRoles?page=0&size=1000&search=&userRole="

        logger.info("Fetching roles list from %s", endpoint)
        return APIClient.send_request(
            page,
            api_base_url,
            api_username,
            api_password,
            "GET",
            endpoint,
        )

    @staticmethod
    def delete_role(
        page,
        role_id,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """Delete a role by role ID via API.

        Args:
            page: Playwright page object with request context.
            role_id: ID of the role to delete.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            dict: API response payload.
        """
        if "sampark-qa" in api_base_url or api_base_url.rstrip("/").endswith(
            "sampark-qa.accoladeelectronics.com"
        ):
            endpoint = f"/api/roles/deleteRole?roleId={role_id}"
        else:
            endpoint = f"/roles/deleteRole?roleId={role_id}"

        logger.info("Sending DELETE request for role ID %s to %s", role_id, endpoint)
        return APIClient.send_request(
            page,
            api_base_url,
            api_username,
            api_password,
            "DELETE",
            endpoint,
        )

    @staticmethod
    def delete_roles(
        page,
        api_base_url=API_BASE_URL,
        api_username=API_USERNAME,
        api_password=API_PASSWORD,
    ):
        """Fetch all roles count and attempt to delete role permissions using GET and DELETE methods.

        Args:
            page: Playwright page object with request context.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            dict: Summary of deletion execution.
        """
        logger.info("Testing delete role permission functionality via API")

        # Step 1: GET all roles count
        response = RoleManagementAPI.get_roles(
            page, api_base_url, api_username, api_password
        )
        total_roles = response.get("totalItems", 0)

        # Step 2: Iterate and DELETE role by ID
        for i in range(1, total_roles + 1):
            try:
                del_response = RoleManagementAPI.delete_role(
                    page, i, api_base_url, api_username, api_password
                )

                assert (
                    del_response.get("message") == "Success"
                ), f"Failed to delete permission for role group {i}"

                logger.info("Deleted role group %s successfully", i)

            except Exception as e:
                error_message = str(e)

                if (
                    "Cannot delete role: Role is assigned to one or more users."
                    in error_message
                ):
                    logger.warning(
                        "Cannot delete role group %s: Role is assigned to users",
                        i,
                    )
                    continue

                logger.error(
                    "Unexpected error while deleting role group %s: %s",
                    i,
                    error_message,
                )
                raise

        logger.info("Delete role management API operation completed")
        return {"success": True, "total_roles_processed": total_roles}
