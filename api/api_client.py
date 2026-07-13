"""API Client for authentication and common request handling."""

import json
from utils.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    """Client for authenticated API requests with centralized token management."""

    @staticmethod
    def validate_credentials(api_username, api_password):
        """Validate that API credentials are configured.

        Args:
            api_username: API username.
            api_password: API password.

        Raises:
            ValueError: If api_username or api_password is not set.
        """
        if not api_username or not api_password:
            raise ValueError(
                "api_username / api_password must be provided "
                "(or derive from project configuration)."
            )

    @staticmethod
    def get_bearer_token(page, api_base_url, api_username, api_password):
        """Authenticate with API and retrieve bearer token.

        Args:
            page: Playwright page object with request context.
            api_base_url: Base URL for API.
            api_username: API username.
            api_password: API password.

        Returns:
            str: Bearer token for subsequent API requests.

        Raises:
            Exception: If login fails or token is not found in response.
        """
        APIClient.validate_credentials(api_username, api_password)

        # Some projects (e.g., sampark) expose the login endpoint under
        # `/api/users/login` while others use `/users/login`. Choose the
        # correct path based on the api_base_url so token retrieval works
        # consistently across projects.
        if "sampark-qa" in api_base_url or api_base_url.rstrip("/").endswith(
            "sampark-qa.accoladeelectronics.com"
        ):
            login_url = f"{api_base_url}/api/users/login"
        else:
            login_url = f"{api_base_url}/users/login"

        login_payload = {
            "userEmail": api_username,
            "password": api_password,
        }

        logger.info("Logging in to API user %s", api_username)
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
    def get_request_headers(
        page,
        api_base_url,
        api_username,
        api_password,
        extra_headers=None,
        include_json_content_type=True,
        token=None,
    ):
        if token is None:
            token = APIClient.get_bearer_token(
                page,
                api_base_url,
                api_username,
                api_password,
            )

        headers = {
            "Authorization": f"Bearer {token}",
        }

        if include_json_content_type:
            headers["Content-Type"] = "application/json"

        if extra_headers:
            headers.update(extra_headers)

        return headers

    @staticmethod
    def send_request(
        page, api_base_url, api_username, api_password, method, endpoint, **kwargs
    ):
        """Send an authenticated API request."""

        headers = kwargs.pop("headers", None)

        files = kwargs.pop("files", None)
        if files is not None:
            kwargs["multipart"] = files

        include_json_content_type = files is None

        # Use supplied token if available
        token = kwargs.pop("token", None)

        headers = APIClient.get_request_headers(
            page,
            api_base_url,
            api_username,
            api_password,
            extra_headers=headers,
            include_json_content_type=include_json_content_type,
            token=token,
        )

        url = f"{api_base_url}{endpoint}"

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

            if response.status == 204:
                return {}

            try:
                return response.json()
            except json.JSONDecodeError as decode_err:
                response_text = response.text()

                if not response_text or response_text.isspace():
                    return {}

                logger.error(
                    "Failed to parse JSON response from %s: %s",
                    endpoint,
                    response_text,
                )

                raise Exception(
                    f"API request to {endpoint} returned invalid JSON: "
                    f"{decode_err}. Response body: {response_text}"
                ) from decode_err

        response_text = response.text()

        logger.warning(
            "API request to %s failed with status %s: %s",
            endpoint,
            response.status,
            response_text,
        )

        raise Exception(
            f"API request to {endpoint} failed: {response.status} {response_text}"
        )
