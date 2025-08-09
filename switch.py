
from homeassistant.helpers.entity import ToggleEntity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    api = hass.data["tuya_manual"]["api"]
    device_id = hass.data["tuya_manual"]["device_id"]

    async_add_entities([
        ValveSwitch(api, device_id, "Valve Switch A", "switch"),
        ValveSwitch(api, device_id, "Valve Switch B", "switch2"),
        RainSensorSwitch(api, device_id, "Rain Sensor On/Off", "rain_sensor_onoff"),
    ])

class TuyaSwitch(ToggleEntity):
    def __init__(self, api, device_id, name, dp_code):
        self.api = api
        self.device_id = device_id
        self._name = name
        self.dp_code = dp_code
        self._state = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    async def async_update(self):
        data = await self.api.get(f"/cloud/thing/{self.device_id}/status")
        if data["success"]:
            dps = {dp["code"]: dp["value"] for dp in data["result"]}
            self._state = dps.get(self.dp_code, False)

    async def async_turn_on(self, **kwargs):
        await self._set_switch(True)

    async def async_turn_off(self, **kwargs):
        await self._set_switch(False)

    async def _set_switch(self, value):
        payload = {
            "commands": [
                {"code": self.dp_code, "value": value}
            ]
        }
        data = await self.api.post(f"/cloud/thing/{self.device_id}/commands", payload)
        if data["success"]:
            self._state = value

class ValveSwitch(TuyaSwitch):
    pass

class RainSensorSwitch(TuyaSwitch):
    pass
