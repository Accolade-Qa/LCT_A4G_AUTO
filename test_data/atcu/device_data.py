import random


class DeviceData:
    def __init__(self):
        self.devices = {
            "device_1": {
                "uin": "ACONSBA102500006341",
                "iccid": "89916450244842405755",
                "imei": "866677075606341",
                "vin": "VIN001",
            },
            "device_2": {
                "uin": "ACONSBA102500007166",
                "iccid": "89916450344844658896",
                "imei": "866677075607166",
                "vin": "VIN002",
            },
            "device_3": {
                "uin": "ACONSBA072500097144",
                "iccid": "89910273509008697144",
                "imei": "866677075597144",
                "vin": "VIN003",
            },
            "device_4": {
                "uin": "ACONSBA102500005921",
                "iccid": "89916450344844659043",
                "imei": "866677075605921",
                "vin": "VIN004",
            },
            "device_5": {
                "uin": "ACONSBA102500017065",
                "iccid": "89916450344844509776",
                "imei": "865005071617065",
                "vin": "VIN005",
            },
            "device_6": {
                "uin": "ACONSBA072500006424",
                "iccid": "89916450344844506424",
                "imei": "866677075606424",
                "vin": "VIN006",
            },
            "device_7": {
                "uin": "ACONSBA102500096989",
                "iccid": "89916450344844658748",
                "imei": "866677075596989",
                "vin": "VIN007",
            },
            "device_8": {
                "uin": "ACONSBA102500007760",
                "iccid": "89916450344844658938",
                "imei": "866677075607760",
                "vin": "VIN008",
            },
            "device_9": {
                "uin": "ACONSBA102500008701",
                "iccid": "89916450344844509818",
                "imei": "866677075608701",
                "vin": "VIN009",
            },
            "device_10": {
                "uin": "ACONSBA102500004866",
                "iccid": "89916450344844658870",
                "imei": "866677075604866",
                "vin": "VIN010",
            },
            "device_11": {
                "uin": "ACONSBA102500008826",
                "iccid": "89916450344844658920",
                "imei": "866677075608826",
                "vin": "VIN011",
            },
            "device_12": {
                "uin": "ACONSBA102500006226",
                "iccid": "89916450344844658672",
                "imei": "866677075606226",
                "vin": "VIN012",
            },
            "device_13": {
                "uin": "ACONSBA122500010245",
                "iccid": "89916450544845101800",
                "imei": "866677078910245",
                "vin": "VIN013",
            },
            "device_14": {
                "uin": "ACONSBA122500010963",
                "iccid": "89916450544845103467",
                "imei": "866677078910963",
                "vin": "VIN014",
            },
            "device_15": {
                "uin": "ACONSBA022600010781",
                "iccid": "89916450544845102337",
                "imei": "866677078910781",
                "vin": "VIN015",
            },
            "device_16": {
                "uin": "ACONSBA122500010641",
                "iccid": "89916450544845103764",
                "imei": "866677078910641",
                "vin": "VIN016",
            },
            "device_17": {
                "uin": "ACONSBA042600008833",
                "iccid": "89916450544846893405",
                "imei": "359869072208833",
                "vin": "VIN017",
            },
            "device_18": {
                "uin": "ACONSBA042600010102",
                "iccid": "89916450544846810102",
                "imei": "359869072210102",
                "vin": "VIN018",
            },
            "device_19": {
                "uin": "ACON4IA202200059000",
                "iccid": "89916430134726579000",
                "imei": "866824069139000",
                "vin": "VIN019",
            },
            "device_20": {
                "uin": "ACON4TA202208008783",
                "iccid": "89916450544846808783",
                "imei": "359869072208783",
                "vin": "VIN020",
            },
        }

    @property
    def device_valid_uin(self):
        return [device["uin"] for device in self.devices.values()]

    @property
    def device_valid_iccid(self):
        return [device["iccid"] for device in self.devices.values()]

    @property
    def device_valid_imei(self):
        return [device["imei"] for device in self.devices.values()]

    @property
    def device_valid_vin(self):
        return [device["vin"] for device in self.devices.values()]

    def get_device_data(self):
        return self.devices

    def get_device(self, device_name):
        return self.devices.get(device_name)

    def get_random_device(self):
        return random.choice(list(self.devices.values()))

    def get_random_uin(self):
        return random.choice(self.device_valid_uin)

    def get_random_iccid(self):
        return random.choice(self.device_valid_iccid)
