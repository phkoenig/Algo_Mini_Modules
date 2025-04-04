#!/usr/bin/env python
"""
BitGet_Futures_Pairs_Extended.py - Extended information about BitGet futures trading pairs

This module provides detailed information about BitGet futures trading pairs,
including human-readable names, trading specifications, and other metadata.
Returns data as pandas DataFrames for easy analysis and display.

Functions:
    get_futures_pairs_extended(): Returns detailed information about all futures pairs
    get_active_pairs_extended(): Returns detailed information about active futures pairs only
"""
import os
import sys
import requests
import pandas as pd
from typing import Dict, Any
from tabulate import tabulate

# Add project root to path if running as script
if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
    sys.path.insert(0, project_root)

# Constants
BITGET_API_BASE = "https://api.bitget.com/api/mix/v1/market"
USDT_FUTURES_TYPE = "umcbl"  # USDT-margined futures
COIN_FUTURES_TYPE = "dmcbl"  # Coin-margined futures

# Common cryptocurrency names mapping
CRYPTO_NAMES = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "SOL": "Solana",
    "XRP": "Ripple",
    "ADA": "Cardano",
    "DOGE": "Dogecoin",
    "DOT": "Polkadot",
    "AVAX": "Avalanche",
    "MATIC": "Polygon",
    "LINK": "Chainlink",
    "UNI": "Uniswap",
    "ATOM": "Cosmos",
    "LTC": "Litecoin",
    "BCH": "Bitcoin Cash",
    "ETC": "Ethereum Classic",
    # Add more mappings as needed
}

def get_human_readable_name(symbol: str) -> str:
    """
    Convert trading pair symbol to human-readable name
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT_UMCBL')
        
    Returns:
        str: Human-readable name (e.g., 'Bitcoin/USDT Perpetual')
    """
    # Remove the _UMCBL or _DMCBL suffix
    base_symbol = symbol.split('_')[0]
    
    # Extract base currency (everything before USDT)
    base_currency = base_symbol.replace('USDT', '')
    
    # Look up human-readable name or use base currency if not found
    readable_name = CRYPTO_NAMES.get(base_currency, base_currency)
    
    # Add market type
    if '_UMCBL' in symbol:
        return f"{readable_name}/USDT Perpetual"
    elif '_DMCBL' in symbol:
        return f"{readable_name} Coin-M Perpetual"
    return readable_name

def get_futures_pairs_extended() -> pd.DataFrame:
    """
    Fetch detailed information about all futures trading pairs from BitGet
    
    Returns:
        pd.DataFrame: DataFrame containing detailed pair information
    """
    # Fetch USDT-M futures
    url = f"{BITGET_API_BASE}/contracts"
    
    all_data = []
    
    # Fetch USDT-M futures
    try:
        response = requests.get(url, params={"productType": USDT_FUTURES_TYPE})
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == "00000" and data.get("data"):
            for pair in data["data"]:
                pair_info = {
                    'symbol': pair.get('symbol'),
                    'human_readable_name': get_human_readable_name(pair.get('symbol')),
                    'base_currency': pair.get('baseCoin'),
                    'quote_currency': pair.get('quoteCoin'),
                    'market_type': 'USDT-M',
                    'contract_type': pair.get('symbolType', 'perpetual'),
                    'status': pair.get('symbolStatus'),
                    'min_leverage': 1,  # Default values
                    'max_leverage': 125,  # Default values
                    'maker_fee': float(pair.get('makerFeeRate', 0)),
                    'taker_fee': float(pair.get('takerFeeRate', 0)),
                    'min_order_size': float(pair.get('minTradeNum', 0)),
                    'price_precision': int(pair.get('pricePlace', 0)),
                    'quantity_precision': int(pair.get('volumePlace', 0)),
                    'trading_active': pair.get('symbolStatus') == 'normal',
                    'last_updated': pd.Timestamp.now()
                }
                all_data.append(pair_info)
    except Exception as e:
        print(f"Error fetching USDT-M futures data: {e}")

    # Fetch Coin-M futures
    try:
        response = requests.get(url, params={"productType": COIN_FUTURES_TYPE})
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == "00000" and data.get("data"):
            for pair in data["data"]:
                pair_info = {
                    'symbol': pair.get('symbol'),
                    'human_readable_name': get_human_readable_name(pair.get('symbol')),
                    'base_currency': pair.get('baseCoin'),
                    'quote_currency': pair.get('quoteCoin'),
                    'market_type': 'Coin-M',
                    'contract_type': pair.get('symbolType', 'perpetual'),
                    'status': pair.get('symbolStatus'),
                    'min_leverage': 1,  # Default values
                    'max_leverage': 125,  # Default values
                    'maker_fee': float(pair.get('makerFeeRate', 0)),
                    'taker_fee': float(pair.get('takerFeeRate', 0)),
                    'min_order_size': float(pair.get('minTradeNum', 0)),
                    'price_precision': int(pair.get('pricePlace', 0)),
                    'quantity_precision': int(pair.get('volumePlace', 0)),
                    'trading_active': pair.get('symbolStatus') == 'normal',
                    'last_updated': pd.Timestamp.now()
                }
                all_data.append(pair_info)
    except Exception as e:
        print(f"Error fetching Coin-M futures data: {e}")

    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Set symbol as index but keep it as a column too
    df.set_index('symbol', inplace=True, drop=False)
    
    return df

def get_active_pairs_extended() -> pd.DataFrame:
    """
    Get detailed information about active trading pairs only
    
    Returns:
        pd.DataFrame: DataFrame containing detailed information about active pairs
    """
    df = get_futures_pairs_extended()
    return df[df['trading_active'] == True]

def main():
    """Main function for testing"""
    print("Fetching BitGet Futures Trading Pairs with extended information...")
    
    # Get all pairs
    df = get_futures_pairs_extended()
    
    # Display basic information
    print("\nAll Trading Pairs:")
    print(f"Total pairs: {len(df)}")
    print(f"Active pairs: {len(df[df['trading_active']])}")
    
    # Display sample of the data with tabulate
    print("\nSample of available data:")
    sample_df = df.head()
    # Select most important columns for display
    display_columns = ['symbol', 'human_readable_name', 'market_type', 'status', 
                      'min_leverage', 'max_leverage', 'maker_fee', 'taker_fee']
    print(tabulate(sample_df[display_columns], headers='keys', tablefmt='pretty', 
                  showindex=False, floatfmt='.4f'))
    
    # Display summary statistics with tabulate
    print("\nSummary by market type:")
    summary_df = df.groupby('market_type').agg({
        'symbol': 'count',
        'trading_active': 'sum',
        'maker_fee': 'mean',
        'taker_fee': 'mean'
    }).round(4)
    print(tabulate(summary_df, headers='keys', tablefmt='pretty', 
                  floatfmt='.4f'))

if __name__ == "__main__":
    main() 