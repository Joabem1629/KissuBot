import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear_channel", help="Elimina todos los mensajes de un canal.")
    @commands.has_permissions(manage_messages=True)  # Verifica que el usuario tiene permisos
    async def clear_channel(self, ctx):
        """Elimina todos los mensajes de un canal."""
        channel = ctx.channel

        # Confirma si el usuario realmente quiere borrar todos los mensajes
        await ctx.send(f"¿Estás seguro de que deseas eliminar todos los mensajes en {channel.mention}? Responde con 'sí' para confirmar.")
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
            if msg.content.lower() == 'sí':
                # Borra todos los mensajes en el canal
                await channel.purge(limit=1000)  # Puede aumentar el límite si el canal tiene muchos mensajes
                await ctx.send(f"Todos los mensajes de {channel.mention} han sido eliminados.", delete_after=5)
            else:
                await ctx.send("Operación cancelada.")
        except TimeoutError:
            await ctx.send("No se recibió respuesta a tiempo. Operación cancelada.")