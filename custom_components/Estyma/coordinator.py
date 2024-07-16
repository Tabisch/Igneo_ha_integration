"""Example integration using DataUpdateCoordinator."""

from datetime import timedelta
import logging

from homeassistant.components.light import LightEntity
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from EstymaApiWrapper import EstymaApi

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=30)


class EstymaCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass: HomeAssistant, estymaApi: EstymaApi):
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
            always_update=True,
        )

        self.api = estymaApi
        self.dataTextToValues = None
        self.UpdatingSettingTable = None

    async def _async_update_data(self):
        _LOGGER.debug("EstymaCoordinator updating")

        self.dataTextToValues = await self.api.getDeviceData(textToValues=True)
        self.UpdatingSettingTable = await self.api.getUpdatingSettingTable()

        return await self.api.getDeviceData()
