from typing import Literal, Optional

import discord
from discord.ext import commands

from utils.levels_core import COIN, get_levels, level_from_xp, require_mod, xp_for_level

SIN_PINGS = discord.AllowedMentions.none()


class Lvl(commands.Cog):
    """Herramientas de moderación del sistema de niveles: !lvl <subcomando>"""

    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_group(name="lvl", help="Herramientas de moderación de niveles.",
                           description="Herramientas de moderación de niveles")
    async def lvl(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("⚠️ Subcomandos: `addxp` `removexp` `setxp` `setlevel` `reset` `coins` "
                           "`givemedal` `takemedal` `role` `unrole` `ignore` `modrole` "
                           "`levelchannel` `set` `config`")

    # ---------- XP y nivel ----------
    @lvl.command(name="addxp", help="Suma XP a un miembro.", description="Suma XP a un miembro")
    async def addxp(self, ctx, miembro: discord.Member, cantidad: int):
        if not await require_mod(ctx):
            return
        await self.levels.grant_xp(miembro, abs(cantidad))
        nivel = level_from_xp(self.levels.user(ctx.guild.id, miembro.id)["xp"])[0]
        await ctx.send(f"✅ +{abs(cantidad)} XP a {miembro.mention} (nivel {nivel})", allowed_mentions=SIN_PINGS)

    @lvl.command(name="removexp", help="Resta XP a un miembro.", description="Resta XP a un miembro")
    async def removexp(self, ctx, miembro: discord.Member, cantidad: int):
        if not await require_mod(ctx):
            return
        await self.levels.grant_xp(miembro, -abs(cantidad))
        nivel = level_from_xp(self.levels.user(ctx.guild.id, miembro.id)["xp"])[0]
        await ctx.send(f"✅ -{abs(cantidad)} XP a {miembro.mention} (nivel {nivel})", allowed_mentions=SIN_PINGS)

    @lvl.command(name="setxp", help="Fija la XP total de un miembro.", description="Fija la XP total de un miembro")
    async def setxp(self, ctx, miembro: discord.Member, xp: int):
        if not await require_mod(ctx):
            return
        await self.levels.set_total_xp(miembro, xp)
        await ctx.send(f"✅ {miembro.mention} ahora tiene {max(0, xp):,} XP totales", allowed_mentions=SIN_PINGS)

    @lvl.command(name="setlevel", help="Fija el nivel de un miembro.", description="Fija el nivel de un miembro")
    async def setlevel(self, ctx, miembro: discord.Member, nivel: int):
        if not await require_mod(ctx):
            return
        nivel = max(0, nivel)
        await self.levels.set_total_xp(miembro, xp_for_level(nivel))
        await ctx.send(f"✅ {miembro.mention} ahora es nivel **{nivel}**", allowed_mentions=SIN_PINGS)

    @lvl.command(name="reset", help="Reinicia la XP y los mensajes de un miembro.",
                 description="Reinicia XP y mensajes de un miembro")
    async def reset(self, ctx, miembro: discord.Member):
        if not await require_mod(ctx):
            return
        self.levels.user(ctx.guild.id, miembro.id)["messages"] = 0
        await self.levels.set_total_xp(miembro, 0)
        await ctx.send(f"♻️ XP de {miembro.mention} reiniciada", allowed_mentions=SIN_PINGS)

    # ---------- monedas y medallas ----------
    @lvl.command(name="coins", help="Suma o resta monedas (usa un número negativo para restar).",
                 description="Suma o resta monedas")
    async def coins(self, ctx, miembro: discord.Member, cantidad: int):
        if not await require_mod(ctx):
            return
        u = self.levels.user(ctx.guild.id, miembro.id)
        u["coins"] = max(0, u["coins"] + cantidad)
        self.levels.store.dirty()
        await ctx.send(f"✅ {miembro.mention} ahora tiene {u['coins']:,} {COIN}", allowed_mentions=SIN_PINGS)

    @lvl.command(name="givemedal", help="Da una medalla a un miembro.", description="Da una medalla a un miembro")
    async def givemedal(self, ctx, miembro: discord.Member, medalla: str):
        if not await require_mod(ctx):
            return
        g = self.levels.guild(ctx.guild.id)
        clave = medalla.lower()
        if clave not in g["medals"]:
            await ctx.send("⚠️ Esa medalla no existe.")
            return
        u = self.levels.user(ctx.guild.id, miembro.id)
        if clave not in u["medals"]:
            u["medals"].append(clave)
        if clave in u["pending"]:
            u["pending"].remove(clave)
        self.levels.store.dirty()
        m = g["medals"][clave]
        await ctx.send(f"🏅 {miembro.mention} recibió {m['emoji']} **{m['name']}**", allowed_mentions=SIN_PINGS)

    @lvl.command(name="takemedal", help="Quita una medalla a un miembro.", description="Quita una medalla a un miembro")
    async def takemedal(self, ctx, miembro: discord.Member, medalla: str):
        if not await require_mod(ctx):
            return
        u = self.levels.user(ctx.guild.id, miembro.id)
        clave = medalla.lower()
        for lista in (u["medals"], u["pending"]):
            if clave in lista:
                lista.remove(clave)
        self.levels.store.dirty()
        await ctx.send(f"✅ Medalla `{clave}` retirada de {miembro.mention}", allowed_mentions=SIN_PINGS)

    @givemedal.autocomplete("medalla")
    async def autocompletar_give(self, interaction, current: str):
        return self.levels.medal_choices(interaction.guild_id, current)

    @takemedal.autocomplete("medalla")
    async def autocompletar_take(self, interaction, current: str):
        return self.levels.medal_choices(interaction.guild_id, current)

    # ---------- roles por nivel ----------
    @lvl.command(name="role", help="Asigna un rol a un nivel.", description="Asigna un rol a un nivel")
    async def role(self, ctx, nivel: int, rol: discord.Role):
        if not await require_mod(ctx):
            return
        self.levels.cfg(ctx.guild.id)["level_roles"][str(nivel)] = rol.id
        self.levels.store.dirty()
        await ctx.send(f"✅ Nivel **{nivel}** → {rol.mention}", allowed_mentions=SIN_PINGS)

    @lvl.command(name="unrole", help="Quita el rol de un nivel.", description="Quita el rol de un nivel")
    async def unrole(self, ctx, nivel: int):
        if not await require_mod(ctx):
            return
        if self.levels.cfg(ctx.guild.id)["level_roles"].pop(str(nivel), None) is None:
            await ctx.send("⚠️ Ese nivel no tenía rol.")
            return
        self.levels.store.dirty()
        await ctx.send(f"✅ Rol del nivel {nivel} eliminado")

    # ---------- ajustes ----------
    @lvl.command(name="ignore", help="Alterna ignorar un canal o un rol para ganar XP.",
                 description="Alterna ignorar un canal o rol para ganar XP")
    async def ignore(self, ctx, canal: Optional[discord.TextChannel] = None, rol: Optional[discord.Role] = None):
        if not await require_mod(ctx):
            return
        if not canal and not rol:
            await ctx.send("⚠️ Indica un canal o un rol.")
            return
        cfg = self.levels.cfg(ctx.guild.id)
        salida = []
        for obj, clave in ((canal, "ignored_channels"), (rol, "ignored_roles")):
            if obj:
                if obj.id in cfg[clave]:
                    cfg[clave].remove(obj.id)
                    salida.append(f"{obj.mention} ya **gana** XP")
                else:
                    cfg[clave].append(obj.id)
                    salida.append(f"{obj.mention} **ignorado**")
        self.levels.store.dirty()
        await ctx.send("✅ " + " · ".join(salida), allowed_mentions=SIN_PINGS)

    @lvl.command(name="modrole", help="Define un rol de moderador de niveles (además de Gestionar servidor).",
                 description="Rol de moderador de niveles")
    async def modrole(self, ctx, rol: Optional[discord.Role] = None):
        if not await require_mod(ctx):
            return
        self.levels.cfg(ctx.guild.id)["mod_role"] = rol.id if rol else None
        self.levels.store.dirty()
        await ctx.send("✅ Rol de moderador " + (f"= {rol.mention}" if rol else "quitado"), allowed_mentions=SIN_PINGS)

    @lvl.command(name="levelchannel", help="Canal para los avisos de subida de nivel (vacío = donde hablen).",
                 description="Canal de avisos de subida de nivel")
    async def levelchannel(self, ctx, canal: Optional[discord.TextChannel] = None):
        if not await require_mod(ctx):
            return
        self.levels.cfg(ctx.guild.id)["levelup_channel"] = canal.id if canal else None
        self.levels.store.dirty()
        await ctx.send("✅ Avisos en " + (canal.mention if canal else "el mismo canal"))

    @lvl.command(name="set", help="Cambia un ajuste del sistema. Ej: !lvl set cooldown 30",
                 description="Cambia un ajuste del sistema")
    async def set(self, ctx, ajuste: Literal["xp_min", "xp_max", "cooldown", "multiplier", "coins_per_level",
                                             "daily", "drop_chance", "drop_min", "drop_max", "stack_roles"],
                  valor: str):
        if not await require_mod(ctx):
            return
        tipos = {"multiplier": float, "drop_chance": float, "stack_roles": bool}
        tipo = tipos.get(ajuste, int)
        try:
            val = valor.lower() in ("1", "true", "si", "sí", "on", "yes") if tipo is bool else tipo(valor)
        except ValueError:
            await ctx.send(f"⚠️ `{valor}` no es válido para `{ajuste}`.")
            return
        self.levels.cfg(ctx.guild.id)[ajuste] = val
        self.levels.store.dirty()
        await ctx.send(f"✅ `{ajuste}` = `{val}`")

    @lvl.command(name="config", help="Muestra la configuración actual del sistema.",
                 description="Muestra la configuración actual")
    async def config(self, ctx):
        if not await require_mod(ctx):
            return
        c = self.levels.cfg(ctx.guild.id)
        roles = "\n".join(f"Nivel {l} → <@&{r}>"
                          for l, r in sorted(c["level_roles"].items(), key=lambda x: int(x[0]))) or "—"
        embed = discord.Embed(title="⚙️ Configuración de niveles", color=0x3498db)
        embed.add_field(name="XP", value=f"{c['xp_min']}–{c['xp_max']} cada {c['cooldown']}s ×{c['multiplier']}")
        embed.add_field(name="Economía", value=f"{c['coins_per_level']} {COIN}/nivel · daily {c['daily']}\n"
                                                f"drop {c['drop_chance']}% ({c['drop_min']}–{c['drop_max']})")
        embed.add_field(name="Roles acumulables", value=str(c["stack_roles"]))
        embed.add_field(name="Roles por nivel", value=roles, inline=False)
        embed.add_field(name="Canales ignorados", value=" ".join(f"<#{i}>" for i in c["ignored_channels"]) or "—")
        embed.add_field(name="Roles ignorados", value=" ".join(f"<@&{i}>" for i in c["ignored_roles"]) or "—")
        embed.add_field(name="Fondos por rango",
                        value=", ".join(f"nivel {k}" for k in sorted(c["tier_bgs"], key=int)) or "—")
        await ctx.send(embed=embed, allowed_mentions=SIN_PINGS)
