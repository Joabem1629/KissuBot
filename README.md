# 🌸 KissuBot

¡Hola! Soy **KissuBot**, un bot de Discord modular desarrollado en Python con `discord.py`. Actualmente, estoy diseñado para gestionar anuncios de cumpleaños, herramientas de moderación y utilidades de mensajería.

## 📌 Propósito del Proyecto

**KissuBot** nació con el objetivo principal de servir a un servidor de Discord específico, personalizando funciones según sus necesidades. Sin embargo, el proyecto está en constante evolución con la visión de **escalarlo y mejorarlo**, transformándolo en una herramienta versátil de propósito general apta para cualquier comunidad.

---

## ✨ Características Principales

### 🎈 Sistema de Cumpleaños

* **Anuncios Automáticos:** Felicito a los usuarios exactamente a las **9:30 AM (Hora Perú, UTC-5)** cada día.
* **Registro Personalizado:** Permite guardar fechas en formato `MM-DD`.
* **Visualización con Paginación:** Lista elegante y ordenada de los próximos cumpleaños con botones de navegación.
* **Configuración por Servidor:** Cada servidor puede elegir su propio canal de anuncios de forma independiente.

### 🛡️ Moderación y Utilidad

* **Limpieza de Canales:** Comando `clear_channel` para borrar mensajes masivamente (incluye sistema de confirmación de seguridad).
* **Mensajería Directa:** Capacidad para enviar mensajes o Embeds a cualquier usuario a través del bot.
* **Logs de Actividad:** Registro detallado de eventos en la carpeta `logs/`.

---

## 🚀 Instalación y Configuración

### 1. Requisitos

* Python 3.8 o superior.
* Librerías: `discord.py` y `python-dotenv`.

### 2. Configuración de Seguridad

El bot utiliza archivos externos para proteger datos sensibles. Debes configurar los siguientes:

1. **Variables de Entorno:** Crea un archivo `.env` en la raíz con tu token:
```env
DISCORD_TOKEN=tu_token_aqui

```


2. **Configuración del Bot:** Crea un archivo `config.json` basándote en el formato del proyecto:
```json
{
    "prefix": "k!",
    "owner_id": tu_id_de_discord_aqui
}

```



### 3. Ejecución

```bash
# Instalar dependencias
pip install discord.py python-dotenv

# Iniciar el bot
python main.py

```

---

## 📋 Lista de Comandos

El prefijo predeterminado es `k!`.

| Comando | Acción |
| --- | --- |
| `k!add_birthday @usuario MM-DD` | Registra un nuevo cumpleaños en la base de datos. |
| `k!show_birthday` | Muestra los cumpleañeros del servidor (con paginación). |
| `k!set_birthday_channel #canal` | Define el canal de anuncios para el servidor actual. |
| `k!clear_channel` | Elimina el historial de mensajes del canal actual. |
| `k!dm @usuario mensaje` | Envía un mensaje privado simple a través del bot. |
| `k!embedm @usuario mensaje` | Envía un mensaje privado en formato Embed elegante. |

---

## 📁 Arquitectura Modular

KissuBot utiliza una estructura de **Cogs** para facilitar su mantenimiento y escalabilidad:

* `commands/`: Lógica de comandos organizada por módulos.
* `events/`: Controladores de eventos (on_ready, errores, tareas programadas).
* `main.py`: El núcleo del bot que carga dinámicamente todos los componentes.

---

Desarrollado con ❤️ por [Joabem1629](https://www.google.com/search?q=https://github.com/Joabem1629)

