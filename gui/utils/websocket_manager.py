"""
WebSocket Manager - Verwaltet die Verbindungen zu den WebSockets von KuCoin und BitGet

Diese Komponente stellt eine einheitliche Schnittstelle für die Verbindung zu verschiedenen
WebSocket-APIs bereit und verarbeitet die eingehenden Daten.
"""

import sys
import os
import threading
import time
import json
import logging
from datetime import datetime
import pandas as pd

# Füge das Root-Verzeichnis zum Pfad hinzu, damit wir die Module importieren können
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WebSocketManager")

class WebSocketManager:
    """Verwaltet WebSocket-Verbindungen für verschiedene Exchanges"""
    
    def __init__(self, callback=None):
        """
        Initialisiert den WebSocket-Manager
        
        Args:
            callback: Eine Funktion, die aufgerufen wird, wenn neue Daten empfangen werden
        """
        self.callback = callback
        self.websocket_client = None
        self.connected = False
        self.exchange = None
        self.symbol = None
        self.channels = []
        self.market_type = None
        self.data_buffer = pd.DataFrame()
        self.last_update = None
        self.stop_event = threading.Event()
    
    def connect(self, exchange, symbol, channels, market_type="futures", timeout=60):
        """
        Stellt eine Verbindung zum WebSocket her
        
        Args:
            exchange: Die Exchange (KuCoin oder BitGet)
            symbol: Das Währungspaar
            channels: Die zu abonnierenden Kanäle
            market_type: Der Markttyp (futures oder spot)
            timeout: Timeout in Sekunden
            
        Returns:
            bool: True, wenn die Verbindung erfolgreich hergestellt wurde, sonst False
        """
        if self.connected:
            logger.warning("Es besteht bereits eine Verbindung. Bitte trenne diese zuerst.")
            return False
        
        self.exchange = exchange
        self.symbol = symbol
        self.channels = channels
        self.market_type = market_type
        self.stop_event.clear()
        
        try:
            # Importiere das entsprechende WebSocket-Modul
            if exchange == "KuCoin":
                from modules.Websocket_Raw_Data.KuCoin_Websocket_Raw_Data import KuCoinWebSocket
                
                # Erstelle eine Instanz des WebSocket-Clients
                self.websocket_client = KuCoinWebSocket(
                    symbol=symbol,
                    market_type=market_type.upper(),
                    channels=channels,
                    callback=self._data_callback
                )
                
                # Starte die Verbindung in einem separaten Thread
                self.websocket_thread = threading.Thread(
                    target=self._run_kucoin_websocket,
                    args=(timeout,)
                )
                self.websocket_thread.daemon = True
                self.websocket_thread.start()
                
                # Warte kurz, um zu sehen, ob die Verbindung erfolgreich hergestellt wurde
                time.sleep(2)
                self.connected = True
                return True
                
            elif exchange == "BitGet":
                from modules.Websocket_Raw_Data.BitGet_Websocket_Raw_Data import BitGetWebSocket
                
                # Erstelle eine Instanz des WebSocket-Clients
                self.websocket_client = BitGetWebSocket(
                    symbol=symbol,
                    market_type=market_type.upper(),
                    channels=channels,
                    callback=self._data_callback
                )
                
                # Starte die Verbindung in einem separaten Thread
                self.websocket_thread = threading.Thread(
                    target=self._run_bitget_websocket,
                    args=(timeout,)
                )
                self.websocket_thread.daemon = True
                self.websocket_thread.start()
                
                # Warte kurz, um zu sehen, ob die Verbindung erfolgreich hergestellt wurde
                time.sleep(2)
                self.connected = True
                return True
            
            else:
                logger.error(f"Unbekannte Exchange: {exchange}")
                return False
                
        except Exception as e:
            logger.error(f"Fehler beim Verbinden mit {exchange}: {str(e)}")
            return False
    
    def disconnect(self):
        """
        Trennt die WebSocket-Verbindung
        
        Returns:
            bool: True, wenn die Verbindung erfolgreich getrennt wurde, sonst False
        """
        if not self.connected:
            logger.warning("Es besteht keine Verbindung, die getrennt werden könnte.")
            return True
        
        try:
            # Signalisiere dem Thread, dass er stoppen soll
            self.stop_event.set()
            
            # Warte, bis der Thread beendet ist
            if hasattr(self, 'websocket_thread') and self.websocket_thread.is_alive():
                self.websocket_thread.join(timeout=5)
            
            # Setze die Verbindungsvariablen zurück
            self.connected = False
            self.websocket_client = None
            self.last_update = None
            
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Trennen der Verbindung: {str(e)}")
            return False
    
    def _data_callback(self, data):
        """
        Callback-Funktion für eingehende Daten
        
        Args:
            data: Die empfangenen Daten
        """
        try:
            # Verarbeite die Daten je nach Exchange und Kanal
            processed_data = self._process_data(data)
            
            if processed_data:
                # Aktualisiere den Zeitstempel des letzten Updates
                self.last_update = datetime.now()
                
                # Füge die Daten zum Buffer hinzu
                self.data_buffer = pd.concat([self.data_buffer, processed_data], ignore_index=True)
                
                # Begrenze die Größe des Buffers
                if len(self.data_buffer) > 1000:
                    self.data_buffer = self.data_buffer.tail(1000)
                
                # Rufe den externen Callback auf, falls vorhanden
                if self.callback:
                    self.callback(processed_data)
        
        except Exception as e:
            logger.error(f"Fehler bei der Datenverarbeitung: {str(e)}")
    
    def _process_data(self, data):
        """
        Verarbeitet die eingehenden Daten und konvertiert sie in ein einheitliches Format
        
        Args:
            data: Die zu verarbeitenden Daten
            
        Returns:
            pd.DataFrame: Die verarbeiteten Daten als DataFrame oder None, wenn die Daten nicht verarbeitet werden konnten
        """
        try:
            # Konvertiere die Daten in ein Dictionary, falls sie als String vorliegen
            if isinstance(data, str):
                data = json.loads(data)
            
            # Verarbeite die Daten je nach Exchange und Kanal
            if self.exchange == "KuCoin":
                return self._process_kucoin_data(data)
            elif self.exchange == "BitGet":
                return self._process_bitget_data(data)
            else:
                logger.warning(f"Unbekannte Exchange: {self.exchange}")
                return None
                
        except Exception as e:
            logger.error(f"Fehler bei der Datenverarbeitung: {str(e)}")
            return None
    
    def _process_kucoin_data(self, data):
        """
        Verarbeitet Daten von KuCoin
        
        Args:
            data: Die zu verarbeitenden Daten
            
        Returns:
            pd.DataFrame: Die verarbeiteten Daten als DataFrame oder None, wenn die Daten nicht verarbeitet werden konnten
        """
        try:
            # Überprüfe, ob es sich um eine Ticker-Nachricht handelt
            if 'type' in data and data['type'] == 'message' and 'subject' in data and data['subject'] == 'ticker':
                ticker_data = data['data']
                
                # Erstelle ein DataFrame mit den Ticker-Daten
                df = pd.DataFrame([{
                    'timestamp': datetime.now(),
                    'exchange': 'KuCoin',
                    'symbol': ticker_data['symbol'],
                    'price': float(ticker_data['price']),
                    'best_bid': float(ticker_data['bestBidPrice']),
                    'best_ask': float(ticker_data['bestAskPrice']),
                    'volume': float(ticker_data['size']),
                    'side': ticker_data['side'],
                    'raw_data': json.dumps(data)
                }])
                
                return df
            
            # Hier könnten weitere Kanäle verarbeitet werden
            
            return None
            
        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung von KuCoin-Daten: {str(e)}")
            return None
    
    def _process_bitget_data(self, data):
        """
        Verarbeitet Daten von BitGet
        
        Args:
            data: Die zu verarbeitenden Daten
            
        Returns:
            pd.DataFrame: Die verarbeiteten Daten als DataFrame oder None, wenn die Daten nicht verarbeitet werden konnten
        """
        try:
            # Überprüfe, ob es sich um eine Ticker-Nachricht handelt
            if 'action' in data and data['action'] == 'snapshot' and 'arg' in data and 'data' in data:
                if 'channel' in data['arg'] and data['arg']['channel'] == 'ticker':
                    ticker_data = data['data'][0]
                    
                    # Erstelle ein DataFrame mit den Ticker-Daten
                    df = pd.DataFrame([{
                        'timestamp': datetime.now(),
                        'exchange': 'BitGet',
                        'symbol': data['arg']['instId'],
                        'price': float(ticker_data['last']),
                        'best_bid': float(ticker_data['bidPr']),
                        'best_ask': float(ticker_data['askPr']),
                        'volume': float(ticker_data['vol24h']),
                        'side': 'buy' if float(ticker_data['change']) > 0 else 'sell',
                        'raw_data': json.dumps(data)
                    }])
                    
                    return df
            
            # Hier könnten weitere Kanäle verarbeitet werden
            
            return None
            
        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung von BitGet-Daten: {str(e)}")
            return None
    
    def _run_kucoin_websocket(self, timeout):
        """
        Führt den KuCoin WebSocket-Client aus
        
        Args:
            timeout: Timeout in Sekunden
        """
        try:
            # Starte den WebSocket-Client
            self.websocket_client.connect()
            
            # Warte, bis das Stop-Event gesetzt wird oder der Timeout erreicht ist
            if timeout > 0:
                self.stop_event.wait(timeout=timeout)
            else:
                self.stop_event.wait()
            
            # Trenne die Verbindung
            self.websocket_client.disconnect()
            
        except Exception as e:
            logger.error(f"Fehler beim Ausführen des KuCoin WebSocket-Clients: {str(e)}")
        
        finally:
            # Setze die Verbindungsvariablen zurück
            self.connected = False
            self.websocket_client = None
    
    def _run_bitget_websocket(self, timeout):
        """
        Führt den BitGet WebSocket-Client aus
        
        Args:
            timeout: Timeout in Sekunden
        """
        try:
            # Starte den WebSocket-Client
            self.websocket_client.connect()
            
            # Warte, bis das Stop-Event gesetzt wird oder der Timeout erreicht ist
            if timeout > 0:
                self.stop_event.wait(timeout=timeout)
            else:
                self.stop_event.wait()
            
            # Trenne die Verbindung
            self.websocket_client.disconnect()
            
        except Exception as e:
            logger.error(f"Fehler beim Ausführen des BitGet WebSocket-Clients: {str(e)}")
        
        finally:
            # Setze die Verbindungsvariablen zurück
            self.connected = False
            self.websocket_client = None
    
    def get_data(self):
        """
        Gibt die aktuellen Daten zurück
        
        Returns:
            pd.DataFrame: Die aktuellen Daten
        """
        return self.data_buffer
    
    def is_connected(self):
        """
        Überprüft, ob eine Verbindung besteht
        
        Returns:
            bool: True, wenn eine Verbindung besteht, sonst False
        """
        return self.connected
    
    def get_last_update(self):
        """
        Gibt den Zeitstempel des letzten Updates zurück
        
        Returns:
            datetime: Der Zeitstempel des letzten Updates oder None, wenn kein Update vorhanden ist
        """
        return self.last_update 