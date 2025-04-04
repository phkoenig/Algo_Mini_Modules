#!/usr/bin/env python3
"""
Test-Skript für den Bitget REST API Client

Dieses Skript testet die grundlegenden Funktionen des Bitget REST API Clients.
"""

import os
import sys
import json
from pathlib import Path

# Füge das Root-Verzeichnis zum Pfad hinzu, um relative Imports zu ermöglichen
root_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(root_dir))

# Importiere den Bitget REST Client
from modules.Websocket_Raw_Data.bitget_rest_client import BitgetRestClient, is_valid_symbol


def test_ticker():
    """Testet die Ticker-Funktion"""
    print("\n=== Test: Ticker-Daten abrufen ===")
    
    # Initialisiere den Client
    client = BitgetRestClient(verbose=True)
    
    # Teste mit einem gültigen Symbol
    symbol = "BTCUSDT_UMCBL"
    print(f"Teste mit Symbol: {symbol}")
    
    # Hole Ticker-Daten
    ticker_data = client.get_ticker(symbol)
    
    # Überprüfe, ob die Anfrage erfolgreich war
    if "error" in ticker_data:
        print(f"❌ Fehler: {ticker_data['error']}")
        return False
    
    # Überprüfe, ob Daten vorhanden sind
    if "data" not in ticker_data:
        print("❌ Keine Daten in der Antwort")
        return False
    
    # Verarbeite Ticker-Daten
    ticker_df = client.process_ticker_data(ticker_data)
    
    if ticker_df.empty:
        print("❌ Keine Daten im DataFrame")
        return False
    
    print("✅ Ticker-Daten erfolgreich abgerufen und verarbeitet")
    print(f"Daten: {ticker_df[['datetime', 'symbol', 'last_price']].to_string(index=False)}")
    
    return True


def test_klines():
    """Testet die Kerzendaten-Funktion"""
    print("\n=== Test: Kerzendaten abrufen ===")
    
    # Initialisiere den Client
    client = BitgetRestClient(verbose=True)
    
    # Teste mit einem gültigen Symbol
    symbol = "BTCUSDT_UMCBL"
    print(f"Teste mit Symbol: {symbol}")
    
    # Hole Kerzendaten
    klines_data = client.get_klines(symbol, granularity="1m", limit=5)
    
    # Überprüfe, ob die Anfrage erfolgreich war
    if "error" in klines_data:
        print(f"❌ Fehler: {klines_data['error']}")
        return False
    
    # Überprüfe, ob Daten vorhanden sind
    if "data" not in klines_data:
        print("❌ Keine Daten in der Antwort")
        return False
    
    # Verarbeite Kerzendaten
    klines_df = client.process_klines_data(klines_data)
    
    if klines_df.empty:
        print("❌ Keine Daten im DataFrame")
        return False
    
    print("✅ Kerzendaten erfolgreich abgerufen und verarbeitet")
    print(f"Daten: {klines_df[['datetime', 'open', 'close']].head(3).to_string(index=False)}")
    
    return True


def test_orderbook():
    """Testet die Orderbuch-Funktion"""
    print("\n=== Test: Orderbuch abrufen ===")
    
    # Initialisiere den Client
    client = BitgetRestClient(verbose=True)
    
    # Teste mit einem gültigen Symbol
    symbol = "BTCUSDT_UMCBL"
    print(f"Teste mit Symbol: {symbol}")
    
    # Hole Orderbuch
    orderbook_data = client.get_orderbook(symbol, limit=3)
    
    # Überprüfe, ob die Anfrage erfolgreich war
    if "error" in orderbook_data:
        print(f"❌ Fehler: {orderbook_data['error']}")
        return False
    
    # Überprüfe, ob Daten vorhanden sind
    if "data" not in orderbook_data:
        print("❌ Keine Daten in der Antwort")
        return False
    
    data = orderbook_data.get("data", {})
    
    if not data:
        print("❌ Leere Daten in der Antwort")
        return False
    
    asks = data.get("asks", [])
    bids = data.get("bids", [])
    
    if not asks or not bids:
        print("❌ Keine Asks oder Bids im Orderbuch")
        return False
    
    print("✅ Orderbuch erfolgreich abgerufen")
    print(f"Asks (Top 3): {asks[:3]}")
    print(f"Bids (Top 3): {bids[:3]}")
    
    return True


def test_trades():
    """Testet die Trades-Funktion"""
    print("\n=== Test: Trades abrufen ===")
    
    # Initialisiere den Client
    client = BitgetRestClient(verbose=True)
    
    # Teste mit einem gültigen Symbol
    symbol = "BTCUSDT_UMCBL"
    print(f"Teste mit Symbol: {symbol}")
    
    # Hole Trades
    trades_data = client.get_trades(symbol, limit=3)
    
    # Überprüfe, ob die Anfrage erfolgreich war
    if "error" in trades_data:
        print(f"❌ Fehler: {trades_data['error']}")
        return False
    
    # Überprüfe, ob Daten vorhanden sind
    if "data" not in trades_data:
        print("❌ Keine Daten in der Antwort")
        return False
    
    data = trades_data.get("data", [])
    
    if not data:
        print("❌ Leere Daten in der Antwort")
        return False
    
    print("✅ Trades erfolgreich abgerufen")
    print(f"Trades (Top 3): {json.dumps(data[:3], indent=2)}")
    
    return True


def test_symbol_validation():
    """Testet die Symbol-Validierung"""
    print("\n=== Test: Symbol-Validierung ===")
    
    # Teste mit einem gültigen Symbol
    valid_symbol = "BTCUSDT_UMCBL"
    is_valid = is_valid_symbol(valid_symbol)
    print(f"Symbol '{valid_symbol}' ist gültig: {is_valid}")
    
    if not is_valid:
        print(f"❌ Symbol '{valid_symbol}' sollte gültig sein")
        return False
    
    # Teste mit einem ungültigen Symbol
    invalid_symbol = "INVALID_SYMBOL"
    is_valid = is_valid_symbol(invalid_symbol)
    print(f"Symbol '{invalid_symbol}' ist gültig: {is_valid}")
    
    if is_valid:
        print(f"❌ Symbol '{invalid_symbol}' sollte ungültig sein")
        return False
    
    print("✅ Symbol-Validierung funktioniert korrekt")
    
    return True


def run_tests():
    """Führt alle Tests aus"""
    tests = [
        test_symbol_validation,
        test_ticker,
        test_klines,
        test_orderbook,
        test_trades
    ]
    
    results = []
    
    for test in tests:
        result = test()
        results.append(result)
    
    # Zeige Zusammenfassung
    print("\n=== Testergebnisse ===")
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ Bestanden" if result else "❌ Fehlgeschlagen"
        print(f"{i+1}. {test.__name__}: {status}")
    
    # Berechne Erfolgsrate
    success_rate = sum(results) / len(results) * 100
    print(f"\nErfolgsrate: {success_rate:.1f}% ({sum(results)}/{len(results)})")


if __name__ == "__main__":
    run_tests() 