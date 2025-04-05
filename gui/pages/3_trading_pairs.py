import streamlit as st
from gui.utils import load_css, create_sidebar
import pandas as pd
import requests
from modules.Trading_Pairs.BitGet_Futures_Pairs_Extended import get_futures_pairs_extended as get_bitget_pairs_extended
from modules.Trading_Pairs.KuCoin_Futures_Pairs_Extended import get_futures_pairs_extended as get_kucoin_pairs_extended

def show():
    # Load CSS
    load_css()
    
    # Create sidebar
    create_sidebar()
    
    # Main content
    st.title("Trading Pairs")
    
    # Initialize session state for selected pair if not exists
    if 'selected_trading_pair' not in st.session_state:
        st.session_state.selected_trading_pair = None
    
    # Check if an exchange is active
    if 'active_exchange' not in st.session_state:
        st.warning("Please activate an exchange in the Account Info page first.")
        return
        
    active_exchange = st.session_state.active_exchange
    
    try:
        # Get and display trading pairs based on active exchange
        if active_exchange == "BitGet":
            df = get_bitget_pairs_extended()
            df = df[df['trading_active'] == True]  # Filter nur aktive Pairs
            st.subheader("BitGet Futures Trading Pairs")
        elif active_exchange == "KuCoin":
            df = get_kucoin_pairs_extended()
            df = df[df['trading_active'] == True]  # Filter nur aktive Pairs
            st.subheader("KuCoin Futures Trading Pairs")
        else:
            st.error(f"Unknown exchange: {active_exchange}")
            return
            
        # Add search box
        search_term = st.text_input(
            "🔍 Search by name or symbol",
            help="Search in both human readable names (like 'Bitcoin') and symbols (like 'BTC')"
        )
        
        if search_term:
            # Suche in allen relevanten Spalten
            mask = df['human_readable_name'].str.contains(search_term, case=False) | \
                  df['symbol'].str.contains(search_term, case=False) | \
                  df['base_currency'].str.contains(search_term, case=False)
            df = df[mask]
            st.caption(f"Found {len(df)} matching pairs")
        
        # Display the DataFrame
        if not df.empty:
            # Convert DataFrame to display format
            display_df = df[['symbol', 'human_readable_name', 'base_currency', 'quote_currency', 'market_type']].rename(columns={
                'symbol': 'Symbol',
                'human_readable_name': 'Name',
                'base_currency': 'Base Currency',
                'quote_currency': 'Quote Currency',
                'market_type': 'Market Type'
            })

            # Add selection column
            display_df.insert(0, 'Select', False)
            
            # Create the editable dataframe
            edited_df = st.data_editor(
                display_df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Select": st.column_config.CheckboxColumn(
                        "Select",
                        help="Select trading pair",
                        default=False
                    )
                }
            )
            
            # Handle selection
            selected_rows = edited_df[edited_df['Select']]['Symbol'].tolist()
            
            # Update session state based on selection
            if len(selected_rows) > 0:
                # Take the first selected row if multiple are selected
                new_selection = selected_rows[0]
                if new_selection != st.session_state.selected_trading_pair:
                    st.session_state.selected_trading_pair = new_selection
                    st.success(f"Selected trading pair: {new_selection}")
            else:
                st.session_state.selected_trading_pair = None

        else:
            st.warning("No trading pairs found for the selected exchange.")
            
    except Exception as e:
        st.error(f"Error fetching trading pairs: {str(e)}")

if __name__ == "__main__":
    show()