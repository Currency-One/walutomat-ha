"""Tests for the Walutomat sensors."""
from unittest.mock import patch

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.walutomat.const import DOMAIN, CONF_CURRENCY_PAIRS


@pytest.mark.asyncio
async def test_rate_sensors(hass: HomeAssistant) -> None:
    """Test the rate sensors."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={},
        options={
            CONF_CURRENCY_PAIRS: ["EUR_PLN", "USD_PLN"],
        },
        entry_id="test-rates",
    )

    with patch(
        "walutomat_py.WalutomatClient.get_public_rate",
        side_effect=[
            {"buyRate": 4.5, "sellRate": 4.6},
            {"buyRate": 3.8, "sellRate": 3.9},
        ],
    ):
        config_entry.add_to_hass(hass)
        setup_result = await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        assert setup_result
        assert config_entry.state == ConfigEntryState.LOADED

        eur_buy_sensor = hass.states.get("sensor.walutomat_eur_pln_buy_rate")
        eur_sell_sensor = hass.states.get("sensor.walutomat_eur_pln_sell_rate")
        usd_buy_sensor = hass.states.get("sensor.walutomat_usd_pln_buy_rate")
        usd_sell_sensor = hass.states.get("sensor.walutomat_usd_pln_sell_rate")

        assert eur_buy_sensor is not None
        assert eur_sell_sensor is not None
        assert usd_buy_sensor is not None
        assert usd_sell_sensor is not None

        assert eur_buy_sensor.state == "4.5"
        assert eur_sell_sensor.state == "4.6"
        assert usd_buy_sensor.state == "3.8"
        assert usd_sell_sensor.state == "3.9"

        assert eur_buy_sensor.attributes["unit_of_measurement"] == "PLN"
