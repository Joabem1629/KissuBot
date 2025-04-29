import logging
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Comando no encontrado.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Faltan argumentos para este comando.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("No tienes los permisos necesarios para este comando.")
        else:
            await ctx.send("Ha ocurrido un error.")
            logging.error(f"Error no manejado: {str(error)}")
            raise error
