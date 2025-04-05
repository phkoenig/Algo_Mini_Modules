import streamlit as st
from gui.utils import load_css, create_sidebar
import pandas as pd
import requests

def get_bitget_pairs_direct():
    """Direct implementation to fetch and format BitGet pairs"""
    url = "https://api.bitget.com/api/mix/v1/market/contracts"
    pairs = []
    
    # Fetch USDT-M futures
    response = requests.get(url, params={"productType": "umcbl"})
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == "00000" and data.get("data"):
            for pair in data["data"]:
                if pair.get("symbolStatus") == "normal":
                    pairs.append({
                        "symbol": pair.get("symbol"),
                        "base_coin": pair.get("baseCoin"),
                        "quote_coin": pair.get("quoteCoin"),
                        "type": "USDT-M"
                    })
    
    # Fetch Coin-M futures
    response = requests.get(url, params={"productType": "dmcbl"})
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == "00000" and data.get("data"):
            for pair in data["data"]:
                if pair.get("symbolStatus") == "normal":
                    pairs.append({
                        "symbol": pair.get("symbol"),
                        "base_coin": pair.get("baseCoin"),
                        "quote_coin": pair.get("quoteCoin"),
                        "type": "Coin-M"
                    })
    
    return sorted(pairs, key=lambda x: x["symbol"])

def show():
    # Load CSS
    load_css()
    
    # Create sidebar
    create_sidebar()
    
    # Main content
    st.title("Trading Pairs")
    
    # Check if an exchange is active
    if 'active_exchange' not in st.session_state:
        st.warning("Please activate an exchange in the Account Info page first.")
        return
        
    active_exchange = st.session_state.active_exchange
    
    try:
        # Get and display trading pairs based on active exchange
        if active_exchange == "BitGet":
            pairs = get_bitget_pairs_direct()
            st.subheader("BitGet Futures Trading Pairs")
        elif active_exchange == "KuCoin":
            from modules.Trading_Pairs.KuCoin_Futures_Pairs import get_active_symbols_with_info as get_kucoin_pairs
            pairs = get_kucoin_pairs()
            st.subheader("KuCoin Futures Trading Pairs")
        else:
            st.error(f"Unknown exchange: {active_exchange}")
            return
            
        # Convert pairs to DataFrame for nice display
        if pairs:
            df = pd.DataFrame(pairs)
            st.dataframe(
                df[['symbol', 'base_coin', 'quote_coin', 'type']],
                hide_index=True,
                use_container_width=True
            )
        else:
            st.warning("No trading pairs found for the selected exchange.")
            
    except Exception as e:
        st.error(f"Error fetching trading pairs: {str(e)}")

if __name__ == "__main__":
    show()