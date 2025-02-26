#!/usr/bin/env python3
"""
KuCoin WebSocket Raw Data Module
--------------------------------

Dieses Modul stellt eine einfache Schnittstelle zur Verbindung mit der KuCoin WebSocket API
bereit und empfängt Echtzeit-Marktdaten im Rohformat. Es konzentriert sich ausschließlich auf
das Abrufen und Anzeigen der Rohdaten ohne weitere Verarbeitung oder Speicherung.

FUNKTIONSWEISE:
--------------
1. Abrufen eines Tokens für die WebSocket-Verbindung über die REST API
2. Verbindung zur KuCoin WebSocket API herstellen (Futures oder Spot)
3. Abonnieren eines oder mehrerer Kanäle für ein bestimmtes Handelspaar
4. Empfangen und Anzeigen der Rohdaten im JSON-Format
5. Aufrechterhaltung der Verbindung durch regelmäßige Ping-Nachrichten
6. Automatische Wiederverbindung bei Verbindungsabbrüchen oder Token-Ablauf

PARAMETER UND ARGUMENTE:
-----------------------
Kommandozeilenargumente:
  symbol                Das Handelspaar, für das Daten empfangen werden sollen (z.B. BTCUSDT)
                        
  --market [MARKET]     Der Markttyp (Standard: futures)
                        Mögliche Werte: futures, spot
                        
  --channels [CHANNELS] Die zu abonnierenden Kanäle (Standard: ticker)
                        Mögliche Werte für Futures: ticker, level2, execution, etc.
                        
  --timeout TIMEOUT     Timeout in Sekunden, nach dem das Skript automatisch beendet wird
                        (Optional, Standard: läuft bis zum manuellen Abbruch)

BEISPIELE:
---------
# Empfange Ticker-Daten für BTCUSDT im Futures-Markt (Standard)
python -m modules.Websocket_Raw_Data.KuCoin_Websocket_Raw_Data BTCUSDT

# Empfange Orderbuch-Daten für ETHUSDT im Spot-Markt
python -m modules.Websocket_Raw_Data.KuCoin_Websocket_Raw_Data ETHUSDT --market spot --channels level2

# Empfange Ticker- und Trade-Daten für BTCUSDT mit 60 Sekunden Timeout
python -m modules.Websocket_Raw_Data.KuCoin_Websocket_Raw_Data BTCUSDT --channels ticker trade --timeout 60

WICHTIGE HINWEISE:
----------------
- KuCoin verwendet ein Token-basiertes Authentifizierungssystem mit 24h Gültigkeit
- Das Ping-Intervall beträgt 18 Sekunden (laut API-Dokumentation)
- Die Topic-Formate unterscheiden sich je nach Markttyp:
  - Futures: /contractMarket/ticker:{symbol}
  - Spot: /market/ticker:{symbol}
- Rate Limits: 100 Nachrichten/10s pro Verbindung, 300 aktive Subscriptions pro Token
"""

import os
import sys
import json
import time
import logging
import argparse
import threading
import websocket
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dotenv import load_dotenv

# Füge das Root-Verzeichnis zum Pfad hinzu, um relative Imports zu ermöglichen
root_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(root_dir))

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("KuCoinWebSocket")

