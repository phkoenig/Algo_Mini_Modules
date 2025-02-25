"""
Credentials validator module for checking API credentials.
"""
import os
import sys
import argparse
from dotenv import load_dotenv

# Add project root to Python path for imports when running as script
if __name__ == "__main__":
    # Get the absolute path of the script
    script_path = os.path.abspath(__file__)
    # Get the project root (two directories up from the script)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
    # Add project root to Python path
    sys.path.insert(0, project_root)

from utils.common import setup_logging

# Set up logging
logger = setup_logging("Credentials_Validator")

def validate_bitget_credentials(verbose=True):
    """
    Validate BitGet API credentials.
    
    Args:
        verbose (bool): Whether to print detailed information
        
    Returns:
        dict: Dictionary with validation results and credential info
    """
    load_dotenv()
    
    # Get credentials from environment variables
    api_key = os.getenv('BITGET_API_KEY')
    secret_key = os.getenv('BITGET_SECRET_KEY')
    passphrase = os.getenv('BITGET_PASSPHRASE')
    
    # Check if credentials are set
    bitget_creds = {
        'BITGET_API_KEY': api_key,
        'BITGET_SECRET_KEY': secret_key,
        'BITGET_PASSPHRASE': passphrase
    }
    
    # Validate credentials
    validation_results = {}
    all_valid = True
    
    if verbose:
        logger.info("=== Checking BitGet credentials ===")
    
    for key, value in bitget_creds.items():
        is_valid = value is not None and value != ""
        validation_results[key] = is_valid
        
        if not is_valid:
            all_valid = False
        
        if verbose:
            status = "✓ Set" if is_valid else "✗ Missing"
            if is_valid and verbose:
                # Show first few characters of the credential for verification
                masked_value = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
                logger.info(f"{key}: {status} ({masked_value})")
            else:
                logger.info(f"{key}: {status}")
    
    result = {
        'exchange': 'BitGet',
        'all_valid': all_valid,
        'validation_results': validation_results,
        'credentials': {k: (v[:4] + "..." + v[-4:] if v and len(v) > 8 else None) for k, v in bitget_creds.items()}
    }
    
    if verbose:
        if all_valid:
            logger.info("BitGet credentials: All valid ✓")
        else:
            logger.warning("BitGet credentials: Some missing ✗")
        logger.info("=" * 30)
    
    return result

def validate_kucoin_credentials(verbose=True):
    """
    Validate KuCoin API credentials.
    
    Args:
        verbose (bool): Whether to print detailed information
        
    Returns:
        dict: Dictionary with validation results and credential info
    """
    load_dotenv()
    
    # Get credentials from environment variables
    api_key = os.getenv('KUCOIN_API_KEY')
    secret_key = os.getenv('KUCOIN_SECRET_KEY')
    passphrase = os.getenv('KUCOIN_PASSPHRASE')
    
    # Check if credentials are set
    kucoin_creds = {
        'KUCOIN_API_KEY': api_key,
        'KUCOIN_SECRET_KEY': secret_key,
        'KUCOIN_PASSPHRASE': passphrase
    }
    
    # Validate credentials
    validation_results = {}
    all_valid = True
    
    if verbose:
        logger.info("=== Checking KuCoin credentials ===")
    
    for key, value in kucoin_creds.items():
        is_valid = value is not None and value != ""
        validation_results[key] = is_valid
        
        if not is_valid:
            all_valid = False
        
        if verbose:
            status = "✓ Set" if is_valid else "✗ Missing"
            if is_valid and verbose:
                # Show first few characters of the credential for verification
                masked_value = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
                logger.info(f"{key}: {status} ({masked_value})")
            else:
                logger.info(f"{key}: {status}")
    
    result = {
        'exchange': 'KuCoin',
        'all_valid': all_valid,
        'validation_results': validation_results,
        'credentials': {k: (v[:4] + "..." + v[-4:] if v and len(v) > 8 else None) for k, v in kucoin_creds.items()}
    }
    
    if verbose:
        if all_valid:
            logger.info("KuCoin credentials: All valid ✓")
        else:
            logger.warning("KuCoin credentials: Some missing ✗")
        logger.info("=" * 30)
    
    return result

def validate_all_credentials(verbose=True):
    """
    Validate all exchange API credentials.
    
    Args:
        verbose (bool): Whether to print detailed information
        
    Returns:
        dict: Dictionary with validation results for all exchanges
    """
    bitget_result = validate_bitget_credentials(verbose)
    kucoin_result = validate_kucoin_credentials(verbose)
    
    all_valid = bitget_result['all_valid'] and kucoin_result['all_valid']
    
    result = {
        'bitget': bitget_result,
        'kucoin': kucoin_result,
        'all_valid': all_valid
    }
    
    if verbose:
        if all_valid:
            logger.info("SUMMARY: All exchange credentials are valid and ready to use ✓")
        else:
            logger.warning("SUMMARY: Some exchange credentials are missing or invalid ✗")
    
    return result

def validate_specific_exchange(exchange_name, verbose=True):
    """
    Validate credentials for a specific exchange.
    
    Args:
        exchange_name (str): Name of the exchange ('bitget', 'kucoin', or 'all')
        verbose (bool): Whether to print detailed information
        
    Returns:
        dict: Dictionary with validation results
    """
    exchange_name = exchange_name.lower()
    
    if exchange_name == 'bitget':
        return validate_bitget_credentials(verbose)
    elif exchange_name == 'kucoin':
        return validate_kucoin_credentials(verbose)
    elif exchange_name == 'all':
        return validate_all_credentials(verbose)
    else:
        logger.error(f"Unknown exchange: {exchange_name}")
        logger.info("Supported exchanges: bitget, kucoin, all")
        return {'error': f"Unknown exchange: {exchange_name}"}

def main():
    """Main function to run the validator from command line."""
    parser = argparse.ArgumentParser(description='Validate exchange API credentials')
    parser.add_argument('exchange', nargs='?', default='all', 
                        help='Exchange to validate (bitget, kucoin, all)')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress detailed output')
    
    args = parser.parse_args()
    
    result = validate_specific_exchange(args.exchange, verbose=not args.quiet)
    
    # Return non-zero exit code if validation fails
    if 'error' in result or ('all_valid' in result and not result['all_valid']):
        sys.exit(1)

if __name__ == "__main__":
    main() 