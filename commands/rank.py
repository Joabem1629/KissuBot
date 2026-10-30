import asyncio
from typing import Optional

import discord
from discord.ext import commands

from utils import rankcard
from utils.levels_core import get_levels, level_from_xp


class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_command(name="rank", aliases=["nivel", "level"],
                             help="Muestra tu tarjeta de rango (o la de otro miembro).",
                             description="Muestra tu tarjeta de rango")
    @commands.guild_only()
    async def rank(self, ctx, miembro: Optional[discord.Member] = None):
        member = miembro or ctx.author
        await ctx.defer()

        g = self.levels.guild(ctx.guild.id)
        u = self.levels.user(ctx.guild.id, member.id)
        nivel, xp, necesaria = level_from_xp(u["xp"])

        ranking = sorted(g["users"].items(), key=lambda kv: kv[1]["xp"], reverse=True)
        pos = next((i for i, (uid, _) in enumerate(ranking, 1) if uid == str(member.id)), len(ranking) + 1)

        # Fondo: personal > por rango > por defecto
        fondo = None
        if u["bg"]:
            fondo = self.levels.bg_dir / u["bg"]
        else:
            tiers = [int(k) for k in g["config"]["tier_bgs"] if int(k) <= nivel]
            if tiers:
                fondo = self.levels.bg_dir / g["config"]["tier_bgs"][str(max(tiers))]
        if not fondo or not fondo.exists():
            fondo = self.levels.bg_dir / "default.png"

        iconos = [self.levels.medal_dir / g["medals"][m]["image"] for m in u["medals"]
                  if m in g["medals"] and g["medals"][m].get("image")]
        avatar = await member.display_avatar.with_size(256).with_format("png").read()

        buf = await asyncio.to_thread(
            rankcard.render_card, avatar_bytes=avatar, bg_path=fondo, name=member.display_name,
            level=nivel, xp=xp, needed=necesaria, rank=pos, medal_paths=iconos,
            accent=g["config"]["accent"])
        await ctx.send(file=discord.File(buf, "rank.png"))
