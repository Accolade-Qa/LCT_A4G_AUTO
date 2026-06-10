import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


DASHBOARD_URL = os.getenv(
    "DASHBOARD_URL", "http://lct-a4g-qa.accoladeelectronics.com/device-dashboard-page"
)

SIM_DATA_DETAILS_URL = os.getenv(
    "SIM_DATA_DETAILS_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/sensorise-sim-data-details",
)
ROLE_MANAGEMENT_URL = os.getenv(
    "ROLE_MANAGEMENT_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/user-role",
)

ROLE_GROUP_URL = os.getenv(
    "ROLE_GROUP_URL", "http://lct-a4g-qa.accoladeelectronics.com/role-group"
)

DEVICE_DETAILS_URL = os.getenv(
    "DEVICE_DETAILS_URL", "http://lct-a4g-qa.accoladeelectronics.com/device-details"
)

OTA_URL = os.getenv(
    "OTA_URL", "http://lct-a4g-qa.accoladeelectronics.com/ota-batch-page"
)

PRODUCTION_PAGE_URL = os.getenv(
    "PRODUCTION_PAGE_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/production-device-page",
)

CREATE_PRODUCTION_URL = os.getenv(
    "CREATE_PRODUCTION_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/create-production-device",
)

ADD_PRODUCTION_URL = os.getenv(
    "ADD_PRODUCTION_URL",
    "http://lct-a4g-qa.accoladeelectronics.com/add-production-device",
)

USER_MANAGEMENT_URL = os.getenv(
    "USER_MANAGEMENT_URL", "http://lct-a4g-qa.accoladeelectronics.com/user-tab"
)

CUSTOMER_MASTER_URL = os.getenv("CUSTOMER_MASTER_URL", "http://lct-a4g-qa.accoladeelectronics.com/customer-master")


USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")
BROWSER = os.getenv("BROWSER", "chromium")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
VIDEO_RECORDING = os.getenv("VIDEO_RECORDING", "false").lower() == "true"
INVALID_USERNAME = os.getenv("INVALID_USERNAME", "ABCD")
INVALID_PASSWORD = os.getenv("INVALID_PASSWORD", "12345")
API_USERNAME = os.getenv("API_USERNAME", USERNAME)
API_PASSWORD = os.getenv("API_PASSWORD", PASSWORD)
PAGE_TITLE = os.getenv("PAGE_TITLE", "AEPL LCT-A4G QA Diagnostic Cloud")
IMEI = "866677075606341"


# -----------------------------------------------
#               URLs
# -----------------------------------------------
DASHBOARD_URL = "http://lct-a4g-qa.accoladeelectronics.com/device-dashboard-page"

SIM_DATA_DETAILS_URL = (
    "http://lct-a4g-qa.accoladeelectronics.com/sensorise-sim-data-details"
)

ROLE_MANAGEMENT_URL = "http://lct-a4g-qa.accoladeelectronics.com/user-role"

ROLE_GROUP_URL = "http://lct-a4g-qa.accoladeelectronics.com/role-group"

DEVICE_DETAILS_URL = "http://lct-a4g-qa.accoladeelectronics.com/device-details"

OTA_URL = "http://lct-a4g-qa.accoladeelectronics.com/ota-batch-page"

PRODUCTION_PAGE_URL = "http://lct-a4g-qa.accoladeelectronics.com/production-device-page"

CREATE_PRODUCTION_URL = (
    "http://lct-a4g-qa.accoladeelectronics.com/create-production-device"
)

ADD_PRODUCTION_URL = "http://lct-a4g-qa.accoladeelectronics.com/add-production-device"

USER_MANAGEMENT_URL = "http://lct-a4g-qa.accoladeelectronics.com/user-tab"

API_BASE_URL = "http://lct-a4g-qa.accoladeelectronics.com:9090"

GOVERNMENT_SERVERS_URL = "http://lct-a4g-qa.accoladeelectronics.com/govt-servers"

DISPATCHED_DEVICE_URL = "http://lct-a4g-qa.accoladeelectronics.com/dispatch-device-page"

PROFILE_URL = "http://lct-a4g-qa.accoladeelectronics.com/profile"

MODEL_URL = "http://lct-a4g-qa.accoladeelectronics.com/model"

CREATE_NEW_MODEL = "http://lct-a4g-qa.accoladeelectronics.com/model-firmware"

UPDATE_MODEL = "http://lct-a4g-qa.accoladeelectronics.com/model-firmware/11"
