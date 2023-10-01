import yaml

from typing import Dict, Any
from pathlib import Path
from multilogging import multilogger
from yaml.loader import FullLoader
from nonebot.adapters import Event

from .utils import get_group_id, get_user_id
from ..common.const import SAVED_DATA_PATH


logger = multilogger(name="DicerGirl", payload="Card")


class Cards:
    """ DicerGirl 人物卡数据操作类 """
    data_path: Path = SAVED_DATA_PATH

    def __init__(self, mode: str=None, cache_path: Path=None):
        self.data: Dict[str, Dict[str, Any]] = {}
        self.mode = mode if mode else "未知模式"
        self.cache_path = cache_path if cache_path else self.data_path / f"{mode}_cards.yaml"

    def init(self):
        logger.info(f"{self.mode.upper()} 存储文件未建立, 建立它.")
        if not self.cache_path.parent.exists():
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)

        with self.cache_path.open(mode="w", encoding="utf-8") as f:
            yaml.dump({"mode": self.mode, "cards": {}}, f)

    def save(self):
        if not self.cache_path.exists():
            self.init()

        with self.cache_path.open(mode="w", encoding="utf-8") as f:
            yaml.dump({"mode": self.mode, "cards": self.data}, f, allow_unicode=True)

    def load(self) -> dict:
        if not self.cache_path.exists():
            self.init()

        with self.cache_path.open(mode="r", encoding="utf-8") as f:
            data = yaml.load(f, FullLoader)
            if data is None:
                self.data = {}
            else:
                self.data = data["cards"]

        return self.data

    def update(self, event: Event, cha_dict: dict, qid: str="", save: bool=True) -> None:
        group_id = get_group_id(event)
        if not self.data.get(group_id):
            self.data[group_id] = {}

        self.data[group_id].update(
            {qid if qid else get_user_id(event): cha_dict}
            )

        return self.save() if save else None

    def get(self, event: Event, qid=""):
        group_id = get_group_id(event)
        if self.data.get(group_id):
            if self.data[group_id].get(qid if qid else get_user_id(event)):
                return self.data[group_id].get(qid if qid else get_user_id(event))
        else:
            return None

    def delete(self, event: Event, qid: str = "", save: bool = True) -> bool:
        if self.get(event, qid=qid):
            if self.data[get_group_id(event)].get(qid if qid else get_user_id(event)):
                self.data[get_group_id(event)].pop(
                    qid if qid else get_user_id(event))
            if save:
                self.save()
            return True
        return False

    def delete_skill(self, event: Event, skill_name: str, qid: str = "", save: bool = True) -> bool:
        if self.get(event, qid=qid):
            data = self.get(event, qid=qid)
            if data["skills"].get(skill_name):
                data["skills"].pop(skill_name)
                self.update(event, data, qid=qid, save=save)
                return True
        return False