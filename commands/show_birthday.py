import discord
from discord.ext import commands
from discord.ui import View, Button
import json
import os
from datetime import datetime

class PaginadorCumpleaños(View):
    def __init__(self, datos, ctx, por_pagina=8):
        super().__init__(timeout=60)  # 1 minuto para que expiren los botones
        self.ctx = ctx
        self.datos = datos
        self.por_pagina = por_pagina
        self.pagina_actual = 0
        self.total_paginas = (len(datos) - 1) // por_pagina + 1
        self.embed = None

        self.anterior = Button(emoji="⬅️", style=discord.ButtonStyle.primary)
        self.siguiente = Button(emoji="➡️", style=discord.ButtonStyle.primary)

        self.anterior.callback = self.atras
        self.siguiente.callback = self.adelante

        self.add_item(self.anterior)
        self.add_item(self.siguiente)

    async def atras(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message("❌ Solo el autor del comando puede usar los botones.", ephemeral=True)

        self.pagina_actual = (self.pagina_actual - 1) % self.total_paginas

        await interaction.response.edit_message(embed=self.generar_embed(), view=self)

    async def adelante(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message("❌ Solo el autor del comando puede usar los botones.", ephemeral=True)

        self.pagina_actual = (self.pagina_actual + 1) % self.total_paginas

        await interaction.response.edit_message(embed=self.generar_embed(), view=self)

    def generar_embed(self):
        inicio = self.pagina_actual * self.por_pagina
        fin = inicio + self.por_pagina
        hoy = datetime.now()

        embed = discord.Embed(
            title="🎉 Lista de Cumpleaños 🎉",
            description=f"Página {self.pagina_actual + 1} de {self.total_paginas}",
            color=0x3498db,
            timestamp=hoy
        )
        embed.set_footer(text=f"Solicitado por {self.ctx.author.name}", icon_url=self.ctx.author.avatar.url)

        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        for days_until, nombre, mes, dia in self.datos[inicio:fin]:
            mes_nombre = meses[mes - 1]
            embed.add_field(
                name=f"👤 {nombre}",
                value=f"{dia} de {mes_nombre} ({days_until} días restantes)",
                inline=False
            )

        return embed


class ShowBirthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = 'birthdays.json'

    @commands.command(name="show_birthday", help="Muestra los cumpleaños registrados, ordenados de más cercano a más lejano.")
    async def show_birthday(self, ctx):
        if not os.path.exists(self.file_path):
            await ctx.send(f"⚠️ El archivo no se encuentra en: `{os.path.abspath(self.file_path)}`.")
            return

        with open(self.file_path, "r") as f:
            birthdays = json.load(f)

        guild_id = ctx.guild.id
        filtered = {
            user_id: data for user_id, data in birthdays.items() if data.get("guild_id") == guild_id
        }

        if not filtered:
            await ctx.send("⚠️ No hay cumpleaños registrados para este servidor.")
            return

        today = datetime.now()
        upcoming = []

        for user_id, data in filtered.items():
            nombre = data["name"]
            mes, dia = map(int, data["date"].split("-"))
            cumple = datetime(year=today.year, month=mes, day=dia)

            if cumple < today:
                cumple = datetime(year=today.year + 1, month=mes, day=dia)

            dias_restantes = (cumple - today).days
            upcoming.append((dias_restantes, nombre, mes, dia))

        upcoming.sort(key=lambda x: x[0])

        view = PaginadorCumpleaños(upcoming, ctx)
        await ctx.send(embed=view.generar_embed(), view=view)