class KuCoinWebSocket:
    """
    KuCoin WebSocket Client für den Empfang von Echtzeit-Marktdaten.
    
    Diese Klasse bietet eine einfache Schnittstelle zum Verbinden mit der
    KuCoin WebSocket API und zum Empfangen von Echtzeit-Marktdaten.
    """
    
    def __init__(self, api_key: str = None, api_secret: str = None, passphrase: str = None, 
                 market_type: str = "futures", verbose: bool = False):
        """
        Initialisiert den KuCoin WebSocket Client.
        
        Args:
            api_key: API-Schlüssel (optional für öffentliche Kanäle)
            api_secret: API-Secret (optional für öffentliche Kanäle)
            passphrase: API-Passphrase (optional für öffentliche Kanäle)
            market_type: Markttyp (futures oder spot)
            verbose: Aktiviert ausführliche Logging-Ausgaben
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.market_type = market_type.lower()
        self.verbose = verbose
        self.ws = None
        self.connected = False
        self.last_ping = 0
        self.symbol = None
        self.channels = None
        self.reconnect_count = 0
        self.max_reconnects = 5
        self.reconnect_delay = 5  # Sekunden
        
        # Token-Management
        self.token = None
        self.token_expiry = 0
        self.endpoint = None
        
        # REST API URLs
        if self.market_type == "futures":
            self.rest_url = "https://api-futures.kucoin.com"
        else:  # spot
            self.rest_url = "https://api.kucoin.com"
        
        logger.info(f"KuCoinWebSocket initialisiert für {market_type.upper()}-Markt")
    
    def _get_ws_token(self) -> str:
        """
        Holt ein Token für die WebSocket-Verbindung.
        
        Returns:
            str: Die vollständige WebSocket-URL mit Token
        """
        # Prüfe, ob ein gültiges Token vorhanden ist
        current_time = time.time()
        if self.token and current_time < self.token_expiry:
            return f"{self.endpoint}?token={self.token}"
        
        # Hole ein neues Token
        endpoint = "/api/v1/bullet-public"
        url = f"{self.rest_url}{endpoint}"
        
        try:
            response = requests.post(url)
            data = response.json()
            
            if data.get('code') != '200000':
                raise Exception(f"Token-Anfrage fehlgeschlagen: {data.get('msg', 'Unbekannter Fehler')}")
            
            self.token = data['data']['token']
            self.endpoint = data['data']['instanceServers'][0]['endpoint']
            
            # Token ist 24 Stunden gültig, setze Ablaufzeit auf 23 Stunden zur Sicherheit
            self.token_expiry = current_time + 23 * 3600
            
            logger.info("Neues WebSocket-Token erhalten")
            return f"{self.endpoint}?token={self.token}"
            
        except Exception as e:
            logger.error(f"Fehler beim Abrufen des WebSocket-Tokens: {e}")
            raise
    
    def on_message(self, ws, message):
        """
        Callback-Funktion für eingehende WebSocket-Nachrichten.
        
        Args:
            ws: WebSocket-Verbindung
            message: Empfangene Nachricht
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
        
        Args:
            ws: WebSocket-Verbindung
            error: Aufgetretener Fehler
        """
        logger.error(f"WebSocket-Fehler: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """
        Callback-Funktion für das Schließen der WebSocket-Verbindung.
        
        Args:
            ws: WebSocket-Verbindung
            close_status_code: Status-Code beim Schließen
            close_msg: Nachricht beim Schließen
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
        
        Args:
            ws: WebSocket-Verbindung
        """
        self.connected = True
        self.last_ping = time.time()
        self.reconnect_count = 0  # Zurücksetzen des Reconnect-Zählers
        logger.info("WebSocket-Verbindung geöffnet")
        
        # Abonniere Kanäle nach dem Verbinden
        if self.symbol and self.channels:
            self.subscribe(self.symbol, self.channels)
    
    def _send_ping(self):
        """Sendet einen Ping, um die Verbindung aufrechtzuerhalten."""
        if self.ws and self.connected:
            # Gemäß Dokumentation: Ping-Format für KuCoin WebSocket
            ping_msg = {
                "id": str(int(time.time() * 1000)),
                "type": "ping"
            }
            self.ws.send(json.dumps(ping_msg))
            self.last_ping = time.time()
            
            if self.verbose:
                logger.debug("Ping gesendet")
    
    def _get_topic(self, channel: str, symbol: str) -> str:
        """
        Erstellt das Topic für ein bestimmtes Symbol und einen Kanal.
        
        Args:
            channel: Der Kanal (z.B. ticker, level2)
            symbol: Das Symbol (z.B. BTCUSDT)
            
        Returns:
            str: Das formatierte Topic
        """
        if self.market_type == "futures":
            # Futures-Markt Topics
            if channel == "ticker":
                return f"/contractMarket/ticker:{symbol}"
            elif channel == "level2":
                return f"/contractMarket/level2:{symbol}"
            elif channel == "execution":
                return f"/contractMarket/execution:{symbol}"
            elif channel == "trade":
                return f"/contractMarket/trade:{symbol}"
            else:
                return f"/contractMarket/{channel}:{symbol}"
        else:
            # Spot-Markt Topics
            if channel == "ticker":
                return f"/market/ticker:{symbol}"
            elif channel == "level2":
                return f"/market/level2:{symbol}"
            elif channel == "trade":
                return f"/market/match:{symbol}"
            else:
                return f"/market/{channel}:{symbol}"
    
    def subscribe(self, symbol: str, channels: List[str] = None):
        """
        Abonniert Kanäle für ein bestimmtes Symbol.
        
        Args:
            symbol: Das Symbol, für das Kanäle abonniert werden sollen
            channels: Liste der zu abonnierenden Kanäle (Standard: ["ticker"])
        """
        if not channels:
            channels = ["ticker"]
        
        # Erstelle Abonnement-Anfrage gemäß der KuCoin API-Dokumentation
        for channel in channels:
            topic = self._get_topic(channel, symbol)
            subscription_msg = {
                "id": str(int(time.time() * 1000)),
                "type": "subscribe",
                "topic": topic,
                "response": True
            }
            
            # Sende Abonnement-Anfrage
            if self.ws and self.connected:
                try:
                    self.ws.send(json.dumps(subscription_msg))
                    logger.info(f"Abonniert: {topic}")
                    
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
        
        try:
            # Hole WebSocket-URL mit Token
            ws_url = self._get_ws_token()
            
            # Erstelle WebSocket-Verbindung
            websocket.enableTrace(self.verbose)
            self.ws = websocket.WebSocketApp(
                ws_url,
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
            
        except Exception as e:
            logger.error(f"Fehler beim Verbinden mit der WebSocket-API: {e}")
            raise


def run_websocket(symbol: str, market_type: str = "futures", channels: List[str] = None, timeout: int = None):
    """
    Führt den WebSocket-Client aus und gibt Rohdaten aus.
    
    Args:
        symbol: Das Symbol, für das Daten empfangen werden sollen
        market_type: Der Markttyp (futures oder spot)
        channels: Liste der zu abonnierenden Kanäle (Standard: ["ticker"])
        timeout: Timeout in Sekunden, nach dem das Skript beendet wird (Standard: None = kein Timeout)
    """
    # Lade Umgebungsvariablen aus .env-Datei
    load_dotenv(root_dir / '.env')
    
    # API-Schlüssel aus Umgebungsvariablen laden
    api_key = os.getenv("KUCOIN_API_KEY")
    api_secret = os.getenv("KUCOIN_SECRET_KEY")
    passphrase = os.getenv("KUCOIN_PASSPHRASE")
    
    # Überprüfe, ob API-Schlüssel vorhanden sind
    if not all([api_key, api_secret, passphrase]):
        logger.warning("API-Schlüssel nicht vollständig. Nur öffentliche Kanäle sind verfügbar.")
    
    # Initialisiere den WebSocket-Client
    client = KuCoinWebSocket(
        api_key=api_key,
        api_secret=api_secret,
        passphrase=passphrase,
        market_type=market_type,
        verbose=True
    )
    
    try:
        # Verbinde mit der WebSocket-API
        print(f"\nVerbinde mit KuCoin WebSocket für Symbol: {symbol} ({market_type.upper()}-Markt)")
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
            
            # Sende alle 18 Sekunden einen Ping, um die Verbindung aufrechtzuerhalten
            # KuCoin empfiehlt ein Ping-Intervall von 18 Sekunden
            if time.time() - client.last_ping > 18:
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
        
        print("\nKuCoin WebSocket beendet.")


def main():
    """Hauptfunktion"""
    # Parse Kommandozeilenargumente
    parser = argparse.ArgumentParser(description="KuCoin WebSocket Raw Data")
    parser.add_argument("symbol", type=str, help="Das Symbol, für das Daten empfangen werden sollen (z.B. BTCUSDT)")
    parser.add_argument("--market", type=str, default="futures", choices=["futures", "spot"], 
                        help="Der Markttyp (futures oder spot)")
    parser.add_argument("--channels", type=str, nargs="+", default=["ticker"], 
                        help="Die zu abonnierenden Kanäle (z.B. ticker, level2, trade)")
    parser.add_argument("--timeout", type=int, default=None, 
                        help="Timeout in Sekunden, nach dem das Skript beendet wird")
    args = parser.parse_args()
    
    # Starte den WebSocket-Client
    run_websocket(args.symbol, args.market, args.channels, args.timeout)


if __name__ == "__main__":
    main() 