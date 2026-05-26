from pages.api.api_client import APIClient
from pages.api.login_api import LoginAPI
from utils.logger import get_logger

logger = get_logger(__name__)


class GovtServerAPI(APIClient):
    """API client for government server operations."""

    @staticmethod
    def _get_user_id(page):
        """
        Fetch logged-in user ID.
        """

        login = LoginAPI.login(page)

        return login.get("id")

    @staticmethod
    def _send_get_request(page, endpoint, success_message):
        """
        Common GET request handler.
        """

        logger.info("Request endpoint: %s", endpoint)

        try:
            response_data = APIClient.send_request(
                page,
                "GET",
                endpoint,
            )

            logger.info(success_message)

            return response_data.get("data", [])

        except Exception as e:
            logger.error("%s : %s", success_message, str(e))
            raise

    @staticmethod
    def _get_all_servers_list(page):
        """
        Fetch all servers from government server list.

        Returns:
            tuple: (servers_list, first_server_id)
        """

        user_id = GovtServerAPI._get_user_id(page)

        endpoint = (
            "/stateServers/getAllStateServerList?"
            f"page=0&size=1000&search=&userId={user_id}"
        )

        servers = GovtServerAPI._send_get_request(
            page,
            endpoint,
            "Successfully fetched all servers",
        )

        if not servers:
            raise ValueError("No servers found in API response")

        server_id = servers[0].get("id")

        logger.info(
            "Retrieved %d servers from API",
            len(servers),
        )

        logger.debug("Servers: %s", servers)

        return servers, server_id

    @staticmethod
    def get_all_firmware(page):
        """
        Fetch all firmware versions.
        """

        endpoint = (
            "/firmwareMaster/getAllFirmwareList?"
            "page=0&size=1000&search=&firmwareType="
        )

        firmware_versions = GovtServerAPI._send_get_request(
            page,
            endpoint,
            "Successfully fetched all firmware versions",
        )

        logger.info(
            "Retrieved %d firmware versions from API",
            len(firmware_versions),
        )

        logger.debug(
            "Firmware versions: %s",
            firmware_versions,
        )

        return firmware_versions

    @staticmethod
    def _get_firmwares_by_type(page, firmware_type):
        """
        Fetch firmware list by firmware type.

        Args:
            firmware_type: OC or D

        Returns:
            list: Firmware list
        """

        _, server_id = GovtServerAPI._get_all_servers_list(page)

        endpoint = (
            "/firmwareMaster/getFirmwaresListNotAddedInState?"
            f"page=0&size=1000&search=&firmwareType={firmware_type}"
            f"&stateServerId={server_id}"
        )

        firmware_versions = GovtServerAPI._send_get_request(
            page,
            endpoint,
            f"Successfully fetched {firmware_type} firmware versions",
        )

        logger.debug(
            "%s firmware versions: %s",
            firmware_type,
            firmware_versions,
        )

        return firmware_versions

    @staticmethod
    def get_oc_firmwares(page):
        """
        Fetch OC firmware list.
        """

        return GovtServerAPI._get_firmwares_by_type(page, "OC")

    @staticmethod
    def get_d_firmwares(page):
        """
        Fetch D firmware list.
        """

        return GovtServerAPI._get_firmwares_by_type(page, "D")

    @staticmethod
    def get_state_server_details_by_id(page):
        """
        Fetch state server details by ID.
        """

        _, server_id = GovtServerAPI._get_all_servers_list(page)

        endpoint = f"/stateServers/getStateServerDetails?id={server_id}"

        response = GovtServerAPI._send_get_request(
            page,
            endpoint,
            "Successfully fetched state server details",
        )

        oc_firmwares = GovtServerAPI.get_oc_firmwares(page)

        d_firmwares = GovtServerAPI.get_d_firmwares(page)

        logger.debug(
            "State server response: %s",
            response,
        )

        return response, oc_firmwares, d_firmwares
