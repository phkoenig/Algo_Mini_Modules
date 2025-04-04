import os
from dotenv import load_dotenv

def test_credentials():
    load_dotenv()
    
    # BitGet credentials
    bitget_creds = {
        'BITGET_API_KEY': os.getenv('BITGET_API_KEY'),
        'BITGET_SECRET_KEY': os.getenv('BITGET_SECRET_KEY'),
        'BITGET_PASSPHRASE': os.getenv('BITGET_PASSPHRASE')
    }
    
    # KuCoin credentials
    kucoin_creds = {
        'KUCOIN_API_KEY': os.getenv('KUCOIN_API_KEY'),
        'KUCOIN_SECRET_KEY': os.getenv('KUCOIN_SECRET_KEY'),
        'KUCOIN_PASSPHRASE': os.getenv('KUCOIN_PASSPHRASE')
    }
    
    print("\nChecking BitGet credentials:")
    for key, value in bitget_creds.items():
        status = "✓ Set" if value else "✗ Missing"
        print(f"{key}: {status}")
    
    print("\nChecking KuCoin credentials:")
    for key, value in kucoin_creds.items():
        status = "✓ Set" if value else "✗ Missing"
        print(f"{key}: {status}")

if __name__ == "__main__":
    test_credentials() 