import discord
from discord.ext import commands

from utils.levels_core import COIN, get_levels


class Tienda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_command(name="tienda", help="Muestra el catálogo de medallas del servidor.",
                             description="Catálogo de medallas")
    @commands.guild_only()
    async def tienda(self, ctx):
        medallas = self.levels.guild(ctx.guild.id)["medals"]
        lineas = []
        for clave, m in medallas.items():
            if m.get("price") is not None:
                como = f"{COIN} {m['price']:,}"
            elif m.get("auto_type"):
                como = f"🔓 {m['auto_type']} {m['auto_value']}"
            else:
                como = "🎖️ Solo la dan los mods"
            lineas.append(f"{m['emoji']} **{m['name']}** (`{clave}`) — {m['desc']}\n　{como}")

        embed = discord.Embed(title="🏅 Medallas", color=0xf1c40f,
                              description="\n".join(lineas) or "Aún no hay medallas.")
        await ctx.send(embed=embed)
