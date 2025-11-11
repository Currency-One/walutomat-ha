"""Test the Walutomat integration."""
from unittest.mock import patch

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.walutomat.const import DOMAIN


@pytest.mark.asyncio
async def test_setup_unload_and_reload_entry(hass: HomeAssistant) -> None:
    """Test setting up and unloading the integration."""
    # Create a mock config entry
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_API_KEY: "test-api-key"},
        entry_id="test",
    )

    # Mock the API call to return some sample data
    mock_balances = [
        {
            "currency": "EUR",
            "balanceAvailable": "90.50",
            "balanceTotal": "100.50",
            "balanceReserved": "10.00",
        },
        {
            "currency": "PLN",
            "balanceAvailable": "500.00",
            "balanceTotal": "500.00",
            "balanceReserved": "0.00",
        },
    ]
    with patch(
        "walutomat_py.WalutomatClient.get_balances", return_value=mock_balances
    ), patch(
        "walutomat_py.WalutomatClient.get_public_rate",
        return_value={"buyRate": 4.5, "sellRate": 4.6},
    ):
        # Add the config entry to Home Assistant
        config_entry.add_to_hass(hass)
        setup_result = await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        # --- 1. Test Setup ---
        assert setup_result
        assert config_entry.state == ConfigEntryState.LOADED

        # Check that sensors were created
        eur_sensor = hass.states.get("sensor.walutomat_balance_eur")
        pln_sensor = hass.states.get("sensor.walutomat_balance_pln")

        assert eur_sensor is not None
        assert pln_sensor is not None

        # Check sensor states and attributes
        assert eur_sensor.state == "90.50"
        assert pln_sensor.state == "500.00"

        # --- 2. Test Unload ---
        unload_result = await hass.config_entries.async_unload(config_entry.entry_id)
        await hass.async_block_till_done()

        assert unload_result
        assert config_entry.state == ConfigEntryState.NOT_LOADED
        assert hass.states.get("sensor.walutomat_balance_eur").state == "unavailable"
        assert hass.states.get("sensor.walutomat_balance_pln").state == "unavailable"
