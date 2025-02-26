#!/usr/bin/env python3
"""
Bitget REST API Client Beispiel

Dieses Skript zeigt, wie man den Bitget REST API Client verwenden kann,
um Marktdaten abzurufen.

Verwendung:
    python bitget_rest_example.py [--symbol SYMBOL] [--verbose]
"""

import os
import sys
from pathlib import Path

# Füge das Root-Verzeichnis zum Pfad hinzu, um relative Imports zu ermöglichen
root_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(root_dir))

# Importiere den Bitget REST Client
from modules.Websocket_Raw_Data.bitget_rest_client import BitgetRestClient, is_valid_symbol, get_user_input_symbol


def main():
    """Hauptfunktion"""
    # Prüfe, ob ein Symbol als Kommandozeilenargument übergeben wurde
    symbol = None
    verbose = False
    
    # Einfache Kommandozeilenargument-Verarbeitung
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith("--symbol="):
                symbol = arg.split("=")[1]
            elif arg == "--verbose":
                verbose = True
    
    # Symbol überprüfen oder Benutzer zur Eingabe auffordern
    if symbol:
        if not is_valid_symbol(symbol):
            print(f"Ungültiges Symbol: {symbol}")
            symbol = get_user_input_symbol()
    else:
        symbol = get_user_input_symbol()
    
    print(f"\nVerwende Symbol: {symbol}")
    
    # Initialisiere den REST API Client
    client = BitgetRestClient(verbose=verbose)
    
    # Hole und zeige Ticker-Daten an
    print("\n1. Ticker-Daten abrufen")
    print("-----------------------")
    ticker_data = client.get_ticker(symbol)
    
    if "error" in ticker_data:
        print(f"Fehler: {ticker_data['error']}")
    else:
        ticker_df = client.process_ticker_data(ticker_data)
        if not ticker_df.empty:
            print("\nTicker-Daten als DataFrame:")
            print(ticker_df[['datetime', 'symbol', 'last_price', 'high_24h', 'low_24h', 'volume_24h']])
            
            # Berechne Prozentänderung vom Tief zum Hoch
            low = ticker_df['low_24h'].values[0]
            high = ticker_df['high_24h'].values[0]
            change_percent = ((high - low) / low) * 100 if low > 0 else 0
            
            print(f"\nPreisspanne 24h: {low:.2f} - {high:.2f} ({change_percent:.2f}%)")
    
    # Hole und zeige Kerzendaten an
    print("\n2. Kerzendaten abrufen")
    print("----------------------")
    klines_data = client.get_klines(symbol, granularity="15m", limit=5)
    
    if "error" in klines_data:
        print(f"Fehler: {klines_data['error']}")
    else:
        klines_df = client.process_klines_data(klines_data)
        if not klines_df.empty:
            print("\nLetzte 5 Kerzen (15 Minuten):")
            print(klines_df[['datetime', 'open', 'high', 'low', 'close', 'volume']])
            
            # Berechne durchschnittliches Volumen
            avg_volume = klines_df['volume'].mean()
            print(f"\nDurchschnittliches Volumen: {avg_volume:.2f}")
    
    # Hole und zeige Orderbuch an
    print("\n3. Orderbuch abrufen")
    print("--------------------")
    orderbook_data = client.get_orderbook(symbol, limit=3)
    
    if "error" in orderbook_data:
        print(f"Fehler: {orderbook_data['error']}")
    else:
        data = orderbook_data.get("data", {})
        
        if data:
            asks = data.get("asks", [])
            bids = data.get("bids", [])
            
            print("\nVerkaufsangebote (Asks):")
            for i, ask in enumerate(asks):
                print(f"  {i+1}. Preis: {ask[0]}, Menge: {ask[1]}")
            
            print("\nKaufangebote (Bids):")
            for i, bid in enumerate(bids):
                print(f"  {i+1}. Preis: {bid[0]}, Menge: {bid[1]}")
            
            # Berechne Spread
            if asks and bids:
                lowest_ask = float(asks[0][0])
                highest_bid = float(bids[0][0])
                spread = lowest_ask - highest_bid
                spread_percent = (spread / lowest_ask) * 100
                
                print(f"\nSpread: {spread:.8f} ({spread_percent:.4f}%)")
    
    # Hole und zeige letzte Trades an
    print("\n4. Letzte Trades abrufen")
    print("------------------------")
    trades_data = client.get_trades(symbol, limit=5)
    
    if "error" in trades_data:
        print(f"Fehler: {trades_data['error']}")
    else:
        data = trades_data.get("data", [])
        
        if data:
            print("\nLetzte 5 Trades:")
            for i, trade in enumerate(data):
                side = trade.get("side", "")
                price = trade.get("price", "")
                size = trade.get("size", "")
                timestamp = trade.get("timestamp", "")
                
                side_str = "Kauf" if side == "buy" else "Verkauf"
                print(f"  {i+1}. {side_str} - Preis: {price}, Menge: {size}, Zeit: {timestamp}")
    
    print("\nBitget REST API Client Beispiel beendet.")


if __name__ == "__main__":
    main() 