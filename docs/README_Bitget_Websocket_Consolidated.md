# Bitget WebSocket API - Dokumentation und Implementierungsleitfaden

Dieses Dokument bietet eine umfassende Anleitung zur Integration der Bitget WebSocket API für den Empfang von Echtzeit-Marktdaten, speziell für Futures-Märkte.

## Übersicht

Das BitgetWebSocket-Modul ermöglicht die Verbindung mit der Bitget Börse über WebSocket-Schnittstellen, um Echtzeit-Marktdaten zu empfangen.

### Hauptfunktionen:

- Verbindung mit öffentlichen und privaten Kanälen
- Automatische Reconnect-Logik bei Verbindungsabbrüchen
- Callback-System für benutzerdefinierte Datenverarbeitung
- Datenpufferung in einem DataFrame für einfache Analyse

## Vorbereitung der Entwicklungsumgebung

### Installation der benötigten Python-Bibliotheken

```bash
pip install websocket-client pandas python-dotenv
```

Die `websocket-client`-Bibliothek wird für die WebSocket-Verbindung verwendet, während `pandas` für die Datenverarbeitung und `python-dotenv` für die sichere Verwaltung von API-Schlüsseln eingesetzt wird.

### API-Schlüsselgenerierung

1. Bitget-Konto → API-Management
2. **Berechtigungen**: 
   - Lese-/Schreibzugriff für WebSocket
   - IP-Whitelist aktivieren für zusätzliche Sicherheit
3. Sicher speichern in einer `.env`-Datei im Projektverzeichnis: 
```
BITGET_API_KEY="bk_..."
BITGET_SECRET_KEY="sk_..."
BITGET_PASSPHRASE="..."  # Bei Schlüsselerstellung festgelegt
```

## WebSocket-Architektur für Bitget API v2

### Verbindungsparameter

| Parameter             | Wert                          |
|-----------------------|-------------------------------|
| Public Channel        | `wss://ws.bitget.com/v2/ws/public` |
| Private Channel       | `wss://ws.bitget.com/v2/ws/private` |
| Ping-Intervall        | 30 Sekunden                   |
| Ping-Format           | Einfacher String: `"ping"`    |
| Max. Nachrichtenrate  | 10/s                          |

### Wichtige Parameter für Subscription-Requests

#### Korrekte Parameter für USDT-M Futures (API v2)

| Parameter   | Wert            | Beschreibung                                |
|-------------|-----------------|---------------------------------------------|
| instType    | "USDT-FUTURES"  | Instrumententyp für USDT-M Futures          |
| channel     | "ticker"        | Kanal für Echtzeit-Preisdaten               |
| instId      | "BTCUSDT"       | Symbol ohne Suffix (kein "_UMCBL" anhängen) |

#### Beispiel für einen korrekten Subscription-Request

```json
{
  "op": "subscribe",
  "args": [
    {
      "instType": "USDT-FUTURES",
      "channel": "ticker",
      "instId": "BTCUSDT"
    }
  ]
}
```

### Verbindungslebenszyklus

```
graph TD
A[Verbindungsaufbau] --> B[Kanalabonnement]
B --> C{Datenstrom}
C -->|"ping" alle 30s| D[Keepalive]
C -->|Daten| E[Verarbeitung]
D --> C
C --> F[Fehler?]
F --> G[Reconnect]
```

## Einfaches Beispiel

```python
from modules.Websocket_Raw_Data.bitget_websocket import BitgetWebSocket
from pybitget.stream import SubscribeReq

# Initialisiere den WebSocket-Client
ws = BitgetWebSocket(
    api_key="bk_...",
    api_secret="sk_...",
    passphrase="...",
    verbose=True
)

# Definiere einen Callback für eingehende Nachrichten
def process_data(data):
    print(f"Neue Daten empfangen: {data}")

# Registriere den Callback
ws.add_callback(process_data)

# Definiere die zu abonnierenden Kanäle
channels = [
    SubscribeReq("mc", "ticker", "BTCUSDT"),  # Echtzeit-Preise
    SubscribeReq("SP", "candle1m", "ETHUSDT")  # 1-Minuten-Kerzen
]

# Starte die WebSocket-Verbindung
ws.run_forever(channels)
```

