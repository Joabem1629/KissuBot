import discord
from discord.ext import commands
import logging
import json
import os
from dotenv import load_dotenv

from commands import commands_list
from events import events_list

load_dotenv()

with open('config.json') as f:
    config = json.load(f)

logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)

logger = logging.getLogger()

logging.info("Bot is starting...")

intents = discord.Intents.default()
intents.dm_messages = True
intents.message_content = True

class MyBot(commands.Bot):
    async def setup_hook(self):
        for command_class in commands_list:
            if command_class.__name__ not in self.cogs:
                await self.add_cog(command_class(self))

        for event_class in events_list:
            if event_class.__name__ not in self.cogs:
                await self.add_cog(event_class(self))

bot = MyBot(command_prefix=config['prefix'], intents=intents)
bot.remove_command('help')

bot.run(os.getenv('DISCORD_TOKEN'))
