"""
Data Processor - Verarbeitet und speichert WebSocket-Daten

Diese Komponente bietet Funktionen zur Verarbeitung, Analyse und Speicherung von WebSocket-Daten.
"""

import os
import pandas as pd
import numpy as np
import json
from datetime import datetime
import logging

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DataProcessor")

class DataProcessor:
    """Verarbeitet und speichert WebSocket-Daten"""
    
    def __init__(self, max_buffer_size=10000):
        """
        Initialisiert den DataProcessor
        
        Args:
            max_buffer_size: Maximale Anzahl an Datenpunkten im Buffer
        """
        self.data_buffer = pd.DataFrame()
        self.max_buffer_size = max_buffer_size
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')
        
        # Erstelle den Ausgabeordner, falls er nicht existiert
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def process_data(self, data):
        """
        Verarbeitet eingehende Daten und fügt sie zum Buffer hinzu
        
        Args:
            data: Die zu verarbeitenden Daten als DataFrame
            
        Returns:
            pd.DataFrame: Die verarbeiteten Daten
        """
        if data is None or data.empty:
            return self.data_buffer
        
        # Füge die Daten zum Buffer hinzu
        self.data_buffer = pd.concat([self.data_buffer, data], ignore_index=True)
        
        # Begrenze die Größe des Buffers
        if len(self.data_buffer) > self.max_buffer_size:
            self.data_buffer = self.data_buffer.tail(self.max_buffer_size)
        
        return self.data_buffer
    
    def get_data(self):
        """
        Gibt die aktuellen Daten zurück
        
        Returns:
            pd.DataFrame: Die aktuellen Daten
        """
        return self.data_buffer
    
    def clear_data(self):
        """
        Löscht alle Daten im Buffer
        """
        self.data_buffer = pd.DataFrame()
    
    def save_to_csv(self, filename=None):
        """
        Speichert die Daten als CSV-Datei
        
        Args:
            filename: Der Dateiname (ohne Pfad und Erweiterung)
            
        Returns:
            str: Der Pfad zur gespeicherten Datei oder None, wenn ein Fehler aufgetreten ist
        """
        try:
            if self.data_buffer.empty:
                logger.warning("Keine Daten zum Speichern vorhanden.")
                return None
            
            # Erstelle einen Dateinamen, falls keiner angegeben wurde
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                symbol = self.data_buffer['symbol'].iloc[0] if 'symbol' in self.data_buffer.columns else "unknown"
                exchange = self.data_buffer['exchange'].iloc[0] if 'exchange' in self.data_buffer.columns else "unknown"
                filename = f"{exchange}_{symbol}_{timestamp}"
            
            # Erstelle den vollständigen Pfad
            filepath = os.path.join(self.output_dir, f"{filename}.csv")
            
            # Speichere die Daten
            self.data_buffer.to_csv(filepath, index=False)
            
            logger.info(f"Daten erfolgreich gespeichert: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Daten: {str(e)}")
            return None
    
    def load_from_csv(self, filepath):
        """
        Lädt Daten aus einer CSV-Datei
        
        Args:
            filepath: Der Pfad zur CSV-Datei
            
        Returns:
            pd.DataFrame: Die geladenen Daten oder None, wenn ein Fehler aufgetreten ist
        """
        try:
            if not os.path.exists(filepath):
                logger.error(f"Datei nicht gefunden: {filepath}")
                return None
            
            # Lade die Daten
            data = pd.read_csv(filepath)
            
            # Konvertiere Zeitstempel
            if 'timestamp' in data.columns:
                data['timestamp'] = pd.to_datetime(data['timestamp'])
            
            # Füge die Daten zum Buffer hinzu
            self.data_buffer = data
            
            logger.info(f"Daten erfolgreich geladen: {filepath}")
            return self.data_buffer
            
        except Exception as e:
            logger.error(f"Fehler beim Laden der Daten: {str(e)}")
            return None
    
    def calculate_statistics(self):
        """
        Berechnet Statistiken für die aktuellen Daten
        
        Returns:
            dict: Ein Dictionary mit Statistiken oder None, wenn keine Daten vorhanden sind
        """
        try:
            if self.data_buffer.empty:
                logger.warning("Keine Daten für die Statistikberechnung vorhanden.")
                return None
            
            # Berechne grundlegende Statistiken
            stats = {
                'count': len(self.data_buffer),
                'start_time': self.data_buffer['timestamp'].min(),
                'end_time': self.data_buffer['timestamp'].max(),
                'duration_seconds': (self.data_buffer['timestamp'].max() - self.data_buffer['timestamp'].min()).total_seconds()
            }
            
            # Berechne Preis-Statistiken, falls vorhanden
            if 'price' in self.data_buffer.columns:
                price_stats = self.data_buffer['price'].describe().to_dict()
                stats.update({
                    'price_min': price_stats['min'],
                    'price_max': price_stats['max'],
                    'price_mean': price_stats['mean'],
                    'price_std': price_stats['std'],
                    'price_change': self.data_buffer['price'].iloc[-1] - self.data_buffer['price'].iloc[0],
                    'price_change_pct': (self.data_buffer['price'].iloc[-1] / self.data_buffer['price'].iloc[0] - 1) * 100
                })
            
            # Berechne Volumen-Statistiken, falls vorhanden
            if 'volume' in self.data_buffer.columns:
                volume_stats = self.data_buffer['volume'].describe().to_dict()
                stats.update({
                    'volume_total': self.data_buffer['volume'].sum(),
                    'volume_mean': volume_stats['mean'],
                    'volume_std': volume_stats['std']
                })
            
            return stats
            
        except Exception as e:
            logger.error(f"Fehler bei der Statistikberechnung: {str(e)}")
            return None
    
    def get_latest_data(self, n=10):
        """
        Gibt die neuesten n Datenpunkte zurück
        
        Args:
            n: Anzahl der zurückzugebenden Datenpunkte
            
        Returns:
            pd.DataFrame: Die neuesten n Datenpunkte
        """
        if self.data_buffer.empty:
            return pd.DataFrame()
        
        return self.data_buffer.tail(n)
    
    def get_ohlc(self, timeframe='1min'):
        """
        Berechnet OHLC-Daten (Open, High, Low, Close) für den angegebenen Zeitrahmen
        
        Args:
            timeframe: Der Zeitrahmen für die Aggregation (z.B. '1min', '5min', '1h')
            
        Returns:
            pd.DataFrame: Die OHLC-Daten oder None, wenn keine Daten vorhanden sind oder ein Fehler aufgetreten ist
        """
        try:
            if self.data_buffer.empty or 'price' not in self.data_buffer.columns:
                logger.warning("Keine Preis-Daten für die OHLC-Berechnung vorhanden.")
                return None
            
            # Stelle sicher, dass der Zeitstempel als Index verwendet wird
            df = self.data_buffer.copy()
            df.set_index('timestamp', inplace=True)
            
            # Berechne OHLC-Daten
            ohlc = df['price'].resample(timeframe).ohlc()
            
            # Füge Volumen hinzu, falls vorhanden
            if 'volume' in df.columns:
                volume = df['volume'].resample(timeframe).sum()
                ohlc['volume'] = volume
            
            # Setze den Index zurück
            ohlc.reset_index(inplace=True)
            
            return ohlc
            
        except Exception as e:
            logger.error(f"Fehler bei der OHLC-Berechnung: {str(e)}")
            return None 