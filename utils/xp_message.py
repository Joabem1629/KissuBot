import random
import time

import discord
from discord.ext import commands

from utils.levels_core import get_levels


class XpMessage(commands.Cog):
    """Da XP por mensaje (con cooldown). El resto lo hacen los eventos level_up, rank_up, etc."""

    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)
        self.cooldowns = {}  # {(guild_id, user_id): momento del último mensaje con XP}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        # Los comandos no dan XP
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return

        cfg = self.levels.cfg(message.guild.id)
        if message.channel.id in cfg["ignored_channels"]:
            return
        if any(r.id in cfg["ignored_roles"] for r in getattr(message.author, "roles", [])):
            return

        key = (message.guild.id, message.author.id)
        ahora = time.monotonic()
        if ahora - self.cooldowns.get(key, 0) < cfg["cooldown"]:
            return
        self.cooldowns[key] = ahora

        cantidad = max(1, round(
            random.randint(cfg["xp_min"], max(cfg["xp_min"], cfg["xp_max"])) * cfg["multiplier"]
        ))
        self.levels.user(message.guild.id, message.author.id)["messages"] += 1
        await self.levels.grant_xp(message.author, cantidad, natural=True, channel=message.channel)
        self.bot.dispatch("xp_gain", message)  # lo escucha coin_drop.py
