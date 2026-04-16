"""AcondEntity class."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
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
        self, coordinator: AcondDataUpdateCoordinator, device_name: str
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_has_entity_name = True
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.data[CONF_MAC],
                    device_name,
                ),
            },
            name=device_name,
            model="Acond Pro",
            manufacturer="Acond",
        )


@dataclass(frozen=True, kw_only=True)
class AcondBaseDescription(EntityDescription):
    """Baza z automatycznym generowaniem klucza urządzenia."""

    device_name: str  # Podajesz np. "Water Heater"

    @property
    def device_key(self) -> str:
        """Generuje 'water_heater' z 'Water Heater'."""
        return self.device_name.lower().replace(" ", "_")


@dataclass(frozen=True, kw_only=True)
class AcondSensorDescription(SensorEntityDescription, AcondBaseDescription):
    """Hybryda dla zwykłych sensorów."""


@dataclass(frozen=True, kw_only=True)
class AcondBinarySensorDescription(BinarySensorEntityDescription, AcondBaseDescription):
    """Hybryda dla binarnych sensorów."""


@dataclass(frozen=True, kw_only=True)
class AcondWaterHeaterEntityDescription(
    WaterHeaterEntityDescription, AcondBaseDescription
):
    """Hybryda dla water heater."""
