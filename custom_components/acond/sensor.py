"""Sensor platform for acond."""

from __future__ import annotations

from typing import TYPE_CHECKING

import const
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import AcondProEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AcondDataUpdateCoordinator
    from .data import AcondProConfigEntry


ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="__TA725D6FD_REAL_.0f",
        name="Electric Energy",
        icon="mdi:lightning-bolt",
        native_unit_of_measurement="kWh",
        unit_of_measurement="kWh",
        state_class="total_increasing",
        device_class="energy",
    ),
    SensorEntityDescription(
        key="__T6BEBB72C_REAL_.0f",
        name="Thermal Energy",
        icon="mdi:water-boiler",
        native_unit_of_measurement="GJ",
        unit_of_measurement="GJ",
        state_class="total_increasing",
        device_class="energy",
    ),
    SensorEntityDescription(
        key="__TD50B2FF2_REAL_.2f",
        name="Pump Efficiency",
        icon="mdi:lightning-bolt",
        native_unit_of_measurement="kW",
        unit_of_measurement="kW",
    ),
    SensorEntityDescription(
        key=const.OUTDOR_TEMPERATURE,
        name="Outdoor Temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement="°C",
        unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="__TDE3BFC02_REAL_.1f",
        name="Outdoor Temperature Average",
        icon="mdi:thermometer",
        native_unit_of_measurement="°C",
        unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="__T50A32455_REAL_.1f",
        name="Heat Pump Water Inbound Temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement="°C",
        unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="__T9E13248E_REAL_.1f",
        name="Heat Pump Water Outbound Temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement="°C",
        unit_of_measurement="°C",
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
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AcondProSensor(AcondProEntity, SensorEntity):
    """acond Sensor class."""

    def __init__(
        self,
        coordinator: AcondDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data[self.entity_description.key]
