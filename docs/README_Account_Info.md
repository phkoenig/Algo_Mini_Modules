# Account Information Modules

Diese Module dienen dazu, detaillierte Kontoinformationen von verschiedenen Exchanges abzurufen.
Sie sind Teil des Algo-Trading-Systems und ermöglichen es, den aktuellen Kontostand, offene Positionen
und andere wichtige Informationen in Echtzeit zu überwachen.

## Verfügbare Module

### BitGet Account Info
Das BitGet Account Info Modul (`modules/Account_Info/BitGet_Account_Info.py`) bietet folgende Funktionalitäten:

#### Features
- Abrufen von Account-Übersichten für spezifische Trading-Paare
- Anzeigen aller aktiven Positionen
- Abrufen von Account-Transaktionshistorie
- Formatierte Ausgabe wichtiger Kontoinformationen

#### Hauptfunktionen
```python
get_account_overview(symbol: str = "BTCUSDT_UMCBL", marginCoin: str = "USDT") -> Dict
get_positions(productType: str = "umcbl") -> Dict
get_account_bills(symbol: str, marginCoin: str, startTime: Optional[str], endTime: Optional[str], limit: int) -> Dict
display_account_summary()
```

#### Verwendung
```python
from modules.Account_Info.BitGet_Account_Info import BitGetAccountInfo

# Initialisiere den Client
client = BitGetAccountInfo(api_key, secret_key, passphrase)

# Hole Account-Übersicht
account_info = client.get_account_overview("BTCUSDT_UMCBL", "USDT")

# Zeige alle Informationen formatiert an
client.display_account_summary()
```

#### Konfiguration
Das Modul erwartet folgende Umgebungsvariablen:
- `BITGET_API_KEY`: Dein BitGet API Key
- `BITGET_SECRET_KEY`: Dein BitGet Secret Key
- `BITGET_PASSPHRASE`: Dein BitGet API Passphrase

#### API Endpoints
Das Modul nutzt folgende BitGet API Endpoints:
- `/api/mix/v1/account/account`: Account-Übersicht
- `/api/mix/v1/position/allPosition`: Aktive Positionen
- `/api/mix/v1/account/accountBill`: Transaktionshistorie

### KuCoin Account Info
*Coming soon*

## Allgemeine Struktur
Alle Account Info Module folgen dieser grundlegenden Struktur:
1. Authentifizierung über API Keys
2. Standardisierte Methoden zum Abrufen von:
   - Account-Übersicht
   - Positionen
   - Transaktionshistorie
3. Formatierte Ausgabe der Informationen
4. Fehlerbehandlung und Logging

## Best Practices
- API Keys sollten immer als Umgebungsvariablen gespeichert werden
- Sensitive Informationen nie im Code speichern
- Regelmäßiges Logging für Debugging
- Fehlerbehandlung für alle API-Aufrufe
- Rate Limits der Exchanges beachten

## Entwicklung
Neue Account Info Module sollten:
1. Die gleiche grundlegende Struktur befolgen
2. Dieselben Hauptfunktionen implementieren
3. Exchange-spezifische Features hinzufügen
4. Gründliche Dokumentation bereitstellen

## Changelog

### v1.0.0 (2024-03-16)
- Initiale Version des BitGet Account Info Moduls
- Implementierung der Hauptfunktionen
- Dokumentation erstellt 

# Account Info Modules Documentation

This documentation covers the Account Info modules for BitGet and KuCoin exchanges. These modules provide functionality to retrieve account information, positions, and balances from the respective exchanges.

## Available Modules

1. BitGet Account Info (`modules/Account_Info/BitGet_Account_Info.py`)
2. KuCoin Account Info (`modules/Account_Info/KuCoin_Account_Info.py`)

## Main Functions

### BitGet Account Info

```python
# Initialize BitGet client
from modules.Account_Info.BitGet_Account_Info import BitGetAccountInfo
client = BitGetAccountInfo(api_key, secret_key, passphrase)

# Get account overview
account_info = client.get_account_overview()

# Get open positions
positions = client.get_open_positions()

# Display account summary
client.display_account_summary()
```

### KuCoin Account Info

```python
# Initialize KuCoin client
from modules.Account_Info.KuCoin_Account_Info import KuCoinAccountInfo
client = KuCoinAccountInfo(api_key, secret_key, passphrase)

# Get account overview for USDT
account_info = client.get_account_overview("USDT")

# Get position details for a specific symbol
position = client.get_position_details("BTCUSDTM")

# Get all positions
positions = client.get_all_positions()

# Display account summary
client.display_account_summary()
```

## Configuration

Both modules require API credentials to be set in environment variables:

### BitGet
```
BITGET_API_KEY=your_api_key
BITGET_SECRET_KEY=your_secret_key
BITGET_PASSPHRASE=your_passphrase
```

### KuCoin
```
KUCOIN_API_KEY=your_api_key
KUCOIN_SECRET_KEY=your_secret_key
KUCOIN_PASSPHRASE=your_passphrase
```

## API Endpoints

### BitGet Endpoints
- Account Overview: `/api/mix/v1/account/accounts`
- Open Positions: `/api/mix/v1/position/allPosition`
- Account Bills: `/api/mix/v1/account/accountBill`

### KuCoin Endpoints
- Account Overview: `/api/v1/account-overview`
- Position Details: `/api/v1/position`
- All Positions: `/api/v1/positions`

## Best Practices

1. **API Key Management**
   - Store API keys securely in environment variables
   - Never hardcode API keys in the code
   - Use API keys with minimum required permissions

2. **Error Handling**
   - All methods include comprehensive error handling
   - Failed requests return empty dictionaries
   - Errors are logged with detailed information

3. **Rate Limiting**
   - Be aware of exchange rate limits
   - Implement appropriate delays between requests
   - Monitor response headers for rate limit information

## Example Usage

```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize clients
bitget_client = BitGetAccountInfo(
    os.getenv("BITGET_API_KEY"),
    os.getenv("BITGET_SECRET_KEY"),
    os.getenv("BITGET_PASSPHRASE")
)

kucoin_client = KuCoinAccountInfo(
    os.getenv("KUCOIN_API_KEY"),
    os.getenv("KUCOIN_SECRET_KEY"),
    os.getenv("KUCOIN_PASSPHRASE")
)

# Display account summaries
print("=== BitGet Account ===")
bitget_client.display_account_summary()

print("\n=== KuCoin Account ===")
kucoin_client.display_account_summary()
```

## Response Data Structure

### BitGet Account Overview
```python
{
    "marginCoin": "USDT",
    "locked": "0",
    "available": "100.0000",
    "crossMaxAvailable": "100.0000",
    "fixedMaxAvailable": "100.0000",
    "maxTransferOut": "100.0000",
    "equity": "100.0000",
    "usdtEquity": "100.0000"
}
```

### KuCoin Account Overview
```python
{
    "accountEquity": 100.0000,
    "unrealisedPNL": 0,
    "marginBalance": 100.0000,
    "positionMargin": 0,
    "orderMargin": 0,
    "availableBalance": 100.0000,
    "riskRatio": "0"
}
```

## Error Codes

Both modules handle common error codes and provide appropriate error messages:

- 200000: Success
- 400: Bad Request
- 401: Unauthorized
- 429: Too Many Requests
- 500: Internal Server Error

For detailed error handling, refer to the respective exchange API documentation. 