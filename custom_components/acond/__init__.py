"""
Custom integration to integrate acond with Home Assistant.

For more details about this integration, please refer to
https://github.com/piotrekcrash/acond
"""

from __future__ import annotations

import ssl
from datetime import timedelta
from typing import TYPE_CHECKING

import aiohttp
from homeassistant.const import CONF_IP_ADDRESS, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.loader import async_get_loaded_integration

from .api import AcondProApiClient
from .const import DOMAIN, LOGGER
from .coordinator import AcondDataUpdateCoordinator
from .data import AcondProData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import AcondProConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.CLIMATE,
]

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AcondProConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = AcondDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(seconds=30),
    )
    cookie_jar = aiohttp.CookieJar(unsafe=True)
    tcp_conn = aiohttp.TCPConnector(ssl=ssl_context)
    entry.runtime_data = AcondProData(
        client=AcondProApiClient(
            ip_address=entry.data[CONF_IP_ADDRESS],
            username=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD],
            session=aiohttp.ClientSession(cookie_jar=cookie_jar, connector=tcp_conn)
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True

async def async_unload_entry(
    hass: HomeAssistant,
    entry: AcondProConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

async def async_reload_entry(
    hass: HomeAssistant,
    entry: AcondProConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
