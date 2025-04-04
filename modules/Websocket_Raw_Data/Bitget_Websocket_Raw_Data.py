#!/usr/bin/env python3
"""
Bitget WebSocket Raw Data Module
--------------------------------

Dieses Modul stellt eine einfache Schnittstelle zur Verbindung mit der Bitget WebSocket API v2
bereit und empfängt Echtzeit-Marktdaten im Rohformat. Es konzentriert sich ausschließlich auf
das Abrufen und Anzeigen der Rohdaten ohne weitere Verarbeitung oder Speicherung.

FUNKTIONSWEISE:
--------------
1. Verbindung zur Bitget WebSocket API v2 herstellen
2. Abonnieren eines oder mehrerer Kanäle für ein bestimmtes Handelspaar
3. Empfangen und Anzeigen der Rohdaten im JSON-Format
4. Aufrechterhaltung der Verbindung durch regelmäßige Ping-Nachrichten
5. Automatische Wiederverbindung bei Verbindungsabbrüchen

PARAMETER UND ARGUMENTE:
-----------------------
Kommandozeilenargumente:
  symbol                Das Handelspaar, für das Daten empfangen werden sollen (z.B. BTCUSDT)
                        Hinweis: Für API v2 wird das Symbol ohne Suffix verwendet
                        
  --channels [CHANNELS] Die zu abonnierenden Kanäle (Standard: ticker)
                        Mögliche Werte: ticker, candle1m, books5, trade, etc.
                        
  --timeout TIMEOUT     Timeout in Sekunden, nach dem das Skript automatisch beendet wird
                        (Optional, Standard: läuft bis zum manuellen Abbruch)

BEISPIELE:
---------
# Empfange Ticker-Daten für BTCUSDT (Standard-Kanal)
python -m modules.Websocket_Raw_Data.Bitget_Websocket_Raw_Data BTCUSDT

# Empfange Kerzendaten und Orderbuch für ETHUSDT mit 30 Sekunden Timeout
python -m modules.Websocket_Raw_Data.Bitget_Websocket_Raw_Data ETHUSDT --channels candle1m books5 --timeout 30

# Wenn ein Symbol mit Suffix eingegeben wird (z.B. BTCUSDT_UMCBL), wird das Suffix automatisch entfernt
python -m modules.Websocket_Raw_Data.Bitget_Websocket_Raw_Data BTCUSDT_UMCBL

WICHTIGE HINWEISE:
----------------
- Für die Bitget API v2 muss der Instrumententyp "USDT-FUTURES" für USDT-M Futures verwendet werden
- Das Symbol muss ohne Suffix angegeben werden (z.B. "BTCUSDT" statt "BTCUSDT_UMCBL")
- Der Ping muss als einfacher String "ping" gesendet werden (nicht als JSON-Objekt)
- Die Verbindung wird alle 30 Sekunden durch einen Ping aufrechterhalten
"""

import os
import sys
import json
import time
import logging
import argparse
import threading
import websocket
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dotenv import load_dotenv

# Füge das Root-Verzeichnis zum Pfad hinzu, um relative Imports zu ermöglichen
root_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(root_dir))

# Importiere das Trading_Pairs Modul
from modules.Trading_Pairs.BitGet_Futures_Pairs import get_active_symbols

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BitgetWebSocket")

class BitgetWebSocket:
    """
    Bitget WebSocket Client für den Empfang von Echtzeit-Marktdaten.
    
    Diese Klasse bietet eine einfache Schnittstelle zum Verbinden mit der
    Bitget WebSocket API und zum Empfangen von Echtzeit-Marktdaten.
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
        
        # WebSocket-URLs
        self.public_url = "wss://ws.bitget.com/v2/ws/public"
        self.private_url = "wss://ws.bitget.com/v2/ws/private"
        
        logger.info("BitgetWebSocket initialisiert")
    
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
            # Gemäß Dokumentation: Ping-Format für Bitget WebSocket v2
            self.ws.send("ping")
            self.last_ping = time.time()
            
            if self.verbose:
                logger.debug("Ping gesendet")
    
    def subscribe(self, symbol: str, channels: List[str] = None):
        """
        Abonniert Kanäle für ein bestimmtes Symbol.
        
        Args:
            symbol: Das Symbol, für das Kanäle abonniert werden sollen
            channels: Liste der zu abonnierenden Kanäle (Standard: ["ticker"])
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


