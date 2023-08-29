from .agent import Agent
from .nbhandlers import commands
from .scpcards import scp_cards

scp_cards.load()

__type__ = "plugin"
__charactor__ = Agent
__name__ = "scp"
__cname__ = "特工"
__nbhandler__ = nbhandlers
__nbcommands__ = commands