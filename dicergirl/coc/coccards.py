from typing import Dict, List
try:
    from ..utils.cards import Cards
except ImportError:
    from dicergirl.utils.cards import Cards

coc_cards = Cards(mode="coc")
coc_cache_cards = Cards(mode="coc")
coc_attrs_dict: Dict[str, List[str]] = {
    "名字": ["name", "名字", "名称", "姓名"],
    "性别": ["sex", "性别"],
    "年龄": ["age", "年龄"],
    "力量": ["str", "力量", "攻击", "攻击力"],
    "体质": ["con", "体质"],
    "体型": ["siz", "体型"],
    "敏捷": ["dex", "敏捷"],
    "外貌": ["app", "外貌"],
    "智力": ["int", "智力", "灵感"],
    "意志": ["pow", "意志", "精神"],
    "教育": ["edu", "教育"],
    "幸运": ["luc", "幸运"],
    "理智": ["san", "理智", "精神状态", "san值"],
    "生命": ["hp", "生命"]
}
coc_rolls = {}