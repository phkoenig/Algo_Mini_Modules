import requests
import hmac
import base64
import time
import json
import logging
import urllib.parse
from typing import Dict, Optional
from dotenv import load_dotenv
import os
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KuCoinAccountInfo:
    def __init__(self, api_key: str, secret_key: str, passphrase: str):
        """Initialize KuCoin client with API credentials"""
        self.api_key = api_key.strip()  # Remove any whitespace
        self.secret_key = secret_key.strip()
        self.passphrase = passphrase.strip()
        
        # Base URLs for different API types
        self.futures_url = "https://api-futures.kucoin.com"
        self.spot_url = "https://api.kucoin.com"
        
        # API Endpoints
        self.futures_account_endpoint = "/api/v1/account-overview"
        self.futures_position_endpoint = "/api/v1/position"
        self.futures_positions_endpoint = "/api/v1/positions"
        self.spot_accounts_endpoint = "/api/v1/accounts"
        
        # Encrypt passphrase for API v2
        self.encrypted_passphrase = base64.b64encode(
            hmac.new(
                self.secret_key.encode('utf-8'),
                self.passphrase.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode()
        
        logger.info("KuCoin client initialized")
        
    def _generate_signature(self, timestamp: str, method: str, endpoint: str, params: Optional[Dict] = None) -> str:
        """Generate KuCoin API signature"""
        # For GET requests, add query parameters to endpoint
        if params and method.upper() == "GET":
            query_string = urllib.parse.urlencode(params)
            endpoint = f"{endpoint}?{query_string}"
            
        str_to_sign = timestamp + method.upper() + endpoint
        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode('utf-8'),
                str_to_sign.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode()
        
        return signature

    def _send_request(self, method: str, endpoint: str, params: Optional[Dict] = None, is_futures: bool = True) -> Dict:
        """Send signed request to KuCoin API"""
        timestamp = str(int(time.time() * 1000))
        
        # Generate signature
        signature = self._generate_signature(timestamp, method, endpoint, params)
        
        headers = {
            "KC-API-KEY": self.api_key,
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": timestamp,
            "KC-API-PASSPHRASE": self.encrypted_passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json"
        }
        
        base_url = self.futures_url if is_futures else self.spot_url
        url = base_url + endpoint
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            else:
                response = requests.post(url, headers=headers, json=params)
            
            logger.debug(f"Request URL: {response.url}")
            logger.debug(f"Request Headers: {headers}")
            logger.debug(f"Response Status: {response.status_code}")
            logger.debug(f"Response Text: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to {endpoint}: {str(e)}")
            return {"code": -1, "msg": str(e)}

    def get_spot_accounts(self, currency: Optional[str] = None) -> Dict:
        """Get spot account information for all or a specific currency"""
        try:
            params = {"currency": currency} if currency else {}
            accounts = self._send_request("GET", self.spot_accounts_endpoint, params, is_futures=False)
            
            if accounts.get("code") == "200000":
                logger.info("Successfully retrieved spot accounts")
                return accounts["data"]
            else:
                logger.error(f"Error getting spot accounts: {accounts}")
                return {}
                
        except Exception as e:
            logger.error(f"Error in get_spot_accounts: {str(e)}")
            return {}

    def get_futures_overview(self, currency: str = "USDT") -> Dict:
        """Get futures account overview for a specific currency"""
        try:
            params = {"currency": currency}
            account_info = self._send_request("GET", self.futures_account_endpoint, params)
            
            if account_info.get("code") == "200000":
                logger.info("Successfully retrieved futures account overview")
                return account_info["data"]
            else:
                logger.error(f"Error getting futures account overview: {account_info}")
                return {}
                
        except Exception as e:
            logger.error(f"Error in get_futures_overview: {str(e)}")
            return {}

    def get_position_details(self, symbol: str) -> Dict:
        """Get position details for a specific symbol"""
        try:
            params = {"symbol": symbol}
            position = self._send_request("GET", self.futures_position_endpoint, params)
            
            if position.get("code") == "200000":
                logger.info("Successfully retrieved position details")
                return position["data"]
            else:
                logger.error(f"Error getting position details: {position}")
                return {}
                
        except Exception as e:
            logger.error(f"Error in get_position_details: {str(e)}")
            return {}

    def get_all_positions(self) -> Dict:
        """Get all positions"""
        try:
            positions = self._send_request("GET", self.futures_positions_endpoint)
            
            if positions.get("code") == "200000":
                logger.info("Successfully retrieved all positions")
                return positions["data"]
            else:
                logger.error(f"Error getting positions: {positions}")
                return {}
                
        except Exception as e:
            logger.error(f"Error in get_all_positions: {str(e)}")
            return {}

    def display_account_summary(self):
        """Display a summary of the account information"""
        try:
            # Get spot account information
            spot_accounts = self.get_spot_accounts()
            if spot_accounts:
                print("\n=== Spot Account Overview ===")
                total_spot_value = 0
                for account in spot_accounts:
                    balance = float(account.get('balance', '0'))
                    if balance > 0:
                        print(f"{account.get('currency', 'N/A')}: {balance} (Available: {account.get('available', 'N/A')}, Holds: {account.get('holds', 'N/A')})")
                        if account.get('currency') == 'USDT':
                            total_spot_value += balance

            # Get futures account overview for USDT
            futures_account = self.get_futures_overview("USDT")
            if futures_account:
                print("\n=== Futures Account Overview (USDT) ===")
                print(f"Account Equity: {futures_account.get('accountEquity', 'N/A')} USDT")
                print(f"Unrealized PNL: {futures_account.get('unrealisedPNL', 'N/A')} USDT")
                print(f"Margin Balance: {futures_account.get('marginBalance', 'N/A')} USDT")
                print(f"Position Margin: {futures_account.get('positionMargin', 'N/A')} USDT")
                print(f"Available Balance: {futures_account.get('availableBalance', 'N/A')} USDT")
                print(f"Risk Ratio: {futures_account.get('riskRatio', 'N/A')}")

            # Get all futures positions
            positions = self.get_all_positions()
            if positions:
                print("\n=== Current Futures Positions ===")
                for pos in positions:
                    print(f"\nSymbol: {pos.get('symbol', 'N/A')}")
                    print(f"Position Size: {pos.get('currentQty', 'N/A')}")
                    print(f"Entry Price: {pos.get('avgEntryPrice', 'N/A')}")
                    print(f"Mark Price: {pos.get('markPrice', 'N/A')}")
                    print(f"Unrealized PNL: {pos.get('unrealisedPnl', 'N/A')}")
                    print(f"Margin Mode: {pos.get('marginMode', 'N/A')}")
                    print(f"Leverage: {pos.get('leverage', 'N/A')}x")
                    print(f"Liquidation Price: {pos.get('liquidationPrice', 'N/A')}")

        except Exception as e:
            logger.error(f"Error displaying account summary: {str(e)}")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Get API credentials from environment variables
    api_key = os.getenv("KUCOIN_API_KEY")
    secret_key = os.getenv("KUCOIN_SECRET_KEY")
    passphrase = os.getenv("KUCOIN_PASSPHRASE")
    
    if not all([api_key, secret_key, passphrase]):
        logger.error("Please set KUCOIN_API_KEY, KUCOIN_SECRET_KEY, and KUCOIN_PASSPHRASE in your environment")
        exit(1)
    
    # Enable debug logging
    logger.setLevel(logging.DEBUG)
        
    client = KuCoinAccountInfo(api_key, secret_key, passphrase)
    client.display_account_summary() 