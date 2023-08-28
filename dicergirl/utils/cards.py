from pathlib import Path
from multilogging import multilogger

try:
    from .utils import get_group_id, get_user_id
except ImportError:
    from dicergirl.utils.utils import get_group_id, get_user_id

import json

logger = multilogger(name="Dicer Girl", payload="Card")

class Cards():
    data_path: Path = Path.home() / ".dicergirl" / "data"

    def __init__(self, mode: str=None, cache_path: Path=None):
        self.data = {}
        self.mode = mode if mode else "未知模式"
        self.cache_path = cache_path if cache_path else self.data_path / f"{mode}_cards.json"

    def init(self):
        logger.info(f"{self.mode.upper()} 存储文件未建立, 建立它.")
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False)

    def save(self):
        logger.info(f"保存 {self.mode.upper()} 人物卡数据.")
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False)

    def load(self) -> dict:
        if not self.cache_path.exists():
            self.init()

        with open(self.cache_path, "r", encoding="utf-8") as f:
            data = f.read()
            if not data:
                self.data = {}
            else:
                self.data = json.loads(data)

        return self.data

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