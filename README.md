[Polska wersja instrukcji znajduje się poniżej](#polska-wersja-instrukcji)

# Walutomat Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

The `walutomat-ha` integration allows you to monitor public exchange rates from Walutomat.pl for selected currency pairs, with no authorization required. Additionally, after providing an API key, you can monitor your account balances directly in Home Assistant.

## Features

-   Public exchange rate sensors for selected currency pairs (does not require an API key).
-   Creates a sensor for each currency in your Walutomat wallet (requires API key).
-   Displays the available balance as the sensor's state.
-   Shows total and reserved balances as additional attributes.
-   Configurable polling intervals for both balances and exchange rates.

## Prerequisites

-   An account on [Walutomat.pl](https://www.walutomat.pl/) is only needed if you want to monitor your account balances.
-   An API Key, generated in the [Walutomat user panel](https://user.walutomat.pl/#/api), is required for balance monitoring.

## Installation via HACS (Home Assistant Community Store)

This is the recommended way to install the integration.

1.  **Go to HACS.**
    -   Navigate to **HACS** > **Integrations**.
2.  **Install the Integration:**
    -   Search for "Walutomat" and install it.
3.  **Restart Home Assistant:**
    -   After installation, you must restart Home Assistant for the integration to be loaded.

## Configuration

Once installed, you can configure the integration through the Home Assistant UI.

1.  Navigate to **Settings** > **Devices & Services**.
2.  Click the **"+ ADD INTEGRATION"** button in the bottom right corner.
3.  Search for **"Walutomat"** and click on it.
4.  A configuration dialog will appear.
    -   **For Public Exchange Rates:** Leave the API Key field empty.
    -   **For Account Balances:** Enter your **API Key**.
    -   You can add the integration multiple times if you have more than one account, but only once for public rates.
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

***

## Polska wersja instrukcji

### Integracja Walutomat dla Home Assistant

Integracja `walutomat-ha` pozwala na monitorowanie publicznych kursów wymiany walut z Walutomat.pl dla wybranych par walutowych, bez potrzeby autoryzacji. Dodatkowo, po podaniu klucza API, można monitorować salda na koncie bezpośrednio w Home Assistant.

### Funkcjonalności

-   Publiczne sensory kursów walut dla wybranych par walutowych (nie wymaga klucza API).
-   Tworzy sensor dla każdej waluty w Twoim portfelu Walutomat (wymaga klucza API).
-   Wyświetla dostępne saldo jako stan sensora.
-   Pokazuje całkowite i zarezerwowane salda jako dodatkowe atrybuty.
-   Konfigurowalne interwały odpytywania dla sald i kursów wymiany.

### Wymagania wstępne

-   Konto na [Walutomat.pl](https://www.walutomat.pl/) jest potrzebne tylko jeśli chcesz monitorować salda na swoim koncie.
-   Klucz API, wygenerowany w [panelu użytkownika Walutomat](https://user.walutomat.pl/#/api), jest wymagany do monitorowania salda.

### Instalacja przez HACS (Home Assistant Community Store)

To jest rekomendowany sposób instalacji integracji.

1.  **Przejdź do HACS.**
    -   Przejdź do **HACS** > **Integracje**.
2.  **Zainstaluj integrację:**
    -   Wyszukaj "Walutomat" i zainstaluj.
3.  **Uruchom ponownie Home Assistant:**
    -   Po instalacji musisz ponownie uruchomić Home Assistant, aby integracja została załadowana.

### Konfiguracja

Po zainstalowaniu możesz skonfigurować integrację poprzez interfejs użytkownika Home Assistant.

1.  Przejdź do **Ustawienia** > **Urządzenia i usługi**.
2.  Kliknij przycisk **"+ DODAJ INTEGRACJĘ"** w prawym dolnym rogu.
3.  Wyszukaj **"Walutomat"** i kliknij.
4.  Pojawi się okno konfiguracji.
    -   **Dla publicznych kursów wymiany:** Pozostaw pole Klucz API puste.
    -   **Dla sald konta:** Wprowadź swój **Klucz API**.
    -   Możesz dodać integrację wielokrotnie, jeśli masz więcej niż jedno konto, ale tylko raz dla kursów publicznych.
5.  Kliknij **"Zatwierdź"**.

Jeśli podasz klucz API, integracja utworzy sensory dla sald Twojego konta. Niezależnie od tego, ustawi urządzenie dla publicznych kursów wymiany.

### Konfiguracja sensorów kursów i sald

Możesz dostosować zachowanie integracji po początkowej konfiguracji.

1.  Przejdź do **Ustawienia** > **Urządzenia i usługi**.
2.  Znajdź kartę integracji Walutomat i kliknij **"Konfiguruj"**.
3.  Pojawi się nowe okno, w którym możesz:
    -   **Wybierz pary walutowe:** Wybierz, które sensory kursów walut utworzyć (np. `EUR_PLN`, `USD_PLN`). Integracja utworzy osobne sensory "kupna" i "sprzedaży" dla każdej wybranej pary.
    -   **Ustaw interwał aktualizacji kursów:** Określ, jak często (w minutach) kursy walut powinny być aktualizowane. Domyślna wartość to 1 minuta.
    -   **Ustaw interwał aktualizacji sald:** Jeśli skonfigurowałeś klucz API, możesz określić, jak często Twoje salda konta powinny być odpytywane. Domyślna wartość to 5 minut.
4.  Kliknij **"Zatwierdź"**, aby zastosować zmiany. Integracja przeładuje się automatycznie.
