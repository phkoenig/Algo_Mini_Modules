"""
Channel Selector - Komponente zur Auswahl der WebSocket-Kanäle

Diese Komponente bietet eine Benutzeroberfläche zur Auswahl der zu abonnierenden WebSocket-Kanäle.
"""

import streamlit as st

class ChannelSelector:
    """Komponente zur Auswahl der WebSocket-Kanäle"""
    
    def __init__(self):
        """Initialisiert die Channel-Selector-Komponente"""
        # Initialisiere Session State für persistente Daten
        if 'selected_channels' not in st.session_state:
            st.session_state.selected_channels = ["ticker"]
    
    def get_available_channels(self, exchange, market_type="futures"):
        """
        Gibt die verfügbaren Kanäle für die ausgewählte Exchange zurück
        
        Args:
            exchange: Die Exchange (KuCoin oder BitGet)
            market_type: Der Markttyp (futures oder spot)
            
        Returns:
            dict: Ein Dictionary mit Kanal-Namen und Beschreibungen
        """
        # Gemeinsame Kanäle für alle Exchanges
        common_channels = {
            "ticker": "Ticker-Daten (Preis, Volumen, etc.)",
            "trade": "Trade-Daten (einzelne Trades)",
            "orderbook": "Orderbook-Daten (Kauf- und Verkaufsaufträge)"
        }
        
        # Exchange-spezifische Kanäle
        if exchange == "KuCoin":
            if market_type == "futures":
                return {
                    **common_channels,
                    "kline": "Kline/Candlestick-Daten",
                    "execution": "Ausführungsdaten",
                    "funding": "Funding-Daten"
                }
            else:  # spot
                return {
                    **common_channels,
                    "kline": "Kline/Candlestick-Daten",
                    "match": "Match-Daten",
                    "level2": "Level-2-Marktdaten"
                }
        
        elif exchange == "BitGet":
            if market_type == "futures":
                return {
                    **common_channels,
                    "candle": "Candlestick-Daten",
                    "depth": "Tiefendaten des Orderbooks",
                    "funding_rate": "Funding-Rate-Daten"
                }
            else:  # spot
                return {
                    **common_channels,
                    "candle": "Candlestick-Daten",
                    "depth": "Tiefendaten des Orderbooks"
                }
        
        # Fallback für unbekannte Exchanges
        return common_channels
    
    def render(self, exchange, market_type="futures"):
        """
        Rendert die Channel-Selector-Komponente
        
        Args:
            exchange: Die Exchange (KuCoin oder BitGet)
            market_type: Der Markttyp (futures oder spot)
            
        Returns:
            list: Die ausgewählten Kanäle
        """
        st.subheader("Kanäle")
        
        # Hole verfügbare Kanäle
        available_channels = self.get_available_channels(exchange, market_type)
        
        # Erstelle eine Liste von Kanal-Namen und Beschreibungen für die Anzeige
        channel_options = list(available_channels.keys())
        channel_descriptions = [f"{channel} - {desc}" for channel, desc in available_channels.items()]
        
        # Zeige Informationen zu den Kanälen
        with st.expander("Kanal-Informationen", expanded=False):
            for channel, desc in available_channels.items():
                st.markdown(f"**{channel}**: {desc}")
        
        # Kanal-Auswahl
        selected_channels = st.multiselect(
            "Kanäle auswählen",
            channel_options,
            default=st.session_state.selected_channels,
            format_func=lambda x: f"{x} - {available_channels[x]}",
            key="channel_selector"
        )
        
        # Stelle sicher, dass mindestens ein Kanal ausgewählt ist
        if not selected_channels:
            st.warning("Bitte wähle mindestens einen Kanal aus.")
            selected_channels = ["ticker"]  # Standardkanal
        
        # Aktualisiere Session State
        st.session_state.selected_channels = selected_channels
        
        return selected_channels
    
    def get_selected_channels(self):
        """
        Gibt die ausgewählten Kanäle zurück
        
        Returns:
            list: Die ausgewählten Kanäle
        """
        return st.session_state.selected_channels 