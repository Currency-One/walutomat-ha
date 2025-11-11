"""DataUpdateCoordinators for the Walutomat integration."""
import asyncio
import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from walutomat_py import WalutomatAPIError, WalutomatClient

from .const import (
    CONF_BALANCES_UPDATE_INTERVAL,
    CONF_CURRENCY_PAIRS,
    CONF_RATES_UPDATE_INTERVAL,
    DEFAULT_BALANCES_UPDATE_INTERVAL,
    DEFAULT_CURRENCY_PAIRS,
    DEFAULT_RATES_UPDATE_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class WalutomatBalancesCoordinator(DataUpdateCoordinator[List[Dict[str, Any]]]):
    """Class to manage fetching Walutomat balances data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client: WalutomatClient):
        """Initialize."""
        self.client = client
        update_interval = timedelta(
            minutes=entry.options.get(
                CONF_BALANCES_UPDATE_INTERVAL, DEFAULT_BALANCES_UPDATE_INTERVAL
            )
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_balances",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> List[Dict[str, Any]]:
        """Fetch data from API endpoint."""
        try:
            balances = await self.hass.async_add_executor_job(self.client.get_balances)
            _LOGGER.debug("Fetched balances data: %s", balances)
            return balances
        except WalutomatAPIError as err:
            raise UpdateFailed(f"Error communicating with API for balances: {err}") from err
        except Exception as err:
            _LOGGER.error("Unexpected error fetching walutomat_balances data", exc_info=True)
            raise UpdateFailed(f"Unexpected error fetching walutomat_balances data: {err}") from err


class WalutomatRatesCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Class to manage fetching Walutomat public rates data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize."""
        self.entry = entry
        update_interval = timedelta(
            minutes=entry.options.get(
                CONF_RATES_UPDATE_INTERVAL, DEFAULT_RATES_UPDATE_INTERVAL
            )
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_rates",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from public API endpoint."""
        selected_pairs = self.entry.options.get(
            CONF_CURRENCY_PAIRS, DEFAULT_CURRENCY_PAIRS
        )
        if not selected_pairs:
            return {}

        async def _fetch_pair(pair: str):
            try:
                return await self.hass.async_add_executor_job(
                    WalutomatClient.get_public_rate, pair
                )
            except WalutomatAPIError as err:
                _LOGGER.warning("Error fetching rate for %s: %s", pair, err)
                return None

        results = await asyncio.gather(
            *[_fetch_pair(pair) for pair in selected_pairs]
        )

        rates = {
            pair: rate
            for pair, rate in zip(selected_pairs, results)
            if rate is not None
        }
        _LOGGER.debug("Fetched rates data: %s", rates)
        return rates
