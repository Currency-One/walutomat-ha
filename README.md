# Walutomat Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

The `walutomat-ha` integration allows you to monitor your Walutomat.pl account balances directly in Home Assistant.

## Features

-   Creates a sensor for each currency in your Walutomat wallet.
-   Displays the available balance as the sensor's state.
-   Shows total and reserved balances as additional attributes.
-   Configurable polling interval (via integration options).

## Prerequisites

-   You must have an account on [Walutomat.pl](https://www.walutomat.pl/).
-   You need to generate an API Key in the Walutomat user panel: [https://user.walutomat.pl/#/api](https://user.walutomat.pl/#/api).

## Installation via HACS (Home Assistant Community Store)

This is the recommended way to install the integration.

1.  **Add Custom Repository to HACS:**
    -   Go to your Home Assistant instance.
    -   Navigate to **HACS** > **Integrations**.
    -   Click the three dots (⋮) in the top right corner and select **"Custom repositories"**.
    -   In the "Repository" field, paste the URL of this GitHub repository:
        ```
        https://github.com/theundefined/walutomat-ha
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
4.  A configuration dialog will appear. Enter your **API Key** that you generated from the Walutomat user panel.
5.  Click **"Submit"**.

The integration will validate the API key. If successful, it will automatically create sensors for all currencies found in your Walutomat account.

## Changing the Update Interval

By default, the integration polls for new data every 15 minutes. You can change this interval:

1.  Navigate to **Settings** > **Devices & Services**.
2.  Find your Walutomat integration card and click **"Configure"**.
3.  Enter a new update interval in minutes and click **"Submit"**.
4.  The integration will be reloaded with the new polling interval.
