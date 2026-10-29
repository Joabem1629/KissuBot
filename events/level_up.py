import discord
from discord.ext import commands

from utils.levels_core import COIN, get_levels


class LevelUp(commands.Cog):
    """Avisa cuando alguien sube de nivel hablando."""

    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.Cog.listener()
    async def on_level_up(self, member: discord.Member, viejo: int, nuevo: int, canal, monedas: int):
        cfg = self.levels.cfg(member.guild.id)
        destino = member.guild.get_channel(cfg["levelup_channel"]) if cfg["levelup_channel"] else None
        destino = destino or canal
        if not destino:
            return
        try:
            await destino.send(f"🎉 {member.mention} subió al **nivel {nuevo}** (+{monedas} {COIN})")
        except discord.HTTPException:
            pass
