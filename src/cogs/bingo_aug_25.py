# src/cogs/Bingo_aug_25.py
import tomllib
from pathlib import Path
from loguru import logger
import discord
from discord.ext import commands
from discord import app_commands

# Define the path to the bingo data directory relative to this file's location
BINGO_DATA_DIR = Path(__file__).resolve().parent.parent / "cogs" /"bingo_aug_25"
BINGO_TILES_FILE = BINGO_DATA_DIR / "bingo_tiles.toml"


class Bingo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bingo_tiles = self._load_bingo_tiles()

    def _load_bingo_tiles(self):
        """Loads bingo tile data from the TOML file."""
        logger.debug(f"Attempting to load bingo tiles from: {BINGO_TILES_FILE}")
        try:
            with open(BINGO_TILES_FILE, "rb") as f:
                data = tomllib.load(f)
                logger.info(f"Successfully loaded {len(data)} bingo tiles from {BINGO_TILES_FILE}")
                return data
        except FileNotFoundError:
            logger.error(f"Bingo tiles file not found at: {BINGO_TILES_FILE}")
            return {}
        except Exception as e:
            logger.error(f"Failed to load or parse bingo tiles file: {e}")
            return {}

    @commands.hybrid_command(name='place_holder', description='A placeholder command.')
    async def place_holder(self, ctx: commands.Context):
        await ctx.send(f'Hello, {ctx.author.mention}!')

    @app_commands.command(name='bingo_tile', description='Look up information for a bingo tile.')
    async def bingo_tile(self, interaction: discord.Interaction, tile: str):
        """Displays information about a specific bingo tile."""
        tile_id = tile.upper()
        tile_data = self.bingo_tiles.get(tile_id)

        if not tile_data:
            await interaction.response.send_message(
                f"Sorry, I couldn't find a bingo tile with the ID `{tile_id}`.",
                ephemeral=True
            )
            return

        # --- Build the Embed ---
        title = f"{tile_id}: {tile_data.get('name', 'No Name Provided')}"
        description = tile_data.get('description', 'No description available.')

        # Handle color
        color_name = tile_data.get('color')
        embed_color = discord.Color.default()
        if color_name and hasattr(discord.Color, color_name):
            embed_color = getattr(discord.Color, color_name)()

        embed = discord.Embed(title=title, description=description, color=embed_color)

        # Add points field if it exists in the tile data
        points = tile_data.get('points')
        if points is not None:
            embed.add_field(name="Points", value=str(points))

        # Handle image attachment
        image_filename = tile_data.get('image')
        discord_file = None
        if image_filename:
            image_path = BINGO_DATA_DIR / image_filename
            if image_path.is_file():
                discord_file = discord.File(image_path, filename=image_filename)
                embed.set_thumbnail(url=f"attachment://{image_filename}")

        # Send the response, only including the 'file' kwarg if it exists.
        kwargs = {'embed': embed}
        if discord_file:
            kwargs['file'] = discord_file
        
        await interaction.response.send_message(**kwargs)

async def setup(bot: commands.Bot):
    await bot.add_cog(Bingo(bot))