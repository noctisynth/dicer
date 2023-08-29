from .agent import Agent
from .nbhandlers import commands
from .scpcards import scp_cards
from .scputils import scp_at, scp_dam, scp_ra, scp_en

scp_cards.load()

__type__ = "plugin"
__charactor__ = Agent
__name__ = "scp"
__cname__ = "特工"
__nbhandler__ = nbhandlers
__nbcommands__ = commands
__commands__ = {
    "at": scp_at,
    "dam": scp_dam,
    "ra": scp_ra,
    "en": scp_en
}