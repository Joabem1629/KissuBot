import json
import logging
from pathlib import Path

import discord
from discord.ext import commands

REPLIES_FILE = Path(__file__).resolve().parent.parent / "custom_replies.json"


def load_replies() -> dict:
    """Carga las respuestas rápidas desde custom_replies.json (formato: {"_trigger": "respuesta"})."""
    try:
        return json.loads(REPLIES_FILE.read_text("utf-8"))
    except FileNotFoundError:
        logging.warning("No existe %s: las respuestas rápidas están desactivadas.", REPLIES_FILE.name)
    except json.JSONDecodeError as e:
        logging.error("%s no es un JSON válido: %s", REPLIES_FILE.name, e)
    return {}


class OnMessage(commands.Cog):
    """Responde con un texto o imagen cuando alguien escribe exactamente un trigger."""

    def __init__(self, bot):
        self.bot = bot
        self.replies = load_replies()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        reply = self.replies.get(message.content.lower())
        if reply is None:
            return

        try:
            await message.delete()
        except discord.HTTPException:
            pass  # sin permiso de borrar (o en DM): se responde igual
        await message.channel.send(reply)

        guild_id = message.guild.id if message.guild else "DM"
        logging.info("Respuesta rápida %s | usuario %s | servidor %s",
                     message.content.lower(), message.author.id, guild_id)
