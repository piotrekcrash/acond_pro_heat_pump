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
        key="__TA725D6FD_REAL_.0f",
        name="Acond Electric Enery",
        icon="mdi:format-quote-close",
        native_unit_of_measurement="kWh",
        unit_of_measurement="kWh",
        state_class="total_increasing",
        device_class="energy",
    ),
    SensorEntityDescription(
        key="__T6BEBB72C_REAL_.0f",
        name="Acond Thermal Enery",
        icon="mdi:format-quote-close",
        native_unit_of_measurement="GJ",
        unit_of_measurement="GJ",
        state_class="total_increasing",
        device_class="energy",
    ),
    SensorEntityDescription(
        key="__TD50B2FF2_REAL_.2f",
        name="Wydajnosc PC",
        icon="mdi:format-quote-close",
        native_unit_of_measurement="kW",
        unit_of_measurement="kW",
    ),
    SensorEntityDescription(
        key="__T61E4AC91_BOOL_i",
        name="Sprezarka",
        icon="mdi:format-quote-close",
    ),
    SensorEntityDescription(
        key="__T9FF6A530_BOOL_i",
        name="Wentylator",
        icon="mdi:format-quote-close",
    ),
    # SensorEntityDescription(
    #    key="__T2BA2EA36_BOOL_i",
    #    name="Pompa glowna",
    #    icon="mdi:format-quote-close",
    #),
    SensorEntityDescription(
        key="__TD3998BF7_BOOL_i",
        name="Biwalencja",
        icon="mdi:format-quote-close",
    ),
    SensorEntityDescription(
        key="__T56A70EC9_BOOL_i",
        name="Biwalencja 2",
        icon="mdi:format-quote-close",
    ),
    #SensorEntityDescription(
    #    key="__T6F64FA70_BOOL_i",
    #    name="Pompa obiegowa",
    #    icon="mdi:format-quote-close",
    #),
    SensorEntityDescription(
        key="__TE1D81C79_BOOL_i",
        name="Defrost",
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
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data[self.entity_description.key]
