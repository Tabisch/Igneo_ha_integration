import logging
from datetime import timedelta
from tokenize import String
from typing import Any, Callable, Dict, Optional

import EstymaApi

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
    CONF_NAME
)

from .const import(
ATTR_consumption_fuel_total_current_sub1,
ATTR_temp_boiler_return_sub1,
ATTR_temp_heating_curcuit1_sub1,
ATTR_temp_heating_curcuit2_sub1,
ATTR_temp_heating_curcuit3_sub1,
ATTR_temp_heating_curcuit4_sub1,
ATTR_power_output_boiler_sub1,
ATTR_lamda_pwm_sub1,
ATTR_temp_lamda_sub1,
ATTR_temp_boiler_sub1,
ATTR_temp_boiler_obli_sub1,
ATTR_temp_exhaust_boiler_sub1,
ATTR_oxygen_content_exhaust_sub1,
ATTR_status_burner_current_sub1,
ATTR_fuel_fill_level_sub1,
ATTR_temp_outside_sub1,
ATTR_energy_meter_sub1,
ATTR_status_boiler_pump_sub1,
ATTR_sensor_type_circuit1_sub1,
ATTR_target_temp_obw1_sub1,
ATTR_status_pump_heating_curcuit1_sub1,
ATTR_temp_buffer_top_sub1,
ATTR_temp_buffer_bottom_sub1,
ATTR_device_type_sub1,
ATTR_number_obw_heating_curcuit_sub1,
ATTR_number_obw_cwu_sub1,
ATTR_number_buffers_sub1,
ATTR_status_solar_connected_sub1,
ATTR_state_lamda_sub1,
ATTR_temp_boiler_target_sub1,
ATTR_temp_boiler_target_sub3,
ATTR_temp_boiler_target_sub4,
ATTR_burner_enabled_sub1,
ATTR_operation_mode_boiler_sub1,
ATTR_status_controller_sub1,
ATTR_cwu_heat_now_sub1,
ATTR_target_temp_room_comf_heating_curcuit_sub1,
ATTR_target_temp_room_comf_heating_curcuit_sub3,
ATTR_target_temp_room_comf_heating_curcuit_sub4,
ATTR_target_temp_room_eco_heating_curcuit_sub1,
ATTR_target_temp_room_eco_heating_curcuit_sub3,
ATTR_target_temp_room_eco_heating_curcuit_sub4,
ATTR_heating_curcuit_prog_obw1_sub1,
ATTR_target_temp_buffer_top_sub1,
ATTR_target_temp_buffer_top_sub3,
ATTR_target_temp_buffer_top_sub4,
ATTR_target_temp_buffer_bottom_sub1,
ATTR_target_temp_buffer_bottom_sub3,
ATTR_target_temp_buffer_bottom_sub4,
ATTR_timer_heating_curcuit1_monday_sub1,
ATTR_timer_heating_curcuit1_tuesday_sub1,
ATTR_timer_heating_curcuit1_wednesday_sub1,
ATTR_timer_heating_curcuit1_thursday_sub1,
ATTR_timer_heating_curcuit1_friday_sub1,
ATTR_timer_heating_curcuit1_saturday_sub1,
ATTR_timer_heating_curcuit1_sunday_sub1,
ATTR_current_status_burner_sub1_int,
ATTR_daystats_data,
ATTR_rangeFrom,
ATTR_rangeTo,
ATTR_solar_power_used,
ATTR_consumption_fuel_end_of_last_day,
ATTR_date,
ATTR_online,
ATTR_is_online,
ATTR_last_date,
ATTR_diff,
ATTR_can_status,
ATTR_number_of_alarms,
ATTR__execution_time,
ATTR_count_buffers_sub1   
)

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(seconds=30)

CONF_DEVICES = "devices"

IGNEO_DEVICE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.Number,
        vol.Optional(CONF_NAME): cv.string
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_DEVICES): vol.All(cv.ensure_list,[IGNEO_DEVICE_SCHEMA])
    }
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    print("")

async def async_setup_platform(hass: HomeAssistantType, config: ConfigType, async_add_entities: Callable, discovery_info: Optional[DiscoveryInfoType] = None,) -> None:
    """Set up the sensor platform."""
    Api = EstymaApi(config[CONF_USERNAME],config[CONF_PASSWORD])
    sensors = [IgneoSensor(Api, repo) for repo in config[CONF_REPOS]]
    async_add_entities(sensors, update_before_add=True)



class IgneoSensor(SensorEntity):

    def __init__(self, estymaapi, Device_Id, Name) -> None:
        super().__init__()
        self.estymaapi = estymaapi
        self._name = Name
        self._Device_Id = Device_Id
        self.attrs: Dict[str, Any] = {}
        self._available = True

    @property
    def name(self) -> str:
        return self._name

    @property
    def device_id(self) -> str:
        return self._Device_Id

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    @property
    def state(self) -> Optional[str]:
        return self._state

