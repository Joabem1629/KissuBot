import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        message = "" # Help Message
        embed = discord.Embed(description=message, color=0xc51856)
        await ctx.send(embed=embed)
        await ctx.message.delete()
