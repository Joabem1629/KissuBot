import discord
from discord.ext import commands

class MsgCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def msg(self, ctx, canal: discord.TextChannel, *, mensaje: str):
        await canal.send(mensaje)
        await ctx.message.delete()
