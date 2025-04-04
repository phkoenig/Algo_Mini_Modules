import streamlit as st
import time
import requests
from datetime import datetime
from modules.Websocket_Raw_Data.Bitget_Websocket_Raw_Data import BitgetWebSocket
from modules.Websocket_Raw_Data.KuCoin_Websocket_Raw_Data import KuCoinWebSocket
from modules.Account_Info.KuCoin_Account_Info import KuCoinAccountInfo
from modules.Account_Info.BitGet_Account_Info import BitGetAccountInfo
from modules.Credentials.BitGet_Credentials import validate_bitget_credentials
from modules.Credentials.KuCoin_Credentials import validate_kucoin_credentials

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=3)
        return True
    except requests.RequestException:
        return False

def check_exchange_api(url: str, exchange: str):
    try:
        if exchange == "KuCoin":
            response = requests.get("https://api.kucoin.com/api/v1/timestamp")
        else:  # BitGet
            response = requests.get("https://api.bitget.com/api/spot/v1/public/time")
        return response.status_code == 200
    except:
        return False

def check_websocket(exchange: str):
    try:
        if exchange == "KuCoin":
            ws = KuCoinWebSocket(market_type="futures", verbose=False)
            ws.connect("BTCUSDT", ["ticker"])
        else:  # BitGet
            ws = BitgetWebSocket(verbose=False)
            ws.connect("BTCUSDT", ["ticker"])
        return True
    except:
        return False

def display_status(label: str, status: bool):
    color = "#1B4332" if status else "#3D1C1C"
    icon = "✅" if status else "❌"
    st.markdown(
        f"""
        <div style="padding: 10px; border-radius: 5px; background-color: {color};">
            {label}: {icon}
        </div>
        """,
        unsafe_allow_html=True
    )

def display_account_info(exchange: str):
    try:
        if exchange == "KuCoin":
            client = KuCoinAccountInfo(
                st.secrets["KUCOIN_API_KEY"],
                st.secrets["KUCOIN_SECRET_KEY"],
                st.secrets["KUCOIN_PASSPHRASE"]
            )
            
            # Get spot accounts
            spot_accounts = client.get_spot_accounts()
            if spot_accounts:
                st.markdown("### Account Information")
                st.markdown("#### Spot Account")
                for account in spot_accounts:
                    balance = float(account.get('balance', '0'))
                    if balance > 0:
                        st.write(f"{account.get('currency', 'N/A')}: {balance:.8f}")
            
            # Get futures account
            futures = client.get_futures_overview("USDT")
            if futures:
                st.markdown("#### Futures Account")
                st.write(f"Account Equity: {futures.get('accountEquity', 'N/A')} USDT")
                st.write(f"Available Balance: {futures.get('availableBalance', 'N/A')} USDT")
                st.write(f"Unrealized PNL: {futures.get('unrealisedPNL', 'N/A')} USDT")
        
        elif exchange == "BitGet":
            client = BitGetAccountInfo(
                st.secrets["BITGET_API_KEY"],
                st.secrets["BITGET_SECRET_KEY"],
                st.secrets["BITGET_PASSPHRASE"]
            )
            
            # Get both spot and futures info
            account_info = client.get_account_overview()
            if account_info:
                st.markdown("### Account Information")
                
                # Spot info
                if account_info.get("spot"):
                    st.markdown("#### Spot Account")
                    for asset in account_info["spot"].get("data", []):
                        balance = float(asset.get('available', '0'))
                        if balance > 0:
                            st.write(f"{asset.get('coinName', 'N/A')}: {balance:.8f}")
                
                # Futures info
                if account_info.get("futures"):
                    futures_data = account_info["futures"].get("data", {})
                    if futures_data:
                        st.markdown("#### Futures Account")
                        st.write(f"Account Equity: {futures_data.get('equity', 'N/A')} USDT")
                        st.write(f"Available Balance: {futures_data.get('available', 'N/A')} USDT")
                        st.write(f"Unrealized PNL: {futures_data.get('unrealizedPL', 'N/A')} USDT")
    
    except Exception as e:
        st.error(f"Error getting {exchange} account info: {str(e)}")

def main():
    st.set_page_config(
        page_title="Algo Trading System",
        page_icon="🏠",
        layout="wide"
    )

    st.title("🏠 System Status")
    st.write("Last update:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("KuCoin")
        display_status("Internet Connection", check_internet_connection())
        display_status("API Connection", check_exchange_api("https://api.kucoin.com", "KuCoin"))
        display_status("WebSocket Connection", check_websocket("KuCoin"))
        display_status("API Credentials", validate_kucoin_credentials(verbose=False)["all_valid"])
        
        # Display account info if all checks pass
        if all([
            check_internet_connection(),
            check_exchange_api("https://api.kucoin.com", "KuCoin"),
            validate_kucoin_credentials(verbose=False)["all_valid"]
        ]):
            display_account_info("KuCoin")

    with col2:
        st.subheader("BitGet")
        display_status("Internet Connection", check_internet_connection())
        display_status("API Connection", check_exchange_api("https://api.bitget.com", "BitGet"))
        display_status("WebSocket Connection", check_websocket("BitGet"))
        display_status("API Credentials", validate_bitget_credentials(verbose=False)["all_valid"])
        
        # Display account info if all checks pass
        if all([
            check_internet_connection(),
            check_exchange_api("https://api.bitget.com", "BitGet"),
            validate_bitget_credentials(verbose=False)["all_valid"]
        ]):
            display_account_info("BitGet")

    # Auto-refresh every 5 seconds
    time.sleep(5)
    st.rerun()

if __name__ == "__main__":
    main() 