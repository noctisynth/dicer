from dicergirl.common.const import BOT_MODES_FILE
from dicergirl.utils.handlers import get_group_id
from typing import Dict

import json


def load_modes() -> Dict[str, list]:
    """ 加载当前不同群聊的跑团模式 """
    return json.loads(open(BOT_MODES_FILE, "r").read())


def set_mode(event, mode) -> bool:
    """ 设置当前群聊的跑团模式 """
    lm = load_modes()
    lm[get_group_id(event)] = mode
    json.dump(lm, open(BOT_MODES_FILE, "w"))


def get_mode(event) -> str:
    """ 获得当前群聊的跑团模式 """
    lm = load_modes()
    if not get_group_id(event) in lm.keys():
        lm[get_group_id(event)] = "coc"
        json.dump(lm, open(BOT_MODES_FILE, "w"))
        return "coc"

    return lm[get_group_id(event)]