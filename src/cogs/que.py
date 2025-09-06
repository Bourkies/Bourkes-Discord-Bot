# src/cogs/Que.py
from loguru import logger
import asyncio
import discord
from discord.ext import commands
from discord import app_commands

class Que(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot




async def setup(bot: commands.Bot):
    await bot.add_cog(Que(bot))
