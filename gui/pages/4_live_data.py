import streamlit as st
from gui.utils import load_css, create_sidebar
from modules.Websocket_Raw_Data.Bitget_Websocket_Raw_Data import BitgetWebSocket
import json

def price_callback(data):
    """Callback function to update the price in session state"""
    try:
        if "data" in data and len(data["data"]) > 0:
            price_data = data["data"][0]
            if "lastPr" in price_data:
                st.session_state.current_price = float(price_data["lastPr"])
    except Exception as e:
        st.error(f"Error processing price data: {e}")

def show():
    # Load CSS
    load_css()
    
    # Create sidebar
    create_sidebar()
    
    # Main content
    st.title("Live Market Data")
    
    # Initialize session state for WebSocket and price
    if 'ws_client' not in st.session_state:
        st.session_state.ws_client = None
    if 'current_price' not in st.session_state:
        st.session_state.current_price = None
    
    # Create two columns - main content (90%) and ticker (10%)
    main_col, ticker_col = st.columns([90, 10])
    
    # Main column for chart (90%)
    with main_col:
        st.subheader("Chart Area")
        st.info("Chart will be implemented here")
    
    # Ticker column (10%)
    with ticker_col:
        st.subheader("Live Price")
        
        # Check if we have a trading pair selected
        if 'selected_trading_pair' in st.session_state and st.session_state.selected_trading_pair:
            # Display current price if available
            if st.session_state.current_price is not None:
                st.metric(
                    "Price",
                    f"${st.session_state.current_price:,.2f}"
                )
            else:
                st.info("Waiting for price data...")
                
            # Initialize WebSocket connection if not already done
            if st.session_state.ws_client is None:
                try:
                    # Create WebSocket client
                    ws_client = BitgetWebSocket(verbose=False)
                    
                    # Override the on_message method to use our callback
                    def custom_on_message(ws, message):
                        try:
                            data = json.loads(message)
                            price_callback(data)
                        except Exception as e:
                            st.error(f"Error in WebSocket message handler: {e}")
                    
                    ws_client.on_message = custom_on_message
                    
                    # Connect and subscribe to ticker
                    ws_client.connect(st.session_state.selected_trading_pair, ["ticker"])
                    
                    # Store the client in session state
                    st.session_state.ws_client = ws_client
                    
                except Exception as e:
                    st.error(f"Error initializing WebSocket: {e}")
        else:
            st.warning("Please select a trading pair first")

if __name__ == "__main__":
    show()