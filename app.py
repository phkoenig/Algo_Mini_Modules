"""
WebSocket Data Explorer - Hauptanwendung

Diese Anwendung ermöglicht die Verbindung zu WebSocket-APIs von KuCoin und BitGet,
um Echtzeit-Marktdaten zu empfangen und zu visualisieren.
"""

import streamlit as st
import pandas as pd
import sys
import os
import threading
import time
from datetime import datetime
import json

# Füge das Projektverzeichnis zum Pfad hinzu
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importiere die Komponenten
from gui.components.exchange_selector import ExchangeSelector
from gui.components.pair_selector import PairSelector
from gui.components.channel_selector import ChannelSelector
from gui.components.data_display import DataDisplay
from gui.utils.websocket_manager import WebSocketManager
from gui.utils.data_processor import DataProcessor

# Konfiguriere die Streamlit-Seite
st.set_page_config(
    page_title="WebSocket Data Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisiere Session State für persistente Daten
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if 'websocket_manager' not in st.session_state:
    st.session_state.websocket_manager = None
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor(max_buffer_size=10000)
if 'update_thread' not in st.session_state:
    st.session_state.update_thread = None
if 'stop_thread' not in st.session_state:
    st.session_state.stop_thread = False

def on_data_received(data):
    """
    Callback-Funktion für empfangene WebSocket-Daten
    
    Args:
        data: Die empfangenen Daten
    """
    if st.session_state.data_processor:
        st.session_state.data_processor.process_data(data)

def update_data_loop():
    """
    Hintergrund-Thread zur regelmäßigen Aktualisierung der Daten
    """
    while not st.session_state.stop_thread:
        # Aktualisiere die Daten im Session State
        if st.session_state.data_processor:
            st.session_state.data = st.session_state.data_processor.get_current_data()
        
        # Warte kurz, um CPU-Last zu reduzieren
        time.sleep(0.5)

def connect_websocket():
    """
    Verbindet mit dem WebSocket-Server
    """
    # Hole die ausgewählten Werte
    exchange = st.session_state.exchange_selector.get_selected_exchange()
    market_type = st.session_state.exchange_selector.get_selected_market_type()
    symbol = st.session_state.pair_selector.get_selected_symbol()
    channels = st.session_state.channel_selector.get_selected_channels()
    
    # Erstelle den WebSocket-Manager, falls noch nicht vorhanden
    if not st.session_state.websocket_manager:
        st.session_state.websocket_manager = WebSocketManager()
    
    # Setze den Callback für empfangene Daten
    st.session_state.websocket_manager.set_data_callback(on_data_received)
    
    # Verbinde mit dem WebSocket-Server
    success = st.session_state.websocket_manager.connect(
        exchange=exchange,
        market_type=market_type,
        symbol=symbol,
        channels=channels
    )
    
    if success:
        st.session_state.connected = True
        
        # Starte den Update-Thread, falls noch nicht gestartet
        if not st.session_state.update_thread or not st.session_state.update_thread.is_alive():
            st.session_state.stop_thread = False
            st.session_state.update_thread = threading.Thread(target=update_data_loop)
            st.session_state.update_thread.daemon = True
            st.session_state.update_thread.start()
        
        return True
    else:
        st.session_state.connected = False
        return False

def disconnect_websocket():
    """
    Trennt die Verbindung zum WebSocket-Server
    """
    if st.session_state.websocket_manager:
        st.session_state.websocket_manager.disconnect()
    
    # Stoppe den Update-Thread
    st.session_state.stop_thread = True
    
    # Setze den Verbindungsstatus zurück
    st.session_state.connected = False

def save_data():
    """
    Speichert die aktuellen Daten in eine CSV-Datei
    """
    if st.session_state.data_processor and not st.session_state.data.empty:
        exchange = st.session_state.exchange_selector.get_selected_exchange()
        symbol = st.session_state.pair_selector.get_selected_symbol()
        
        # Speichere die Daten
        filename = st.session_state.data_processor.save_to_csv(
            data=st.session_state.data,
            prefix=f"{exchange}_{symbol}"
        )
        
        return filename
    
    return None

def clear_data():
    """
    Löscht die aktuellen Daten
    """
    if st.session_state.data_processor:
        st.session_state.data_processor.clear_buffer()
        st.session_state.data = pd.DataFrame()

def main():
    """
    Hauptfunktion der Anwendung
    """
    # Titel der Anwendung
    st.title("WebSocket Data Explorer")
    
    # Sidebar für die Konfiguration
    with st.sidebar:
        st.header("Konfiguration")
        
        # Exchange-Auswahl
        if 'exchange_selector' not in st.session_state:
            st.session_state.exchange_selector = ExchangeSelector()
        
        exchange, market_type = st.session_state.exchange_selector.render()
        
        # Pair-Auswahl
        if 'pair_selector' not in st.session_state:
            st.session_state.pair_selector = PairSelector()
        
        symbol = st.session_state.pair_selector.render(exchange, market_type)
        
        # Channel-Auswahl
        if 'channel_selector' not in st.session_state:
            st.session_state.channel_selector = ChannelSelector()
        
        channels = st.session_state.channel_selector.render(exchange, market_type)
        
        # Verbindungs-Steuerung
        st.header("Verbindung")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not st.session_state.connected:
                if st.button("Verbinden", use_container_width=True):
                    with st.spinner("Verbinde..."):
                        if connect_websocket():
                            st.success("Verbunden!")
                        else:
                            st.error("Verbindung fehlgeschlagen!")
            else:
                if st.button("Trennen", use_container_width=True):
                    with st.spinner("Trenne Verbindung..."):
                        disconnect_websocket()
                        st.success("Verbindung getrennt!")
        
        with col2:
            if st.button("Daten löschen", use_container_width=True):
                clear_data()
                st.success("Daten gelöscht!")
        
        # Daten speichern
        if not st.session_state.data.empty:
            if st.button("Daten speichern", use_container_width=True):
                with st.spinner("Speichere Daten..."):
                    filename = save_data()
                    if filename:
                        st.success(f"Daten gespeichert: {filename}")
                    else:
                        st.error("Fehler beim Speichern der Daten!")
        
        # Verbindungsstatus
        st.header("Status")
        
        if st.session_state.connected:
            st.success("Verbunden")
            
            # Zeige Verbindungsdetails
            exchange = st.session_state.exchange_selector.get_selected_exchange()
            market_type = st.session_state.exchange_selector.get_selected_market_type()
            symbol = st.session_state.pair_selector.get_selected_symbol()
            channels = st.session_state.channel_selector.get_selected_channels()
            
            st.write(f"Exchange: {exchange}")
            st.write(f"Markt: {market_type}")
            st.write(f"Symbol: {symbol}")
            st.write(f"Kanäle: {', '.join(channels)}")
            
            # Zeige Datenstatistik
            if not st.session_state.data.empty:
                st.write(f"Datenpunkte: {len(st.session_state.data)}")
                
                if 'timestamp' in st.session_state.data.columns:
                    latest_time = st.session_state.data['timestamp'].max()
                    st.write(f"Letzte Aktualisierung: {latest_time.strftime('%H:%M:%S')}")
        else:
            st.warning("Nicht verbunden")
    
    # Hauptbereich für die Datenanzeige
    if 'data_display' not in st.session_state:
        st.session_state.data_display = DataDisplay()
    
    # Zeige die Daten an
    if st.session_state.connected and not st.session_state.data.empty:
        exchange = st.session_state.exchange_selector.get_selected_exchange()
        symbol = st.session_state.pair_selector.get_selected_symbol()
        
        st.session_state.data_display.render(
            data=st.session_state.data,
            symbol=symbol,
            exchange=exchange
        )
    else:
        st.session_state.data_display.render_empty_state()

if __name__ == "__main__":
    main() 