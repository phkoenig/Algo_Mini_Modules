"""
Exchange Selector - Komponente zur Auswahl der Exchange

Diese Komponente bietet eine Benutzeroberfläche zur Auswahl der Exchange und des Markttyps.
"""

import streamlit as st
import sys
import os

# Füge das Root-Verzeichnis zum Pfad hinzu, damit wir die Module importieren können
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class ExchangeSelector:
    """Komponente zur Auswahl der Exchange"""
    
    def __init__(self):
        """Initialisiert die Exchange-Selector-Komponente"""
        # Initialisiere Session State für persistente Daten
        if 'selected_exchange' not in st.session_state:
            st.session_state.selected_exchange = "KuCoin"
        if 'selected_market_type' not in st.session_state:
            st.session_state.selected_market_type = "futures"
    
    def render(self):
        """
        Rendert die Exchange-Selector-Komponente
        
        Returns:
            tuple: (exchange, market_type)
        """
        st.subheader("Exchange & Markt")
        
        # Exchange-Auswahl
        exchange = st.selectbox(
            "Exchange auswählen",
            options=["KuCoin", "BitGet"],
            index=0 if st.session_state.selected_exchange == "KuCoin" else 1,
            key="exchange_selector_box"
        )
        
        # Markttyp-Auswahl
        market_type = st.radio(
            "Markttyp",
            options=["Futures", "Spot"],
            index=0 if st.session_state.selected_market_type == "futures" else 1,
            key="market_type_selector_radio"
        )
        
        # Aktualisiere Session State
        st.session_state.selected_exchange = exchange
        st.session_state.selected_market_type = market_type.lower()
        
        return exchange, market_type.lower()
    
    def get_selected_exchange(self):
        """
        Gibt die ausgewählte Exchange zurück
        
        Returns:
            str: Die ausgewählte Exchange
        """
        return st.session_state.selected_exchange
    
    def get_selected_market_type(self):
        """
        Gibt den ausgewählten Markttyp zurück
        
        Returns:
            str: Der ausgewählte Markttyp
        """
        return st.session_state.selected_market_type 