# src/cogs/general.py
from loguru import logger
import asyncio
import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='hello', description='Say hello!')
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello, {ctx.author.mention}!')

    @commands.hybrid_command(name='bigmass', description='big splash!')
    async def bigmass(self, ctx: commands.Context):
        await ctx.send('Big Mass! Big Splash!')
    
    @app_commands.command(name='111', description='111 someone.')
    async def one_one_one(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        # Send the message and store the returned Message object
        await interaction.response.send_message(f'111 {user.mention} "{reason}" by: {interaction.user.mention}.')
        message = await interaction.original_response()
        await message.add_reaction('💀')

        await asyncio.sleep(120)

        try:
            fresh_message = await interaction.channel.fetch_message(message.id)
        except discord.NotFound:
            logger.warning(f"Message {message.id} for 111 command was deleted before check could complete.")
            return 

        skull_reaction = discord.utils.get(fresh_message.reactions, emoji='💀')
        required_reactions = 11
        if skull_reaction and skull_reaction.count >= required_reactions:
            await interaction.channel.send(f"cya hick {user.mention}")
        else:
            await interaction.channel.send(f"cya hick {interaction.user.mention}")

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
