import discord
from discord.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        p = ctx.clean_prefix
        owner = f"<@{self.bot.owner_id}>" if self.bot.owner_id else "Joabem1629"

        # Las respuestas rápidas se leen de custom_replies.json (las carga el cog OnMessage)
        on_message = self.bot.get_cog("OnMessage")
        triggers = sorted(on_message.replies) if on_message else []
        fun = " ".join(f"`{t}`" for t in triggers) or "No hay configuradas."

        message = (
            f"Hola, soy KissuBot, un bot creado por {owner} para el servidor de Kissu.\n"
            "Soy manca asi que no me pidas mucho.\n\n"
            "**Niveles y economía**\n"
            f"`{p}rank` `{p}top` `{p}balance` `{p}daily` `{p}tienda` `{p}comprar` `{p}medallas` `{p}reclamar`\n\n"
            "**Cumpleaños**\n"
            f"`{p}add_birthday MM-DD` (mods: `{p}add_birthday @usuario MM-DD`) `{p}show_birthday`\n\n"
            f"**Comandos divertidos** (escríbelos solos en un mensaje)\n{fun}\n\n"
            f"Si tienes alguna duda o sugerencia, contacta con {owner}.\n"
            "Espero haberte sido de ayuda. UwU"
        )
        embed = discord.Embed(description=message, color=0xc51856)
        await ctx.send(embed=embed)
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass