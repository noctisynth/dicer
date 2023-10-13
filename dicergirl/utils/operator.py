from pathlib import Path
from typing import Dict, List
from dicergirl.common.const import BOT_MODES_FILE, BOT_STATUS_FILE, DICERGIRL_DATA_PATH, DICERGIRL_LOGS_PATH, LOGGERS_CACHE_FILE, SAVED_DATA_PATH, SUPERUSER_FILE
from dicergirl.reply.init import init as reply_init
from dicergirl.utils.handlers import get_group_id
from dicergirl.utils.loggers import load_loggers
from dicergirl.utils.settings import change_status, load_status_settings
from multilogging import multilogger

import json


logger = multilogger(name="DicerGirl", payload="utils.operator")
""" `operator.py`日志 """


def set_name(name) -> bool | str:
    """ 给骰娘命名 """
    if len(name) >= 5:
        return "我不想要太长的名字!"

    with open(DICERGIRL_DATA_PATH / "name", "w") as f:
        f.write(name)

    return True


def get_name() -> str:
    """ 获得骰娘的名字 """
    path = DICERGIRL_DATA_PATH / "name"
    if not path.exists():
        return "欧若可"

    return path.open(mode="r").read()


def botoff(event):
    """ 机器人在`event`所指向的群聊中开启指令限制 """
    status = load_status_settings()
    status[get_group_id(event)] = False
    change_status(status)
    f = open(BOT_STATUS_FILE, "w")
    json.dump(status, f)


def boton(event):
    """ 机器人在`event`所指向的群聊中开启完全功能 """
    status = load_status_settings()
    status[get_group_id(event)] = True
    change_status(status)
    f = open(BOT_STATUS_FILE, "w")
    json.dump(status, f)


def get_status(event):
    """ 判断机器人在`event`所指向的群聊中是否处于完全功能状态 """
    status = load_status_settings()
    group_id = get_group_id(event)

    if group_id in ("private", "botmessage"):
        return True

    if group_id not in status.keys():
        status[get_group_id(event)] = True
        f = open(BOT_STATUS_FILE, "w")
        json.dump(status, f)
        return True

    return status[get_group_id(event)]


def load_status() -> dict:
    """ 导入目前所存储的机器人在各群聊中状态 """
    status_text = BOT_STATUS_FILE.read_text(encoding="utf-8")
    if status_text:
        status = json.loads(status_text)
    else:
        status = {}

    change_status(status)
    return status


def init() -> None:
    """ 骰娘初始化 """
    global saved_loggers
    dirs: Dict[str, List[Path, list]] = {
        "Dicer Girl": [DICERGIRL_DATA_PATH, "dir"],
        "Dicer Girl 数据": [SAVED_DATA_PATH, "dir"],
        "Dicer Girl 日志": [DICERGIRL_LOGS_PATH, "dir"],
        "Dicer Girl 状态管理": [BOT_STATUS_FILE, "file"],
        "日志管理": [LOGGERS_CACHE_FILE, "file"],
        "跑团模式存储": [BOT_MODES_FILE, "file"],
        "超级用户存储": [SUPERUSER_FILE, "file"]
    }
    for name, dir in dirs.items():
        if not dir[0].exists():
            logger.info(f"{name}{'文件夹' if dir[1] == 'dir' else '文件'}未建立, 建立它.")
            if dir[1] == "dir":
                dir[0].mkdir(parents=True, exist_ok=True)
            else:
                with open(dir[0], "w", encoding="utf-8") as f:
                    f.write("{}")
    saved_loggers = load_loggers()
    load_status()
    reply_init()