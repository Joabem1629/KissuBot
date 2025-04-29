import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta

class ShowBirthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = 'birthdays.json'

    @commands.command(name="show_birthday", help="Muestra los cumpleaños registrados, ordenados de más cercano a más lejano.")
    async def show_birthday(self, ctx):
        # Verificar si el archivo existe
        if not os.path.exists(self.file_path):
            await ctx.send(f"⚠️ El archivo no se encuentra en la ruta: {os.path.abspath(self.file_path)}.")
            return

        # Leer el archivo de cumpleaños
        with open(self.file_path, "r") as f:
            birthdays = json.load(f)

        # Filtrar por el servidor actual
        guild_id = ctx.guild.id
        filtered_birthdays = {
            user_id: data for user_id, data in birthdays.items() if data.get("guild_id") == guild_id
        }

        if not filtered_birthdays:
            await ctx.send("⚠️ No hay cumpleaños registrados para este servidor.")
            return

        # Obtener la fecha actual
        today = datetime.now()

        # Crear una lista de cumpleaños con cálculo de días restantes
        upcoming_birthdays = []
        for user_id, data in filtered_birthdays.items():
            nombre = data["name"]
            mes, dia = map(int, data["date"].split("-"))  # Convertir mes y día a enteros
            birthday_this_year = datetime(year=today.year, month=mes, day=dia)

            # Si el cumpleaños ya pasó este año, calcular para el próximo año
            if birthday_this_year < today:
                birthday_this_year = datetime(year=today.year + 1, month=mes, day=dia)

            # Calcular días restantes y agregar a la lista
            days_until = (birthday_this_year - today).days
            upcoming_birthdays.append((days_until, nombre, mes, dia))

        # Ordenar los cumpleaños por días restantes
        upcoming_birthdays.sort(key=lambda x: x[0])

        # Crear un embed con los cumpleaños ordenados
        embed = discord.Embed(
            title="🎉 Lista de Cumpleaños 🎉",
            description="Cumpleaños ordenados desde el más cercano al más lejano:",
            color=0x3498db,
            timestamp=today
        )
        embed.set_footer(text="Comando solicitado por {}".format(ctx.author.name), icon_url=ctx.author.avatar.url)

        # Mapeo de números de mes a nombres
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        # Agregar los cumpleaños al embed
        for days_until, nombre, mes, dia in upcoming_birthdays:
            mes_nombre = meses[mes - 1]
            embed.add_field(
                name=f"Usuario: {nombre}",
                value=f"{dia} - {mes_nombre} ({days_until} días restantes)",
                inline=False
            )

        # Enviar el embed en el canal donde se ejecutó el comando
        await ctx.send(embed=embed)
