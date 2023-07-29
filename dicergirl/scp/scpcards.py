from typing import Dict, List
try:
    from ..utils.utils import logger as _log, _scp_cachepath
    from ..utils.utils import get_group_id, get_user_id
except ImportError:
    from dicergirl.utils.utils import logger as _log, _scp_cachepath
    from dicergirl.utils.utils import get_group_id, get_user_id

import json

class Cards():
    def __init__(self):
        self.data = {}

    def save(self):
        _log.info("[cards] 保存SCP人物卡数据.")
        with open(_scp_cachepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False)

    def load(self):
        with open(_scp_cachepath, "r", encoding="utf-8") as f:
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

scp_cards = Cards()
scp_cache_cards = Cards()
scp_attrs_dict: Dict[str, List[str]] = {
    "名字": ["name", "名字", "名称", "姓名"],
    "性别": ["sex", "性别"],
    "年龄": ["age", "年龄"],
    "强度": ["str", "力量", "攻击", "强度"],
    "灵巧": ["dex", "灵巧"],
    "健康": ["hth", "健康"],
    "命运": ["fte", "命运"],
    "魅力": ["chr", "魅力"],
    "情报": ["int", "情报"],
    "意志": ["wil", "意志", "精神"],
    "生命": ["hp", "生命"]
}