## Vollständige Implementierung eines WebSocket-Clients

```python
import os
import sys
import json
import time
import logging
import threading
import websocket
from typing import List
from dotenv import load_dotenv

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BitgetWebSocket")

class BitgetWebSocket:
    """
    Bitget WebSocket Client für den Empfang von Echtzeit-Marktdaten.
    """
    
    def __init__(self, api_key: str = None, api_secret: str = None, passphrase: str = None, verbose: bool = False):
        """
        Initialisiert den Bitget WebSocket Client.
        
        Args:
            api_key: API-Schlüssel (optional für öffentliche Kanäle)
            api_secret: API-Secret (optional für öffentliche Kanäle)
            passphrase: API-Passphrase (optional für öffentliche Kanäle)
            verbose: Aktiviert ausführliche Logging-Ausgaben
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.verbose = verbose
        self.ws = None
        self.connected = False
        self.last_ping = 0
        self.symbol = None
        self.channels = None
        self.reconnect_count = 0
        self.max_reconnects = 5
        self.reconnect_delay = 5  # Sekunden
        
        # WebSocket-URLs für API v2
        self.public_url = "wss://ws.bitget.com/v2/ws/public"
        self.private_url = "wss://ws.bitget.com/v2/ws/private"
        
        logger.info("BitgetWebSocket initialisiert")
    
    def on_message(self, ws, message):
        """
        Callback-Funktion für eingehende WebSocket-Nachrichten.
        """
        try:
            data = json.loads(message)
            
            # Ausgabe der Rohdaten
            print(json.dumps(data, indent=2))
            
            if self.verbose:
                logger.debug(f"Nachricht empfangen: {message}")
        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung der Nachricht: {e}")
    
    def on_error(self, ws, error):
        """
        Callback-Funktion für WebSocket-Fehler.
        """
        logger.error(f"WebSocket-Fehler: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """
        Callback-Funktion für das Schließen der WebSocket-Verbindung.
        """
        self.connected = False
        logger.info(f"WebSocket-Verbindung geschlossen: {close_status_code} - {close_msg}")
        
        # Versuche, die Verbindung wiederherzustellen
        if self.reconnect_count < self.max_reconnects:
            self.reconnect_count += 1
            logger.info(f"Versuche Reconnect ({self.reconnect_count}/{self.max_reconnects}) in {self.reconnect_delay} Sekunden...")
            time.sleep(self.reconnect_delay)
            self.connect(self.symbol, self.channels)
        else:
            logger.error(f"Maximale Anzahl an Reconnect-Versuchen erreicht ({self.max_reconnects})")
    
    def on_open(self, ws):
        """
        Callback-Funktion für das Öffnen der WebSocket-Verbindung.
        """
        self.connected = True
        self.last_ping = time.time()
        self.reconnect_count = 0  # Zurücksetzen des Reconnect-Zählers
        logger.info("WebSocket-Verbindung geöffnet")
        
        # Abonniere Kanäle nach dem Verbinden
        if self.symbol and self.channels:
            self.subscribe(self.symbol, self.channels)
    
    def _send_ping(self):
        """
        Sendet einen Ping, um die Verbindung aufrechtzuerhalten.
        
        WICHTIG: Für Bitget API v2 muss der Ping als einfacher String "ping" gesendet werden,
        NICHT als JSON-Objekt wie bei älteren API-Versionen.
        """
        if self.ws and self.connected:
            # Korrektes Ping-Format für Bitget WebSocket v2
            self.ws.send("ping")
            self.last_ping = time.time()
            
            if self.verbose:
                logger.debug("Ping gesendet")
    
    def subscribe(self, symbol: str, channels: List[str] = None):
        """
        Abonniert Kanäle für ein bestimmtes Symbol.
        
        Args:
            symbol: Das Symbol, für das Kanäle abonniert werden sollen (z.B. "BTCUSDT")
            channels: Liste der zu abonnierenden Kanäle (Standard: ["ticker"])
            
        WICHTIG: Für Bitget API v2 muss das Symbol ohne Suffix verwendet werden (z.B. "BTCUSDT" statt "BTCUSDT_UMCBL")
        und der instType muss "USDT-FUTURES" für USDT-M Futures sein.
        """
        if not channels:
            channels = ["ticker"]
        
        # Entferne das Suffix "_UMCBL", "_DMCBL", etc. wenn vorhanden
        clean_symbol = symbol
        if "_" in symbol:
            clean_symbol = symbol.split("_")[0]
        
        # Verwende den korrekten Instrumententyp für die v2 API
        inst_type = "USDT-FUTURES"  # Korrekte Bezeichnung für USDT-M Futures in v2 API
        
        # Erstelle Abonnement-Anfrage gemäß der Bitget API v2-Dokumentation
        subscription_msg = {
            "op": "subscribe",
            "args": []
        }
        
        for channel in channels:
            # Füge jeden Kanal als separates Argument hinzu
            subscription_msg["args"].append({
                "instType": inst_type,
                "channel": channel,
                "instId": clean_symbol
            })
        
        # Sende Abonnement-Anfrage
        if self.ws and self.connected:
            try:
                self.ws.send(json.dumps(subscription_msg))
                logger.info(f"Abonniert: {symbol} - Kanäle: {channels}")
                
                if self.verbose:
                    logger.debug(f"Abonnement-Anfrage gesendet: {subscription_msg}")
            except Exception as e:
                logger.error(f"Fehler beim Senden der Abonnement-Anfrage: {e}")
    
    def connect(self, symbol: str, channels: List[str] = None):
        """
        Stellt eine Verbindung zur WebSocket-API her und abonniert Kanäle.
        
        Args:
            symbol: Das Symbol, für das Kanäle abonniert werden sollen
            channels: Liste der zu abonnierenden Kanäle (Standard: ["ticker"])
        """
        # Speichere Symbol und Kanäle für die Verwendung in on_open
        self.symbol = symbol
        self.channels = channels if channels else ["ticker"]
        
        # Verwende öffentliche URL für öffentliche Kanäle
        url = self.public_url
        
        # Erstelle WebSocket-Verbindung
        websocket.enableTrace(self.verbose)
        self.ws = websocket.WebSocketApp(
            url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        # Starte WebSocket-Verbindung in einem separaten Thread
        ws_thread = threading.Thread(target=self.ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()
        
        # Warte kurz, bis die Verbindung hergestellt ist
        time.sleep(1)
```

