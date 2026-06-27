from pages.atcu.simple_atcu_page import SimpleAtcuPage


class DeviceStateConfigPage(SimpleAtcuPage):
    def __init__(self, page, url: str):
        super().__init__(page, url, "device-state-config", "State")
