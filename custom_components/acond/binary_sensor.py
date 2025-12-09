"""Binary sensor platform for acond."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import AcondProEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AcondDataUpdateCoordinator
    from .data import AcondProConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="__T2BA2EA36_BOOL_i",
        name="Main Pump",
        device_class=BinarySensorDeviceClass.RUNNING,
        icon="mdi:pump",
    ),
    BinarySensorEntityDescription(
        key="__T6F64FA70_BOOL_i",
        name="Circulation Pump",
        device_class=BinarySensorDeviceClass.RUNNING,
        icon="mdi:pump",
    ),
    BinarySensorEntityDescription(
        key="__TE1D81C79_BOOL_i",
        name="Defrost",
        icon="mdi:snowflake-melt",
    ),
    BinarySensorEntityDescription(
        key="__TD3998BF7_BOOL_i",
        name="Bivalence 1",
        icon="mdi:heat-wave",
    ),
    BinarySensorEntityDescription(
        key="__T56A70EC9_BOOL_i",
        name="Bivalence 1",
        icon="mdi:heat-wave",
    ),
    BinarySensorEntityDescription(
        key="__T61E4AC91_BOOL_i",
        name="Compressor",
        icon="mdi:heat-pump",
    ),
    BinarySensorEntityDescription(
        key="__T9FF6A530_BOOL_i",
        name="Fan",
        icon="mdi:fan",
    ), 
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AcondProConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        AcondProBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AcondProBinarySensor(AcondProEntity, BinarySensorEntity):
    """acond binary_sensor class."""

    def __init__(
        self,
        coordinator: AcondDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
    #    return self.coordinator.data.get("title", "") == "foo"
        return self.coordinator.data[self.entity_description.key] == "1"
