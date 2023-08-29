from .trailblazer import Trailblazer
from .nbhandlers import commands
from .hsrcards import hsr_cards

hsr_cards.load()

__type__ = "plugin"
__charactor__ = Trailblazer
__name__ = "hsr"
__cname__ = "开拓者"
__nbhandler__ = nbhandlers
__nbcommands__ = commands