from typing import Optional

import discord
from discord.ext import commands

from utils.levels_core import get_levels


class Medallas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_command(name="medallas", help="Muestra tus medallas (o las de otro miembro).",
                             description="Mira tus medallas")
    @commands.guild_only()
    async def medallas(self, ctx, miembro: Optional[discord.Member] = None):
        member = miembro or ctx.author
        g = self.levels.guild(ctx.guild.id)
        u = self.levels.user(ctx.guild.id, member.id)

        tiene = [g["medals"][m] for m in u["medals"] if m in g["medals"]]
        embed = discord.Embed(title=f"🏅 Medallas de {member.display_name}", color=0xf1c40f)
        embed.description = "\n".join(f"{m['emoji']} **{m['name']}** — {m['desc']}" for m in tiene) \
            or "Sin medallas todavía."

        pendientes = [g["medals"][m] for m in u["pending"] if m in g["medals"]]
        if pendientes:
            embed.add_field(name="Pendientes de reclamar (usa el comando reclamar)",
                            value=" ".join(f"{m['emoji']} {m['name']}" for m in pendientes))
        await ctx.send(embed=embed)
