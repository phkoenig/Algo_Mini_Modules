#!/usr/bin/env python
"""
Example script demonstrating how to use the BitGet_Futures_Pairs module
"""
import os
import sys
import json

# Add project root to path
script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(script_path))
sys.path.insert(0, project_root)

# Import the module
from modules.Trading_Pairs.BitGet_Futures_Pairs import (
    get_all_futures_pairs,
    filter_active_pairs,
    get_simplified_pairs_list,
    print_summary,
    save_pairs_to_json
)

def main():
    """Main function"""
    print("Example 1: Get all futures pairs and print summary")
    usdt_futures, coin_futures = get_all_futures_pairs()
    print_summary(usdt_futures, coin_futures)
    
    print("\nExample 2: Get only active pairs")
    active_usdt = filter_active_pairs(usdt_futures)
    active_coin = filter_active_pairs(coin_futures)
    
    print(f"Active USDT-M Futures: {len(active_usdt)}")
    print(f"Active Coin-M Futures: {len(active_coin)}")
    
    print("\nExample 3: Get simplified list of all active pair symbols")
    active_symbols = get_simplified_pairs_list(include_inactive=False)
    print(f"Active symbols ({len(active_symbols)}):")
    for symbol in active_symbols[:10]:  # Show first 10 only
        print(f"- {symbol}")
    
    if len(active_symbols) > 10:
        print(f"... and {len(active_symbols) - 10} more")
    
    print("\nExample 4: Save all pairs to JSON file")
    output_file = "example_bitget_pairs.json"
    if save_pairs_to_json(usdt_futures, coin_futures, filename=output_file):
        print(f"Data saved to {output_file}")
        
        # Read and display file structure
        with open(output_file, "r") as f:
            data = json.load(f)
            print(f"\nJSON file structure:")
            print(f"- timestamp: {data.get('timestamp')}")
            print(f"- fetch_time: {data.get('fetch_time')}")
            print(f"- usdt_futures: {len(data.get('usdt_futures', []))} items")
            print(f"- coin_futures: {len(data.get('coin_futures', []))} items")

if __name__ == "__main__":
    main() 