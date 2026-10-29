import asyncio

import discord
from discord.ext import commands

from utils import rankcard
from utils.levels_core import get_levels, leer_imagen, require_mod


class RankBg(commands.Cog):
    """Fondos de la tarjeta de rango: !rankbg <rango|usuario|defecto|quitarrango|quitarusuario>"""

    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_group(name="rankbg", help="Gestiona los fondos de la tarjeta de rango.",
                           description="Fondos de la tarjeta de rango")
    async def rankbg(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("⚠️ Subcomandos: `rango` `quitarrango` `usuario` `quitarusuario` `defecto`")

    @rankbg.command(name="rango", help="Fondo que se usa desde cierto nivel en adelante. Adjunta la imagen.",
                    description="Fondo desde cierto nivel en adelante")
    async def rango(self, ctx, nivel: int, imagen: discord.Attachment):
        if not await require_mod(ctx):
            return
        await ctx.defer()
        data = await leer_imagen(ctx, imagen)
        if not data:
            return
        nombre = f"{ctx.guild.id}_tier_{nivel}.png"
        await asyncio.to_thread(rankcard.save_background, data, self.levels.bg_dir / nombre)
        self.levels.cfg(ctx.guild.id)["tier_bgs"][str(nivel)] = nombre
        self.levels.store.dirty()
        await ctx.send(f"🖼️ Fondo desde el nivel **{nivel}** actualizado")

    @rankbg.command(name="quitarrango", help="Quita el fondo de un nivel.", description="Quita el fondo de un nivel")
    async def quitarrango(self, ctx, nivel: int):
        if not await require_mod(ctx):
            return
        nombre = self.levels.cfg(ctx.guild.id)["tier_bgs"].pop(str(nivel), None)
        if not nombre:
            await ctx.send("⚠️ Ese nivel no tenía fondo.")
            return
        (self.levels.bg_dir / nombre).unlink(missing_ok=True)
        self.levels.store.dirty()
        await ctx.send(f"🗑️ Fondo del nivel {nivel} eliminado")

    @rankbg.command(name="usuario", help="Fondo personal para un miembro (tiene prioridad). Adjunta la imagen.",
                    description="Fondo personal para un miembro")
    async def usuario(self, ctx, miembro: discord.Member, imagen: discord.Attachment):
        if not await require_mod(ctx):
            return
        await ctx.defer()
        data = await leer_imagen(ctx, imagen)
        if not data:
            return
        nombre = f"{ctx.guild.id}_user_{miembro.id}.png"
        await asyncio.to_thread(rankcard.save_background, data, self.levels.bg_dir / nombre)
        self.levels.user(ctx.guild.id, miembro.id)["bg"] = nombre
        self.levels.store.dirty()
        await ctx.send(f"🖼️ Fondo personal de {miembro.mention} actualizado",
                       allowed_mentions=discord.AllowedMentions.none())

    @rankbg.command(name="quitarusuario", help="Quita el fondo personal de un miembro.",
                    description="Quita el fondo personal de un miembro")
    async def quitarusuario(self, ctx, miembro: discord.Member):
        if not await require_mod(ctx):
            return
        u = self.levels.user(ctx.guild.id, miembro.id)
        if u["bg"]:
            (self.levels.bg_dir / u["bg"]).unlink(missing_ok=True)
        u["bg"] = None
        self.levels.store.dirty()
        await ctx.send(f"🗑️ Fondo personal de {miembro.mention} eliminado",
                       allowed_mentions=discord.AllowedMentions.none())

    @rankbg.command(name="defecto", help="Fondo general (cuando no hay de rango ni personal). Adjunta la imagen.",
                    description="Fondo general de la tarjeta")
    async def defecto(self, ctx, imagen: discord.Attachment):
        if not await require_mod(ctx):
            return
        await ctx.defer()
        data = await leer_imagen(ctx, imagen)
        if not data:
            return
        await asyncio.to_thread(rankcard.save_background, data, self.levels.bg_dir / "default.png")
        await ctx.send("🖼️ Fondo por defecto actualizado")
