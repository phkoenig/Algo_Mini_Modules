# KuCoin WebSocket API - Dokumentation und Implementierungsleitfaden

Dieses Dokument bietet eine umfassende Anleitung zur Integration der KuCoin WebSocket API für den Empfang von Echtzeit-Marktdaten, speziell für Futures-Märkte.

## Übersicht

Das KuCoinWebSocket-Modul ermöglicht die Verbindung mit der KuCoin Börse über WebSocket-Schnittstellen, um Echtzeit-Marktdaten zu empfangen.

### Hauptfunktionen:

- Verbindung mit öffentlichen und privaten Kanälen
- Automatische Token-Verwaltung mit 24h Gültigkeit
- Automatische Reconnect-Logik bei Verbindungsabbrüchen
- Unterstützung für Futures und Spot Märkte
- Validierung von Handelssymbolen gegen die aktive Symbolliste

## Vorbereitung der Entwicklungsumgebung

### Installation der benötigten Python-Bibliotheken

```bash
pip install websocket-client pandas python-dotenv requests
```

### API-Schlüssel generieren

1. Melde dich bei deinem KuCoin-Konto an
2. Navigiere zu "API Management"
3. Klicke auf "Create API"
4. Wähle "Futures Trading" als API-Typ
5. Notiere dir den API-Schlüssel, das Secret und die Passphrase
6. Speichere diese Informationen sicher in einer `.env`-Datei:

```
KUCOIN_API_KEY=dein_api_key
KUCOIN_API_SECRET=dein_api_secret
KUCOIN_PASSPHRASE=deine_passphrase
```

## WebSocket-Architektur für KuCoin API

KuCoin verwendet ein zweistufiges Verbindungsverfahren:

1. **Token-Anfrage**: Zuerst muss ein Token über die REST-API angefordert werden
2. **WebSocket-Verbindung**: Mit diesem Token wird dann die WebSocket-Verbindung hergestellt

### Wichtige Endpunkte

- **Public Token-Endpunkt**: `https://api-futures.kucoin.com/api/v1/bullet-public`
- **Private Token-Endpunkt**: `https://api-futures.kucoin.com/api/v1/bullet-private`

Der erhaltene Token ist 24 Stunden gültig.

### Verbindungsparameter

- **WebSocket-URL**: Die URL wird in der Token-Antwort bereitgestellt (z.B. `wss://ws-api-futures.kucoin.com/endpoint?token=xxx`)
- **Ping-Intervall**: Alle 18-20 Sekunden sollte ein Ping gesendet werden
- **Reconnect-Strategie**: Bei Verbindungsabbrüchen sollte automatisch ein neuer Token angefordert werden

### Wichtige Parameter für Subscription-Anfragen

- **id**: Eine eindeutige ID für die Anfrage (z.B. ein Zeitstempel)
- **type**: Der Typ der Anfrage (z.B. "subscribe")
- **topic**: Der Kanal, den du abonnieren möchtest (z.B. "/contractMarket/ticker:XBTUSDTM")
- **privateChannel**: Boolean-Wert, ob ein privater Kanal verwendet wird
- **response**: Boolean-Wert, ob eine Antwort erwartet wird

## Einfaches Beispiel

```python
from modules.Websocket_Raw_Data.KuCoin_Websocket_Raw_Data import KuCoinWebSocket
import time

# Initialisiere den WebSocket-Client
ws = KuCoinWebSocket(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
    passphrase="YOUR_PASSPHRASE",
    market_type="futures",
    verbose=True
)

# Verbinde mit der WebSocket-API und abonniere Kanäle
ws.connect("XBTUSDTM", ["ticker"])

# Halte das Skript am Laufen
try:
    while True:
        time.sleep(1)
        
        # Sende alle 18 Sekunden einen Ping
        if time.time() - ws.last_ping > 18:
            ws._send_ping()
except KeyboardInterrupt:
    print("Beende WebSocket-Verbindung...")
finally:
    if ws.ws:
        ws.ws.close()
```

## Vollständige Implementierung eines WebSocket-Clients

Hier ist eine vollständige Implementierung eines WebSocket-Clients für KuCoin Futures:

