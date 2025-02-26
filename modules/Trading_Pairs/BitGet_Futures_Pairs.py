#!/usr/bin/env python
"""
BitGet_Futures_Pairs.py - Module to fetch available futures trading pairs from BitGet

This module provides functions to retrieve all available futures trading pairs
from the BitGet exchange, including both USDT-M and Coin-M futures.

Functions:
    get_usdt_futures_pairs(): Retrieves all USDT-margined futures pairs
    get_coin_futures_pairs(): Retrieves all Coin-margined futures pairs
    get_all_futures_pairs(): Retrieves both USDT-M and Coin-M futures pairs
    filter_active_pairs(pairs): Filters only active trading pairs
    get_active_symbols(): Returns a simple list of active trading pair symbols
"""
import os
import sys
import requests
from typing import List, Dict, Any, Tuple

# Add project root to path if running as script
if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
    sys.path.insert(0, project_root)

# Constants
BITGET_API_BASE = "https://api.bitget.com/api/mix/v1/market"
USDT_FUTURES_TYPE = "umcbl"  # USDT-margined futures
COIN_FUTURES_TYPE = "dmcbl"  # Coin-margined futures


def get_usdt_futures_pairs() -> List[Dict[str, Any]]:
    """
    Fetch all available USDT-M futures trading pairs from BitGet
    
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing pair information
    """
    url = f"{BITGET_API_BASE}/contracts"
    params = {"productType": USDT_FUTURES_TYPE}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("code") == "00000" and data.get("data"):
            return data["data"]
        else:
            print(f"Error: {data.get('msg', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"Error fetching USDT-M futures data: {e}")
        return []


def get_coin_futures_pairs() -> List[Dict[str, Any]]:
    """
    Fetch all available Coin-M futures trading pairs from BitGet
    
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing pair information
    """
    url = f"{BITGET_API_BASE}/contracts"
    params = {"productType": COIN_FUTURES_TYPE}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("code") == "00000" and data.get("data"):
            return data["data"]
        else:
            print(f"Error: {data.get('msg', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"Error fetching Coin-M futures data: {e}")
        return []


def get_all_futures_pairs() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Fetch all available futures trading pairs from BitGet (both USDT-M and Coin-M)
    
    Returns:
        Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: Tuple containing 
        (usdt_futures_pairs, coin_futures_pairs)
    """
    usdt_futures = get_usdt_futures_pairs()
    coin_futures = get_coin_futures_pairs()
    return usdt_futures, coin_futures


def filter_active_pairs(pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter only active trading pairs
    
    Args:
        pairs (List[Dict[str, Any]]): List of trading pairs
        
    Returns:
        List[Dict[str, Any]]: List of active trading pairs
    """
    return [pair for pair in pairs if pair.get("status") == "normal"]


def get_active_symbols(include_inactive: bool = False) -> List[str]:
    """
    Get a simple list of active trading pair symbols
    
    Args:
        include_inactive (bool, optional): Whether to include inactive pairs. Defaults to False.
        
    Returns:
        List[str]: List of trading pair symbols
    """
    usdt_futures, coin_futures = get_all_futures_pairs()
    
    if not include_inactive:
        usdt_futures = filter_active_pairs(usdt_futures)
        coin_futures = filter_active_pairs(coin_futures)
    
    # Extract symbols
    symbols = [pair.get("symbol") for pair in usdt_futures + coin_futures]
    return sorted(symbols)


def get_active_symbols_with_info(include_inactive: bool = False) -> List[Dict[str, str]]:
    """
    Get a list of active trading pairs with basic information
    
    Args:
        include_inactive (bool, optional): Whether to include inactive pairs. Defaults to False.
        
    Returns:
        List[Dict[str, str]]: List of dictionaries with symbol, base_coin, quote_coin
    """
    usdt_futures, coin_futures = get_all_futures_pairs()
    
    if not include_inactive:
        usdt_futures = filter_active_pairs(usdt_futures)
        coin_futures = filter_active_pairs(coin_futures)
    
    # Extract relevant information
    result = []
    for pair in usdt_futures + coin_futures:
        result.append({
            "symbol": pair.get("symbol"),
            "base_coin": pair.get("baseCoin"),
            "quote_coin": pair.get("quoteCoin"),
            "type": "USDT-M" if pair.get("productType") == USDT_FUTURES_TYPE else "Coin-M"
        })
    
    return sorted(result, key=lambda x: x["symbol"])


def print_summary(usdt_futures: List[Dict[str, Any]], coin_futures: List[Dict[str, Any]]) -> None:
    """
    Print a summary of the futures pairs
    
    Args:
        usdt_futures (List[Dict[str, Any]]): USDT-M futures pairs
        coin_futures (List[Dict[str, Any]]): Coin-M futures pairs
    """
    active_usdt = len(filter_active_pairs(usdt_futures))
    active_coin = len(filter_active_pairs(coin_futures))
    
    print(f"\nBitGet Futures Trading Pairs Summary:")
    print(f"- Active USDT-M Futures: {active_usdt}/{len(usdt_futures)}")
    print(f"- Active Coin-M Futures: {active_coin}/{len(coin_futures)}")
    print(f"- Total Active Pairs: {active_usdt + active_coin}/{len(usdt_futures) + len(coin_futures)}")


def main():
    """
    Main function when module is run directly
    """
    print("Fetching BitGet Futures Trading Pairs...")
    
    # Get simple list of active symbols
    active_symbols = get_active_symbols(include_inactive=False)
    
    print("\nActive Futures Trading Pairs:")
    if active_symbols:
        for symbol in active_symbols:
            print(symbol)
        print(f"\nTotal active pairs: {len(active_symbols)}")
    else:
        print("No active trading pairs found.")
        
        # If no active pairs, show all pairs
        all_symbols = get_active_symbols(include_inactive=True)
        print("\nAll Futures Trading Pairs (including inactive):")
        for symbol in all_symbols:
            print(symbol)
        print(f"\nTotal pairs: {len(all_symbols)}")
    
    # Get all pairs for summary
    usdt_futures, coin_futures = get_all_futures_pairs()
    print_summary(usdt_futures, coin_futures)


if __name__ == "__main__":
    main() 