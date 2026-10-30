import discord
from discord.ext import commands

from utils.levels_core import get_levels


class RankUp(commands.Cog):
    """Asigna/quita los roles de rango según el nivel (también cuando un mod cambia el nivel)."""

    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.Cog.listener()
    async def on_level_change(self, member: discord.Member, viejo: int, nuevo: int):
        await self.levels.sync_roles(member, nuevo)
