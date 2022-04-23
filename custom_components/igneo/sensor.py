import logging
from datetime import timedelta
from tokenize import String
import traceback
from typing import Any, Callable, Dict, Optional
import json
from typing_extensions import Self

from EstymaApiWrapper import EstymaApi

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)

from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_DEVICE_ID,
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT
)

from .const import *

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(ATTR_language): cv.string
    }
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    _LOGGER.critical("igneo entry")

async def async_setup_platform(hass: HomeAssistantType, config: ConfigType, async_add_entities: Callable, discovery_info: Optional[DiscoveryInfoType] = None,) -> None:
    """Set up the sensor platform."""
    Api = EstymaApi(config[CONF_USERNAME],config[CONF_PASSWORD], config[ATTR_language])
    
    await Api.initialize()

    sensors = []

    for device_id in list(Api.Devices.keys()):
        sensors.append(IgneoSensor(Api, ATTR_temp_heating_curcuit1_sub1, device_id))
        sensors.append(IgneoSensor(Api, ATTR_consumption_fuel_total_current_sub1, device_id))
        sensors.append(IgneoSensor(Api, ATTR_temp_buffer_top_sub1, device_id))
        sensors.append(IgneoSensor(Api, ATTR_temp_buffer_bottom_sub1, device_id))
        sensors.append(IgneoSensor(Api, ATTR_temp_boiler_sub1, device_id))
    
    
    async_add_entities(sensors, update_before_add=True)

class IgneoSensor(SensorEntity):

    def __init__(self, estymaapi: EstymaApi, deviceAttribute, Device_Id) -> None:
        super().__init__()
        self._estymaapi = estymaapi
        self._name = f"{Device_Id}_{deviceAttribute}"
        self._attributename = deviceAttribute
        self._state = None
        self._available = True
        self.attrs: Dict[str, Any] = {CONF_DEVICE_ID: Device_Id}

    @property
    def name(self) -> str:
        return self._name

    @property
    def unique_id(self) -> str:
        return f"{self._name}"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    @property
    def state(self) -> Optional[str]:
        return self._state

    async def async_update(self):
        if(self._estymaapi.initialized == False):
            _LOGGER.info("igneo api not initialized")
            _LOGGER.info(f'igneo api return code {self._estymaapi.returncode}')
            return

        try:
            _LOGGER.info(f"updating {self._name} - {self.attrs[CONF_DEVICE_ID]}")
            self._state = (self._estymaapi.getDeviceData(self.attrs[CONF_DEVICE_ID]))[self._attributename]
        except:
            _LOGGER.exception(traceback.print_exc())