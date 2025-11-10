"""Sensor platform for Walutomat."""
from __future__ import annotations

from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WalutomatDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Walutomat sensors."""
    coordinator: WalutomatDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create sensors for each currency found
    entities = [
        WalutomatBalanceSensor(coordinator, currency_data)
        for currency_data in coordinator.data
    ]
    async_add_entities(entities)


class WalutomatBalanceSensor(CoordinatorEntity[WalutomatDataUpdateCoordinator], SensorEntity):
    """Representation of a Walutomat Balance Sensor."""

    def __init__(
        self,
        coordinator: WalutomatDataUpdateCoordinator,
        currency_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._currency = currency_data.get("currency", "UNKNOWN")
        self._attr_name = f"Walutomat Balance {self._currency}"
        self._attr_unique_id = f"walutomat_{self._currency.lower()}_balance"
        self._attr_icon = "mdi:currency-eur"  # Generic currency icon
        self._attr_native_unit_of_measurement = self._currency

        self._update_attributes(currency_data)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Find the correct currency data from the coordinator's list
        for currency_data in self.coordinator.data:
            if currency_data.get("currency") == self._currency:
                self._update_attributes(currency_data)
                self.async_write_ha_state()
                break

    def _update_attributes(self, currency_data: Dict[str, Any]) -> None:
        """Update sensor attributes from new data."""
        self._attr_native_value = currency_data.get("balanceAvailable")
        self._attr_extra_state_attributes = {
            "total_balance": currency_data.get("balanceTotal"),
            "reserved_balance": currency_data.get("balanceReserved"),
        }
