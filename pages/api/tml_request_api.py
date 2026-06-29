from utils.logger import get_logger
from config.config import TICKET_BASE_URL, TICKET_USERNAME, TICKET_PASSWORD
from utils.helpers import Helpers

import json

logger = get_logger(__name__)


class TmlRequestApi:

    @staticmethod
    def _get_token(
        page,
        api_base_url=TICKET_BASE_URL,
    ):
        """
        Generate authentication token for the CRM APIs.
        """
        payload = {
            "username": TICKET_USERNAME,
            "password": TICKET_PASSWORD,
        }

        endpoint = "/api/crm/generateToken"

        logger.info("Fetching authentication token from %s", endpoint)

        try:
            response = page.request.post(api_base_url + endpoint, data=payload)

            if not response.ok:
                raise Exception(
                    f"Token request failed: {response.status} {response.text()}"
                )

            token_data = response.json()
            token = token_data.get("token")

            print("token :> ", token)

            if not token:
                raise Exception("Authentication token not found in response.")

            logger.info("Successfully fetched authentication token.")

            return token

        except Exception as e:
            logger.error("Failed to fetch authentication token: %s", str(e))
            raise

    @staticmethod
    def post_tml_request_log(
        page,
        api_base_url=TICKET_BASE_URL,
    ):
        payload = [
            {
                "VIN_NO": f"ACCDEV07241580{Helpers.generate_random_number(3)}",
                "ICCID": "89916420534724851291",
                "UIN_NO": "ACON4NA082300092233",
                "DEVICE_IMEI": "861564061380138",
                "DEVICE_MAKE": "Accolade",
                "DEVICE_MODEL": "AEPL051401",
                "ENGINE_NO": "ENGINE_FIXED_00001",
                "REG_NUMBER": "AN01AB1000",
                "REGISTERED_MOBILE_NUMBER": "9730922327",
                "VEHICLE_OWNER_FIRST_NAME": "SURAJ",
                "VEHICLE_OWNER_MIDDLE_NAME": "S",
                "VEHICLE_OWNER_LAST_NAME": "BHALERAO",
                "ADDRESS_LINE_1": "SHIVANE",
                "ADDRESS_LINE_2": "SHIVANE",
                "VEHICLE_OWNER_CITY": "PUNE",
                "VEHICLE_OWNER_DISTRICT": "PUNE",
                "VEHICLE_OWNER_STATE": "Maharashtra",
                "VEHICLE_OWNER_COUNTRY": "India",
                "VEHICLE_OWNER_PINCODE": "411045",
                "VEHICLE_OWNER_REGISTERED_MOBILE": "9730922327",
                "POS_CODE": "AB123",
                "POA_DOC_NAME": "PANAB123",
                "POA_DOC_NO": "PAN1AB123",
                "POI_DOC_TYPE": "ADHARAB123",
                "POI_DOC_NO": "ADHARXYZ123",
                "RTO_OFFICE_CODE": "MH12",
                "RTO_STATE": "MH",
                "PRIMARY_OPERATOR": "BSNL",
                "SECONDARY_OPERATOR": "BHA",
                "PRIMARY_MOBILE_NUMBER": "7777777777",
                "SECONDARY_MOBILE_NUMBER": "9876543210",
                "VEHICLE_MODEL": "NANO",
                "DEALER_CODE": "1000",
                "COMMERCIAL_ACTIVATION_START_DATE": "2024-06-07",
                "COMMERCIAL_ACTIVATION_EXPIRY_DATE": "2028-06-07",
                "MFG_YEAR": "2024",
                "ACCOLADE_POSTING_DATE_TIME": "2024-10-04",
                "SURAJ": "SURAJ DEMO",
                "INVOICE_DATE": "2025-05-01",
                "INVOICE_NUMBER": "AEPL100000000",
                "CERTIFICATE_VALIDITY_DURATION_IN_YEAR": "2",
            }
        ]

        endpoint = "/api/crm/generateTickets"

        logger.info("Creating TML request ticket.")

        try:
            token = TmlRequestApi._get_token(page)

            response = page.request.post(
                api_base_url + endpoint,
                data=json.dumps(payload),
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
            )

            print("response :> ", response)

            if not response.ok:
                raise Exception(
                    f"Ticket request failed: {response.status} {response.text()}"
                )

            tml_request_log_data = response.json()

            data = tml_request_log_data.get("data", {})

            ticket_number = data.get("TICKET_NO")
            VIN = data.get("VIN_NO")
            UIN = data.get("UIN_NO")
            ICCID = data.get("ICCID")

            logger.info(
                "Successfully created TML request. Ticket Number: %s",
                ticket_number,
            )

            return (
                payload,
                VIN,
                UIN,
                ICCID,
                ticket_number,
            )

        except Exception as e:
            logger.error("Failed to create TML request: %s", str(e))
            raise
