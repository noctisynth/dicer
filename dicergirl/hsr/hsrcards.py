try:
    from ..utils.cards import Cards
except ImportError:
    from dicergirl.utils.cards import Cards

scp_cards = Cards(mode="hsr")
scp_cache_cards = Cards(mode="hsr")