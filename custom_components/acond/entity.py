"""AcondEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .coordinator import AcondDataUpdateCoordinator


class AcondProEntity(CoordinatorEntity[AcondDataUpdateCoordinator]):
    """AcondEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: AcondDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        entry = coordinator.config_entry
        self._attr_unique_id = entry.entry_id
        self._attr_device_info = DeviceInfo(
        identifiers={
            (entry.domain, entry.entry_id),
        },
        default_name=entry.title or "Acond device",
        default_model="Acond Pro",
        default_manufacturer="Acond",
    )
