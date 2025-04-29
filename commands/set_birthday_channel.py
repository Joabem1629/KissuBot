import discord
from discord.ext import commands
import json

class SetBirthdayChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_birthday_channel(self, ctx, canal: discord.TextChannel):
        """
        Configura el canal donde se enviarán los mensajes de cumpleaños.
        """
        guild_id = str(ctx.guild.id)

        # Estructura del canal
        channel_data = {
            "channel_id": canal.id,
            "channel_name": canal.name,
            "guild_id": ctx.guild.id,
            "guild_name": ctx.guild.name
        }

        try:
            with open("birthday_channel.json", "r") as f:
                channels = json.load(f)
        except FileNotFoundError:
            channels = {}

        # Actualizamos la información del canal en el JSON
        channels[guild_id] = channel_data

        with open("birthday_channel.json", "w") as f:
            json.dump(channels, f, indent=4)

        await ctx.send(f"Canal configurado correctamente: {canal.mention} para los mensajes de cumpleaños.")

async def setup(bot):
    await bot.add_cog(SetBirthdayChannel(bot))
