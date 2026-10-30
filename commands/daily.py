import time

from discord.ext import commands

from utils.levels_core import COIN, get_levels


class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_command(name="daily", help="Reclama tu recompensa diaria de monedas.",
                             description="Recompensa diaria")
    @commands.guild_only()
    async def daily(self, ctx):
        u = self.levels.user(ctx.guild.id, ctx.author.id)
        faltan = 86400 - (time.time() - u["last_daily"])
        if faltan > 0:
            await ctx.send(f"⏳ Vuelve en **{int(faltan // 3600)}h {int(faltan % 3600 // 60)}m**.")
            return

        cantidad = self.levels.cfg(ctx.guild.id)["daily"]
        u["coins"] += cantidad
        u["last_daily"] = time.time()
        self.levels.store.dirty()
        await ctx.send(f"🎁 Reclamaste tu diario: **+{cantidad}** {COIN}")
