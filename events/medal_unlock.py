import discord
from discord.ext import commands

from utils.levels_core import get_levels
from utils.levels_views import ClaimView


class MedalUnlock(commands.Cog):
    """Avisa cuando se desbloquea una medalla automática y deja el botón para reclamarla."""

    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.Cog.listener()
    async def on_medal_unlock(self, member: discord.Member, medal_id: str, canal):
        if not canal:  # desbloqueada por un cambio de un mod: se reclama con el comando reclamar
            return
        m = self.levels.guild(member.guild.id)["medals"].get(medal_id)
        if not m:
            return
        embed = discord.Embed(
            description=f"🏅 {member.mention} desbloqueó **{m['emoji']} {m['name']}**\n*{m['desc']}*",
            color=0xf1c40f)
        try:
            await canal.send(embed=embed, view=ClaimView(self.levels, member.id))
        except discord.HTTPException:
            pass
