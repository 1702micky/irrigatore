
from homeassistant.helpers.entity import Entity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    api = hass.data["tuya_manual"]["api"]
    device_id = hass.data["tuya_manual"]["device_id"]

    async_add_entities([
        BatterySensor(api, device_id),
        RainStatusSensor(api, device_id),
    ])

class TuyaSensor(Entity):
    def __init__(self, api, device_id, name, dp_code):
        self.api = api
        self.device_id = device_id
        self._name = name
        self.dp_code = dp_code
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        data = await self.api.get(f"/cloud/thing/{self.device_id}/status")
        if data["success"]:
            dps = {dp["code"]: dp["value"] for dp in data["result"]}
            self._state = dps.get(self.dp_code)

class BatterySensor(TuyaSensor):
    def __init__(self, api, device_id):
        super().__init__(api, device_id, "Battery Percentage", "battery_percentage")

class RainStatusSensor(TuyaSensor):
    def __init__(self, api, device_id):
        super().__init__(api, device_id, "Rain Status", "rain_status")
