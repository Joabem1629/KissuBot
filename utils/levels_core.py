"""
Lógica compartida del sistema de niveles (la usan commands/ y events/).

Se accede desde cualquier Cog con:   self.levels = get_levels(bot)
El servicio se crea una sola vez y se guarda en bot.levels.

Eventos personalizados que dispara (se escuchan con @commands.Cog.listener()):
    on_level_change(member, nivel_viejo, nivel_nuevo)               -> cualquier cambio de nivel
    on_level_up(member, nivel_viejo, nivel_nuevo, canal, monedas)   -> subida natural por mensajes
    on_medal_unlock(member, id_medalla, canal)                      -> medalla lista para reclamar
    on_xp_gain(message)                                             -> mensaje que dio XP
"""
import atexit
import logging
import os
from pathlib import Path
from typing import Optional

import discord
from discord import app_commands
from discord.ext import tasks

from utils.storage import JsonStore

COIN = "🪙"
GEM = "💎"


# =====================================================================
#  Matemática de niveles (misma curva que ProBot/MEE6)
# =====================================================================
def xp_for_next(level: int) -> int:
    return 5 * level ** 2 + 50 * level + 100


def level_from_xp(total: int):
    """Devuelve (nivel, xp dentro del nivel, xp necesaria para el siguiente)."""
    lvl = 0
    while total >= xp_for_next(lvl):
        total -= xp_for_next(lvl)
        lvl += 1
    return lvl, total, xp_for_next(lvl)


def xp_for_level(level: int) -> int:
    return sum(xp_for_next(i) for i in range(level))


# =====================================================================
#  Servicio
# =====================================================================
class LevelsService:
    def __init__(self, bot):
        self.bot = bot
        # Se lee aquí (y no al importar) porque load_dotenv() corre después de los imports.
        self.data_dir = Path(os.getenv("LEVELS_DIR", "data"))
        self.bg_dir = self.data_dir / "backgrounds"
        self.medal_dir = self.data_dir / "medals"
        self.store = JsonStore(self.data_dir / "levels.json")
        atexit.register(self.store.save_sync)  # guarda al cerrar el bot
        self._autosave.start()

    @tasks.loop(seconds=30)
    async def _autosave(self):
        await self.store.save()

    # ---------- acceso rápido ----------
    def guild(self, guild_id):
        return self.store.guild(guild_id)

    def cfg(self, guild_id):
        return self.store.guild(guild_id)["config"]

    def user(self, guild_id, user_id):
        return self.store.user(guild_id, user_id)

    # ---------- roles por nivel ----------
    async def sync_roles(self, member: discord.Member, level: int):
        cfg = self.cfg(member.guild.id)
        mapping = {int(l): r for l, r in cfg["level_roles"].items()}
        if not mapping:
            return
        earned = {l: r for l, r in mapping.items() if l <= level}
        if cfg["stack_roles"]:
            keep = set(earned.values())
        else:
            keep = {earned[max(earned)]} if earned else set()
        to_add = [member.guild.get_role(r) for r in keep if not member.get_role(r)]
        to_rem = [member.guild.get_role(r) for r in set(mapping.values()) - keep if member.get_role(r)]
        try:
            if any(to_add):
                await member.add_roles(*[r for r in to_add if r], reason="Rol por nivel")
            if any(to_rem):
                await member.remove_roles(*[r for r in to_rem if r], reason="Rol por nivel")
        except discord.Forbidden:
            logging.warning(f"Sin permisos para gestionar roles en {member.guild} "
                            f"(el rol del bot debe estar POR ENCIMA de los roles de nivel)")

    # ---------- XP ----------
    async def grant_xp(self, member: discord.Member, amount: int, *, natural=False,
                       channel: Optional[discord.abc.Messageable] = None):
        """Suma/resta XP. Devuelve (nivel_viejo, nivel_nuevo) y dispara los eventos."""
        u = self.user(member.guild.id, member.id)
        old = level_from_xp(u["xp"])[0]
        u["xp"] = max(0, u["xp"] + amount)
        new = level_from_xp(u["xp"])[0]

        coins = 0
        if natural and new > old:
            coins = (new - old) * self.cfg(member.guild.id)["coins_per_level"]
            u["coins"] += coins
        self.store.dirty()

        if new != old:
            self.bot.dispatch("level_change", member, old, new)
            if natural and new > old:
                self.bot.dispatch("level_up", member, old, new, channel, coins)
        await self.check_medals(member, channel)
        return old, new

    async def set_total_xp(self, member: discord.Member, total: int):
        u = self.user(member.guild.id, member.id)
        old = level_from_xp(u["xp"])[0]
        u["xp"] = max(0, total)
        new = level_from_xp(u["xp"])[0]
        self.store.dirty()
        if new != old:
            self.bot.dispatch("level_change", member, old, new)
        await self.check_medals(member, None)

    # ---------- medallas ----------
    async def check_medals(self, member: discord.Member, channel):
        g = self.guild(member.guild.id)
        u = self.user(member.guild.id, member.id)
        stats = {"nivel": level_from_xp(u["xp"])[0], "mensajes": u["messages"]}
        for mid, m in g["medals"].items():
            if not m.get("auto_type") or mid in u["medals"] or mid in u["pending"]:
                continue
            if stats.get(m["auto_type"], 0) >= m["auto_value"]:
                u["pending"].append(mid)
                self.store.dirty()
                self.bot.dispatch("medal_unlock", member, mid, channel)

    def claim_all(self, guild_id, user_id):
        g = self.guild(guild_id)
        u = self.user(guild_id, user_id)
        got, coins = [], 0
        for mid in list(u["pending"]):
            u["pending"].remove(mid)
            m = g["medals"].get(mid)
            if m and mid not in u["medals"]:
                u["medals"].append(mid)
                coins += m.get("reward", 0)
                got.append(m)
        u["coins"] += coins
        self.store.dirty()
        return got, coins

    def medal_choices(self, guild_id, current: str):
        """Para el autocompletado de slash commands."""
        cur = current.lower()
        return [app_commands.Choice(name=f"{m['emoji']} {m['name']}"[:100], value=k)
                for k, m in self.guild(guild_id)["medals"].items()
                if cur in k or cur in m["name"].lower()][:25]


def get_levels(bot) -> LevelsService:
    """Devuelve el servicio único del bot (lo crea la primera vez)."""
    if not hasattr(bot, "levels"):
        bot.levels = LevelsService(bot)
    return bot.levels


# =====================================================================
#  Utilidades para comandos
# =====================================================================
async def require_mod(ctx) -> bool:
    """True si el autor es moderador (Gestionar servidor o el rol configurado). Si no, avisa."""
    if not ctx.guild:
        return False
    perms = ctx.author.guild_permissions
    if perms.manage_guild or perms.administrator:
        return True
    rid = get_levels(ctx.bot).cfg(ctx.guild.id)["mod_role"]
    if rid and ctx.author.get_role(rid):
        return True
    await ctx.send("❌ Necesitas ser moderador para usar este comando.")
    return False


async def leer_imagen(ctx, att: discord.Attachment) -> Optional[bytes]:
    """Descarga un adjunto validando que sea imagen y no pese más de 8 MB."""
    if not (att.content_type or "").startswith("image/"):
        await ctx.send("⚠️ El archivo debe ser una imagen.")
        return None
    if att.size > 8 * 1024 * 1024:
        await ctx.send("⚠️ La imagen pesa más de 8 MB.")
        return None
    return await att.read()
