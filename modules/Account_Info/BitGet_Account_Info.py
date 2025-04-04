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

# Importiere die Basisklasse und das Credentials-Modul
from modules.Account_Info.Exchange_Account_Info import ExchangeAccountInfo
from modules.Credentials.BitGet_Credentials import get_credentials

def setup_logging():
    """Konfiguriert das Logging für das Modul"""
    # Erstelle einen Console Handler für alle Ausgaben
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # Formatiere die Log-Ausgabe
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Konfiguriere den Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Entferne existierende Handler
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Füge den Console Handler hinzu
    root_logger.addHandler(console_handler)
    
    return logging.getLogger("BitGetAccountInfo")

# Initialisiere Logger
logger = setup_logging()

class BitGetAccountInfo(ExchangeAccountInfo):
    """BitGet Account Information Handler"""
    
    def __init__(self, api_key: str, secret_key: str, passphrase: str):
        """Initialisiert die BitGet API mit den Credentials"""
        self.api_key = api_key.strip()
        self.secret_key = secret_key.strip()
        self.passphrase = passphrase.strip()
        self.base_url = "https://api.bitget.com"
        
        # API Endpoints
        self.spot_accounts_endpoint = "/api/spot/v1/account/assets"
        self.futures_account_endpoint = "/api/mix/v1/account/accounts"
        self.futures_position_endpoint = "/api/mix/v1/position/single-position"
        self.futures_positions_endpoint = "/api/mix/v1/position/all-position"
        self.margin_accounts_endpoint = "/api/margin/v1/account/assets"
        self.trading_accounts_endpoint = "/api/spot/v1/account/bills"
        self.staking_accounts_endpoint = "/api/spot/v1/account/staking"
        self.earn_accounts_endpoint = "/api/spot/v1/account/earn"
        
        logger.info("BitGet client initialized")
    
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
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error response: {response.text}")
                return {"code": -1, "msg": f"{response.status_code} {response.reason}: {response.text}"}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to {endpoint}: {str(e)}")
            return {"code": -1, "msg": str(e)}
    
    def get_btc_usdt_price(self) -> float:
        """Get current BTC-USDT price from BitGet"""
        try:
            endpoint = "/api/spot/v1/market/ticker"
            params = {"symbol": "BTCUSDT"}
            response = self._send_request("GET", endpoint, params)
            if response.get("code") == "00000" and response.get("data"):
                return float(response["data"]["close"])
            logger.error(f"Error getting BTC price: {response}")
            return 0
        except Exception as e:
            logger.error(f"Error getting BTC-USDT price: {str(e)}")
            return 0
    
    def get_account_status(self) -> Dict[str, str]:
        """Get status of different account types"""
        status = {}
        
        # Check Spot Account
        try:
            spot_accounts = self.get_spot_accounts()
            status["spot"] = "Aktiviert" if spot_accounts else "Nicht aktiviert"
        except Exception as e:
            status["spot"] = "Fehler beim Abrufen"
        
        # Check Futures Account
        try:
            futures_account = self.get_futures_account()
            status["futures"] = "Aktiviert" if futures_account else "Nicht aktiviert"
        except Exception as e:
            status["futures"] = "Fehler beim Abrufen"
        
        # Check Margin Account
        try:
            margin_accounts = self.get_margin_accounts()
            status["margin"] = "Aktiviert" if margin_accounts else "Nicht aktiviert"
        except Exception as e:
            status["margin"] = "Fehler beim Abrufen"
        
        # Check Trading Account
        try:
            trading_accounts = self.get_trading_accounts()
            status["trading"] = "Aktiviert" if trading_accounts else "Nicht aktiviert"
        except Exception as e:
            status["trading"] = "Fehler beim Abrufen"
        
        # Check Staking Account
        try:
            staking_accounts = self.get_staking_accounts()
            status["staking"] = "Aktiviert" if staking_accounts else "Nicht aktiviert"
        except Exception as e:
            status["staking"] = "Fehler beim Abrufen"
        
        # Check Earn Account
        try:
            earn_accounts = self.get_earn_accounts()
            status["earn"] = "Aktiviert" if earn_accounts else "Nicht aktiviert"
        except Exception as e:
            status["earn"] = "Fehler beim Abrufen"
        
        return status
    
    def get_spot_accounts(self) -> List[Dict[str, Any]]:
        """Get spot account balances"""
        try:
            accounts = self._send_request("GET", self.spot_accounts_endpoint)
            logger.debug(f"Raw API response: {json.dumps(accounts, indent=2)}")
            
            if accounts.get("code") == "00000":
                logger.info("Successfully retrieved spot accounts")
                # Filter out zero balances and add proper currency names
                non_zero_accounts = []
                for account in accounts["data"]:
                    available = float(account.get("available", "0"))
                    frozen = float(account.get("frozen", "0"))
                    if available > 0 or frozen > 0:
                        currency = account.get("coinName", "N/A")
                        non_zero_accounts.append({
                            "currency": currency,
                            "available": available,
                            "holds": frozen,
                            "total": available + frozen
                        })
                        logger.info(f"Found non-zero balance for {currency}: {available} (available) + {frozen} (frozen)")
                
                if not non_zero_accounts:
                    logger.info("No non-zero balances found in spot accounts")
                else:
                    logger.info(f"Found {len(non_zero_accounts)} accounts with non-zero balances")
                
                return non_zero_accounts
            else:
                logger.error(f"Error getting spot accounts: {accounts}")
                return []
                
        except Exception as e:
            logger.error(f"Error in get_spot_accounts: {str(e)}")
            return []
    
    def get_futures_account(self) -> Dict[str, Any]:
        """Get futures account information"""
        try:
            params = {"productType": "umcbl"}  # USDT-M Contract
            account_info = self._send_request("GET", self.futures_account_endpoint, params)
            
            if account_info.get("code") == "00000" and account_info.get("data"):
                logger.debug("Successfully retrieved futures account overview")
                return account_info["data"]
            else:
                logger.debug(f"Error getting futures account overview: {account_info}")
                return {}
                
        except Exception as e:
            logger.debug(f"Error in get_futures_account: {str(e)}")
            return {}
    
    def get_margin_accounts(self) -> List[Dict[str, Any]]:
        """Get margin account information"""
        # BitGet doesn't support margin trading API
        return []
    
    def get_trading_accounts(self) -> List[Dict[str, Any]]:
        """Get trading account information"""
        # BitGet doesn't support separate trading accounts
        return []
    
    def get_staking_accounts(self) -> List[Dict[str, Any]]:
        """Get staking account information"""
        # BitGet doesn't support staking API
        return []
    
    def get_earn_accounts(self) -> List[Dict[str, Any]]:
        """Get BitGet Earn account information"""
        # BitGet doesn't support earn API
        return []

    def get_account_summary_json(self) -> Dict:
        """Get a structured JSON summary of all account information"""
        # Get BTC price first
        btc_price = self.get_btc_usdt_price()
        logger.info(f"Current BTC price: {btc_price} USDT")
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_values": {
                "btc_price_usdt": btc_price,
                "btc_holdings_usdt": 0.0,
                "direct_usdt_holdings": 0.0,
                "total_portfolio_value_usdt": 0.0
            },
            "account_status": self.get_account_status(),
            "accounts": {
                "spot": [],
                "futures": [],
                "margin": [],
                "trading": [],
                "staking": [],
                "earn": []
            }
        }
        
        # Get spot accounts
        spot_accounts = self.get_spot_accounts()
        if spot_accounts:
            summary["accounts"]["spot"] = spot_accounts
            for account in spot_accounts:
                if account["currency"] == "BTC":
                    btc_value = account["available"] * btc_price
                    summary["total_values"]["btc_holdings_usdt"] += btc_value
                    logger.info(f"BTC holdings value: {btc_value} USDT")
                elif account["currency"] == "USDT":
                    summary["total_values"]["direct_usdt_holdings"] += account["available"]
                    logger.info(f"Direct USDT holdings: {account['available']} USDT")
        
        # Get futures account
        futures_account = self.get_futures_account()
        if futures_account:
            for account in futures_account:
                futures_data = {
                    "currency": "USDT",
                    "available": float(account.get("available", "0")),
                    "margin_balance": float(account.get("marginBalance", "0")),
                    "position_margin": float(account.get("positionMargin", "0")),
                    "order_margin": float(account.get("orderMargin", "0")),
                    "unrealized_pnl": float(account.get("unrealizedPL", "0")),
                    "realized_pnl": float(account.get("realizedPL", "0"))
                }
                summary["accounts"]["futures"].append(futures_data)
                summary["total_values"]["direct_usdt_holdings"] += futures_data["margin_balance"]
                logger.info(f"Futures margin balance: {futures_data['margin_balance']} USDT")
        
        # Calculate total portfolio value
        summary["total_values"]["total_portfolio_value_usdt"] = (
            summary["total_values"]["btc_holdings_usdt"] +
            summary["total_values"]["direct_usdt_holdings"]
        )
        logger.info(f"Total portfolio value: {summary['total_values']['total_portfolio_value_usdt']} USDT")
        
        return summary

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
        
        # Erstelle eine Instanz der AccountInfo-Klasse
        account = BitGetAccountInfo(api_key, secret_key, passphrase)
        
        # Hole und zeige JSON-Zusammenfassung
        summary = account.get_account_summary_json()
        print("\n=== JSON Account Summary ===")
        print(json.dumps(summary, indent=2))
        
        # Zeige formatierte Account-Zusammenfassung
        account.display_account_summary()
        
        # Warte auf Benutzer-Eingabe, bevor das Fenster geschlossen wird
        input("\nDrücke Enter zum Beenden...")
        
    except Exception as e:
        logger.error(f"Fehler in der Hauptfunktion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 