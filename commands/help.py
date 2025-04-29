import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        message = """
        | Hola, soy KissuBot, un bot creado por <@610956498998394880> para el servidor de Kissu.
        | Soy manca asi que no me pidas mucho.
        | Comandos divertidos:
        ↳ **!esta**
        ↳ **!fyou**
        ↳ **!manca**
        ↳ **!simp**
        ↳ **!dance**
        ↳ **!nooo**
        ↳ **!catyep**
        ↳ **!catnope**
        ↳ **!mods**
        ↳ **!quieres**
        ↳ **!bigote**
        ↳ **!uwu**
        ↳ **!ignorar**
        ↳ **!actuali**
        ↳ **!kissudrilo**
        ↳ **!mizahuevo**
        ↳ **!kisuhuevo**
        ↳ **!huevos**
        ↳ **!bueno**
        ↳ **!supremacy**
        ↳ **!mamadisima**
        ↳ **!inseminar**
        ↳ **!kiss**
        ↳ **!pollo**
        ↳ **!paja**
        ↳ **!redes**
        | Si tienes alguna duda o sugerencia, contacta con <@610956498998394880>.
        | Espero haberte sido de ayuda.
        | UwU
        """
        embed = discord.Embed(description=message, color=0xc51856)
        await ctx.send(embed=embed)
        await ctx.message.delete()
