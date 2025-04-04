#!/usr/bin/env python3
"""
KuCoin Account Info Module
-------------------------

Dieses Modul ruft detaillierte Kontoinformationen von KuCoin ab.
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
from modules.Credentials.KuCoin_Credentials import get_credentials

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
    
    return logging.getLogger("KuCoinAccountInfo")

# Initialisiere Logger
logger = setup_logging()

class KuCoinAccountInfo(ExchangeAccountInfo):
    """KuCoin Account Information Handler"""
    
    def __init__(self, api_key: str, secret_key: str, passphrase: str):
        """Initialisiert die KuCoin API mit den Credentials"""
        self.api_key = api_key.strip()
        self.secret_key = secret_key.strip()
        self.passphrase = passphrase.strip()
        self.spot_url = "https://api.kucoin.com"
        self.futures_url = "https://api-futures.kucoin.com"
        
        # API Endpoints
        self.spot_accounts_endpoint = "/api/v1/accounts"
        self.futures_account_endpoint = "/api/v1/account-overview"
        self.futures_position_endpoint = "/api/v1/positions"
        self.futures_positions_endpoint = "/api/v1/positions"
        self.margin_accounts_endpoint = "/api/v1/margin/account"
        self.trading_accounts_endpoint = "/api/v1/accounts/trade-accounts"
        self.staking_accounts_endpoint = "/api/v1/accounts/staking-accounts"
        self.earn_accounts_endpoint = "/api/v1/accounts/earn-accounts"
        self.sub_accounts_endpoint = "/api/v1/sub-accounts"
        
        logger.info("KuCoin client initialized")
    
    def _generate_signature(self, timestamp: str, method: str, request_path: str, params: Optional[Dict] = None, body: str = "") -> str:
        """Generate KuCoin API signature"""
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
    
    def _send_request(self, method: str, endpoint: str, params: Optional[Dict] = None, is_futures: bool = False) -> Dict:
        """Send signed request to KuCoin API"""
        timestamp = str(int(time.time() * 1000))
        
        # Generate signature
        signature = self._generate_signature(timestamp, method, endpoint, params)
        
        headers = {
            "KC-API-KEY": self.api_key,
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": timestamp,
            "KC-API-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }
        
        url = (self.futures_url if is_futures else self.spot_url) + endpoint
        
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
        """Get current BTC-USDT price from KuCoin"""
        try:
            endpoint = "/api/v1/market/orderbook/level1?symbol=BTC-USDT"
            response = self._send_request("GET", endpoint, is_futures=False)
            if response.get("code") == "200000":
                return float(response["data"]["price"])
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
            accounts = self._send_request("GET", self.spot_accounts_endpoint, is_futures=False)
            
            if accounts.get("code") == "200000":
                logger.info("Successfully retrieved spot accounts")
                return accounts["data"]
            else:
                logger.error(f"Error getting spot accounts: {accounts}")
                return []
                
        except Exception as e:
            logger.error(f"Error in get_spot_accounts: {str(e)}")
            return []
    
    def get_futures_account(self) -> Dict[str, Any]:
        """Get futures account information"""
        try:
            params = {"currency": "USDT"}
            account_info = self._send_request("GET", self.futures_account_endpoint, params, is_futures=True)
            
            if account_info.get("code") == "200000":
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
        try:
            accounts = self._send_request("GET", self.margin_accounts_endpoint, is_futures=False)
            
            if accounts.get("code") == "200000":
                return accounts["data"]
            return []
                
        except Exception:
            return []
    
    def get_trading_accounts(self) -> List[Dict[str, Any]]:
        """Get trading account information"""
        try:
            accounts = self._send_request("GET", self.trading_accounts_endpoint, is_futures=False)
            
            if accounts.get("code") == "200000":
                return accounts["data"]
            return []
                
        except Exception:
            return []
    
    def get_staking_accounts(self) -> List[Dict[str, Any]]:
        """Get staking account information"""
        try:
            accounts = self._send_request("GET", self.staking_accounts_endpoint, is_futures=False)
            
            if accounts.get("code") == "200000":
                return accounts["data"]
            return []
                
        except Exception:
            return []
    
    def get_earn_accounts(self) -> List[Dict[str, Any]]:
        """Get KuCoin Earn account information"""
        try:
            accounts = self._send_request("GET", self.earn_accounts_endpoint, is_futures=False)
            
            if accounts.get("code") == "200000":
                return accounts["data"]
            return []
                
        except Exception:
            return []

def main():
    """Hauptfunktion zum Testen des Moduls"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get API credentials from environment variables
        api_key = os.getenv("KUCOIN_API_KEY")
        secret_key = os.getenv("KUCOIN_SECRET_KEY")
        passphrase = os.getenv("KUCOIN_PASSPHRASE")
        
        if not all([api_key, secret_key, passphrase]):
            logger.error("Please set KUCOIN_API_KEY, KUCOIN_SECRET_KEY, and KUCOIN_PASSPHRASE in your environment")
            exit(1)
        
        # Erstelle eine Instanz der AccountInfo-Klasse
        account = KuCoinAccountInfo(api_key, secret_key, passphrase)
        
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