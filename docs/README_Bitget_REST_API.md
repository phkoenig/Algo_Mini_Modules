# Bitget REST API Client

Dieses Modul bietet eine einfache Schnittstelle zur Verbindung mit der Bitget REST API und zum Empfangen von Marktdaten.

## Funktionen

Der Bitget REST API Client bietet folgende Hauptfunktionen:

- Abrufen von Ticker-Daten für ein bestimmtes Symbol
- Abrufen von Kerzendaten (K-Lines) für ein bestimmtes Symbol
- Abrufen des Orderbuchs für ein bestimmtes Symbol
- Abrufen der letzten Trades für ein bestimmtes Symbol
- Verarbeitung der Daten in Pandas DataFrames für einfache Analyse

## Installation

Stelle sicher, dass alle erforderlichen Abhängigkeiten installiert sind:

```bash
pip install -r requirements.txt
```

## Verwendung

### Als Modul importieren

```python
from modules.Websocket_Raw_Data.bitget_rest_client import BitgetRestClient, is_valid_symbol

# Initialisiere den Client
client = BitgetRestClient(verbose=True)

# Überprüfe, ob ein Symbol gültig ist
if is_valid_symbol("BTCUSDT_UMCBL"):
    # Hole Ticker-Daten
    ticker_data = client.get_ticker("BTCUSDT_UMCBL")
    
    # Verarbeite Ticker-Daten
    ticker_df = client.process_ticker_data(ticker_data)
    print(ticker_df)
```

### Als Standalone-Skript

Das Modul kann auch direkt als Skript ausgeführt werden:

```bash
python -m modules.Websocket_Raw_Data.bitget_rest_client --symbol=BTCUSDT_UMCBL --verbose
```

Wenn kein Symbol angegeben wird, fordert das Skript den Benutzer zur Eingabe eines gültigen Symbols auf.

## Beispielskript

Ein Beispielskript, das die Verwendung des Clients demonstriert, ist im Verzeichnis `examples` verfügbar:

```bash
python examples/bitget_rest_example.py --symbol=BTCUSDT_UMCBL --verbose
```

## API-Endpunkte

Der Client unterstützt folgende Bitget API-Endpunkte:

### Ticker

```
GET /api/mix/v1/market/ticker
```

Ruft die aktuellen Ticker-Daten für ein bestimmtes Symbol ab.

### Kerzendaten (K-Lines)

```
GET /api/mix/v1/market/candles
```

Ruft historische Kerzendaten für ein bestimmtes Symbol ab. Unterstützt verschiedene Zeitintervalle wie 1m, 5m, 15m, 30m, 1h, 4h, 12h, 1d, 1w.

### Orderbuch

```
GET /api/mix/v1/market/depth
```

Ruft das aktuelle Orderbuch für ein bestimmtes Symbol ab.

### Trades

```
GET /api/mix/v1/market/fills
```

Ruft die letzten Trades für ein bestimmtes Symbol ab.

## Datenverarbeitung

Der Client bietet Methoden zur Verarbeitung der API-Antworten in Pandas DataFrames:

- `process_ticker_data()`: Verarbeitet Ticker-Daten
- `process_klines_data()`: Verarbeitet Kerzendaten

Diese Methoden erleichtern die Analyse und Visualisierung der Daten.

## Symbolvalidierung

Der Client bietet Funktionen zur Überprüfung der Gültigkeit von Symbolen:

- `is_valid_symbol()`: Überprüft, ob ein Symbol gültig ist
- `get_user_input_symbol()`: Fordert den Benutzer zur Eingabe eines gültigen Symbols auf

Diese Funktionen verwenden das Trading_Pairs Modul, um die Liste der verfügbaren Symbole zu erhalten.

## Fehlerbehandlung

Der Client behandelt Fehler bei API-Anfragen und gibt ein Dictionary mit einem Fehlerschlüssel zurück, wenn ein Fehler auftritt. Dies ermöglicht eine einfache Fehlerbehandlung in der aufrufenden Anwendung.

## Logging

Der Client verwendet das Python-Logging-Modul für Debugging und Fehlerberichte. Die Ausführlichkeit der Logging-Ausgaben kann mit dem `verbose`-Parameter gesteuert werden.

## Authentifizierung

Für öffentliche Endpunkte ist keine Authentifizierung erforderlich. Für private Endpunkte müssen API-Schlüssel, Secret und Passphrase angegeben werden. Diese können als Parameter an den Konstruktor übergeben oder aus Umgebungsvariablen geladen werden.

## Umgebungsvariablen

Der Client kann API-Schlüssel aus einer `.env`-Datei laden. Folgende Umgebungsvariablen werden unterstützt:

- `BITGET_API_KEY`: Dein Bitget API-Schlüssel
- `BITGET_SECRET_KEY`: Dein Bitget API-Secret
- `BITGET_PASSPHRASE`: Dein Bitget API-Passphrase

## Hinweise

- Die Bitget API hat Ratenlimits. Übermäßige Anfragen können zu temporären Sperren führen.
- Für Produktionsumgebungen sollte eine angemessene Fehlerbehandlung und Wiederholungslogik implementiert werden.
- Die API-Dokumentation von Bitget kann sich ändern. Überprüfe die offizielle Dokumentation für die neuesten Informationen.

## Ressourcen

- [Offizielle Bitget API-Dokumentation](https://bitgetlimited.github.io/apidoc/en/mix/#introduction)
- [Bitget API GitHub Repository](https://github.com/BitgetLimited/v3-bitget-api-sdk) 