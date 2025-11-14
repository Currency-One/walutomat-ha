# Walutomat Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

The `walutomat-ha` integration allows you to monitor your Walutomat.pl account balances directly in Home Assistant.

## Features

-   Creates a sensor for each currency in your Walutomat wallet (requires API key).
-   Displays the available balance as the sensor's state.
-   Shows total and reserved balances as additional attributes.
-   Public exchange rate sensors for selected currency pairs (does not require an API key).
-   Configurable polling intervals for both balances and exchange rates.

## Prerequisites

-   An account on [Walutomat.pl](https://www.walutomat.pl/) is only needed if you want to monitor your account balances.
-   An API Key, generated in the [Walutomat user panel](https://user.walutomat.pl/#/api), is required for balance monitoring.

## Installation via HACS (Home Assistant Community Store)

This is the recommended way to install the integration.

1.  **Add Custom Repository to HACS:**
    -   Go to your Home Assistant instance.
    -   Navigate to **HACS** > **Integrations**.
    -   Click the three dots (⋮) in the top right corner and select **"Custom repositories"**.
    -   In the "Repository" field, paste the URL of this GitHub repository:
        ```
        https://github.com/Currency-One/walutomat-ha
        ```
    -   In the "Category" dropdown, select **"Integration"**.
    -   Click **"Add"**.

2.  **Install the Integration:**
    -   The "Walutomat" integration should now appear in your HACS integrations list.
    -   Click on it and then click **"Download"**.
    -   Follow the instructions to download the integration.

3.  **Restart Home Assistant:**
    -   After installation, you must restart Home Assistant for the integration to be loaded.

## Configuration

Once installed, you can configure the integration through the Home Assistant UI.

1.  Navigate to **Settings** > **Devices & Services**.
2.  Click the **"+ ADD INTEGRATION"** button in the bottom right corner.
3.  Search for **"Walutomat"** and click on it.
4.  A configuration dialog will appear.
    -   **For Account Balances:** Enter your **API Key**.
    -   **For Public Exchange Rates:** Leave the API Key field empty. You can add the integration multiple times if you have more than one account, but only once for public rates.
5.  Click **"Submit"**.

If you provide an API key, the integration will create sensors for your account balances. Independently, it will set up a device for public exchange rates.

## Configuring Exchange Rate & Balance Sensors

You can customize the integration's behavior after the initial setup.

1.  Navigate to **Settings** > **Devices & Services**.
2.  Find your Walutomat integration card and click **"Configure"**.
3.  A new dialog will appear where you can:
    -   **Select Currency Pairs:** Choose which exchange rate sensors to create (e.g., `EUR_PLN`, `USD_PLN`). The integration will create separate "buy" and "sell" sensors for each selected pair.
    -   **Set Rates Update Interval:** Define how often (in minutes) the exchange rates should be updated. The default is 1 minute.
    -   **Set Balances Update Interval:** If you configured an API key, you can define how often your account balances should be polled. The default is 5 minutes.
4.  Click **"Submit"** to apply the changes. The integration will reload automatically.