def is_valid_symbol(symbol: str) -> bool:
    """
    Überprüft, ob ein Symbol gültig ist.
    
    Args:
        symbol: Das zu überprüfende Symbol
    
    Returns:
        bool: True, wenn das Symbol gültig ist, sonst False
    """
    try:
        # Importiere das BitGet_Futures_Pairs-Modul
        from modules.Trading_Pairs.BitGet_Futures_Pairs import get_active_symbols
        
        # Hole die Liste der verfügbaren Symbole
        available_symbols = get_active_symbols(include_inactive=True)
        
        # Überprüfe, ob das Symbol in der Liste ist
        return symbol in available_symbols
    except Exception as e:
        logger.error(f"Fehler bei der Symbolvalidierung: {e}")
        # Im Fehlerfall akzeptieren wir das Symbol ohne Validierung
        return True


def get_user_input_symbol() -> str:
    """
    Fordert den Benutzer zur Eingabe eines Symbols auf und überprüft die Gültigkeit.
    
    Returns:
        str: Das gültige Symbol
    """
    try:
        # Importiere das BitGet_Futures_Pairs-Modul
        from modules.Trading_Pairs.BitGet_Futures_Pairs import get_active_symbols
        
        # Hole die Liste der verfügbaren Symbole
        available_symbols = get_active_symbols(include_inactive=True)
        
        while True:
            print("\nVerfügbare Symbole (Beispiele):")
            # Zeige die ersten 10 Symbole an
            for i, symbol in enumerate(available_symbols[:10]):
                print(f"  {i+1}. {symbol}")
            print(f"  ... und {len(available_symbols) - 10} weitere")
            
            symbol = input("\nBitte gib ein gültiges Symbol ein (z.B. BTCUSDT_UMCBL): ")
            
            if symbol in available_symbols:
                return symbol
            else:
                print(f"Ungültiges Symbol: {symbol}")
                print("Bitte gib ein gültiges Symbol ein.")
    except Exception as e:
        logger.error(f"Fehler beim Laden der Symbole: {e}")
        # Im Fehlerfall akzeptieren wir die Benutzereingabe ohne Validierung
        return input("\nBitte gib ein Symbol ein (z.B. BTCUSDT_UMCBL): ")


def run_websocket(symbol: str, channels: List[str] = None, timeout: int = None):
    """
    Führt den WebSocket-Client aus und gibt Rohdaten aus.
    
    Args:
        symbol: Das Symbol, für das Daten empfangen werden sollen
        channels: Liste der zu abonnierenden Kanäle (Standard: ["ticker"])
        timeout: Timeout in Sekunden, nach dem das Skript beendet wird (Standard: None = kein Timeout)
    """
    # Lade Umgebungsvariablen aus .env-Datei
    load_dotenv(root_dir / '.env')
    
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


def main():
    """Hauptfunktion"""
    # Parse Kommandozeilenargumente
    parser = argparse.ArgumentParser(description="Bitget WebSocket Raw Data")
    parser.add_argument("symbol", nargs="?", type=str, help="Das Symbol, für das Daten empfangen werden sollen (z.B. BTCUSDT_UMCBL)")
    parser.add_argument("--channels", type=str, nargs="+", default=["ticker"], help="Die zu abonnierenden Kanäle (z.B. ticker, candle1m, books5)")
    parser.add_argument("--timeout", type=int, default=None, help="Timeout in Sekunden, nach dem das Skript beendet wird")
    args = parser.parse_args()
    
    # Symbol aus Kommandozeilenargumenten oder Benutzereingabe
    symbol = args.symbol
    
    if symbol:
        # Überprüfe, ob das Symbol gültig ist
        if not is_valid_symbol(symbol):
            print(f"Ungültiges Symbol: {symbol}")
            symbol = get_user_input_symbol()
    else:
        # Fordere den Benutzer zur Eingabe eines Symbols auf
        symbol = get_user_input_symbol()
    
    # Starte den WebSocket-Client
    run_websocket(symbol, args.channels, args.timeout)


if __name__ == "__main__":
    main() 