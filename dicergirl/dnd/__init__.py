from .adventurer import Adventurer
from .nbhandlers import commands
from .dndcards import dnd_cards

dnd_cards.load()

__type__ = "plugin"
__charactor__ = Adventurer
__name__ = "dnd"
__cname__ = "冒险者"
__nbhandler__ = nbhandlers
__nbcommands__ = commands