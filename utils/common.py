"""
Common utility functions for the Algotrading project.
"""
import os
import json
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
def setup_logging(module_name, log_level=logging.INFO):
    """Set up logging for a module."""
    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

def load_config(config_name):
    """
    Load configuration from a JSON file.
    
    Args:
        config_name (str): Name of the config file (without .json extension)
        
    Returns:
        dict: Configuration data
    """
    config_path = Path(__file__).parent.parent / "config" / f"{config_name}_config.json"
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file {config_path} not found")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file {config_path}")

def timestamp_to_datetime(timestamp_ms):
    """Convert millisecond timestamp to datetime object."""
    return datetime.fromtimestamp(timestamp_ms / 1000)

def datetime_to_timestamp(dt):
    """Convert datetime object to millisecond timestamp."""
    return int(dt.timestamp() * 1000)

def format_number(number, decimals=8):
    """Format a number with a specific number of decimal places."""
    return f"{number:.{decimals}f}" 