## Hauptfunktion zum Ausführen des WebSocket-Clients

```python
def run_websocket(symbol: str, channels: List[str] = None, timeout: int = None):
    """
    Führt den WebSocket-Client aus und gibt Rohdaten aus.
    
    Args:
        symbol: Das Symbol, für das Daten empfangen werden sollen
        channels: Liste der zu abonnierenden Kanäle (Standard: ["ticker"])
        timeout: Timeout in Sekunden, nach dem das Skript beendet wird (Standard: None = kein Timeout)
    """
    # Lade Umgebungsvariablen aus .env-Datei
    load_dotenv()
    
    # API-Schlüssel aus Umgebungsvariablen laden
    api_key = os.getenv("BITGET_API_KEY")
    api_secret = os.getenv("BITGET_SECRET_KEY")
    passphrase = os.getenv("BITGET_PASSPHRASE")
    
    # Überprüfe, ob API-Schlüssel vorhanden sind
    if not all([api_key, api_secret, passphrase]):
        logger.warning("API-Schlüssel nicht vollständig. Nur öffentliche Kanäle sind verfügbar.")
    
    # Initialisiere den WebSocket-Client
    client = BitgetWebSocket(
        api_key=api_key,
        api_secret=api_secret,
        passphrase=passphrase,
        verbose=True
    )
    
    try:
        # Verbinde mit der WebSocket-API
        print(f"\nVerbinde mit Bitget WebSocket für Symbol: {symbol}")
        print(f"Abonnierte Kanäle: {channels or ['ticker']}")
        if timeout:
            print(f"\nSkript wird nach {timeout} Sekunden automatisch beendet.")
        else:
            print("\nDrücke Strg+C zum Beenden...\n")
        
        # Starte die WebSocket-Verbindung
        client.connect(symbol, channels)
        
        # Startzeit für Timeout
        start_time = time.time()
        
        # Halte das Skript am Laufen
        while True:
            time.sleep(1)
            
            # Sende alle 30 Sekunden einen Ping, um die Verbindung aufrechtzuerhalten
            if time.time() - client.last_ping > 30:
                client._send_ping()
                
            # Beende das Skript nach dem Timeout
            if timeout and time.time() - start_time > timeout:
                print(f"\nTimeout von {timeout} Sekunden erreicht. Beende WebSocket-Verbindung...")
                break
    
    except KeyboardInterrupt:
        print("\nBeende WebSocket-Verbindung...")
    except Exception as e:
        logger.error(f"Fehler: {e}")
    finally:
        # Schließe die WebSocket-Verbindung
        if client.ws:
            client.ws.close()
        
        print("\nBitget WebSocket beendet.")

# Beispielaufruf
if __name__ == "__main__":
    # Symbol ohne Suffix für API v2
    run_websocket("BTCUSDT", ["ticker"], timeout=60)
```

