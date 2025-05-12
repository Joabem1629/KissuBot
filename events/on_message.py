import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_message(self, message):

        contenidos = {
        "!esta" : ("https://imgur.com/5iYBBt9", "esta"),
        "!fyou" : ("https://imgur.com/V5ysaHz", "fyou"),
        "!manca" : ("https://imgur.com/GcPck8z", "manca"),
        "!simp" : ("https://imgur.com/VDZwDLd", "simp"),
        "!dance" : ("https://imgur.com/YTGlynN", "dance"),
        "!nooo" : ("https://imgur.com/KoBBOM9", "nooo"),
        "!catyep" : ("https://imgur.com/8CKfyvA", "catyep"),
        "!catnope" : ("https://imgur.com/jXVzkXA", "catnope"),
        "!mods" : ("https://imgur.com/0gWi7Qn", "mods"),
        "!quieres" : ("https://imgur.com/iUC1hgz", "quieres"),
        "!bigote" : ("https://imgur.com/tURudPT", "bigote"),
        "!uwu" : ("https://imgur.com/Y1kGLj2", "uwu"),
        "!ignorar" : ("https://imgur.com/KSKiT1L", "ignorar"),
        "!actuali" : ("https://imgur.com/Ph7WpES", "actuali"),
        "!kissudrilo" : ("https://imgur.com/Md0FiR7", "kissudrilo"),
        "!mizahuevo" : ("https://imgur.com/MGFcefM", "mizahuevo"),
        "!kisuhuevo" : ("https://imgur.com/RTLkBhT", "kisuhuevo"),
        "!huevos" : ("https://imgur.com/oSV7w1e", "huevos"),
        "!bueno" : ("https://imgur.com/mOSIzD5", "bueno"),
        "!supremacy" : ("https://imgur.com/yEQJ05w", "supremacy"),
        "!mamadisima" : ("https://imgur.com/TLJsU65", "mamadisima"),
        "!inseminar" : ("https://imgur.com/NJ39elJ", "inseminar"),
        "!kiss" : ("https://imgur.com/rFyyVGM", "kiss"),
        "!pixel" : ("https://imgur.com/0H3AVAx", "pixel"),
        "!pollo" : ("https://imgur.com/BLgaA8d", "pollo"),
        "!paja" : ("https://imgur.com/ifcBpge", "paja"),
        "!cum" : ("https://imgur.com/4ssJ1tV", "cum"),
        "!react" : ("https://imgur.com/4ssJ1tV", "react"),
        "!only" : ("☆ **[onlyfans.com/MomoiroKissu](https://onlyfanskissuvt.github.io/)** ☆", "only"),
        "!redes" : ("# ✿ TODAS LAS REDES AQUI ABAJO ✿\n# o .｡.:*☆*: .｡. o(   **[Carrd](https://momoirokiss.carrd.co/)**   )o .｡.:*☆*: .｡. o\n# o .｡.:*☆*: .｡. o(  **[Twitter](https://twitter.com/KissuVt)**  )o .｡.:*☆*: .｡. o\n# o .｡.:*☆*: .｡. o( **[Instagram](https://www.instagram.com/kissu_vt)** )o .｡.:*☆*: .｡. o\n# o .｡.:*☆*: .｡. o(  **[Facebook](https://www.facebook.com/kissvt)** )o .｡.:*☆*: .｡. o\n# o .｡.:*☆*: .｡. o(   **[Twitch](https://www.twitch.tv/kissuvt)**  )o .｡.:*☆*: .｡. o\n# o .｡.:*☆*: .｡. o(   **[TikTok](https://www.tiktok.com/@kissuvt)**  )o .｡.:*☆*: .｡. o\n# o .｡.:*☆*: .｡. o(  **[Patreon](https://www.patreon.com/momoirokiss)**  )o .｡.:*☆*: .｡. o\n# o .｡.:*☆*: .｡. o( **[Ko-fi](https://www.ko-fi.com/kissuvt)** )o .｡.:*☆*: .｡. o\n# o .｡.:*☆*: .｡. o( **[OnlyFans](https://onlyfanskissuvt.github.io/)**  )o .｡.:*☆*: .｡. o", "redes"),
        "support" : ("\nkissu abrio una meta de donaciones para los que puedan y quiernan, la apoyen.\nDona de manera resposalbe y no te quedes sin comer, por favor.\n# ☆ **[Donaciones](https://ko-fi.com/kissuvt/goal?g=27)** ☆\n", "support"),
        "ko-fi" : ("# ☆ **[Donaciones](https://ko-fi.com/kissuvt/goal?g=27)** ☆", "ko-fi"),
        }

        content = message.content.lower()
        user = message.author
        channel = message.channel
        guild = message.guild if isinstance(channel, discord.TextChannel) else None

        def log_event(event_name):
            print("----------------------------------------------")
            print(f"Evento activado: {event_name}")
            print(f"Usuario: {user.name} ({user.id})")
            if guild:
                print(f"Servidor: {guild.name} ({guild.id})")
                print(f"Canal: {channel.name} ({channel.id})")
            else:
                print(f"DM con {user.name} ({user.id})")
            print("----------------------------------------------")

        for command in contenidos:
            if content == command:
                await message.delete()
                await message.channel.send(contenidos[command][0])
                log_event(contenidos[command][1])
                break