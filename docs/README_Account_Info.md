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