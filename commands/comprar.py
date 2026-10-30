from discord.ext import commands

from utils.levels_core import COIN, get_levels


class Comprar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = get_levels(bot)

    @commands.hybrid_command(name="comprar", help="Compra una medalla de la tienda con tus monedas.",
                             description="Compra una medalla de la tienda")
    @commands.guild_only()
    async def comprar(self, ctx, medalla: str):
        clave = medalla.lower()
        m = self.levels.guild(ctx.guild.id)["medals"].get(clave)
        if not m or m.get("price") is None:
            await ctx.send("⚠️ Esa medalla no está a la venta.")
            return

        u = self.levels.user(ctx.guild.id, ctx.author.id)
        if clave in u["medals"]:
            await ctx.send("⚠️ Ya tienes esa medalla.")
            return
        if u["coins"] < m["price"]:
            await ctx.send(f"❌ Te faltan **{m['price'] - u['coins']:,}** {COIN}.")
            return

        u["coins"] -= m["price"]
        u["medals"].append(clave)
        self.levels.store.dirty()
        await ctx.send(f"✅ Compraste {m['emoji']} **{m['name']}**")

    @comprar.autocomplete("medalla")
    async def autocompletar_medalla(self, interaction, current: str):
        return self.levels.medal_choices(interaction.guild_id, current)