## Beispiel für die Datenstruktur der empfangenen Nachrichten

Für den Ticker-Kanal sieht die Antwort wie folgt aus:
```json
{
  "action": "snapshot",
  "arg": {
    "instType": "USDT-FUTURES",
    "channel": "ticker",
    "instId": "BTCUSDT"
  },
  "data": [
    {
      "instId": "BTCUSDT",
      "lastPr": "88650",
      "bidPr": "88649.6",
      "askPr": "88650.3",
      "bidSz": "0.0002",
      "askSz": "1.6412",
      "open24h": "87196.0",
      "high24h": "92500",
      "low24h": "86020.4",
      "change24h": "-0.03817",
      "fundingRate": "0.00005",
      "nextFundingTime": "1740528000000",
      "markPrice": "88677.5",
      "indexPrice": "88719.802166",
      "holdingAmount": "47519.4904",
      "baseVolume": "233234.0741",
      "quoteVolume": "20737510352.0349",
      "openUtc": "91514.8",
      "symbolType": "1",
      "symbol": "BTCUSDT",
      "deliveryPrice": "0",
      "ts": "1740526884804"
    }
  ],
  "ts": 1740526884807
}
```

## Häufige Fehler und deren Behebung

### "Param error" (Code 30016)
Dieser Fehler tritt auf, wenn die Parameter im Subscription-Request nicht korrekt sind.

#### Häufige Ursachen und Lösungen:
1. **Falscher instType**: 
   - Falsch: `"instType": "UMCBL"` oder `"instType": "mc"`
   - Richtig: `"instType": "USDT-FUTURES"` für USDT-M Futures

2. **Falsches Symbol-Format**:
   - Falsch: `"instId": "BTCUSDT_UMCBL"`
   - Richtig: `"instId": "BTCUSDT"` (ohne Suffix)

3. **Falsches Ping-Format**:
   - Falsch: `{"ping": ""}`
   - Richtig: `"ping"` (einfacher String)

### Verbindungsabbrüche
Wenn die Verbindung häufig abbricht, überprüfe folgende Punkte:

1. **Ping-Intervall**: Stelle sicher, dass alle 30 Sekunden ein Ping gesendet wird
2. **Ping-Format**: Verwende das korrekte Format `"ping"` für API v2
3. **Netzwerkstabilität**: Überprüfe deine Internetverbindung
4. **Reconnect-Mechanismus**: Implementiere einen robusten Reconnect-Mechanismus

## Datenverarbeitung für Trading-Strategien