```python
import json
import time
import threading
import websocket
import requests
from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen
load_dotenv()

class KuCoinWebSocket:
    def __init__(self, api_key=None, api_secret=None, passphrase=None, market_type="futures", verbose=False):
        self.api_key = api_key or os.getenv("KUCOIN_API_KEY")
        self.api_secret = api_secret or os.getenv("KUCOIN_API_SECRET")
        self.passphrase = passphrase or os.getenv("KUCOIN_PASSPHRASE")
        self.market_type = market_type.lower()  # "futures" oder "spot"
        self.verbose = verbose
        
        self.ws = None
        self.ws_thread = None
        self.last_ping = time.time()
        self.connected = False
        self.reconnect_required = False
        
        # Basis-URLs
        if self.market_type == "futures":
            self.base_url = "https://api-futures.kucoin.com"
        else:
            self.base_url = "https://api.kucoin.com"
    
    def _get_token(self):
        """Token für WebSocket-Verbindung anfordern"""
        if self.api_key and self.api_secret and self.passphrase:
            endpoint = "/api/v1/bullet-private"
            headers = {
                "KC-API-KEY": self.api_key,
                "KC-API-SIGN": self._generate_signature("POST", endpoint, ""),
                "KC-API-TIMESTAMP": str(int(time.time() * 1000)),
                "KC-API-PASSPHRASE": self.passphrase,
                "KC-API-KEY-VERSION": "2"
            }
            response = requests.post(f"{self.base_url}{endpoint}", headers=headers)
        else:
            endpoint = "/api/v1/bullet-public"
            response = requests.post(f"{self.base_url}{endpoint}")
        
        if response.status_code == 200:
            data = response.json()
            if data["code"] == "200000":
                return data["data"]
        
        raise Exception(f"Fehler beim Abrufen des WebSocket-Tokens: {response.text}")
    
    def _generate_signature(self, method, endpoint, data):
        """Generiere die Signatur für API-Anfragen"""
        # Implementierung der Signatur-Generierung gemäß KuCoin-Dokumentation
        # ...
        
    def connect(self, symbol, channels=["ticker"]):
        """Verbindung zur WebSocket-API herstellen und Kanäle abonnieren"""
        token_data = self._get_token()
        
        # Konstruiere WebSocket-URL
        ws_endpoint = token_data["instanceServers"][0]["endpoint"]
        token = token_data["token"]
        ws_url = f"{ws_endpoint}?token={token}&connectId={int(time.time() * 1000)}"
        
        if self.verbose:
            print(f"Verbinde mit WebSocket: {ws_url}")
        
        # WebSocket-Verbindung initialisieren
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_open=lambda ws: self._on_open(ws, symbol, channels),
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        
        # Starte WebSocket in einem separaten Thread
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()
        
        # Warte auf Verbindung
        timeout = 10
        start_time = time.time()
        while not self.connected and time.time() - start_time < timeout:
            time.sleep(0.1)
        
        if not self.connected:
            raise Exception("Timeout beim Verbinden mit WebSocket")
        
        return True
    
    def _on_open(self, ws, symbol, channels):
        """Callback bei erfolgreicher Verbindung"""
        self.connected = True
        self.last_ping = time.time()
        
        if self.verbose:
            print("WebSocket-Verbindung hergestellt")
        
        # Kanäle abonnieren
        for channel in channels:
            self._subscribe(symbol, channel)
    
    def _on_message(self, ws, message):
        """Callback bei eingehender Nachricht"""
        data = json.loads(message)
        
        # Ping-Antwort verarbeiten
        if "type" in data and data["type"] == "pong":
            if self.verbose:
                print("Pong erhalten")
            return
        
        # Welcome-Nachricht verarbeiten
        if "type" in data and data["type"] == "welcome":
            if self.verbose:
                print("Welcome-Nachricht erhalten")
            return
        
        # Subscription-Bestätigung verarbeiten
        if "type" in data and data["type"] == "ack":
            if self.verbose:
                print(f"Subscription bestätigt: {data}")
            return
        
        # Marktdaten verarbeiten
        if "data" in data:
            if self.verbose:
                print(f"Daten erhalten: {json.dumps(data, indent=2)}")
            return
        
        # Andere Nachrichten
        if self.verbose:
            print(f"Unbekannte Nachricht: {message}")
    
    def _on_error(self, ws, error):
        """Callback bei Fehler"""
        print(f"WebSocket-Fehler: {error}")
        self.reconnect_required = True
    
    def _on_close(self, ws, close_status_code, close_msg):
        """Callback bei Verbindungsschluss"""
        self.connected = False
        print(f"WebSocket-Verbindung geschlossen: {close_status_code} - {close_msg}")
        
        if self.reconnect_required:
            print("Versuche Reconnect in 5 Sekunden...")
            time.sleep(5)
            self.reconnect_required = False
            # Hier würde die Reconnect-Logik implementiert werden
    
    def _subscribe(self, symbol, channel):
        """Kanal abonnieren"""
        if channel == "ticker":
            topic = f"/contractMarket/ticker:{symbol}"
        elif channel == "candle":
            topic = f"/contractMarket/candle:{symbol}"
        elif channel == "trade":
            topic = f"/contractMarket/execution:{symbol}"
        elif channel == "depth":
            topic = f"/contractMarket/level2:{symbol}"
        else:
            raise ValueError(f"Unbekannter Kanal: {channel}")
        
        subscription = {
            "id": int(time.time() * 1000),
            "type": "subscribe",
            "topic": topic,
            "privateChannel": False,
            "response": True
        }
        
        if self.verbose:
            print(f"Abonniere Kanal: {topic}")
        
        self.ws.send(json.dumps(subscription))
    
    def _send_ping(self):
        """Ping-Nachricht senden"""
        if self.ws and self.connected:
            ping_msg = {"id": int(time.time() * 1000), "type": "ping"}
            self.ws.send(json.dumps(ping_msg))
            self.last_ping = time.time()
            
            if self.verbose:
                print("Ping gesendet")
```

