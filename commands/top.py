from discord.ext import commands

from utils.levels_core import get_levels
from utils.levels_views import PaginadorRanking


class Top(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_command(name="top", aliases=["leaderboard", "lb"],
                             help="Muestra el ranking de niveles del servidor.",
                             description="Ranking de niveles del servidor")
    @commands.guild_only()
    async def top(self, ctx):
        filas = sorted(
            ((int(uid), d["xp"]) for uid, d in self.levels.guild(ctx.guild.id)["users"].items() if d["xp"] > 0),
            key=lambda r: r[1], reverse=True)
        view = PaginadorRanking(filas, ctx)
        await ctx.send(embed=view.generar_embed(), view=view)
