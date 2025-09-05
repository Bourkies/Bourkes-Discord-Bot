# src/main.py
from loguru import logger
import tomllib
import os
from pathlib import Path
import sys
from loguru_setup import loguru_setup

def main():
    '''Main function'''
    logger.info("Running main.py")
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

    loguru_setup(config, PROJECT_ROOT)
    logger.info("Start of main.py")



    logger.info("End of main.py")


if __name__ == '__main__':
    main()