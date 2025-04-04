import streamlit as st
from gui.utils import load_css, create_sidebar
from modules.Account_Info.BitGet_Account_Info import BitGetAccountInfo
from modules.Account_Info.KuCoin_Account_Info import KuCoinAccountInfo
from modules.Credentials.BitGet_Credentials import get_credentials as get_bitget_credentials
from modules.Credentials.KuCoin_Credentials import get_credentials as get_kucoin_credentials
import pandas as pd

def show():
    # Load CSS
    load_css()
    
    # Create sidebar
    create_sidebar()
    
    # Initialize session state for active exchange if not exists
    if 'active_exchange' not in st.session_state:
        st.session_state.active_exchange = None
    
    # Main content
    st.title("Account Connection")
    
    # Create tabs for different exchanges
    bitget_tab, kucoin_tab, bitunix_tab = st.tabs(["BitGet", "KuCoin", "BitUnix"])
    
    with bitget_tab:
        # Add buttons in columns
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh BitGet Data"):
                st.rerun()
        with col2:
            if st.button("🔌 Activate BitGet", type="primary" if st.session_state.active_exchange == "BitGet" else "secondary"):
                st.session_state.active_exchange = "BitGet"
                st.success("BitGet activated!")
            
        try:
            # Get BitGet credentials
            credentials = get_bitget_credentials()
            client = BitGetAccountInfo(
                credentials['apiKey'],
                credentials['secretKey'],
                credentials['passphrase']
            )
            
            # Get account summary
            summary = client.get_account_summary_json()
            
            # Display total portfolio value
            st.header("Portfolio Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Total Portfolio Value",
                    f"${summary['total_values']['total_portfolio_value_usdt']:,.2f}",
                    "USDT"
                )
            with col2:
                st.metric(
                    "BTC Holdings Value",
                    f"${summary['total_values']['btc_holdings_usdt']:,.2f}",
                    "USDT"
                )
            with col3:
                st.metric(
                    "Direct USDT Holdings",
                    f"${summary['total_values']['direct_usdt_holdings']:,.2f}",
                    "USDT"
                )
            
            # Display account status
            st.header("Account Status")
            status_cols = st.columns(3)
            for idx, (account_type, status) in enumerate(summary['account_status'].items()):
                with status_cols[idx % 3]:
                    st.metric(account_type.capitalize(), status)
            
            # Display spot accounts
            if summary['accounts']['spot']:
                st.header("Spot Accounts")
                spot_df = pd.DataFrame(summary['accounts']['spot'])
                st.dataframe(
                    spot_df,
                    column_config={
                        "currency": "Currency",
                        "available": st.column_config.NumberColumn("Available", format="%.8f"),
                        "holds": st.column_config.NumberColumn("Holds", format="%.8f"),
                        "total": st.column_config.NumberColumn("Total", format="%.8f")
                    },
                    hide_index=True
                )
            
            # Display futures accounts
            if summary['accounts']['futures']:
                st.header("Futures Account")
                futures = summary['accounts']['futures'][0]
                futures_cols = st.columns(3)
                with futures_cols[0]:
                    st.metric("Available Margin", f"{futures['available']:,.2f} USDT")
                    st.metric("Position Margin", f"{futures['position_margin']:,.2f} USDT")
                with futures_cols[1]:
                    st.metric("Margin Balance", f"{futures['margin_balance']:,.2f} USDT")
                    st.metric("Order Margin", f"{futures['order_margin']:,.2f} USDT")
                with futures_cols[2]:
                    st.metric("Unrealized PNL", f"{futures['unrealized_pnl']:,.2f} USDT")
                    st.metric("Realized PNL", f"{futures['realized_pnl']:,.2f} USDT")
                    
        except Exception as e:
            st.error(f"Error loading BitGet account information: {str(e)}")
            if "Credentials nicht vollständig" in str(e):
                st.warning("Please set up your BitGet API credentials in the .env file")
            
    with kucoin_tab:
        # Add buttons in columns
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh KuCoin Data"):
                st.rerun()
        with col2:
            if st.button("🔌 Activate KuCoin", type="primary" if st.session_state.active_exchange == "KuCoin" else "secondary"):
                st.session_state.active_exchange = "KuCoin"
                st.success("KuCoin activated!")
            
        try:
            # Get KuCoin credentials
            credentials = get_kucoin_credentials()
            client = KuCoinAccountInfo(
                credentials['api_key'],
                credentials['secret_key'],
                credentials['passphrase']
            )
            
            # Get account summary
            summary = client.get_account_summary_json()
            
            # Display total portfolio value
            st.header("Portfolio Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Total Portfolio Value",
                    f"${summary['total_values']['total_portfolio_value_usdt']:,.2f}",
                    "USDT"
                )
            with col2:
                st.metric(
                    "BTC Holdings Value",
                    f"${summary['total_values']['btc_holdings_usdt']:,.2f}",
                    "USDT"
                )
            with col3:
                st.metric(
                    "Direct USDT Holdings",
                    f"${summary['total_values']['direct_usdt_holdings']:,.2f}",
                    "USDT"
                )
            
            # Display account status
            st.header("Account Status")
            status_cols = st.columns(3)
            for idx, (account_type, status) in enumerate(summary['account_status'].items()):
                with status_cols[idx % 3]:
                    st.metric(account_type.capitalize(), status)
            
            # Display spot accounts
            if summary['accounts']['spot']:
                st.header("Spot Accounts")
                spot_df = pd.DataFrame(summary['accounts']['spot'])
                st.dataframe(
                    spot_df,
                    column_config={
                        "currency": "Currency",
                        "available": st.column_config.NumberColumn("Available", format="%.8f"),
                        "holds": st.column_config.NumberColumn("Holds", format="%.8f"),
                        "total": st.column_config.NumberColumn("Total", format="%.8f")
                    },
                    hide_index=True
                )
            
            # Display futures accounts
            if summary['accounts']['futures']:
                st.header("Futures Account")
                futures = summary['accounts']['futures'][0]
                futures_cols = st.columns(3)
                with futures_cols[0]:
                    st.metric("Available Margin", f"{futures['available']:,.2f} USDT")
                    st.metric("Position Margin", f"{futures['position_margin']:,.2f} USDT")
                with futures_cols[1]:
                    st.metric("Margin Balance", f"{futures['margin_balance']:,.2f} USDT")
                    st.metric("Order Margin", f"{futures['order_margin']:,.2f} USDT")
                with futures_cols[2]:
                    st.metric("Unrealized PNL", f"{futures['unrealized_pnl']:,.2f} USDT")
                    st.metric("Realized PNL", f"{futures['realized_pnl']:,.2f} USDT")
                    
        except Exception as e:
            st.error(f"Error loading KuCoin account information: {str(e)}")
            if "KuCoin API-Zugangsdaten fehlen" in str(e):
                st.warning("Please set up your KuCoin API credentials in the .env file")
        
    with bitunix_tab:
        pass

if __name__ == "__main__":
    show()