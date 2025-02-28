"""DataUpdateCoordinator for acond_pro_heat_pump."""

from __future__ import annotations

import logging

import asyncio
from datetime import timedelta

from typing import TYPE_CHECKING, Any
_LOGGER = logging.getLogger(__name__)

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    AcondProApiClientAuthenticationError,
    AcondProApiClientError,
)

if TYPE_CHECKING:
    from .data import AcondProConfigEntry

SCAN_INTERVAL = timedelta(minutes=5)


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class AcondDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: AcondProConfigEntry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except AcondProApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except AcondProApiClientError as exception:
            raise UpdateFailed(exception) from exception

class MyApiCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(
            hass,
            name="My API",
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        async with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get("http://api.example.com/data") as response:
                    data = await response.json()
                    return data
