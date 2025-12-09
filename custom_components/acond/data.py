"""Custom types for acond."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import AcondProApiClient
    from .coordinator import AcondDataUpdateCoordinator


type AcondProConfigEntry = ConfigEntry[AcondProData]


@dataclass
class AcondProData:
    """Data for the Acond integration."""

    client: AcondProApiClient
    coordinator: AcondDataUpdateCoordinator
    integration: Integration
