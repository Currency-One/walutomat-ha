"""The Walutomat integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant
from walutomat_py import WalutomatClient

from .const import DOMAIN
from .coordinator import WalutomatBalancesCoordinator, WalutomatRatesCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Walutomat from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create and store the rates coordinator if it doesn't exist (singleton)
    if "rates_coordinator" not in hass.data[DOMAIN]:
        rates_coordinator = WalutomatRatesCoordinator(hass, entry)
        await rates_coordinator.async_config_entry_first_refresh()
        hass.data[DOMAIN]["rates_coordinator"] = rates_coordinator

    # Create a balances coordinator only if an API key is provided
    if entry.data.get(CONF_API_KEY):
        client = WalutomatClient(
            api_key=entry.data[CONF_API_KEY], sandbox=entry.data.get("sandbox", False)
        )
        balances_coordinator = WalutomatBalancesCoordinator(hass, entry, client)
        await balances_coordinator.async_config_entry_first_refresh()
        # Store the balances coordinator per config entry
        hass.data[DOMAIN][entry.entry_id] = {
            "balances_coordinator": balances_coordinator
        }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Clean up the entry-specific data
        if entry.entry_id in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(entry.entry_id)

        # Optional: clean up the global coordinator if no other entries are using it
        # For simplicity, we'll leave it for now as it's lightweight.
        # If this were a heavier process, we'd implement reference counting.

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    _LOGGER.debug("Reloading integration to apply updated options")
    await hass.config_entries.async_reload(entry.entry_id)

