#!/usr/bin/env python3
"""
BitGet Credentials Module
------------------------

Dieses Modul lädt die API-Credentials für BitGet aus der .env-Datei
"""

import os
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv

def get_credentials() -> Dict[str, str]:
    """
    Lädt die BitGet API-Credentials aus der .env-Datei
    
    Returns:
        Dict mit den Credentials (apiKey, secretKey, passphrase)
    """
    # Lade .env-Datei aus dem Root-Verzeichnis
    env_path = Path(__file__).resolve().parents[2] / '.env'
    load_dotenv(env_path)
    
    # Hole die Credentials
    api_key = os.getenv('BITGET_API_KEY')
    secret_key = os.getenv('BITGET_SECRET_KEY')
    passphrase = os.getenv('BITGET_PASSPHRASE')
    
    # Überprüfe, ob alle Credentials vorhanden sind
    if not all([api_key, secret_key, passphrase]):
        raise ValueError(
            "BitGet Credentials nicht vollständig. "
            "Bitte stelle sicher, dass BITGET_API_KEY, BITGET_SECRET_KEY und "
            "BITGET_PASSPHRASE in der .env-Datei definiert sind."
        )
    
    return {
        'apiKey': api_key,
        'secretKey': secret_key,
        'passphrase': passphrase
    }

if __name__ == "__main__":
    # Test the credentials loading
    try:
        creds = get_credentials()
        print("BitGet Credentials erfolgreich geladen!")
    except Exception as e:
        print(f"Fehler beim Laden der Credentials: {e}") 