from typing import Optional

import discord
from discord.ext import commands

from utils.levels_core import COIN, get_levels


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_command(name="balance", aliases=["monedas", "bal"],
                             help="Muestra cuántas monedas tienes (o tiene otro miembro).",
                             description="Mira tus monedas")
    @commands.guild_only()
    async def balance(self, ctx, miembro: Optional[discord.Member] = None):
        m = miembro or ctx.author
        u = self.levels.user(ctx.guild.id, m.id)
        embed = discord.Embed(
            description=f"{COIN} **{m.display_name}** tiene **{u['coins']:,}** monedas",
            color=0xf1c40f)
        await ctx.send(embed=embed)