### Extraktion wichtiger Daten aus Ticker-Nachrichten
```python
def process_ticker_data(message):
    """
    Extrahiert wichtige Daten aus einer Ticker-Nachricht.
    
    Args:
        message: Die empfangene JSON-Nachricht
        
    Returns:
        dict: Ein Dictionary mit den wichtigsten Daten
    """
    try:
        data = message["data"][0]
        
        return {
            "symbol": data["instId"],
            "price": float(data["lastPr"]),
            "bid": float(data["bidPr"]),
            "ask": float(data["askPr"]),
            "bid_size": float(data["bidSz"]),
            "ask_size": float(data["askSz"]),
            "spread": float(data["askPr"]) - float(data["bidPr"]),
            "24h_change": float(data["change24h"]),
            "24h_volume": float(data["baseVolume"]),
            "funding_rate": float(data["fundingRate"]),
            "mark_price": float(data["markPrice"]),
            "index_price": float(data["indexPrice"]),
            "timestamp": int(data["ts"])
        }
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"Fehler bei der Verarbeitung der Ticker-Daten: {e}")
        return None
```

### Speichern der Daten in einer CSV-Datei
```python
import pandas as pd
from datetime import datetime

def save_to_csv(data_dict, filename=None):
    """
    Speichert die Daten in einer CSV-Datei.
    
    Args:
        data_dict: Das Dictionary mit den Daten
        filename: Der Dateiname (Standard: "bitget_data_YYYY-MM-DD.csv")
    """
    if data_dict is None:
        return
    
    if filename is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"bitget_data_{date_str}.csv"
    
    # Erstelle ein DataFrame aus dem Dictionary
    df = pd.DataFrame([data_dict])
    
    # Füge einen Zeitstempel hinzu
    df["local_time"] = datetime.now().isoformat()
    
    # Speichere die Daten in einer CSV-Datei (Anhängen, wenn die Datei bereits existiert)
    df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)
    
    logger.info(f"Daten in {filename} gespeichert")
```

## Vollständiges Beispiel mit Datenverarbeitung

```python
# Modifiziere die on_message-Methode in der BitgetWebSocket-Klasse
def on_message(self, ws, message):
    """
    Callback-Funktion für eingehende WebSocket-Nachrichten.
    """
    try:
        data = json.loads(message)
        
        # Ausgabe der Rohdaten
        print(json.dumps(data, indent=2))
        
        # Verarbeite Ticker-Daten
        if "data" in data and len(data["data"]) > 0 and "arg" in data and data["arg"]["channel"] == "ticker":
            processed_data = process_ticker_data(data)
            if processed_data:
                # Speichere die Daten in einer CSV-Datei
                save_to_csv(processed_data)
        
        if self.verbose:
            logger.debug(f"Nachricht empfangen: {message}")
    except Exception as e:
        logger.error(f"Fehler bei der Verarbeitung der Nachricht: {e}")
```

## Zusammenfassung der wichtigsten Punkte

1. **Korrekte WebSocket-URL**: `wss://ws.bitget.com/v2/ws/public` für öffentliche Kanäle
2. **Korrekte Parameter**:
   - `instType`: "USDT-FUTURES" für USDT-M Futures
   - `instId`: Symbol ohne Suffix (z.B. "BTCUSDT")
3. **Korrektes Ping-Format**: Einfacher String `"ping"` (nicht als JSON-Objekt)
4. **Ping-Intervall**: Alle 30 Sekunden
5. **Reconnect-Mechanismus**: Implementiere einen robusten Reconnect-Mechanismus
6. **Fehlerbehandlung**: Behandle Verbindungsabbrüche und Fehler angemessen

## Kommandozeilenbeispiel

Um den WebSocket-Client zu starten:

```bash
python -m modules.Websocket_Raw_Data.Bitget_Websocket_Raw_Data BTCUSDT --timeout 60
```

## Installation

Installiere die benötigten Abhängigkeiten mit:

```bash
pip install -r requirements.txt
```

## Weitere Informationen

Für detaillierte Informationen zur Bitget WebSocket API siehe die [offizielle Dokumentation](https://www.bitget.com/api-doc/common/websocket-intro).

---

*Diese Dokumentation wird kontinuierlich aktualisiert. Letzter Review: 26.02.2025* 