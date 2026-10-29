"""
Almacenamiento en JSON (un solo archivo, organizado por servidor).

Para escalar a SQLite/Mongo/Postgres más adelante solo hay que reemplazar esta
clase manteniendo los métodos: guild(), user(), dirty(), save() y save_sync().
"""
import asyncio
import copy
import json
import time
from pathlib import Path

DEFAULT_CONFIG = {
    "xp_min": 15,
    "xp_max": 25,
    "cooldown": 60,            # segundos entre mensajes que dan XP
    "multiplier": 1.0,         # multiplicador global de XP
    "coins_per_level": 50,     # monedas al subir de nivel
    "daily": 100,              # monedas del daily
    "drop_chance": 2.0,        # % de que aparezca un drop por mensaje con XP
    "drop_min": 20,
    "drop_max": 80,
    "stack_roles": False,      # False = solo el rol más alto; True = acumula todos
    "levelup_channel": None,   # None = el mismo canal donde subió
    "mod_role": None,          # rol extra de moderador (además de Gestionar servidor)
    "ignored_channels": [],
    "ignored_roles": [],
    "level_roles": {},         # {"10": role_id}
    "tier_bgs": {},            # {"10": "archivo.png"} fondo desde ese nivel
    "accent": 0x5865F2,        # color de la barra
}

DEFAULT_USER = {
    "xp": 0,
    "messages": 0,
    "coins": 0,
    "medals": [],
    "pending": [],             # medallas desbloqueadas pendientes de reclamar
    "bg": None,                # fondo personal (lo pone un mod)
    "last_daily": 0,
}


class JsonStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data = {"guilds": {}}
        self._dirty = False
        self._lock = asyncio.Lock()
        self._load()

    # ---------- carga / guardado ----------
    def _load(self):
        if not self.path.exists():
            return
        try:
            self.data = json.loads(self.path.read_text("utf-8"))
        except json.JSONDecodeError:
            # archivo corrupto: lo respaldamos y arrancamos limpio
            backup = self.path.with_suffix(f".corrupto-{int(time.time())}.json")
            self.path.rename(backup)
            print(f"[storage] JSON corrupto, respaldado en {backup}")

    def dirty(self):
        self._dirty = True

    async def save(self):
        if not self._dirty:
            return
        async with self._lock:
            self._dirty = False
            snapshot = json.dumps(self.data, ensure_ascii=False, indent=1)
            await asyncio.to_thread(self._write, snapshot)

    def save_sync(self):
        """Guardado síncrono (se usa al cerrar el bot con atexit)."""
        if not self._dirty:
            return
        self._dirty = False
        self._write(json.dumps(self.data, ensure_ascii=False, indent=1))

    def _write(self, text):
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(text, "utf-8")
        tmp.replace(self.path)  # escritura atómica

    # ---------- acceso ----------
    def guild(self, guild_id) -> dict:
        g = self.data["guilds"].setdefault(
            str(guild_id), {"config": {}, "users": {}, "medals": {}}
        )
        for k, v in DEFAULT_CONFIG.items():
            g["config"].setdefault(k, copy.deepcopy(v))
        return g

    def user(self, guild_id, user_id) -> dict:
        u = self.guild(guild_id)["users"].setdefault(str(user_id), {})
        for k, v in DEFAULT_USER.items():
            u.setdefault(k, copy.deepcopy(v))
        return u
