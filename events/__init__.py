from .error_handler import ErrorHandler
from .on_message import OnMessage
from .on_ready import OnReady
# from .birthday_event import BirthdayEvent

# Cargar todos los eventos en una lista para facilitar la gestión
events_list = [ErrorHandler, OnMessage, OnReady]
