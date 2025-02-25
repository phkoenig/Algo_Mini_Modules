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
    get_active_symbols,
    get_active_symbols_with_info,
    print_summary
)

def main():
    """Main function"""
    print("Beispiel 1: Einfache Liste aller aktiven Trading Pairs")
    active_symbols = get_active_symbols(include_inactive=False)
    
    print(f"Aktive Trading Pairs ({len(active_symbols)}):")
    for symbol in active_symbols[:10]:  # Zeige nur die ersten 10
        print(f"- {symbol}")
    
    if len(active_symbols) > 10:
        print(f"... und {len(active_symbols) - 10} weitere")
    
    print("\nBeispiel 2: Alle Trading Pairs (inkl. inaktive)")
    all_symbols = get_active_symbols(include_inactive=True)
    print(f"Anzahl aller Trading Pairs: {len(all_symbols)}")
    
    print("\nBeispiel 3: Trading Pairs mit zusätzlichen Informationen")
    pairs_with_info = get_active_symbols_with_info(include_inactive=True)
    print(f"Trading Pairs mit Info ({len(pairs_with_info)}):")
    
    for pair in pairs_with_info[:5]:  # Zeige nur die ersten 5
        print(f"- {pair['symbol']} ({pair['base_coin']}/{pair['quote_coin']}) - {pair['type']}")
    
    print("\nBeispiel 4: Verwendung in einer Schleife (simuliert)")
    print("Angenommen, wir möchten für jedes Trading Pair eine Aktion ausführen:")
    
    for symbol in active_symbols[:3]:  # Nur die ersten 3 für das Beispiel
        print(f"Verarbeite Trading Pair: {symbol}")
        # Hier würde die eigentliche Verarbeitung stattfinden
        print(f"  - Aktion für {symbol} abgeschlossen")
    
    print("\nBeispiel 5: Verwendung als Parameter für andere Funktionen")
    
    def example_function(trading_pairs):
        """Beispielfunktion, die eine Liste von Trading Pairs verwendet"""
        print(f"Funktion erhielt {len(trading_pairs)} Trading Pairs")
        print(f"Erste 3 Paare: {', '.join(trading_pairs[:3])}")
    
    # Rufe die Beispielfunktion mit der Liste der Trading Pairs auf
    example_function(active_symbols)

if __name__ == "__main__":
    main() 