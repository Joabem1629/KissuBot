# KissuBot

Bot de Discord en Python para la comunidad de un servidor. Incluye **niveles y XP**, una **economía con tienda de medallas**, **tarjeta de rango generada como imagen**, **recordatorio de cumpleaños** y varios comandos de moderación.

Es un proyecto personal que uso en un servidor real, desplegado en un VPS.

## Características

- **Niveles y XP**: se gana XP al escribir (con cooldown), con una curva de niveles tipo MEE6/ProBot. Los roles se asignan automáticamente según el nivel.
- **Tarjeta de rango**: imagen generada con Pillow, con fondos personalizables por rango o por usuario.
- **Economía**: monedas al subir de nivel, recompensa diaria y *drops* aleatorios en el chat que se reclaman con un botón.
- **Medallas**: automáticas (por nivel o por cantidad de mensajes) o a la venta en la tienda, con imagen opcional.
- **Cumpleaños**: cada miembro registra su fecha y el bot lo felicita automáticamente en un canal configurable.
- **Respuestas rápidas**: respuestas fijas (texto o imágenes) a mensajes concretos, cargadas desde un archivo JSON.
- **Moderación**: limpiar canal, enviar mensajes o DMs como el bot, y un panel de administración de niveles (`lvl`).
- **Configurable por servidor**: XP, cooldown, recompensas, canales y roles ignorados, canal de avisos de nivel, etc.

## Tecnologías

Python 3.11+ · discord.py 2.3 · Pillow · python-dotenv · almacenamiento en JSON

## Estructura

```
├── main.py                 # Punto de entrada
├── config.json             # Prefijo y ajustes generales
├── commands/               # Un archivo por comando o grupo de comandos (cogs)
├── events/                 # Listeners: XP, subida de nivel, medallas, cumpleaños, errores...
├── utils/
│   ├── levels_core.py      # Lógica de niveles, XP y medallas
│   ├── levels_views.py     # Botones interactivos (drops, reclamar medallas)
│   ├── rankcard.py         # Generación de la tarjeta de rango con Pillow
│   └── storage.py          # Persistencia en JSON con guardado asíncrono
├── custom_replies.example.json   # Ejemplo de respuestas rápidas
├── .env.example                  # Ejemplo de variables de entorno
└── requirements.txt
```

## Instalación

Necesitas Python 3.11 o superior y una aplicación de bot creada en el [Discord Developer Portal](https://discord.com/developers/applications). En la sección **Bot**, activa los *intents* privilegiados **Message Content Intent** y **Server Members Intent**.

```bash
git clone https://github.com/<tu-usuario>/KissuBot.git
cd KissuBot

python -m venv .venv
source .venv/bin/activate          # En Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # En Windows: copy .env.example .env
cp custom_replies.example.json custom_replies.json
```

Edita `.env` y pon tu token en `DISCORD_TOKEN`. Luego inicia el bot:

```bash
python main.py
```

Al usarlo se crean automáticamente la carpeta `data/` (niveles, fondos y medallas) y los archivos de cumpleaños. Nada de eso se sube al repositorio.

## Configuración

| Archivo | Para qué sirve |
|---|---|
| `.env` | Token del bot (`DISCORD_TOKEN`) y, opcionalmente, `LEVELS_DIR` |
| `config.json` | Prefijo de comandos (por defecto `.`) y ID del dueño del bot |
| `custom_replies.json` | Respuestas rápidas: `{"_hola": "¡Hola!"}`. Si el archivo no existe, la función se desactiva |

La configuración de niveles de cada servidor se ajusta desde Discord con `.lvl set` y se consulta con `.lvl config`.

## Comandos

El prefijo por defecto es `.`.

| Comando | Quién | Descripción |
|---|---|---|
| `rank` (`nivel`, `level`) | Todos | Tarjeta de rango propia o de otro miembro |
| `top` (`lb`) | Todos | Ranking del servidor |
| `balance` (`bal`, `monedas`) | Todos | Monedas propias o de otro miembro |
| `daily` | Todos | Recompensa diaria |
| `tienda` / `comprar` | Todos | Catálogo de medallas y compra |
| `medallas` / `reclamar` | Todos | Medallas propias y reclamo de las desbloqueadas |
| `add_birthday MM-DD` | Todos | Registra tu cumpleaños (los mods pueden registrar el de otros con `@usuario`) |
| `show_birthday` | Todos | Cumpleaños registrados, del más cercano al más lejano |
| `set_birthday_channel #canal` | Mods | Canal donde se felicita |
| `lvl ...` | Mods | Administración de niveles: XP, monedas, medallas, roles por nivel, canales ignorados, ajustes |
| `rankbg ...` | Mods | Fondos de la tarjeta de rango |
| `medalla crear` / `medalla borrar` | Mods | Catálogo de medallas |
| `clear_channel` | Mods | Limpia mensajes del canal (pide confirmación) |
| `msg` / `dm` / `embedm` | Mods | Enviar mensajes como el bot |
| `help` | Todos | Lista de comandos |

"Mods" son quienes tienen el permiso *Gestionar servidor* (o el rol de moderador definido con `.lvl modrole`, en los comandos de niveles).

## Aprendizajes

- Arquitectura modular con *cogs* de discord.py y eventos personalizados que desacoplan la lógica (XP → subida de nivel → roles → medallas).
- Persistencia en JSON con guardado asíncrono, autoguardado y recuperación ante archivos corruptos.
- Generación de imágenes dinámicas con Pillow.
- Manejo de permisos, validación de entradas y mensajes de error claros para el usuario.

## Mejoras futuras

- Migrar el almacenamiento de JSON a SQLite (la clase `JsonStore` está pensada para poder reemplazarse).
- Sincronizar los comandos híbridos como *slash commands*.
- Tests automatizados y CI con GitHub Actions.
- Dockerfile para desplegar más fácilmente.
