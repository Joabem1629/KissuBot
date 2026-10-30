from discord.ext import commands

from utils.levels_core import COIN, get_levels


class Reclamar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_command(name="reclamar", help="Reclama las medallas que ya desbloqueaste.",
                             description="Reclama tus medallas desbloqueadas")
    @commands.guild_only()
    async def reclamar(self, ctx):
        got, coins = self.levels.claim_all(ctx.guild.id, ctx.author.id)
        if not got:
            await ctx.send("⚠️ No tienes medallas pendientes.")
            return
        txt = " ".join(f"{m['emoji']} **{m['name']}**" for m in got)
        await ctx.send(f"🏅 Reclamaste: {txt}" + (f"\n+{coins} {COIN}" if coins else ""))
