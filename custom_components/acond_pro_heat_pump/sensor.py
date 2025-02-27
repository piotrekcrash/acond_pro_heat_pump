"""Sensor platform for acond_pro_heat_pump."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import AcondProEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AcondDataUpdateCoordinator
    from .data import AcondProConfigEntry


ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="acond_pro_heat_pump1",
        name="Integration Sensor 1",
        icon="mdi:format-quote-close",
    ),
    SensorEntityDescription(
        key="acond_pro_heat_pump2",
        name="Integration Sensor 2",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AcondProConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        AcondProSensor(
            entity_description.key,
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AcondProSensor(AcondProEntity, SensorEntity):
    """acond_pro_heat_pump Sensor class."""

    def __init__(
        self,
        coordinator: AcondDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
        name: str
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self.name = name

    @property
    def native_value(self, name) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get(name)
