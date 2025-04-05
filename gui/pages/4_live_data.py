import streamlit as st
from gui.utils import load_css, create_sidebar
from modules.Websocket_Raw_Data.Bitget_Websocket_Raw_Data import BitgetWebSocket
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LiveData")

def price_callback(data):
    """Callback function to update the price in session state"""
    try:
        if "data" in data and len(data["data"]) > 0:
            price_data = data["data"][0]
            if "lastPr" in price_data:
                st.session_state.current_price = float(price_data["lastPr"])
                st.session_state.last_update = time.time()
                logger.info(f"Price updated: {st.session_state.current_price}")
    except Exception as e:
        logger.error(f"Error processing price data: {e}")

def cleanup_websocket():
    """Clean up WebSocket connection"""
    if 'ws_client' in st.session_state and st.session_state.ws_client:
        try:
            st.session_state.ws_client.ws.close()
            st.session_state.ws_client = None
            logger.info("WebSocket connection closed")
        except Exception as e:
            logger.error(f"Error closing WebSocket: {e}")

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
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None
    
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
            # Clean up symbol (remove _UMCBL suffix if present)
            symbol = st.session_state.selected_trading_pair
            if "_" in symbol:
                symbol = symbol.split("_")[0]
            
            st.caption(f"Symbol: {symbol}")
            
            # Initialize WebSocket connection if not already done
            if st.session_state.ws_client is None:
                try:
                    logger.info(f"Initializing WebSocket for {symbol}")
                    
                    # Create WebSocket client with verbose mode for debugging
                    ws_client = BitgetWebSocket(verbose=True)
                    
                    # Override the on_message method to use our callback
                    def custom_on_message(ws, message):
                        try:
                            data = json.loads(message)
                            logger.debug(f"Received message: {data}")
                            price_callback(data)
                            # Force Streamlit to update
                            st.experimental_rerun()
                        except Exception as e:
                            logger.error(f"Error in WebSocket message handler: {e}")
                    
                    ws_client.on_message = custom_on_message
                    
                    # Connect and subscribe to ticker
                    ws_client.connect(symbol, ["ticker"])
                    logger.info("WebSocket connected and subscribed")
                    
                    # Store the client in session state
                    st.session_state.ws_client = ws_client
                    
                except Exception as e:
                    logger.error(f"Error initializing WebSocket: {e}")
                    st.error(f"Error initializing WebSocket: {e}")
            
            # Display current price if available
            if st.session_state.current_price is not None:
                # Calculate time since last update
                time_since_update = time.time() - (st.session_state.last_update or time.time())
                
                # Format the price display
                price_display = f"${st.session_state.current_price:,.4f}"
                if time_since_update > 5:  # If no update for 5 seconds
                    st.warning(price_display + " (delayed)")
                else:
                    st.metric(
                        "Price",
                        price_display,
                        delta=None  # We could add price change here later
                    )
            else:
                st.info("Waiting for price data...")
                
        else:
            st.warning("Please select a trading pair first")
            cleanup_websocket()  # Clean up any existing connection

if __name__ == "__main__":
    show()