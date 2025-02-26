"""
Konfigurationseinstellungen für die WebSocket Data Explorer App

Diese Datei enthält Konfigurationseinstellungen für die Anwendung.
"""

import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Allgemeine Einstellungen
APP_NAME = "WebSocket Data Explorer"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Pfad-Einstellungen
DATA_DIR = os.getenv("DATA_DIR", "data")
LOG_DIR = os.getenv("LOG_DIR", "logs")

# Stellen Sie sicher, dass die Verzeichnisse existieren
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# WebSocket-Einstellungen
WEBSOCKET_TIMEOUT = int(os.getenv("WEBSOCKET_TIMEOUT", "10"))
WEBSOCKET_RECONNECT_DELAY = int(os.getenv("WEBSOCKET_RECONNECT_DELAY", "5"))
WEBSOCKET_PING_INTERVAL = int(os.getenv("WEBSOCKET_PING_INTERVAL", "30"))

# Daten-Einstellungen
MAX_BUFFER_SIZE = int(os.getenv("MAX_BUFFER_SIZE", "10000"))
DEFAULT_TIMEFRAME = os.getenv("DEFAULT_TIMEFRAME", "1min")

# KuCoin API-Einstellungen
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY", "")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET", "")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE", "")

# BitGet API-Einstellungen
BITGET_API_KEY = os.getenv("BITGET_API_KEY", "")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET", "")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE", "")

# WebSocket-URLs
KUCOIN_WEBSOCKET_ENDPOINT = {
    "futures": "wss://futures-ws.kucoin.com",
    "spot": "wss://ws-api.kucoin.com"
}

BITGET_WEBSOCKET_ENDPOINT = {
    "futures": "wss://ws.bitget.com/mix/v1/stream",
    "spot": "wss://ws.bitget.com/spot/v1/stream"
}

# Verfügbare Kanäle
AVAILABLE_CHANNELS = {
    "kucoin": {
        "futures": ["ticker", "kline", "trade", "depth", "depth5", "depth50", "execution", "position"],
        "spot": ["ticker", "kline", "trade", "depth", "depth5", "depth50", "match", "level2"]
    },
    "bitget": {
        "futures": ["ticker", "candle", "trade", "depth", "depth5", "depth20", "depth400", "liquidation"],
        "spot": ["ticker", "candle", "trade", "depth", "depth5", "depth20", "depth400"]
    }
}

# Streamlit-Einstellungen
STREAMLIT_THEME = {
    "primaryColor": "#FF4B4B",
    "backgroundColor": "#0E1117",
    "secondaryBackgroundColor": "#262730",
    "textColor": "#FAFAFA",
    "font": "sans serif"
} 