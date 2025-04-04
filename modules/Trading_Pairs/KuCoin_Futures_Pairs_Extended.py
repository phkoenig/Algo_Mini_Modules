#!/usr/bin/env python
"""
KuCoin_Futures_Pairs_Extended.py - Extended information about KuCoin futures trading pairs

This module provides detailed information about KuCoin futures trading pairs,
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
KUCOIN_FUTURES_API_BASE = "https://api-futures.kucoin.com/api/v1"

# Common cryptocurrency names mapping
CRYPTO_NAMES = {
    "XBT": "Bitcoin",  # KuCoin uses XBT instead of BTC for Bitcoin
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
        symbol: Trading pair symbol (e.g., 'XBTUSDTM')
        
    Returns:
        str: Human-readable name (e.g., 'Bitcoin/USDT Perpetual')
    """
    # Remove the M suffix for perpetual contracts
    base_symbol = symbol.replace('M', '')
    
    # Extract base currency (everything before USDT)
    base_currency = base_symbol.replace('USDT', '')
    
    # Look up human-readable name or use base currency if not found
    readable_name = CRYPTO_NAMES.get(base_currency, base_currency)
    
    # Add market type (all are perpetual on KuCoin Futures)
    return f"{readable_name}/USDT Perpetual"

def get_futures_pairs_extended() -> pd.DataFrame:
    """
    Fetch detailed information about all futures trading pairs from KuCoin
    
    Returns:
        pd.DataFrame: DataFrame containing detailed pair information
    """
    url = f"{KUCOIN_FUTURES_API_BASE}/contracts/active"
    
    all_data = []
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == "200000" and data.get("data"):
            for pair in data["data"]:
                # Safely convert values to float, using 0 as default for None
                try:
                    maker_fee = float(pair.get('makerFeeRate', 0.0002))
                except (TypeError, ValueError):
                    maker_fee = 0.0002

                try:
                    taker_fee = float(pair.get('takerFeeRate', 0.0006))
                except (TypeError, ValueError):
                    taker_fee = 0.0006

                try:
                    funding_rate = float(pair.get('fundingFeeRate', 0))
                except (TypeError, ValueError):
                    funding_rate = 0.0

                try:
                    min_leverage = float(pair.get('minLeverage', 1))
                except (TypeError, ValueError):
                    min_leverage = 1.0

                try:
                    max_leverage = float(pair.get('maxLeverage', 100))
                except (TypeError, ValueError):
                    max_leverage = 100.0

                pair_info = {
                    'symbol': pair.get('symbol'),
                    'human_readable_name': get_human_readable_name(pair.get('symbol')),
                    'base_currency': pair.get('baseCurrency'),
                    'quote_currency': pair.get('quoteCurrency', 'USDT'),
                    'market_type': 'USDT-M',  # KuCoin Futures are all USDT-margined
                    'contract_type': 'perpetual',
                    'status': pair.get('status', 'active'),
                    'min_leverage': min_leverage,
                    'max_leverage': max_leverage,
                    'maker_fee': maker_fee,
                    'taker_fee': taker_fee,
                    'min_order_size': float(pair.get('lotSize', 1)),
                    'price_precision': int(pair.get('pricePrecision', 1)),
                    'quantity_precision': int(pair.get('lotSize', 1)),
                    'trading_active': pair.get('status') == 'Open',
                    'max_order_size': float(pair.get('maxOrderQty', 1000000)),
                    'multiplier': float(pair.get('multiplier', 1)),
                    'funding_rate': funding_rate,
                    'index_price': float(pair.get('indexPrice', 0)),
                    'mark_price': float(pair.get('markPrice', 0)),
                    'last_updated': pd.Timestamp.now()
                }
                all_data.append(pair_info)
    except Exception as e:
        print(f"Error fetching KuCoin futures data: {e}")

    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Set symbol as index but keep it as a column too
    if not df.empty:
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
    print("Fetching KuCoin Futures Trading Pairs with extended information...")
    
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
    display_columns = ['symbol', 'human_readable_name', 'status', 
                      'min_leverage', 'max_leverage', 'maker_fee', 'taker_fee',
                      'funding_rate']
    print(tabulate(sample_df[display_columns], headers='keys', tablefmt='pretty', 
                  showindex=False, floatfmt='.4f'))
    
    # Display summary statistics with tabulate
    print("\nSummary statistics:")
    summary_df = pd.DataFrame(df.agg({
        'symbol': 'count',
        'trading_active': 'sum',
        'maker_fee': 'mean',
        'taker_fee': 'mean',
        'min_leverage': 'min',
        'max_leverage': 'max',
        'funding_rate': 'mean'
    })).round(4)
    summary_df.columns = ['Value']
    print(tabulate(summary_df, headers='keys', tablefmt='pretty', 
                  floatfmt='.4f'))

if __name__ == "__main__":
    main() 