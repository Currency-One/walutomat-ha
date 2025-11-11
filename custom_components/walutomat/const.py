"""Constants for the Walutomat integration."""

DOMAIN = "walutomat"
PLATFORMS = ["sensor"]

# Configuration keys
CONF_API_KEY = "api_key"
CONF_BALANCES_UPDATE_INTERVAL = "balances_update_interval"
CONF_RATES_UPDATE_INTERVAL = "rates_update_interval"

# Defaults
DEFAULT_BALANCES_UPDATE_INTERVAL = 5  # in minutes
DEFAULT_RATES_UPDATE_INTERVAL = 1  # in minutes

# Currency Pairs
CONF_CURRENCY_PAIRS = "currency_pairs"
DEFAULT_CURRENCY_PAIRS = ["EUR_PLN", "USD_PLN", "CHF_PLN", "GBP_PLN"]
AVAILABLE_CURRENCY_PAIRS = [
    "EUR_GBP", "EUR_USD", "EUR_CHF", "EUR_PLN", "GBP_USD", "GBP_CHF", "GBP_PLN",
    "USD_CHF", "USD_PLN", "CHF_PLN", "EUR_SEK", "EUR_NOK", "EUR_DKK", "EUR_CZK",
    "CZK_PLN", "DKK_PLN", "NOK_PLN", "SEK_PLN", "AUD_PLN", "BGN_PLN", "CAD_PLN",
    "CNY_PLN", "HKD_PLN", "HUF_PLN", "ILS_PLN", "JPY_PLN", "MXN_PLN", "NZD_PLN",
    "RON_PLN", "SGD_PLN", "TRY_PLN", "ZAR_PLN", "EUR_AUD", "EUR_BGN", "EUR_CAD",
    "EUR_CNY", "EUR_HKD", "EUR_HUF", "EUR_ILS", "EUR_JPY", "EUR_MXN", "EUR_NZD",
    "EUR_RON", "EUR_SGD", "EUR_TRY", "EUR_ZAR"
]
