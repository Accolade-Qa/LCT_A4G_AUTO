"""API Client for authentication and common request handling."""

import json

from config.config import API_BASE_URL, API_PASSWORD, API_USERNAME
from utils.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    """Client for authenticated API requests with centralized token management."""

    @staticmethod
    def validate_credentials():
        """Validate that API credentials are configured.

        Raises:
            ValueError: If API_USERNAME or API_PASSWORD is not set.
        """
        if not API_USERNAME or not API_PASSWORD:
            raise ValueError(
                "API_USERNAME / API_PASSWORD must be set in the environment "
                "(or derive from APP_USERNAME / APP_PASSWORD)."
            )

    @staticmethod
    def get_bearer_token(page):
        """Authenticate with API and retrieve bearer token.

        Args:
            page: Playwright page object with request context.

        Returns:
            str: Bearer token for subsequent API requests.

        Raises:
            Exception: If login fails or token is not found in response.
        """
        APIClient.validate_credentials()

        login_url = f"{API_BASE_URL}/users/login"
        login_payload = {
            "userEmail": API_USERNAME,
            "password": API_PASSWORD,
        }

        logger.info("Logging in to API user %s", API_USERNAME)
        login_response = page.request.post(
            login_url,
            data=json.dumps(login_payload),
            headers={"Content-Type": "application/json"},
        )

        if not login_response.ok:
            raise Exception(
                f"API login failed: {login_response.status} {login_response.text()}"
            )
        logger.info("API login succeeded with status %s", login_response.status)

        login_data = login_response.json()
        token = login_data.get("data", {}).get("token")

        if not token:
            raise Exception("Token not found in login response payload")

        return token

    @staticmethod
    def get_request_headers(page, extra_headers=None, include_json_content_type=True):
        """Get authorization headers for API requests.

        Args:
            page: Playwright page object with request context.
            extra_headers: Optional headers to merge.
            include_json_content_type: If False, omit Content-Type.

        Returns:
            dict: Authorization headers for API requests.
        """
        token = APIClient.get_bearer_token(page)
        headers = {
            "Authorization": f"Bearer {token}",
        }
        if include_json_content_type:
            headers["Content-Type"] = "application/json"
        if extra_headers:
            headers.update(extra_headers)
        return headers

    @staticmethod
    def send_request(page, method, endpoint, **kwargs):
        """Send an authenticated API request.

        Args:
            page: Playwright page object with request context.
            method: HTTP method ('GET', 'POST', 'PUT', 'PATCH', or 'DELETE').
            endpoint: API endpoint path (e.g., '/device/getProductionDeviceCount').
            **kwargs: Additional arguments to pass to page.request.

        Returns:
            dict: Parsed JSON response.

        Raises:
            Exception: If the request fails.
        """
        headers = kwargs.pop("headers", None)

        files = kwargs.pop("files", None)
        if files is not None:
            kwargs["multipart"] = files
        include_json_content_type = files is None
        headers = APIClient.get_request_headers(
            page,
            extra_headers=headers,
            include_json_content_type=include_json_content_type,
        )
        url = f"{API_BASE_URL}{endpoint}"

        logger.info("Sending %s request to %s", method, endpoint)

        method_upper = method.upper()
        if method_upper == "GET":
            response = page.request.get(url, headers=headers, **kwargs)
        elif method_upper == "POST":
            response = page.request.post(url, headers=headers, **kwargs)
        elif method_upper == "PUT":
            response = page.request.put(url, headers=headers, **kwargs)
        elif method_upper == "PATCH":
            response = page.request.patch(url, headers=headers, **kwargs)
        elif method_upper == "DELETE":
            response = page.request.delete(url, headers=headers, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if response.ok:
            logger.info("API request succeeded with status %s", response.status)
            if response.status == 204:  # No Content
                return {}
            return response.json()
        else:
            logger.warning(
                "API request to %s failed with status %s: %s",
                endpoint,
                response.status,
                response.text(),
            )
            raise Exception(
                f"API request to {endpoint} failed: {response.status} {response.text()}"
            )
