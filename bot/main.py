import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=f"{os.getenv('PREFIX')}",
    intents=intents
)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')

    # Important so commands still work
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run(os.getenv('DISCORD_TOKEN'))