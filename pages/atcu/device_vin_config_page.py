from pages.atcu.simple_atcu_page import SimpleAtcuPage


class DeviceVinConfigPage(SimpleAtcuPage):
    def __init__(self, page, url: str):
        super().__init__(page, url, "device-vin-config", "VIN")
