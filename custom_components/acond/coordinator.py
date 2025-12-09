"""DataUpdateCoordinator for acond."""

from __future__ import annotations
from typing import TYPE_CHECKING, Any
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import (
    AcondProApiClientAuthenticationError,
    AcondProApiClientError,
)

if TYPE_CHECKING:
    from .data import AcondProConfigEntry

class AcondDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: AcondProConfigEntry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_home()
        except AcondProApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except AcondProApiClientError as exception:
            raise UpdateFailed(exception) from exception
