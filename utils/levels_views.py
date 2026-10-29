"""Botones y paginadores del sistema de niveles."""
import discord
from discord.ui import View, Button

from utils.levels_core import COIN, GEM, level_from_xp


class DropView(View):
    """Drop de monedas: el primero que pulsa se lo lleva (como las kakeras)."""

    def __init__(self, levels, cantidad):
        super().__init__(timeout=60)
        self.levels = levels
        self.cantidad = cantidad
        self.reclamado = False
        self.message = None

    @discord.ui.button(label="Reclamar", style=discord.ButtonStyle.success, emoji=GEM)
    async def reclamar(self, interaction: discord.Interaction, button: Button):
        if self.reclamado:
            return await interaction.response.send_message("❌ Ya lo reclamaron 😔", ephemeral=True)
        self.reclamado = True  # sin await antes: no hay carrera posible
        u = self.levels.user(interaction.guild_id, interaction.user.id)
        u["coins"] += self.cantidad
        self.levels.store.dirty()
        button.disabled = True
        button.label = "Reclamado"
        embed = discord.Embed(
            description=f"{GEM} {interaction.user.mention} reclamó **{self.cantidad}** {COIN}",
            color=0x2ecc71)
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()

    async def on_timeout(self):
        if self.reclamado or not self.message:
            return
        for item in self.children:
            item.disabled = True
        try:
            await self.message.edit(
                embed=discord.Embed(description="💨 El drop se esfumó...", color=0x95a5a6),
                view=self)
        except discord.HTTPException:
            pass


class ClaimView(View):
    """Botón para reclamar las medallas desbloqueadas."""

    def __init__(self, levels, owner_id):
        super().__init__(timeout=900)
        self.levels = levels
        self.owner_id = owner_id

    @discord.ui.button(label="Reclamar medalla", style=discord.ButtonStyle.primary, emoji="🏅")
    async def reclamar(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("❌ Esta medalla no es tuya.", ephemeral=True)
        got, coins = self.levels.claim_all(interaction.guild_id, interaction.user.id)
        button.disabled = True
        txt = " ".join(f"{m['emoji']} **{m['name']}**" for m in got) or "Nada pendiente."
        if coins:
            txt += f"\n+{coins} {COIN}"
        await interaction.response.edit_message(
            embed=discord.Embed(description=f"🏅 {interaction.user.mention} reclamó: {txt}", color=0xf1c40f),
            view=self)
        self.stop()


class PaginadorRanking(View):
    def __init__(self, filas, ctx, por_pagina=10):
        super().__init__(timeout=60)  # 1 minuto para que expiren los botones
        self.ctx = ctx
        self.filas = filas  # [(user_id, xp), ...] ya ordenado
        self.por_pagina = por_pagina
        self.pagina_actual = 0
        self.total_paginas = max(1, (len(filas) - 1) // por_pagina + 1)

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
        lineas = []
        for i, (uid, xp) in enumerate(self.filas[inicio:inicio + self.por_pagina], inicio + 1):
            m = self.ctx.guild.get_member(uid)
            nombre = m.display_name if m else f"Usuario {uid}"
            lineas.append(f"`#{i}` **{nombre}** — nivel {level_from_xp(xp)[0]} · {xp:,} XP")

        embed = discord.Embed(
            title=f"🏆 Ranking de {self.ctx.guild.name}",
            description="\n".join(lineas) or "Aún no hay nadie en el ranking.",
            color=0x3498db)
        embed.set_footer(text=f"Página {self.pagina_actual + 1} de {self.total_paginas} · "
                              f"Solicitado por {self.ctx.author.name}")
        return embed
