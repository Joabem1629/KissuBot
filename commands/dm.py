import discord
from discord.ext import commands

class DmCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dm(self, ctx, user: discord.Member, *, mensaje: str):
        await user.send(mensaje)
        await ctx.message.delete()
