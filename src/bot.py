# src/bot.py
import os
from pathlib import Path
from loguru import logger
import discord
from discord.ext import commands


class AuOsrsBot(commands.Bot):
    """A custom Discord client for the AuOSRS community."""

    def __init__(self, server_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_id = server_id
        self.synced = False

    async def setup_hook(self):
        """This is called once when the bot logs in, before on_ready."""
        logger.info("Running setup hook...")
        await self.load_cogs()

    async def load_cogs(self):
        """Finds and loads all cogs in the 'cogs' directory."""
        cogs_dir = Path(__file__).parent / "cogs"
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    logger.success(f"Loaded cog: {filename}")
                except Exception as e:
                    logger.error(f"Failed to load cog {filename}: {e}")

    async def on_ready(self):
        """Called when the bot is ready and connected to Discord."""
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')

        # Log connected guilds and enforce single-server policy.
        logger.info("Checking guild connections...")
        authorized_guild = None
        for guild in self.guilds:
            if guild.id == self.server_id:
                logger.info(f"- Connected to authorized guild: {guild.name} (ID: {guild.id})")
                authorized_guild = guild
            else:
                logger.warning(f"- Found in unauthorized guild: {guild.name} (ID: {guild.id}). Leaving...")
                await guild.leave()

        # Sync commands only if we are in the authorized guild and haven't synced yet.
        if authorized_guild and not self.synced:
            logger.info(f"Syncing commands to {authorized_guild.name}...")
            guild_for_sync = discord.Object(id=self.server_id)
            self.tree.copy_global_to(guild=guild_for_sync)
            await self.tree.sync(guild=guild_for_sync)
            logger.info(f"Commands synced to {authorized_guild.name} ID:{self.server_id}")
            self.synced = True
        elif not authorized_guild:
            logger.warning(f"Bot is not in the authorized server (ID: {self.server_id}). Commands will not be available.")

        logger.info(f"{'Bot Running':-^60}")

    async def on_guild_join(self, guild: discord.Guild):
        """Called when the bot joins a new guild. Enforces the single-server policy."""
        if guild.id != self.server_id:
            logger.warning(f"Joined unauthorized guild: {guild.name} (ID: {guild.id}). Leaving immediately.")
            await guild.leave()
        else:
            logger.info(f"Joined authorized guild: {guild.name} (ID: {guild.id})")

    async def on_command_completion(self, ctx: commands.Context):
        """Logs when a command has been successfully invoked."""
        # Since the bot is locked to one server, we can be specific.
        # The check for ctx.guild is still good practice.
        if ctx.guild:
            location = f"in channel #{ctx.channel.name}"
        else:
            location = "in a DM"

        logger.info(f"Command '{ctx.command.name}' used by '{ctx.author}' (ID: {ctx.author.id}) {location}.")
