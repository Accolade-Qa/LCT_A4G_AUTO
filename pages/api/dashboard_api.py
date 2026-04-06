import json

from config.config import API_BASE_URL, API_PASSWORD, API_USERNAME


class DashboardAPI:
    @staticmethod
    def _fetch_dashboard_cards_from_api(page):
        """
        Authenticate with the dashboard backend, then call each card-specific
        endpoint to return a map of the expected titles (in upper case) to counts.
        """

        if not API_USERNAME or not API_PASSWORD:
            raise ValueError(
                "API_USERNAME / API_PASSWORD must be set in the environment "
                "(or derive from APP_USERNAME / APP_PASSWORD)."
            )

        login_url = f"{API_BASE_URL}/users/login"

        login_payload = {
            "userEmail": API_USERNAME,
            "password": API_PASSWORD,
        }

        login_response = page.request.post(
            login_url,
            data=json.dumps(login_payload),
            headers={"Content-Type": "application/json"},
        )

        if not login_response.ok:
            raise Exception(
                f"API login failed: {login_response.status} {login_response.text()}"
            )

        login_data = login_response.json()
        token = login_data.get("data", {}).get("token")

        if not token:
            raise Exception("Token not found in login response payload")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        api_endpoints = {
            "TOTAL PRODUCTION DEVICES": "/device/getProductionDeviceCount?selectedDeviceModelId=&selectedCustomerId=",
            "TOTAL DISPATCHED DEVICES": "/device/getDispatchDeviceCount?selectedDeviceModelId=&selectedCustomerId=",
            "TOTAL INSTALLED DEVICES": "/device/getInstalledDeviceCount?selectedDeviceModelId=&selectedCustomerId=",
            "TOTAL DISCARDED DEVICES": "/device/getDiscardedDeviceCount?selectedDeviceModelId=&selectedCustomerId=",
        }

        result = {}

        for title, endpoint in api_endpoints.items():
            response = page.request.get(
                f"{API_BASE_URL}{endpoint}",
                headers=headers,
            )

            if response.ok:
                data = response.json()
                count = data.get("data")
                print(f"API response for '{title}': {data}")  # Debugging line to check API response
                if count is None:
                    count = data.get("count")
                    print(f"API response for '{title}' using 'count' field: {data}")  # Debugging line to check alternative count field
                result[title] = int(count)
            else:
                result[title] = 0

        return result
