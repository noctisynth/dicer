from nonebot.adapters.onebot.v11 import GroupMessageEvent
from loguru._logger import Logger
from typing import Dict, List

from ..common.const import LOGGERS_CACHE_FILE
from .handlers import get_group_id

import json


loggers: Dict[str, Dict[int, List[Logger | str]]] = {}
""" 正在运行的日志 """
saved_loggers: Dict[str, dict]
""" 存储的日志 """


def load_loggers() -> Dict[str, list]:
    """ 加载所有的已存储的日志 """
    return json.loads(open(LOGGERS_CACHE_FILE, "r").read())


def get_loggers(event) -> List[str]:
    """ 获取`event`所指向的群聊中所有的日志 """
    got_loggers = json.load(open(LOGGERS_CACHE_FILE, "r"))
    if not get_group_id(event) in got_loggers:
        return []

    return got_loggers[get_group_id(event)]


def add_logger(event: GroupMessageEvent, logname) -> bool:
    """ 新增日志序列 """
    global saved_loggers
    if not get_group_id(event) in saved_loggers.keys():
        saved_loggers[get_group_id(event)] = []

    try:
        saved_loggers[get_group_id(event)].append(logname)
        json.dump(saved_loggers, open(LOGGERS_CACHE_FILE, "w"))
        return True
    except:
        return False


def remove_logger(event: GroupMessageEvent, id: int) -> Dict[str, list]:
    """ 从存储的`loggers.json`中移除指定`logger` """
    saved_loggers[get_group_id(event)].pop(id)
    json.dump(saved_loggers, open(LOGGERS_CACHE_FILE, "w"))
    return saved_loggers