## Hauptfunktion zum Ausführen des WebSocket-Clients

```python
def main():
    import argparse
    import time
    
    parser = argparse.ArgumentParser(description="KuCoin WebSocket Client")
    parser.add_argument("symbol", help="Symbol to subscribe to (e.g. XBTUSDTM)")
    parser.add_argument("--channels", nargs="+", default=["ticker"], 
                        choices=["ticker", "candle", "trade", "depth"],
                        help="Channels to subscribe to")
    parser.add_argument("--market", default="futures", choices=["futures", "spot"],
                        help="Market type (futures or spot)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--timeout", type=int, default=0, 
                        help="Timeout in seconds (0 for no timeout)")
    
    args = parser.parse_args()
    
    # Initialisiere WebSocket-Client
    ws = KuCoinWebSocket(market_type=args.market, verbose=args.verbose)
    
    try:
        # Verbinde und abonniere Kanäle
        ws.connect(args.symbol, args.channels)
        
        # Halte das Skript am Laufen
        start_time = time.time()
        while True:
            time.sleep(1)
            
            # Sende alle 18 Sekunden einen Ping
            if time.time() - ws.last_ping > 18:
                ws._send_ping()
            
            # Prüfe Timeout
            if args.timeout > 0 and time.time() - start_time > args.timeout:
                print(f"Timeout nach {args.timeout} Sekunden erreicht")
                break
                
    except KeyboardInterrupt:
        print("Beende WebSocket-Verbindung...")
    finally:
        if ws.ws:
            ws.ws.close()

if __name__ == "__main__":
    main()
```

## Beispiel für die Datenstruktur empfangener Nachrichten

### Ticker-Nachricht

```json
{
  "type": "message",
  "topic": "/contractMarket/ticker:XBTUSDTM",
  "subject": "ticker.XBTUSDTM",
  "data": {
    "symbol": "XBTUSDTM",
    "sequence": 1630809710677,
    "side": "sell",
    "size": 1,
    "price": "88387.4",
    "bestBidSize": 1245,
    "bestBidPrice": "88387.3",
    "bestAskPrice": "88387.4",
    "bestAskSize": 3423,
    "ts": 1708950436957
  }
}
```

## Häufige Fehler und deren Behebung

### Verbindungsprobleme

- **Problem**: WebSocket-Verbindung kann nicht hergestellt werden
  **Lösung**: Überprüfe deine Internetverbindung und stelle sicher, dass die KuCoin-Server erreichbar sind

- **Problem**: Authentifizierungsfehler
  **Lösung**: Überprüfe API-Schlüssel, Secret und Passphrase auf Korrektheit

- **Problem**: Verbindung wird nach kurzer Zeit getrennt
  **Lösung**: Stelle sicher, dass regelmäßig Ping-Nachrichten gesendet werden (alle 18-20 Sekunden)

### Symbol-Validierung

- **Problem**: Ungültiges Symbol
  **Lösung**: Verwende die `KuCoin_Futures_Pairs.py`-Funktion, um gültige Symbole zu überprüfen:

```python
from modules.Trading_Pairs.KuCoin_Futures_Pairs import get_active_symbols

# Überprüfe, ob das Symbol gültig ist
valid_symbols = get_active_symbols()
if symbol not in valid_symbols:
    print(f"Warnung: {symbol} ist kein aktives Symbol auf KuCoin Futures")
    print(f"Verfügbare Symbole: {', '.join(valid_symbols[:10])}...")
```

### Besonderheiten bei Bitcoin-Symbol

Beachte, dass KuCoin für Bitcoin in Futures-Märkten das Symbol "XBT" statt "BTC" verwendet:
- Korrektes Symbol für Bitcoin-USDT Futures: `XBTUSDTM`

## Datenverarbeitung für Trading-Strategien

### Beispiel: Ticker-Daten in CSV speichern

