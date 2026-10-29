import asyncio
from typing import Literal, Optional

import discord
from discord.ext import commands

from utils import rankcard
from utils.levels_core import get_levels, leer_imagen, require_mod


class MedalAdmin(commands.Cog):
    """Catálogo de medallas (solo mods): !medalla <crear|borrar>. La lista pública es !tienda."""

    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_group(name="medalla", help="Gestiona el catálogo de medallas.",
                           description="Gestión del catálogo de medallas")
    async def medalla(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("⚠️ Subcomandos: `crear` `borrar` (la lista pública es `tienda`)")

    @medalla.command(name="crear",
                     help='Crea una medalla. Ej: !medalla crear veterano "Veterano" 🎖️ "Llegó al nivel 20" nivel 20 100',
                     description="Crea una medalla (automática, a la venta o con imagen)")
    async def crear(self, ctx, clave: str, nombre: str, emoji: str, descripcion: str,
                    tipo_auto: Optional[Literal["nivel", "mensajes"]] = None,
                    valor_auto: Optional[int] = None,
                    recompensa: int = 0,
                    precio: Optional[int] = None,
                    imagen: Optional[discord.Attachment] = None):
        if not await require_mod(ctx):
            return
        clave = clave.lower()
        if not clave.isalnum():
            await ctx.send("⚠️ La clave solo puede tener letras y números.")
            return
        if (tipo_auto is None) != (valor_auto is None):
            await ctx.send("⚠️ Si es automática, indica `tipo_auto` y `valor_auto`.")
            return

        await ctx.defer()
        archivo = None
        if imagen:
            data = await leer_imagen(ctx, imagen)
            if not data:
                return
            archivo = f"{ctx.guild.id}_{clave}.png"
            await asyncio.to_thread(rankcard.save_icon, data, self.levels.medal_dir / archivo)

        self.levels.guild(ctx.guild.id)["medals"][clave] = {
            "name": nombre, "emoji": emoji, "desc": descripcion,
            "auto_type": tipo_auto, "auto_value": valor_auto,
            "reward": max(0, recompensa), "price": precio, "image": archivo,
        }
        self.levels.store.dirty()
        await ctx.send(f"✅ Medalla {emoji} **{nombre}** creada (`{clave}`)")

    @medalla.command(name="borrar", help="Elimina una medalla del catálogo.",
                     description="Elimina una medalla del catálogo")
    async def borrar(self, ctx, clave: str):
        if not await require_mod(ctx):
            return
        clave = clave.lower()
        g = self.levels.guild(ctx.guild.id)
        m = g["medals"].pop(clave, None)
        if not m:
            await ctx.send("⚠️ Esa medalla no existe.")
            return
        if m.get("image"):
            (self.levels.medal_dir / m["image"]).unlink(missing_ok=True)
        for u in g["users"].values():
            for lista in (u["medals"], u["pending"]):
                if clave in lista:
                    lista.remove(clave)
        self.levels.store.dirty()
        await ctx.send(f"🗑️ Medalla `{clave}` eliminada")

    @borrar.autocomplete("clave")
    async def autocompletar_clave(self, interaction, current: str):
        return self.levels.medal_choices(interaction.guild_id, current)
