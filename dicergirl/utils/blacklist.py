from typing import List
from yaml.loader import FullLoader
from ..common.const import BLACKLIST_FILE

import yaml


class BlackList:
    """黑名单类"""

    def __init__(self) -> None:
        if not BLACKLIST_FILE.exists():
            BLACKLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
            yaml.dump({"user": None, "group": None}, BLACKLIST_FILE.open("w"))

        if not self.load():
            raise OSError

    def load(self) -> bool:
        try:
            self.blacklist: list = (
                yaml.load(BLACKLIST_FILE.open("r"), FullLoader)["user"] or []
            )
            self.group_blacklist: list = (
                yaml.load(BLACKLIST_FILE.open("r"), FullLoader)["group"] or []
            )
            return True
        except:
            return False

    def dump(self) -> str:
        BLACKLIST_FILE.write_text("")
        return yaml.dump(
            {"user": self.blacklist, "group": self.group_blacklist},
            BLACKLIST_FILE.open("w"),
        )

    def get_blacklist(self) -> List[str]:
        return self.blacklist or []

    def add_blacklist(self, qid: str) -> str:
        self.blacklist.append(qid)
        return self.dump()

    def remove_blacklist(self, qid: str) -> str:
        self.blacklist.remove(qid)
        return self.dump()

    def get_group_blacklist(self) -> List[str]:
        return self.group_blacklist or []

    def add_group_blacklist(self, gid: str) -> str:
        self.group_blacklist.append(gid)
        return self.dump()

    def remove_group_blacklist(self, gid: str) -> str:
        self.group_blacklist.remove(gid)
        return self.dump()


blacklist = BlackList()
