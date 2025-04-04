#!/usr/bin/env python3
"""
KuCoin Credentials Module
------------------------

Dieses Modul lädt die API-Zugangsdaten für KuCoin aus der .env-Datei.
"""

import os
from dotenv import load_dotenv
from typing import Dict, Optional

def get_credentials() -> Dict[str, str]:
    """
    Lädt die KuCoin API-Zugangsdaten aus der .env-Datei.
    
    Returns:
        Dict mit den Zugangsdaten (api_key, secret_key, passphrase)
    """
    # Lade .env Datei
    load_dotenv()
    
    # Hole Zugangsdaten aus Umgebungsvariablen
    api_key = os.getenv("KUCOIN_API_KEY")
    secret_key = os.getenv("KUCOIN_SECRET_KEY")
    passphrase = os.getenv("KUCOIN_PASSPHRASE")
    
    # Prüfe ob alle Zugangsdaten vorhanden sind
    if not all([api_key, secret_key, passphrase]):
        raise ValueError(
            "KuCoin API-Zugangsdaten fehlen in der .env-Datei. "
            "Bitte stelle sicher, dass KUCOIN_API_KEY, KUCOIN_SECRET_KEY "
            "und KUCOIN_PASSPHRASE gesetzt sind."
        )
    
    return {
        "api_key": api_key,
        "secret_key": secret_key,
        "passphrase": passphrase
    } 