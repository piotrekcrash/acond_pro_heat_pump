"""Select platform for acond."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.const import Platform

from .entity import AcondProEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AcondDataUpdateCoordinator
    from .data import AcondProConfigEntry

# Definicja dostępnych opcji i identyfikatorów zmiennych
# W tym przykładzie, 'key' to unikalny identyfikator parametru z API Acond,
# a 'options' to mapa 'wyświetlana_nazwa': 'wartość_do_wysłania_do_API'.
SELECT_ENTITY_DESCRIPTIONS = (
    SelectEntityDescription(
        key="__T47138CF2_INT_.1f",  # Przykładowy klucz zmiennej API Acond
        name="Acond Operating Mode",
        icon="mdi:thermostat",
    ),
)

# Mapa opcji dla danego klucza zmiennej
# Wartości kluczy muszą odpowiadać kluczom w SELECT_ENTITY_DESCRIPTIONS
MODE_OPTIONS: dict[str, dict[str, str]] = {
    "__T47138CF2_INT_.1f": {
        "Auto Mode": "0",  # "Auto Mode" to nazwa widoczna w HA, "0" to wartość do API
        "Heating Only": "1",
        "Cooling Only": "2",
        "Off": "3",
    }
}


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AcondProConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    async_add_entities(
        AcondProSelect(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in SELECT_ENTITY_DESCRIPTIONS
    )


class AcondProSelect(AcondProEntity, SelectEntity):
    """acond select class."""

    def __init__(
        self,
        coordinator: AcondDataUpdateCoordinator,
        entity_description: SelectEntityDescription,
    ) -> None:
        """Initialize the select class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        # POPRAWKA UNIKALNOŚCI: Łączymy MAC z kluczem encji
        # Gwarantuje unikalność w przypadku wielu urządzeń Acond
        mac = coordinator.config_entry.data.get("mac", "unknown_mac")
        self._attr_unique_id = f"{mac}_{entity_description.key}"
        # Ustawienie dostępnych opcji
        self._attr_options = list(MODE_OPTIONS[entity_description.key].keys())


    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        # 1. Pobierz aktualną surową wartość z koordynatora
        api_key = self.entity_description.key
        current_api_value = self.coordinator.data.get(api_key)

        if current_api_value is None:
            return None

        # 2. Odwróć słownik mapowania opcji
        # (wartość API -> nazwa wyświetlana)
        options_map = MODE_OPTIONS[api_key]
        reversed_options_map = {v: k for k, v in options_map.items()}

        # 3. Zwróć wyświetlaną nazwę
        # Home Assistant oczekuje jednej z wartości z self._attr_options
        return reversed_options_map.get(current_api_value)


    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        api_key = self.entity_description.key

        # 1. Pobierz wartość API na podstawie wybranej opcji (nazwy)
        value_to_send = MODE_OPTIONS[api_key].get(option)

        if value_to_send is None:
            self.coordinator.hass.async_log_warn(
                Platform.SELECT, 
                f"Attempted to select unknown option: {option} for {self.entity_description.name}"
            )
            return

        # 2. Wyślij wartość do API
        await self.coordinator.config_entry.runtime_data.client.async_set_value(
            api_key, 
            value_to_send
        )
        # 3. Odśwież dane
        await self.coordinator.async_request_refresh()
