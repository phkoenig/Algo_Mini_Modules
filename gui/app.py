"""
WebSocket Explorer - Eine Streamlit-GUI für die Verbindung zu Kryptowährungs-WebSockets

Diese Anwendung ermöglicht es, eine Verbindung zu WebSockets von KuCoin und BitGet herzustellen,
Währungspaare auszuwählen und Echtzeit-Daten zu visualisieren.
"""

import streamlit as st
import sys
import os
import time
import threading
import json
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go

# Füge das Root-Verzeichnis zum Pfad hinzu, damit wir die Module importieren können
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importiere die WebSocket-Module
from modules.Trading_Pairs.BitGet_Futures_Pairs import get_active_symbols as get_bitget_symbols
from modules.Trading_Pairs.KuCoin_Futures_Pairs import get_active_symbols as get_kucoin_symbols

# Konfiguration der Streamlit-Seite
st.set_page_config(
    page_title="WebSocket Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisiere Session State für persistente Daten
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'websocket_client' not in st.session_state:
    st.session_state.websocket_client = None
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'symbols' not in st.session_state:
    st.session_state.symbols = []
if 'selected_exchange' not in st.session_state:
    st.session_state.selected_exchange = None

# Funktionen für die WebSocket-Verbindung
def load_symbols(exchange):
    """Lädt die verfügbaren Symbole für die ausgewählte Exchange"""
    if exchange == "KuCoin":
        return get_kucoin_symbols()
    elif exchange == "BitGet":
        return get_bitget_symbols()
    return []

def connect_websocket(exchange, symbol, channels, market_type="futures"):
    """Stellt eine Verbindung zum WebSocket her"""
    # Diese Funktion wird später implementiert
    # Hier nur ein Platzhalter für den Prototyp
    st.session_state.connected = True
    st.session_state.last_update = datetime.now()
    
    # Simuliere einige Daten für den Prototyp
    def update_data():
        import random
        while st.session_state.connected:
            # Simuliere Ticker-Daten
            price = 50000 + random.uniform(-100, 100)
            volume = random.uniform(1, 10)
            timestamp = datetime.now()
            
            # Füge Daten zum DataFrame hinzu
            new_data = pd.DataFrame([{
                'timestamp': timestamp,
                'symbol': symbol,
                'price': price,
                'volume': volume,
                'exchange': exchange
            }])
            
            st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
            st.session_state.last_update = timestamp
            
            # Begrenze die Datenmenge
            if len(st.session_state.data) > 100:
                st.session_state.data = st.session_state.data.tail(100)
                
            time.sleep(1)
    
    # Starte den Update-Thread
    thread = threading.Thread(target=update_data)
    thread.daemon = True
    thread.start()
    
    return True

def disconnect_websocket():
    """Trennt die WebSocket-Verbindung"""
    st.session_state.connected = False
    st.session_state.websocket_client = None
    return True

# UI-Komponenten
def sidebar():
    """Erstellt die Sidebar mit Konfigurationsoptionen"""
    with st.sidebar:
        st.title("WebSocket Explorer")
        st.markdown("---")
        
        # Exchange-Auswahl
        exchange = st.selectbox(
            "Exchange auswählen",
            ["KuCoin", "BitGet"],
            index=0 if st.session_state.selected_exchange == "KuCoin" else 1 if st.session_state.selected_exchange == "BitGet" else 0
        )
        
        if exchange != st.session_state.selected_exchange:
            st.session_state.selected_exchange = exchange
            st.session_state.symbols = load_symbols(exchange)
        
        # Markttyp-Auswahl
        market_type = st.radio(
            "Markttyp",
            ["Futures", "Spot"],
            index=0
        )
        
        # Symbol-Auswahl mit Autovervollständigung
        if not st.session_state.symbols:
            st.session_state.symbols = load_symbols(exchange)
        
        symbol_search = st.text_input("Symbol suchen", value="BTC")
        
        # Filtere Symbole basierend auf der Suche
        filtered_symbols = [s for s in st.session_state.symbols if symbol_search.upper() in s.upper()]
        
        if filtered_symbols:
            symbol = st.selectbox(
                "Symbol auswählen",
                filtered_symbols,
                index=0
            )
        else:
            symbol = st.selectbox(
                "Symbol auswählen",
                ["Keine passenden Symbole gefunden"],
                index=0
            )
            symbol = None
        
        # Kanal-Auswahl
        channels = st.multiselect(
            "Kanäle auswählen",
            ["ticker", "kline", "orderbook", "trade"],
            default=["ticker"]
        )
        
        # Timeout-Einstellung
        timeout = st.slider(
            "Timeout (Sekunden)",
            min_value=5,
            max_value=300,
            value=60,
            step=5
        )
        
        # Verbindungs-Buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if not st.session_state.connected:
                if st.button("Verbinden", use_container_width=True, type="primary"):
                    if symbol:
                        with st.spinner(f"Verbinde zu {exchange} {symbol}..."):
                            success = connect_websocket(exchange, symbol, channels, market_type.lower())
                            if success:
                                st.success("Verbunden!")
                            else:
                                st.error("Verbindung fehlgeschlagen!")
                    else:
                        st.warning("Bitte wähle ein gültiges Symbol aus.")
        
        with col2:
            if st.session_state.connected:
                if st.button("Trennen", use_container_width=True):
                    with st.spinner("Trenne Verbindung..."):
                        success = disconnect_websocket()
                        if success:
                            st.info("Verbindung getrennt.")
        
        # Status-Anzeige
        st.markdown("---")
        st.subheader("Status")
        
        status_color = "🟢" if st.session_state.connected else "🔴"
        status_text = "Verbunden" if st.session_state.connected else "Nicht verbunden"
        
        st.markdown(f"{status_color} **{status_text}**")
        
        if st.session_state.connected and st.session_state.last_update:
            st.text(f"Letztes Update: {st.session_state.last_update.strftime('%H:%M:%S')}")

def main_content():
    """Erstellt den Hauptinhalt der Anwendung"""
    st.title("WebSocket Daten Explorer")
    
    if not st.session_state.connected:
        st.info("Bitte wähle eine Exchange und ein Symbol aus und klicke auf 'Verbinden', um Daten zu sehen.")
        
        # Zeige Beispiel-Chart
        st.subheader("Beispiel-Visualisierung")
        
        # Erstelle Beispieldaten
        dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
        prices = [50000 + i * 100 + (i % 5) * 200 for i in range(30)]
        example_df = pd.DataFrame({'timestamp': dates, 'price': prices})
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=example_df['timestamp'], y=example_df['price'],
                                mode='lines+markers', name='BTC Preis'))
        fig.update_layout(title='Beispiel: Bitcoin Preisentwicklung',
                        xaxis_title='Datum',
                        yaxis_title='Preis (USD)')
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # Zeige Tabs für verschiedene Visualisierungen
        tab1, tab2, tab3 = st.tabs(["Live-Daten", "Chart", "Statistiken"])
        
        with tab1:
            st.subheader("Live WebSocket Daten")
            
            if not st.session_state.data.empty:
                st.dataframe(st.session_state.data.tail(10), use_container_width=True)
            else:
                st.info("Warte auf Daten...")
        
        with tab2:
            st.subheader("Preis-Chart")
            
            if not st.session_state.data.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=st.session_state.data['timestamp'], 
                                        y=st.session_state.data['price'],
                                        mode='lines+markers', 
                                        name='Preis'))
                fig.update_layout(title=f'{st.session_state.data["symbol"].iloc[0]} Preisentwicklung',
                                xaxis_title='Zeit',
                                yaxis_title='Preis')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Warte auf Daten für die Chart-Erstellung...")
        
        with tab3:
            st.subheader("Statistiken")
            
            if not st.session_state.data.empty:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Aktueller Preis", f"${st.session_state.data['price'].iloc[-1]:.2f}")
                
                with col2:
                    price_change = st.session_state.data['price'].iloc[-1] - st.session_state.data['price'].iloc[0]
                    st.metric("Preisänderung", f"${price_change:.2f}", 
                            delta=f"{(price_change / st.session_state.data['price'].iloc[0] * 100):.2f}%")
                
                with col3:
                    st.metric("Datenpunkte", len(st.session_state.data))
                
                # Weitere Statistiken
                st.subheader("Zusammenfassung")
                st.dataframe(st.session_state.data['price'].describe(), use_container_width=True)
            else:
                st.info("Warte auf Daten für die Statistikberechnung...")

# Hauptanwendung
def main():
    sidebar()
    main_content()

if __name__ == "__main__":
    main() 