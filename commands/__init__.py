from .dm import DmCommand
from .embedm import EmbedCommand
from .help import HelpCommand
from .msg import MsgCommand
from .add_birthday import AddBirthday
from .set_birthday_channel import SetBirthdayChannel
from .clear_channel import Moderation
from .show_birthday import ShowBirthday

commands_list = [DmCommand, EmbedCommand, HelpCommand, MsgCommand, AddBirthday, SetBirthdayChannel, Moderation, ShowBirthday]
