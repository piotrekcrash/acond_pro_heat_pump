"""Water Heater platform for acond."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityDescription,
    WaterHeaterEntityFeature,
)
from homeassistant.components.water_heater.const import (
    STATE_ECO,
    STATE_ELECTRIC,
    STATE_HEAT_PUMP,
    STATE_PERFORMANCE,
)
from homeassistant.const import ATTR_TEMPERATURE, CONF_MAC, UnitOfTemperature

from . import const
from .entity import AcondProEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AcondDataUpdateCoordinator
    from .data import AcondProConfigEntry

# Mapowanie trybów pracy Water Heater na wartości API Acond
OPERATION_MODE_MAP: dict[str, str] = {
    STATE_ECO: "1",  # Tryb Ekonomiczny (np. tylko Pompa Ciepła)
    STATE_ELECTRIC: "2",  # Tryb Elektryczny (tylko grzałka)
    STATE_PERFORMANCE: "3",  # Tryb Wysokiej Wydajności (np. Pompa + Grzałka)
    STATE_HEAT_PUMP: "4",  # Tryb Pompa Ciepła (jeśli inny niż ECO)
}

# Mapa odwrotna do odczytu stanu
REVERSE_OPERATION_MODE_MAP: dict[str, str] = {
    v: k for k, v in OPERATION_MODE_MAP.items()
}


ENTITY_DESCRIPTIONS = (
    WaterHeaterEntityDescription(
        key="Water Heater",  # Użyj unikalnego klucza dla bojlera
        name="Acond Pro Water Heater",
        icon="mdi:water-boiler",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AcondProConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the water_heater platform."""
    async_add_entities(
        AcondProWaterHeater(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AcondProWaterHeater(AcondProEntity, WaterHeaterEntity):
    """acond water heater class (Boiler)."""

    def __init__(
        self,
        coordinator: AcondDataUpdateCoordinator,
        entity_description: WaterHeaterEntityDescription,
    ) -> None:
        """Initialize the water heater class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

        # Generowanie Unikalnego ID (MAC + klucz encji)
        mac = coordinator.config_entry.data.get(CONF_MAC, "unknown_mac")
        self._attr_unique_id = f"{mac}_{entity_description.key}"

        # Definicja wspieranych funkcji
        self._attr_supported_features = (
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.OPERATION_MODE
        )

        # Definicja dostępnych trybów pracy
        self._attr_operation_list = list(OPERATION_MODE_MAP.keys())
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS

        # Wartości min/max dla C.W.U.
        self._attr_min_temp = 10
        self._attr_max_temp = 50
        self._attr_target_temperature_step = 0.1

    @property
    def current_temperature(self) -> float | None:
        """Return the current water temperature (wartość odczytana z bojlera)."""
        # Przykład: Zmień klucz na właściwy dla odczytu temperatury wody!
        temp_data = self.coordinator.data.get(const.BOILER_TEMPERATURE_CURRENT)
        if temp_data is not None:
            try:
                return float(temp_data)
            except ValueError:
                return None
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach (temperatura zadana)."""
        # Przykład: Zmień klucz na właściwy dla zadanej temperatury wody!
        target_data = self.coordinator.data.get(const.BOILER_TEMPERATURE_TERGET)
        if target_data is not None:
            try:
                return float(target_data)
            except ValueError:
                return None
        return None

    @property
    def current_operation(self) -> str | None:
        """Return current operation mode (aktualny tryb pracy bojlera)."""
        # Przykład: Zmień klucz na właściwy dla trybu pracy bojlera!
        mode_data = self.coordinator.data.get("__T_CURRENT_BOILER_MODE_INT_")
        if mode_data is not None:
            # Tłumaczenie wartości API (np. "1") na stałą HA (np. "eco")
            return REVERSE_OPERATION_MODE_MAP.get(str(mode_data))
        return None

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature (ustawienie nowej temperatury zadanej wody)."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            # Przykład: Zmień klucz na właściwy dla zapisu temperatury zadanej wody!
            await self.coordinator.config_entry.runtime_data.client.async_set_value(
                const.BOILER_TEMPERATURE_TERGET_SET, str(temperature)
            )
            await self.coordinator.async_request_refresh()

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        """Set new operation mode (ustawienie trybu pracy bojlera)."""
        # Tłumaczenie stałej HA (np. "eco") na wartość API (np. "1")
        api_value = OPERATION_MODE_MAP.get(operation_mode)

        if api_value is not None:
            # Przykład: Zmień klucz na właściwy dla zapisu trybu pracy bojlera!
            await self.coordinator.config_entry.runtime_data.client.async_set_value(
                "__T_SET_BOILER_MODE_INT_", api_value
            )
            await self.coordinator.async_request_refresh()
