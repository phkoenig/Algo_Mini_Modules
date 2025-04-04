#!/usr/bin/env python
"""
Script to fetch available futures trading pairs from BitGet
"""
import requests
import json
from tabulate import tabulate

def get_bitget_futures_pairs():
    """
    Fetch all available USDT-M futures trading pairs from BitGet
    """
    # USDT-M Futures
    url = "https://api.bitget.com/api/mix/v1/market/contracts"
    params = {"productType": "umcbl"}  # USDT-M Futures
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        if data.get("code") == "00000" and data.get("data"):
            return data["data"]
        else:
            print(f"Error: {data.get('msg', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def get_bitget_coin_futures_pairs():
    """
    Fetch all available Coin-M futures trading pairs from BitGet
    """
    # Coin-M Futures
    url = "https://api.bitget.com/api/mix/v1/market/contracts"
    params = {"productType": "dmcbl"}  # Coin-M Futures
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        if data.get("code") == "00000" and data.get("data"):
            return data["data"]
        else:
            print(f"Error: {data.get('msg', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def display_futures_pairs(pairs, title):
    """
    Display futures pairs in a formatted table
    """
    if not pairs:
        print(f"No {title} pairs found.")
        return
    
    # Extract relevant information
    table_data = []
    for pair in pairs:
        table_data.append([
            pair.get("symbol"),
            pair.get("baseCoin"),
            pair.get("quoteCoin"),
            pair.get("status"),
            pair.get("minTradeNum"),
            pair.get("priceEndStep")
        ])
    
    # Display table
    headers = ["Symbol", "Base Coin", "Quote Coin", "Status", "Min Trade", "Price Step"]
    print(f"\n{title} ({len(pairs)} pairs):")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def main():
    """Main function"""
    print("Fetching BitGet Futures Trading Pairs...")
    
    # Get USDT-M Futures
    usdt_futures = get_bitget_futures_pairs()
    display_futures_pairs(usdt_futures, "USDT-M Futures")
    
    # Get Coin-M Futures
    coin_futures = get_bitget_coin_futures_pairs()
    display_futures_pairs(coin_futures, "Coin-M Futures")
    
    # Save to JSON file
    all_data = {
        "usdt_futures": usdt_futures,
        "coin_futures": coin_futures,
        "timestamp": requests.get("https://api.bitget.com/api/mix/v1/market/time").json().get("data")
    }
    
    with open("bitget_futures_pairs.json", "w") as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\nData saved to bitget_futures_pairs.json")
    
    # Summary
    active_usdt = sum(1 for p in usdt_futures if p.get("status") == "normal")
    active_coin = sum(1 for p in coin_futures if p.get("status") == "normal")
    
    print(f"\nSummary:")
    print(f"- Active USDT-M Futures: {active_usdt}/{len(usdt_futures)}")
    print(f"- Active Coin-M Futures: {active_coin}/{len(coin_futures)}")
    print(f"- Total Active Pairs: {active_usdt + active_coin}/{len(usdt_futures) + len(coin_futures)}")

if __name__ == "__main__":
    main() 