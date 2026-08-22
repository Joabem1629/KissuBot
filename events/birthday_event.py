import discord
from discord.ext import commands, tasks
import json
from datetime import datetime, timedelta
import os

class BirthdayEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_birthdays.start()

    @tasks.loop(minutes=1)  # Revisa cada minuto en lugar de cada 24 horas
    async def check_birthdays(self):
        await self.bot.wait_until_ready()

        # Hora de Perú (UTC-5)
        now = datetime.utcnow() - timedelta(hours=5)
        if not (now.hour == 7 and now.minute == 30):  # Ejecuta solo a las 9:30 AM hora Perú
            return

        today = now.strftime("%m-%d")
        print(f"Checking birthdays for {today}...")

        # Rutas de los archivos
        birthdays_path = os.path.join(os.path.dirname(__file__), "../birthdays.json")
        channels_path = os.path.join(os.path.dirname(__file__), "../birthday_channel.json")

        try:
            with open(birthdays_path, "r") as f:
                birthdays = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar birthdays.json: {e}")
            return

        try:
            with open(channels_path, "r") as f:
                channels = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar birthday_channel.json: {e}")
            return

        for user_id, data in birthdays.items():
            if data["date"] == today:
                guild_id = str(data["guild_id"])
                channel_data = channels.get(guild_id)

                if not channel_data:
                    print(f"No se encontró un canal para el servidor {guild_id}.")
                    continue

                channel_id = channel_data["channel_id"]
                channel = self.bot.get_channel(channel_id)

                if not channel:
                    print(f"Canal con ID {channel_id} no encontrado en el servidor {guild_id}.")
                    continue

                await self.send_birthday_message(channel, user_id)

    async def send_birthday_message(self, channel, user_id):
        """Envía un mensaje de cumpleaños a un usuario."""
        user = self.bot.get_user(int(user_id))
        if not user:
            try:
                user = await self.bot.fetch_user(int(user_id))
            except discord.NotFound:
                print(f"Usuario con ID {user_id} no encontrado.")
                return

        if user_id == "1083182072216178768":  # Mensaje especial
            special_message = (
                "@everyone\n\n"
                f"Hoy es el cumpleaños de la Diosa de este servidor, la razón por la que está hecho este server, "
                f"este bot, por la cual estamos reunidos hoy, {user.mention}. "
                "Kiss.\n\n"
                "¡Feliz Cumpleaños de parte mía, del bot, y de todo el servidor! ¡Que pases un hermoso día! :kissumanca:"
            )
            await channel.send(special_message)
        else:  # Mensaje estándar
            message__a = "@everyone"
            await channel.send(message__a)
            embed = discord.Embed(
                description=f"🎂 ¡Feliz cumpleaños {user.mention}! 🎉\n"
                            f"¡Esperamos que tengas un día increíble! 🥳",
                color=0xc51856,
            )
            await channel.send(content=user.mention, embed=embed)

    @check_birthdays.before_loop
    async def before_check_birthdays(self):
        # Calcular el tiempo hasta las 9:30 AM hora de Perú (UTC-5)
        now = datetime.utcnow() - timedelta(hours=5)
        next_run = now.replace(hour=7, minute=30, second=0, microsecond=0)
        if now >= next_run:
            next_run += timedelta(days=1)
        wait_time = (next_run - now).total_seconds()
        print(f"Esperando {wait_time} segundos para iniciar el chequeo de cumpleaños.")
        await discord.utils.sleep_until(next_run)

async def setup(bot):
    await bot.add_cog(BirthdayEvent(bot))