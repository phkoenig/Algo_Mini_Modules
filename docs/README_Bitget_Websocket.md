# Websocket Raw Data Module

Dieses Verzeichnis enthält Module für die Verbindung mit verschiedenen Kryptobörsen über WebSocket-Schnittstellen, um Echtzeit-Marktdaten zu empfangen.

## Verfügbare Module

### BitgetWebSocket

Ein Modul für die Verbindung mit dem Bitget WebSocket API, das Echtzeit-Marktdaten empfängt und in einem DataFrame speichert.

#### Hauptfunktionen:

- Verbindung mit öffentlichen und privaten Kanälen
- Automatische Reconnect-Logik bei Verbindungsabbrüchen
- Callback-System für benutzerdefinierte Datenverarbeitung
- Datenpufferung in einem DataFrame für einfache Analyse

#### Beispiel:

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

## Installation

Installiere die benötigten Abhängigkeiten mit:

```bash
pip install -r requirements.txt
```

## Weitere Informationen

Für detaillierte Informationen zur Bitget WebSocket API siehe die [offizielle Dokumentation](https://www.bitget.com/api-doc/common/websocket-intro).

---

*Erstellt am: 25.02.2025* 