#!/usr/bin/env python
"""
KuCoin_Futures_Pairs.py - Module to fetch available futures trading pairs from KuCoin

This module provides functions to retrieve all available futures trading pairs
from the KuCoin Futures exchange.

Functions:
    get_futures_pairs(): Retrieves all futures pairs
    filter_active_pairs(pairs): Filters only active trading pairs
    get_active_symbols(): Returns a simple list of active trading pair symbols
"""
import os
import sys
import requests
from typing import List, Dict, Any

# Add project root to path if running as script
if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
    sys.path.insert(0, project_root)

# Constants
KUCOIN_FUTURES_API_BASE = "https://api-futures.kucoin.com/api/v1"


def get_futures_pairs() -> List[Dict[str, Any]]:
    """
    Fetch all available futures trading pairs from KuCoin
    
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing pair information
    """
    url = f"{KUCOIN_FUTURES_API_BASE}/contracts/active"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("code") == "200000" and data.get("data"):
            return data["data"]
        else:
            print(f"Error: {data.get('msg', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"Error fetching KuCoin futures data: {e}")
        return []


def filter_active_pairs(pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter only active trading pairs
    
    Args:
        pairs (List[Dict[str, Any]]): List of trading pairs
        
    Returns:
        List[Dict[str, Any]]: List of active trading pairs
    """
    # In KuCoin, the /contracts/active endpoint already returns only active pairs
    return pairs


def get_active_symbols(include_inactive: bool = False) -> List[str]:
    """
    Get a simple list of active trading pair symbols
    
    Args:
        include_inactive (bool, optional): Whether to include inactive pairs. Defaults to False.
        
    Returns:
        List[str]: List of trading pair symbols
    """
    futures_pairs = get_futures_pairs()
    
    # Extract symbols
    symbols = [pair.get("symbol") for pair in futures_pairs]
    return sorted(symbols)


def get_active_symbols_with_info(include_inactive: bool = False) -> List[Dict[str, str]]:
    """
    Get a list of active trading pairs with basic information
    
    Args:
        include_inactive (bool, optional): Whether to include inactive pairs. Defaults to False.
        
    Returns:
        List[Dict[str, str]]: List of dictionaries with symbol, base_coin, quote_coin
    """
    futures_pairs = get_futures_pairs()
    
    # Extract relevant information
    result = []
    for pair in futures_pairs:
        result.append({
            "symbol": pair.get("symbol"),
            "base_coin": pair.get("baseCurrency"),
            "quote_coin": pair.get("quoteCurrency"),
            "type": "USDT-M" if pair.get("rootSymbol") == "USDT" else "Coin-M"
        })
    
    return sorted(result, key=lambda x: x["symbol"])


def print_summary(futures_pairs: List[Dict[str, Any]]) -> None:
    """
    Print a summary of the futures pairs
    
    Args:
        futures_pairs (List[Dict[str, Any]]): Futures pairs
    """
    usdt_pairs = [p for p in futures_pairs if p.get("rootSymbol") == "USDT"]
    coin_pairs = [p for p in futures_pairs if p.get("rootSymbol") != "USDT"]
    
    print(f"\nKuCoin Futures Trading Pairs Summary:")
    print(f"- USDT-M Futures: {len(usdt_pairs)}")
    print(f"- Coin-M Futures: {len(coin_pairs)}")
    print(f"- Total Pairs: {len(futures_pairs)}")


def main():
    """
    Main function when module is run directly
    """
    print("Fetching KuCoin Futures Trading Pairs...")
    
    # Get all futures pairs
    futures_pairs = get_futures_pairs()
    
    # Get simple list of active symbols
    active_symbols = get_active_symbols()
    
    print("\nActive Futures Trading Pairs:")
    if active_symbols:
        for symbol in active_symbols:
            print(symbol)
        print(f"\nTotal active pairs: {len(active_symbols)}")
    else:
        print("No active trading pairs found.")
    
    # Print summary
    print_summary(futures_pairs)


if __name__ == "__main__":
    main() 