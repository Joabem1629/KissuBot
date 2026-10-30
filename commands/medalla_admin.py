
import asyncio
import shlex
from typing import Optional

import discord
from discord.ext import commands

from utils import rankcard
from utils.levels_core import get_levels, leer_imagen, require_mod


class MedalAdmin(commands.Cog):
    """Catálogo de medallas: crear y borrar."""

    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_group(
        name="medalla",
        help="Gestiona el catálogo de medallas.",
        description="Gestión del catálogo de medallas"
    )
    async def medalla(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "⚠️ Subcomandos: `crear` y `borrar`. "
                "La lista pública es `tienda`."
            )

    @medalla.command(
        name="crear",
        help="Crea una medalla usando opciones.",
        description="Crea una medalla manual o automática."
    )
    async def crear(
        self,
        ctx,
        clave: str,
        nombre: str,
        emoji: str,
        descripcion: str,
        *,
        opciones: str = ""
    ):
        if not await require_mod(ctx):
            return

        clave = clave.lower()

        if not clave.isalnum():
            await ctx.send(
                "⚠️ La clave solo puede tener letras y números."
            )
            return

        try:
            args = shlex.split(opciones)
        except ValueError:
            await ctx.send("⚠️ Hay comillas sin cerrar en las opciones.")
            return

        tipo_auto = None
        valor_auto = None
        recompensa = 0
        precio = None

        i = 0

        while i < len(args):
            opcion = args[i].lower()

            if opcion == "--tipo":
                if i + 1 >= len(args):
                    await ctx.send("⚠️ Falta el valor de `--tipo`.")
                    return

                tipo_auto = args[i + 1].lower()

                if tipo_auto not in ("nivel", "mensajes"):
                    await ctx.send(
                        "⚠️ El tipo debe ser `nivel` o `mensajes`."
                    )
                    return

                i += 2

            elif opcion == "--valor":
                if i + 1 >= len(args):
                    await ctx.send("⚠️ Falta el valor de `--valor`.")
                    return

                try:
                    valor_auto = int(args[i + 1])
                except ValueError:
                    await ctx.send("⚠️ El valor automático debe ser un número.")
                    return

                if valor_auto < 1:
                    await ctx.send("⚠️ El valor debe ser mayor que cero.")
                    return

                i += 2

            elif opcion == "--recompensa":
                if i + 1 >= len(args):
                    await ctx.send("⚠️ Falta el valor de `--recompensa`.")
                    return

                try:
                    recompensa = int(args[i + 1])
                except ValueError:
                    await ctx.send("⚠️ La recompensa debe ser un número.")
                    return

                if recompensa < 0:
                    await ctx.send("⚠️ La recompensa no puede ser negativa.")
                    return

                i += 2

            elif opcion == "--precio":
                if i + 1 >= len(args):
                    await ctx.send("⚠️ Falta el valor de `--precio`.")
                    return

                try:
                    precio = int(args[i + 1])
                except ValueError:
                    await ctx.send("⚠️ El precio debe ser un número.")
                    return

                if precio < 0:
                    await ctx.send("⚠️ El precio no puede ser negativo.")
                    return

                i += 2

            else:
                await ctx.send(
                    f"⚠️ Opción desconocida: `{args[i]}`."
                )
                return

        if (tipo_auto is None) != (valor_auto is None):
            await ctx.send(
                "⚠️ Si usas `--tipo`, también debes indicar `--valor`."
            )
            return

        await ctx.defer()

        archivo = None

        if ctx.message and ctx.message.attachments:
            imagen = ctx.message.attachments[0]

            data = await leer_imagen(ctx, imagen)

            if not data:
                return

            archivo = f"{ctx.guild.id}_{clave}.png"

            await asyncio.to_thread(
                rankcard.save_icon,
                data,
                self.levels.medal_dir / archivo
            )

        self.levels.guild(ctx.guild.id)["medals"][clave] = {
            "name": nombre,
            "emoji": emoji,
            "desc": descripcion,
            "auto_type": tipo_auto,
            "auto_value": valor_auto,
            "reward": recompensa,
            "price": precio,
            "image": archivo,
        }

        self.levels.store.dirty()

        await ctx.send(
            f"✅ Medalla {emoji} **{nombre}** creada (`{clave}`)."
        )

    @medalla.command(
        name="borrar",
        help="Elimina una medalla del catálogo.",
        description="Elimina una medalla del catálogo."
    )
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
            (
                self.levels.medal_dir / m["image"]
            ).unlink(missing_ok=True)

        for u in g["users"].values():
            for lista in (u["medals"], u["pending"]):
                if clave in lista:
                    lista.remove(clave)

        self.levels.store.dirty()

        await ctx.send(f"🗑️ Medalla `{clave}` eliminada.")

    @borrar.autocomplete("clave")
    async def autocompletar_clave(self, interaction, current: str):
        return self.levels.medal_choices(
            interaction.guild_id,
            current
        )


async def setup(bot):
    await bot.add_cog(MedalAdmin(bot))
