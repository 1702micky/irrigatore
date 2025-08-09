
import asyncio
from homeassistant.helpers import discovery

DOMAIN = "tuya_manual"

async def async_setup(hass, config):
    hass.data[DOMAIN] = {}

    conf = config.get(DOMAIN)
    if conf is None:
        return True

    client_id = conf.get("client_id")
    client_secret = conf.get("client_secret")
    device_id = conf.get("device_id")

    from .tuya_api import TuyaApi
    api = TuyaApi(client_id, client_secret)
    hass.data[DOMAIN]["api"] = api
    hass.data[DOMAIN]["device_id"] = device_id

    hass.async_create_task(
        discovery.async_load_platform(hass, "sensor", DOMAIN, {}, config)
    )
    hass.async_create_task(
        discovery.async_load_platform(hass, "switch", DOMAIN, {}, config)
    )

    return True
