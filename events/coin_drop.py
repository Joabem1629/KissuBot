import random

import discord
from discord.ext import commands

from utils.levels_core import COIN, GEM, get_levels
from utils.levels_views import DropView


class CoinDrop(commands.Cog):
    """Drops de monedas estilo kakera: aparecen al azar y el primero que pulsa se las lleva."""

    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.Cog.listener()
    async def on_xp_gain(self, message: discord.Message):
        cfg = self.levels.cfg(message.guild.id)
        if random.uniform(0, 100) >= cfg["drop_chance"]:
            return
        cantidad = random.randint(cfg["drop_min"], max(cfg["drop_min"], cfg["drop_max"]))
        view = DropView(self.levels, cantidad)
        embed = discord.Embed(
            title=f"{GEM} ¡Apareció un drop!",
            description=f"Pulsa el botón para llevarte **{cantidad}** {COIN}",
            color=0x9b59b6)
        try:
            view.message = await message.channel.send(embed=embed, view=view)
        except discord.HTTPException:
            pass
