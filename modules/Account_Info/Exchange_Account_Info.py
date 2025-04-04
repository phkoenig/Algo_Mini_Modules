#!/usr/bin/env python3
"""
Exchange Account Info Base Module
-------------------------------

Dieses Modul definiert die abstrakte Basisklasse für Exchange Account Info Module.
Es stellt sicher, dass alle Exchange-Implementierungen die gleiche Schnittstelle
und Datenstruktur verwenden.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime

class ExchangeAccountInfo(ABC):
    """Abstrakte Basisklasse für Exchange Account Information Handler"""
    
    @abstractmethod
    def get_btc_usdt_price(self) -> float:
        """Get current BTC-USDT price from the exchange"""
        pass
    
    @abstractmethod
    def get_account_status(self) -> Dict[str, str]:
        """Get status of different account types"""
        pass
    
    @abstractmethod
    def get_spot_accounts(self) -> List[Dict[str, Any]]:
        """Get spot account balances"""
        pass
    
    @abstractmethod
    def get_futures_account(self) -> Dict[str, Any]:
        """Get futures account information"""
        pass
    
    @abstractmethod
    def get_margin_accounts(self) -> List[Dict[str, Any]]:
        """Get margin account information"""
        pass
    
    @abstractmethod
    def get_trading_accounts(self) -> List[Dict[str, Any]]:
        """Get trading account information"""
        pass
    
    @abstractmethod
    def get_staking_accounts(self) -> List[Dict[str, Any]]:
        """Get staking account information"""
        pass
    
    @abstractmethod
    def get_earn_accounts(self) -> List[Dict[str, Any]]:
        """Get earn account information"""
        pass
    
    def get_account_summary_json(self) -> Dict[str, Any]:
        """Get a structured JSON summary of all account information"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_values": {
                "btc_price_usdt": self.get_btc_usdt_price(),
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
            for account in spot_accounts:
                balance = float(account.get('available', '0'))
                if balance > 0:
                    account_data = {
                        "currency": account.get('currency', 'N/A'),
                        "available": float(account.get('available', '0')),
                        "holds": float(account.get('holds', '0')),  # Standardisiert als 'holds'
                        "total": balance
                    }
                    summary["accounts"]["spot"].append(account_data)
                    
                    # Calculate total values
                    if account_data["currency"] == "BTC":
                        btc_value = account_data["available"] * summary["total_values"]["btc_price_usdt"]
                        summary["total_values"]["btc_holdings_usdt"] += btc_value
                    elif account_data["currency"] == "USDT":
                        summary["total_values"]["direct_usdt_holdings"] += account_data["available"]
        
        # Get futures account
        futures_account = self.get_futures_account()
        if futures_account:
            futures_data = {
                "currency": "USDT",
                "available": float(futures_account.get('available', '0')),
                "margin_balance": float(futures_account.get('margin_balance', '0')),
                "position_margin": float(futures_account.get('position_margin', '0')),
                "order_margin": float(futures_account.get('order_margin', '0')),
                "unrealized_pnl": float(futures_account.get('unrealized_pnl', '0')),
                "realized_pnl": float(futures_account.get('realized_pnl', '0'))
            }
            summary["accounts"]["futures"].append(futures_data)
            summary["total_values"]["direct_usdt_holdings"] += futures_data["margin_balance"]
        
        # Get margin accounts
        margin_accounts = self.get_margin_accounts()
        if margin_accounts:
            summary["accounts"]["margin"] = margin_accounts
        
        # Get trading accounts
        trading_accounts = self.get_trading_accounts()
        if trading_accounts:
            summary["accounts"]["trading"] = trading_accounts
        
        # Get staking accounts
        staking_accounts = self.get_staking_accounts()
        if staking_accounts:
            summary["accounts"]["staking"] = staking_accounts
        
        # Get earn accounts
        earn_accounts = self.get_earn_accounts()
        if earn_accounts:
            summary["accounts"]["earn"] = earn_accounts
        
        # Calculate total portfolio value
        summary["total_values"]["total_portfolio_value_usdt"] = (
            summary["total_values"]["btc_holdings_usdt"] +
            summary["total_values"]["direct_usdt_holdings"]
        )
        
        return summary
    
    def display_account_summary(self):
        """Display a summary of the account information"""
        try:
            # Get JSON summary
            summary = self.get_account_summary_json()
            
            # Print account status
            print("\n=== Account Status ===")
            for account_type, status in summary["account_status"].items():
                print(f"{account_type.capitalize()}: {status}")
            
            # Print spot account balances
            if summary["accounts"]["spot"]:
                print("\n=== Spot Account Overview ===")
                for account in summary["accounts"]["spot"]:
                    print(f"{account['currency']}: {account['available']} (Available: {account['available']}, Holds: {account['holds']})")
            
            # Print futures account overview
            if summary["accounts"]["futures"]:
                print("\n=== Futures Account Overview ===")
                futures = summary["accounts"]["futures"][0]
                print(f"Available Margin: {futures['available']} USDT")
                print(f"Margin Balance: {futures['margin_balance']} USDT")
                print(f"Position Margin: {futures['position_margin']} USDT")
                print(f"Order Margin: {futures['order_margin']} USDT")
                print(f"Unrealized PNL: {futures['unrealized_pnl']} USDT")
                print(f"Realized PNL: {futures['realized_pnl']} USDT")
            
            # Print margin account overview
            if summary["accounts"]["margin"]:
                print("\n=== Margin Account Overview ===")
                for account in summary["accounts"]["margin"]:
                    print(f"Currency: {account.get('currency', 'N/A')}")
                    print(f"Available: {account.get('available', '0')}")
                    print(f"Holds: {account.get('holds', '0')}")
            
            # Print total values
            print("\n=== Total Portfolio Value ===")
            print(f"BTC Price: {summary['total_values']['btc_price_usdt']} USDT")
            print(f"BTC Holdings (in USDT): {summary['total_values']['btc_holdings_usdt']:.2f} USDT")
            print(f"Direct USDT Holdings: {summary['total_values']['direct_usdt_holdings']:.2f} USDT")
            print(f"Total Portfolio Value: {summary['total_values']['total_portfolio_value_usdt']:.2f} USDT")
            
            # Print note about BTC conversion
            print("\nNote: Total value includes BTC converted to USDT at current market price")
            
        except Exception as e:
            print(f"Error displaying account summary: {str(e)}") 