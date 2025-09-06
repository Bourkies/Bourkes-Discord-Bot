# src/main.py
from loguru import logger
import tomllib
import os
from pathlib import Path
import sys
from loguru_setup import loguru_setup
import discord
from dotenv import load_dotenv
from bot import AuOsrsBot

APP_VERSION = '0.0.1'
startup_message = f" Bot Starting Up v{APP_VERSION} "

def main():
    '''Main function to run discord bot'''
    # --- Configuration Loading ---
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    CONFIG_PATH = PROJECT_ROOT / 'config.toml'

    try:
        with open(CONFIG_PATH, 'rb') as config_file:
            config = tomllib.load(config_file)
    except FileNotFoundError:
        logger.critical(f"Configuration file not found at: {CONFIG_PATH}")
        sys.exit(1)

    loguru_setup(config, PROJECT_ROOT)
    logger.info(f"{startup_message:=^60}")

    # --- Environment Variable Loading ---
    load_dotenv()
    discord_token = os.getenv('DISCORD_TOKEN')
    if not discord_token:
        logger.critical('DISCORD_TOKEN not found in environment variables or .env file.')
        logger.critical('Please ensure it is set')
        logger.critical('Exiting...')
        sys.exit(1)

    try:
        discord_server_id = int(os.getenv('DISCORD_SERVER_ID'))
    except (TypeError, ValueError):
        logger.critical('DISCORD_SERVER_ID not found in environment variables or .env file.')
        logger.critical('Please ensure it is set')
        logger.critical('Exiting...')
        sys.exit(1)

    # --- Start discord bot ---
    intents = discord.Intents.default()
    intents.message_content = True

    bot = AuOsrsBot(server_id=discord_server_id, command_prefix='!', intents=intents)
    bot.run(discord_token)

if __name__ == '__main__':
    main()
   