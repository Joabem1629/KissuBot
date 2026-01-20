import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_message(self, message):

        contenidos = {
        "!simp" : ("https://imgur.com/VDZwDLd", "simp"),
        "!dance" : ("https://imgur.com/YTGlynN", "dance"),
        "!nooo" : ("https://imgur.com/KoBBOM9", "nooo"),
        "!catyep" : ("https://imgur.com/8CKfyvA", "catyep"),
        "!catnope" : ("https://imgur.com/jXVzkXA", "catnope"),
        "!mods" : ("https://imgur.com/0gWi7Qn", "mods"),
        }

        content = message.content.lower()
        user = message.author
        channel = message.channel
        guild = message.guild if isinstance(channel, discord.TextChannel) else None

        def log_event(event_name):
            print("----------------------------------------------")
            print(f"Evento activado: {event_name}")
            print(f"Usuario: {user.name} ({user.id})")
            if guild:
                print(f"Servidor: {guild.name} ({guild.id})")
                print(f"Canal: {channel.name} ({channel.id})")
            else:
                print(f"DM con {user.name} ({user.id})")
            print("----------------------------------------------")

        for command in contenidos:
            if content == command:
                await message.delete()
                await message.channel.send(contenidos[command][0])
                log_event(contenidos[command][1])
                break