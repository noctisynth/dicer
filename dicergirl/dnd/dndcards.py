from typing import Dict, List
try:
    from ..utils.cards import Cards
except ImportError:
    from dicergirl.utils.cards import Cards

dnd_cards = Cards(mode="dnd")
dnd_cache_cards = Cards(mode="dnd")
dnd_attrs_dict: Dict[str, List[str]] = {
    "名字": ["name", "名字", "名称", "姓名"],
    "性别": ["sex", "性别"],
    "年龄": ["age", "年龄"],
    "力量": ["str", "力量", "攻击", "攻击力"],
    "敏捷": ["dex", "敏捷"],
    "体质": ["con", "体质"],
    "智力": ["int", "智力", "灵感"],
    "感知": ["fel", "感知", "感觉", "侦查"],
    "魅力": ["chr", "魅力", "外貌"],
    "生命": ["hp", "生命"]
}
