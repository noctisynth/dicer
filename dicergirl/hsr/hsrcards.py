try:
    from ..utils.cards import Cards
except ImportError:
    from dicergirl.utils.cards import Cards

hsr_cards = Cards(mode="hsr")
hsr_cache_cards = Cards(mode="hsr")