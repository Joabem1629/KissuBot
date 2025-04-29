import discord
from discord.ext import commands

class EmbedCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def embedm(self, ctx, user: discord.Member, *, mensaje: str):
        embed = discord.Embed(description=mensaje, color=0xc51856)
        await user.send(embed=embed)
        await ctx.message.delete()
