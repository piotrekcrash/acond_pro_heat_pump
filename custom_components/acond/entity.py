"""AcondEntity class."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.climate import ClimateEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.water_heater import WaterHeaterEntityDescription
from homeassistant.const import CONF_MAC
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .coordinator import AcondDataUpdateCoordinator


class AcondProEntity(CoordinatorEntity[AcondDataUpdateCoordinator]):
    """AcondEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self, coordinator: AcondDataUpdateCoordinator, device_name: str, device_key: str
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_has_entity_name = True
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.data[CONF_MAC],
                    device_key,
                ),
            },
            name=device_name,
            model="Acond Pro",
            manufacturer="Acond",
        )


@dataclass(frozen=True, kw_only=True)
class AcondBaseDescription(EntityDescription):
    """Base for entity derscriptions iwth key generation."""

    device_name: str  # Podajesz np. "Water Heater"

    @property
    def device_key(self) -> str:
        """Generate device_key."""
        return self.device_name.lower().replace(" ", "_")


@dataclass(frozen=True, kw_only=True)
class AcondSensorEntityDescription(SensorEntityDescription, AcondBaseDescription):
    """Hybrid for sensorów."""


@dataclass(frozen=True, kw_only=True)
class AcondBinarySensorEntityDescription(
    BinarySensorEntityDescription, AcondBaseDescription
):
    """Hybrid for binary sensor."""


@dataclass(frozen=True, kw_only=True)
class AcondWaterHeaterEntityDescription(
    WaterHeaterEntityDescription, AcondBaseDescription
):
    """Hybrid for water heater."""


class AcondSwitchEntityDescription(BinarySensorEntityDescription, AcondBaseDescription):
    """Hybrid for a switch."""


@dataclass(frozen=True, kw_only=True)
class AcondSelectEntityDescription(BinarySensorEntityDescription, AcondBaseDescription):
    """Hybrid for select."""


@dataclass(frozen=True, kw_only=True)
class AcondClimateEntityDescription(ClimateEntityDescription, AcondBaseDescription):
    """Hybrid for sensorów."""
