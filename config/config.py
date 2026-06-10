import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=ROOT.parent / ".env")

PROJECT = os.getenv("PROJECT", "lct").lower()
PROJECT_CONFIG_PATH = ROOT / f"{PROJECT}.yaml"

_PROJECT_CONFIG = {}
if PROJECT_CONFIG_PATH.exists():
    with PROJECT_CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        _PROJECT_CONFIG = yaml.safe_load(config_file) or {}


def _get(key, default=None):
    project_value = _PROJECT_CONFIG.get(key.lower())
    if project_value is not None:
        return project_value

    return os.getenv(key, default)


def _get_bool(key, default=False):
    project_value = _PROJECT_CONFIG.get(key.lower())
    if isinstance(project_value, bool):
        return project_value
    if project_value is not None:
        return str(project_value).lower() == "true"

    env_value = os.getenv(key)
    if env_value is not None:
        return str(env_value).lower() == "true"

    return default


BASE_URL = _get("BASE_URL")
USERNAME = _get("USERNAME", _get("APP_USERNAME"))
PASSWORD = _get("PASSWORD", _get("APP_PASSWORD"))
BROWSER = _get("BROWSER", "chromium")
HEADLESS = _get_bool("HEADLESS", False)
SCREENSHOT_ON_FAILURE = _get_bool("SCREENSHOT_ON_FAILURE", True)
LOG_LEVEL = _get("LOG_LEVEL", "INFO")
VIDEO_RECORDING = _get_bool("VIDEO_RECORDING", False)
INVALID_USERNAME = _get("INVALID_USERNAME", "ABCD")
INVALID_PASSWORD = _get("INVALID_PASSWORD", "12345")
API_USERNAME = _get("API_USERNAME", _get("APP_USERNAME", USERNAME))
API_PASSWORD = _get("API_PASSWORD", _get("APP_PASSWORD", PASSWORD))
PAGE_TITLE = _get("PAGE_TITLE", "AEPL LCT-A4G QA Diagnostic Cloud")
IMEI = _get("IMEI", "866677075606341")


# -----------------------------------------------
#               URLs
# -----------------------------------------------
DASHBOARD_URL = _get(
    "DASHBOARD_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/device-dashboard-page",
)
SIM_DATA_DETAILS_URL = _get(
    "SIM_DATA_DETAILS_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/sensorise-sim-data-details",
)
ROLE_MANAGEMENT_URL = _get(
    "ROLE_MANAGEMENT_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/user-role",
)
ROLE_GROUP_URL = _get(
    "ROLE_GROUP_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/role-group",
)
DEVICE_DETAILS_URL = _get(
    "DEVICE_DETAILS_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/device-details",
)
OTA_URL = _get(
    "OTA_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/ota-batch-page",
)
PRODUCTION_PAGE_URL = _get(
    "PRODUCTION_PAGE_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/production-device-page",
)
CREATE_PRODUCTION_URL = _get(
    "CREATE_PRODUCTION_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/create-production-device",
)
ADD_PRODUCTION_URL = _get(
    "ADD_PRODUCTION_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/add-production-device",
)
USER_MANAGEMENT_URL = _get(
    "USER_MANAGEMENT_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/user-tab",
)
API_BASE_URL = _get(
    "API_BASE_URL",
    "http://lct-a4g-qa.accoladeelectronics.com:9090",
)
GOVERNMENT_SERVERS_URL = _get(
    "GOVERNMENT_SERVERS_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/govt-servers",
)
DISPATCHED_DEVICE_URL = _get(
    "DISPATCHED_DEVICE_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/dispatch-device-page",
)
PROFILE_URL = _get(
    "PROFILE_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/profile",
)
MODEL_URL = _get(
    "MODEL_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/model",
)
CREATE_NEW_MODEL = _get(
    "CREATE_NEW_MODEL",
    "http://lct-a4g-qa.accoladeelectronics.com/model-firmware",
)
UPDATE_MODEL = _get(
    "UPDATE_MODEL",
    "http://lct-a4g-qa.accoladeelectronics.com/model-firmware/11",
)
