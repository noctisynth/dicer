from .agent import Agent
from .nbhandlers import commands
from .scpcards import scp_cards, scp_cache_cards
from .attributes import scp_attrs_dict
from .scputils import scp_at, scp_dam, scp_ra, scp_en

scp_cards.load()

__type__ = "plugin"
__charactor__ = Agent
__name__ = "scp"
__cname__ = "特工"
__cards__ = scp_cards
__cache__ = scp_cache_cards
__nbhandler__ = nbhandlers
__nbcommands__ = commands
__commands__ = {
    "at": scp_at,
    "dam": scp_dam,
    "ra": scp_ra,
    "en": scp_en
}
__baseattrs__ = scp_attrs_dict
__description__ = "SCP 模式是基于SCP基金会(SCP Foundation) 设定的 TRPG 跑团模式."