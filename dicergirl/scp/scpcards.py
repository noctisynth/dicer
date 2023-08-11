from typing import Dict, List

try:
    from ..utils.utils import _scp_cachepath
    from ..utils.utils import get_group_id, get_user_id
    from ..utils.multilogging import multilogger
except ImportError:
    from dicergirl.utils.utils import _scp_cachepath
    from dicergirl.utils.utils import get_group_id, get_user_id
    from dicergirl.utils.multilogging import multilogger

import json

logger = multilogger(name="Dicer Girl", payload="SCPCard")

class Cards():
    def __init__(self):
        self.data = {}

    def save(self):
        logger.info("保存 SCP 人物卡数据.")
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