"""DataUpdateCoordinator for the Walutomat integration."""
import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from walutomat_py import WalutomatAPIError, WalutomatClient

from .const import CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class WalutomatDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Walutomat data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client: WalutomatClient):
        """Initialize."""
        self.client = client
        update_interval = timedelta(
            minutes=entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> List[Dict[str, Any]]:
        """Fetch data from API endpoint."""
        try:
            # WalutomatClient.get_balances is a blocking call, run it in an executor
            return await self.hass.async_add_executor_job(self.client.get_balances)
        except WalutomatAPIError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
