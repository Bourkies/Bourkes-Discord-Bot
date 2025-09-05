# src/main.py
from loguru import logger
import tomllib
import os
import pathlib
from pathlib import Path
import sys


# --- Configuration Loading ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / 'config.toml'


try:
    with open(CONFIG_PATH, 'rb') as congif_file:
        logger.debug("opened file")
        config = tomllib.load(congif_file)
except FileNotFoundError:
    logger.critical("FileNotFoundError except error: config file not found")
    sys.exit(1)

# --- Loguru Setup ---
log_config = config.get('logging', {})
log_file = PROJECT_ROOT / log_config.get('file_path', 'logs/default.log')
log_dir = pathlib.Path(log_file).parent
os.makedirs(log_dir, exist_ok=True)
logger.remove()

# Add a handler for console output
logger.add(
    sys.stderr,
    level=log_config.get('level', 'INFO'),
    format=log_config.get('format'),
    colorize=True
)

# Add a handler for file output using settings from the config file
logger.add(
    log_file,
    level=log_config.get('level', 'INFO'),
    format=log_config.get('format'),
    rotation=log_config.get('rotation', '10 MB'),
    retention=log_config.get('retention', '7 days'),
    enqueue=True,
    backtrace=True
)