"""Config flow for Walutomat integration."""
import logging
from typing import Any, Dict

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from walutomat_py import WalutomatAPIError, WalutomatClient

from .const import (
    CONF_API_KEY,
    CONF_BALANCES_UPDATE_INTERVAL,
    CONF_RATES_UPDATE_INTERVAL,
    DEFAULT_BALANCES_UPDATE_INTERVAL,
    DEFAULT_RATES_UPDATE_INTERVAL,
    DOMAIN,
    AVAILABLE_CURRENCY_PAIRS,
    DEFAULT_CURRENCY_PAIRS,
    CONF_CURRENCY_PAIRS,
)
from homeassistant.helpers import selector

_LOGGER = logging.getLogger(__name__)


class WalutomatConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Walutomat."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def _validate_api_key(self, api_key: str, sandbox: bool) -> None:
        """Validate the API key by trying to connect to Walutomat."""
        # API key validation is optional if user only wants public rate sensors
        if not api_key:
            return

        client = WalutomatClient(api_key=api_key, sandbox=sandbox)
        # We need to run the blocking get_balances call in an executor
        await self.hass.async_add_executor_job(client.get_balances)

    async def async_step_user(
        self, user_input: Dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            # Use a unique ID based on the API key to prevent duplicate entries
            # If API key is empty, create a single entry for public rates.
            unique_id = user_input.get(CONF_API_KEY) or DOMAIN
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            try:
                await self._validate_api_key(
                    user_input.get(CONF_API_KEY, ""), user_input.get("sandbox", False)
                )
            except WalutomatAPIError as err:
                _LOGGER.error("Failed to connect to Walutomat API: %s", err)
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception during API key validation")
                errors["base"] = "unknown"
            else:
                title = "Walutomat"
                if user_input.get(CONF_API_KEY):
                    title += f" Account (...{user_input[CONF_API_KEY][-4:]})"
                else:
                    title += " Public Rates"

                return self.async_create_entry(
                    title=title,
                    data={
                        CONF_API_KEY: user_input.get(CONF_API_KEY, ""),
                        "sandbox": user_input.get("sandbox", False),
                    },
                )

        # Adjust schema to make API key optional
        user_schema = vol.Schema(
            {
                vol.Optional(CONF_API_KEY, default=""): str,
                vol.Optional("sandbox", default=False): bool,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=user_schema, errors=errors
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for Walutomat."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current or default values
        balances_interval = self.config_entry.options.get(
            CONF_BALANCES_UPDATE_INTERVAL, DEFAULT_BALANCES_UPDATE_INTERVAL
        )
        rates_interval = self.config_entry.options.get(
            CONF_RATES_UPDATE_INTERVAL, DEFAULT_RATES_UPDATE_INTERVAL
        )
        currency_pairs = self.config_entry.options.get(
            CONF_CURRENCY_PAIRS, DEFAULT_CURRENCY_PAIRS
        )

        options_schema = {
            vol.Required(
                CONF_RATES_UPDATE_INTERVAL, default=rates_interval
            ): int,
            vol.Optional(
                CONF_CURRENCY_PAIRS, default=currency_pairs
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=AVAILABLE_CURRENCY_PAIRS,
                    multiple=True,
                    sort=True,
                )
            ),
        }

        # Only show balances interval if API key is configured
        if self.config_entry.data.get(CONF_API_KEY):
            options_schema[
                vol.Required(
                    CONF_BALANCES_UPDATE_INTERVAL, default=balances_interval
                )
            ] = int

        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(options_schema)
        )
