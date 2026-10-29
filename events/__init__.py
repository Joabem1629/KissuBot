from .error_handler import ErrorHandler
from .on_message import OnMessage
from .on_ready import OnReady
# from .birthday_event import BirthdayEvent
from .xp_message import XpMessage
from .level_up import LevelUp
from .rank_up import RankUp
from .medal_unlock import MedalUnlock
from .coin_drop import CoinDrop

# Cargar todos los eventos en una lista para facilitar la gestión
events_list = [ErrorHandler, OnMessage, OnReady, XpMessage, LevelUp, RankUp, MedalUnlock, CoinDrop]
