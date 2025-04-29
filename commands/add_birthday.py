import discord
from discord.ext import commands
import datetime
import json

class AddBirthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday_file = "birthdays.json"

    @commands.command()
    async def add_birthday(self, ctx, user: discord.Member, date: str):
        """Agrega un cumpleaños. Formato de fecha: MM-DD"""
        try:
            datetime.datetime.strptime(date, "%m-%d")
        except ValueError:
            await ctx.send("Formato de fecha inválido. Usa MM-DD (e.g., 12-25).")
            return

        try:
            with open(self.birthday_file, "r") as f:
                birthdays = json.load(f)
        except FileNotFoundError:
            birthdays = {}

        birthdays[str(user.id)] = {
            "name": user.display_name,
            "date": date,
            "guild_id": ctx.guild.id,
        }

        with open(self.birthday_file, "w") as f:
            json.dump(birthdays, f, indent=4)

        await ctx.send(f"Cumpleaños de {user.mention} agregado para la fecha {date}.")
