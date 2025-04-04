import asyncio
import logging
from modules.Credentials.BitGet_Credentials import get_credentials
from modules.Websocket_Raw_Data.Bitget_Websocket_Raw_Data import BitGetWebsocketRawData

# Logging Setup
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    # Credentials laden
    creds = get_credentials()
    
    # WebSocket Client initialisieren
    client = BitGetWebsocketRawData(
        api_key=creds['apiKey'],
        secret_key=creds['secretKey'],
        passphrase=creds['passphrase']
    )
    
    try:
        # Verbindung aufbauen
        await client.connect()
        logging.info("WebSocket Verbindung hergestellt")
        
        # Test-Channel abonnieren (BTC-USDT Ticker)
        await client.subscribe_ticker("BTCUSDT_UMCBL")
        logging.info("Ticker Channel abonniert")
        
        # 30 Sekunden Daten empfangen
        for _ in range(30):
            data = await client.receive_message()
            if data:
                logging.info(f"Empfangene Daten: {data}")
            await asyncio.sleep(1)
            
    except Exception as e:
        logging.error(f"Fehler: {str(e)}")
    finally:
        # Verbindung schließen
        await client.close()
        logging.info("WebSocket Verbindung geschlossen")

if __name__ == "__main__":
    asyncio.run(main()) 