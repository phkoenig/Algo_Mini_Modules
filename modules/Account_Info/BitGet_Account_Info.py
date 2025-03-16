#!/usr/bin/env python3
"""
BitGet Account Info Module
-------------------------

Dieses Modul ruft detaillierte Kontoinformationen von BitGet ab.
Es zeigt verschiedene Aspekte des Kontos wie:
- Verfügbare Guthaben in verschiedenen Wallets (Spot, Futures, etc.)
- Offene Positionen
- Trading-Statistiken
- Account-Status und Limits
- Margin-Informationen
"""

import os
import sys
import json
import logging
import hmac
import base64
import time
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from decimal import Decimal
import pandas as pd
from tabulate import tabulate
from dotenv import load_dotenv
import urllib.parse

# Füge das Root-Verzeichnis zum Pfad hinzu
root_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(root_dir))

# Importiere das Credentials-Modul
from modules.Credentials.BitGet_Credentials import get_credentials

# Konfiguriere Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BitGetAccountInfo")

class BitGetAccountInfo:
    """BitGet Account Information Handler"""
    
    def __init__(self, api_key: str, secret_key: str, passphrase: str):
        """Initialisiert die BitGet API mit den Credentials"""
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.base_url = "https://api.bitget.com"
        
        # API Endpoints
        self.account_endpoint = "/api/mix/v1/account/account"
        self.positions_endpoint = "/api/mix/v1/position/allPosition"
        self.account_bills_endpoint = "/api/mix/v1/account/accountBill"
        
        logger.info("BitGet Client erfolgreich initialisiert")
    
    def _generate_signature(self, timestamp: str, method: str, request_path: str, params: Optional[Dict] = None, body: str = "") -> str:
        """Generate BitGet API signature"""
        # Add query parameters to request path if present
        if params and method.upper() == "GET":
            query_string = urllib.parse.urlencode(params)
            request_path = f"{request_path}?{query_string}"
            
        message = timestamp + method.upper() + request_path + body
        logger.debug(f"Signature message: {message}")
        
        mac = hmac.new(
            bytes(self.secret_key, encoding='utf8'),
            msg=bytes(message, encoding='utf-8'),
            digestmod='sha256'
        )
        d = mac.digest()
        return base64.b64encode(d).decode()
    
    def _send_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Send signed request to BitGet API"""
        timestamp = str(int(time.time() * 1000))
        
        # Generate signature
        signature = self._generate_signature(timestamp, method, endpoint, params)
        
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }
        
        url = self.base_url + endpoint
        
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
    
    def get_account_overview(self, symbol: str = "BTCUSDT_UMCBL", marginCoin: str = "USDT") -> Dict:
        """Get account overview for a specific trading pair"""
        try:
            params = {
                "symbol": symbol,
                "marginCoin": marginCoin
            }
            account_info = self._send_request("GET", self.account_endpoint, params)
            
            if account_info.get("code") == "00000":
                logger.info("Successfully retrieved account overview")
                return account_info["data"]
            else:
                logger.error(f"Error getting account overview: {account_info}")
                return {}
                
        except Exception as e:
            logger.error(f"Error in get_account_overview: {str(e)}")
            return {}
    
    def get_positions(self, productType: str = "umcbl") -> Dict:
        """Get all positions"""
        try:
            params = {
                "productType": productType
            }
            positions = self._send_request("GET", self.positions_endpoint, params)
            
            if positions.get("code") == "00000":
                logger.info("Successfully retrieved positions")
                return positions["data"]
            else:
                logger.error(f"Error getting positions: {positions}")
                return {}
                
        except Exception as e:
            logger.error(f"Error in get_positions: {str(e)}")
            return {}
    
    def get_account_bills(self, symbol: str = "BTCUSDT_UMCBL", 
                         marginCoin: str = "USDT",
                         startTime: Optional[str] = None,
                         endTime: Optional[str] = None,
                         limit: int = 100) -> Dict:
        """Get account bills/history"""
        try:
            params = {
                "symbol": symbol,
                "marginCoin": marginCoin,
                "limit": limit
            }
            
            if startTime:
                params["startTime"] = startTime
            if endTime:
                params["endTime"] = endTime
                
            bills = self._send_request("GET", self.account_bills_endpoint, params)
            
            if bills.get("code") == "00000":
                logger.info("Successfully retrieved account bills")
                return bills["data"]
            else:
                logger.error(f"Error getting account bills: {bills}")
                return {}
                
        except Exception as e:
            logger.error(f"Error in get_account_bills: {str(e)}")
            return {}

    def display_account_summary(self):
        """Display a summary of the account information"""
        try:
            # Get account overview for BTC-USDT
            btc_account = self.get_account_overview("BTCUSDT_UMCBL", "USDT")
            if btc_account:
                print("\n=== Account Overview (BTC-USDT) ===")
                print(f"Available Margin: {btc_account.get('available', 'N/A')} USDT")
                print(f"Total Margin: {btc_account.get('totalMargin', 'N/A')} USDT")
                print(f"Margin Ratio: {btc_account.get('marginRatio', 'N/A')}%")
                print(f"Unrealized PNL: {btc_account.get('unrealizedPL', 'N/A')} USDT")
                print(f"Realized PNL: {btc_account.get('realizedPL', 'N/A')} USDT")

            # Get all positions
            positions = self.get_positions()
            if positions:
                print("\n=== Current Positions ===")
                for pos in positions:
                    print(f"\nSymbol: {pos.get('symbol', 'N/A')}")
                    print(f"Position Size: {pos.get('total', 'N/A')}")
                    print(f"Entry Price: {pos.get('averageOpenPrice', 'N/A')}")
                    print(f"Mark Price: {pos.get('markPrice', 'N/A')}")
                    print(f"Unrealized PNL: {pos.get('unrealizedPL', 'N/A')}")
                    print(f"Margin Mode: {pos.get('marginMode', 'N/A')}")
                    print(f"Leverage: {pos.get('leverage', 'N/A')}x")

        except Exception as e:
            logger.error(f"Error displaying account summary: {str(e)}")

def main():
    """Hauptfunktion zum Testen des Moduls"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get API credentials from environment variables
        api_key = os.getenv("BITGET_API_KEY")
        secret_key = os.getenv("BITGET_SECRET_KEY")
        passphrase = os.getenv("BITGET_PASSPHRASE")
        
        if not all([api_key, secret_key, passphrase]):
            logger.error("Please set BITGET_API_KEY, BITGET_SECRET_KEY, and BITGET_PASSPHRASE in your environment")
            exit(1)
        
        # Enable debug logging
        logger.setLevel(logging.DEBUG)
        
        # Erstelle eine Instanz der AccountInfo-Klasse
        account = BitGetAccountInfo(api_key, secret_key, passphrase)
        
        # Zeige Account-Zusammenfassung
        account.display_account_summary()
        
    except Exception as e:
        logger.error(f"Fehler in der Hauptfunktion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 