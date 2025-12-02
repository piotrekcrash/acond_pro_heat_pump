"""Climate platform for acond_pro_heat_pump."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.climate import ClimateEntity, ClimateEntityDescription
from homeassistant.components.climate import ClimateEntityFeature
from homeassistant.components.climate.const import HVACMode
from homeassistant.const import UnitOfTemperature
from homeassistant.const import ATTR_TEMPERATURE
# from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS

from .entity import AcondProEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AcondDataUpdateCoordinator
    from .data import AcondProConfigEntry


ENTITY_DESCRIPTIONS = (
    ClimateEntityDescription(
        key="acond_pro_climate",
        name="Acond Pro Heat Pump",
        icon="mdi:heat-pump",
    ),
    ClimateEntityDescription(
        key="acond_pro_climate_2",
        name="Acond Pro Heat Pump",
        icon="mdi:heat-pump",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AcondProConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the climate platform."""
    async_add_entities(
        AcondProClimate(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AcondProClimate(AcondProEntity, ClimateEntity):
    """acond_pro_heat_pump Climate class."""

    def __init__(
        self,
        coordinator: AcondDataUpdateCoordinator,
        entity_description: ClimateEntityDescription,
    ) -> None:
        """Initialize the climate class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
        self._attr_hvac_modes = [HVACMode.HEAT]
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_min_temp = 7
        self._attr_max_temp = 35

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        return float(self.coordinator.data["__T46AA2571_REAL_.1f"])

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach."""
        return float(self.coordinator.data["__T05D9E707_REAL_.1f"])

    @property
    def hvac_mode(self) -> str:
        """Return hvac operation ie. heat, cool mode."""
        # return self.coordinator.data.get("hvac_mode", HVACMode.OFF)
        return HVACMode.HEAT

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        # if temperature is not None:
        #     await self.coordinator.api.set_temperature(temperature)
        #     await self.coordinator.async_request_refresh()
        #
        await self.coordinator.config_entry.runtime_data.client.async_set_value("__TBEC2C30E_REAL_.1f", temperature)
        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""
        #await self.coordinator.api.set_hvac_mode(hvac_mode)
        # await self.coordinator.async_request_refresh()
        # test
