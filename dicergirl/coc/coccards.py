from typing import Dict, List
try:
    from ..utils.messages import help_messages
    from ..utils.dicer import Dice, expr
    from ..utils.utils import _coc_cachepath as _cachepath, get_group_id, get_user_id
    from ..utils.multilogging import multilogger
except ImportError:
    from dicergirl.utils.messages import help_messages
    from dicergirl.utils.dicer import Dice, expr
    from dicergirl.utils.utils import _coc_cachepath as _cachepath, get_group_id, get_user_id
    from dicergirl.utils.multilogging import multilogger

import json

logger = multilogger(name="Dicer Girl", payload="COCCard")

class Cards():
    def __init__(self):
        self.data = {}

    def save(self):
        logger.info("[cards] 保存COC人物卡数据.")
        with open(_cachepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False)

    def load(self):
        with open(_cachepath, "r", encoding="utf-8") as f:
            data = f.read()
            if not data:
                self.data = {}
            else:
                self.data = json.loads(data)

    def update(self, message, inv_dict, qid="", save=True):
        group_id = get_group_id(message)
        if not self.data.get(group_id):
            self.data[group_id] = {}
        self.data[group_id].update(
            {qid if qid else get_user_id(message): inv_dict}
            )
        if save:
            self.save()

    def get(self, message, qid=""):
        group_id = get_group_id(message)
        if self.data.get(group_id):
            if self.data[group_id].get(qid if qid else get_user_id(message)):
                return self.data[group_id].get(qid if qid else get_user_id(message))
        else:
            return None

    def delete(self, message, qid: str = "", save: bool = True) -> bool:
        if self.get(message, qid=qid):
            if self.data[get_group_id(message)].get(qid if qid else get_user_id(message)):
                self.data[get_group_id(message)].pop(
                    qid if qid else get_user_id(message))
            if save:
                self.save()
            return True
        return False

    def delete_skill(self, message, skill_name: str, qid: str = "", save: bool = True) -> bool:
        if self.get(message, qid=qid):
            data = self.get(message, qid=qid)
            if data["skills"].get(skill_name):
                data["skills"].pop(skill_name)
                self.update(message, data, qid=qid, save=save)
                return True
        return False


coc_cards = Cards()
coc_cache_cards = Cards()
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