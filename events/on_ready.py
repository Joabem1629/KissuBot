import logging
from discord.ext import commands

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Bot is ready. Logged in as {self.bot.user.name} ({self.bot.user.id})')
        print(f'Bot is ready. Logged in as {self.bot.user.name} ({self.bot.user.id})')