```python
import pandas as pd
import os
from datetime import datetime

class DataProcessor:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialisiere DataFrame
        self.df = pd.DataFrame(columns=[
            "timestamp", "price", "size", "side", 
            "bestBidPrice", "bestBidSize", "bestAskPrice", "bestAskSize"
        ])
    
    def process_ticker(self, data):
        """Verarbeite Ticker-Daten"""
        if "data" in data:
            ticker = data["data"]
            
            # Erstelle neuen Datensatz
            new_row = {
                "timestamp": pd.to_datetime(ticker["ts"], unit="ms"),
                "price": float(ticker["price"]),
                "size": float(ticker["size"]),
                "side": ticker["side"],
                "bestBidPrice": float(ticker["bestBidPrice"]),
                "bestBidSize": float(ticker["bestBidSize"]),
                "bestAskPrice": float(ticker["bestAskPrice"]),
                "bestAskSize": float(ticker["bestAskSize"])
            }
            
            # Füge Daten zum DataFrame hinzu
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
            
            # Speichere Daten alle 100 Einträge
            if len(self.df) % 100 == 0:
                self.save_to_csv()
    
    def save_to_csv(self):
        """Speichere Daten in CSV-Datei"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{self.data_dir}/{self.symbol}_ticker_{date_str}.csv"
        self.df.to_csv(filename, index=False)
        print(f"Daten in {filename} gespeichert ({len(self.df)} Einträge)")
```

## Vollständiges Beispiel mit Datenverarbeitung

```python
import json
import time
import threading
import websocket
import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()

# KuCoinWebSocket-Klasse hier einfügen...

class DataProcessor:
    # DataProcessor-Klasse hier einfügen...

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="KuCoin WebSocket Client")
    parser.add_argument("symbol", help="Symbol to subscribe to (e.g. XBTUSDTM)")
    parser.add_argument("--channels", nargs="+", default=["ticker"], 
                        choices=["ticker", "candle", "trade", "depth"],
                        help="Channels to subscribe to")
    parser.add_argument("--market", default="futures", choices=["futures", "spot"],
                        help="Market type (futures or spot)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--save-data", action="store_true", help="Save data to CSV")
    parser.add_argument("--timeout", type=int, default=0, 
                        help="Timeout in seconds (0 for no timeout)")
    
    args = parser.parse_args()
    
    # Initialisiere Datenverarbeitung
    processor = DataProcessor(args.symbol) if args.save_data else None
    
    # Initialisiere WebSocket-Client
    ws = KuCoinWebSocket(market_type=args.market, verbose=args.verbose)
    
    # Überschreibe die on_message-Methode, um Daten zu verarbeiten
    if processor:
        original_on_message = ws._on_message
        
        def on_message_with_processing(ws_app, message):
            original_on_message(ws_app, message)
            try:
                data = json.loads(message)
                if "type" in data and data["type"] == "message" and "subject" in data and data["subject"].startswith("ticker."):
                    processor.process_ticker(data)
            except Exception as e:
                print(f"Fehler bei der Datenverarbeitung: {e}")
        
        ws._on_message = on_message_with_processing
    
    try:
        # Verbinde und abonniere Kanäle
        ws.connect(args.symbol, args.channels)
        
        # Halte das Skript am Laufen
        start_time = time.time()
        while True:
            time.sleep(1)
            
            # Sende alle 18 Sekunden einen Ping
            if time.time() - ws.last_ping > 18:
                ws._send_ping()
            
            # Prüfe Timeout
            if args.timeout > 0 and time.time() - start_time > args.timeout:
                print(f"Timeout nach {args.timeout} Sekunden erreicht")
                break
                
    except KeyboardInterrupt:
        print("Beende WebSocket-Verbindung...")
    finally:
        if processor:
            processor.save_to_csv()
        if ws.ws:
            ws.ws.close()

if __name__ == "__main__":
    main()
```

## Kommandozeilenbeispiel

Um den WebSocket-Client zu starten:

```bash
python -m modules.Websocket_Raw_Data.KuCoin_Websocket_Raw_Data XBTUSDTM --timeout 60
```

Dies verbindet mit dem KuCoin Futures WebSocket für das Symbol XBTUSDTM und abonniert den Ticker-Kanal für 60 Sekunden.

## Installation

Installiere die benötigten Abhängigkeiten mit:

```bash
pip install -r requirements.txt
```

## Weitere Informationen

Für detaillierte Informationen zur KuCoin WebSocket API siehe die [offizielle Dokumentation](https://www.kucoin.com/docs/websocket/overview).

---

*Diese Dokumentation wird kontinuierlich aktualisiert. Letzter Review: 26.02.2025* 