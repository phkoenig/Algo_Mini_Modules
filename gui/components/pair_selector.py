"""
Pair Selector - Komponente zur Auswahl des Währungspaars

Diese Komponente bietet eine Benutzeroberfläche zur Auswahl des Währungspaars mit Autovervollständigung.
"""

import streamlit as st
import sys
import os

# Füge das Root-Verzeichnis zum Pfad hinzu, damit wir die Module importieren können
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Importiere die Trading Pairs Module
from modules.Trading_Pairs.BitGet_Futures_Pairs import get_active_symbols as get_bitget_symbols
from modules.Trading_Pairs.KuCoin_Futures_Pairs import get_active_symbols as get_kucoin_symbols

class PairSelector:
    """Komponente zur Auswahl des Währungspaars"""
    
    def __init__(self):
        """Initialisiert die Pair-Selector-Komponente"""
        # Initialisiere Session State für persistente Daten
        if 'symbols' not in st.session_state:
            st.session_state.symbols = []
        if 'selected_symbol' not in st.session_state:
            st.session_state.selected_symbol = None
        if 'symbol_search' not in st.session_state:
            st.session_state.symbol_search = "BTC"
    
    def load_symbols(self, exchange, market_type="futures"):
        """
        Lädt die verfügbaren Symbole für die ausgewählte Exchange
        
        Args:
            exchange: Die Exchange (KuCoin oder BitGet)
            market_type: Der Markttyp (futures oder spot)
            
        Returns:
            list: Die verfügbaren Symbole
        """
        try:
            if exchange == "KuCoin":
                symbols = get_kucoin_symbols()
            elif exchange == "BitGet":
                symbols = get_bitget_symbols()
            else:
                symbols = []
            
            # Filtere nach Markttyp, falls notwendig
            # Hier könnte eine weitere Filterung nach Spot/Futures erfolgen,
            # falls die get_active_symbols-Funktionen nicht bereits nach Markttyp filtern
            
            st.session_state.symbols = symbols
            return symbols
            
        except Exception as e:
            st.error(f"Fehler beim Laden der Symbole: {str(e)}")
            return []
    
    def render(self, exchange, market_type="futures"):
        """
        Rendert die Pair-Selector-Komponente
        
        Args:
            exchange: Die Exchange (KuCoin oder BitGet)
            market_type: Der Markttyp (futures oder spot)
            
        Returns:
            str: Das ausgewählte Symbol
        """
        st.subheader("Währungspaar")
        
        # Lade Symbole, falls noch nicht geladen oder Exchange geändert
        if not st.session_state.symbols or st.session_state.get('last_exchange') != exchange:
            st.session_state.symbols = self.load_symbols(exchange, market_type)
            st.session_state.last_exchange = exchange
        
        # Suchfeld für Symbole
        symbol_search = st.text_input(
            "Symbol suchen",
            value=st.session_state.symbol_search,
            key="symbol_search_input"
        )
        
        # Aktualisiere Session State
        st.session_state.symbol_search = symbol_search
        
        # Filtere Symbole basierend auf der Suche
        filtered_symbols = [s for s in st.session_state.symbols if symbol_search.upper() in s.upper()]
        
        # Zeige Anzahl der gefundenen Symbole
        st.caption(f"{len(filtered_symbols)} Symbole gefunden")
        
        # Symbol-Auswahl
        if filtered_symbols:
            # Bestimme den Index für die Vorauswahl
            default_index = 0
            if st.session_state.selected_symbol in filtered_symbols:
                default_index = filtered_symbols.index(st.session_state.selected_symbol)
            
            symbol = st.selectbox(
                "Symbol auswählen",
                filtered_symbols,
                index=default_index,
                key="symbol_selector"
            )
        else:
            st.warning("Keine passenden Symbole gefunden. Bitte ändere deine Suche.")
            symbol = None
        
        # Aktualisiere Session State
        st.session_state.selected_symbol = symbol
        
        # Zeige zusätzliche Informationen zum ausgewählten Symbol
        if symbol:
            st.success(f"Ausgewähltes Symbol: {symbol}")
            
            # Hier könnten weitere Informationen zum Symbol angezeigt werden,
            # z.B. aktuelle Preise, Handelsvolumen, etc.
        
        return symbol
    
    def get_selected_symbol(self):
        """
        Gibt das ausgewählte Symbol zurück
        
        Returns:
            str: Das ausgewählte Symbol
        """
        return st.session_state.selected_symbol 