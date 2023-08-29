from .investigator import Investigator
from .nbhandlers import commands
from .coccards import coc_cards, coc_cache_cards, coc_attrs_dict
from .cocutils import coc_at, coc_dam, coc_ra, coc_en

coc_cards.load()

__type__ = "plugin"
__charactor__ = Investigator
__name__ = "coc"
__cname__ = "调查员"
__cards__ = coc_cards
__cache__ = coc_cache_cards
__nbhandler__ = nbhandlers
__nbcommands__ = commands
__commands__ = {
    "at": coc_at,
    "dam": coc_dam,
    "ra": coc_ra,
    "en": coc_en
}
__baseattrs__ = coc_attrs_dict