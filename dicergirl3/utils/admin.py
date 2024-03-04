from typing import Dict, List, Literal
from ..common.const import SUPERUSER_FILE
from .handlers import get_user_id

import uuid
import json


su_uuid: str
""" 超级管理员鉴权令牌 """


def make_uuid() -> str:
    """创建新的超级管理员鉴权令牌"""
    global su_uuid
    su_uuid = (str(uuid.uuid1()) + str(uuid.uuid4())).replace("-", "")
    return su_uuid


def get_uuid() -> str:
    """获取超级管理员鉴权令牌"""
    return su_uuid


def add_super_user(message) -> bool:
    """新增超级管理员"""
    with open(SUPERUSER_FILE, "w+") as _su:
        sr = _su.read()
        if not sr:
            sudos = {}
        else:
            sudos = json.loads(sr)
        sudos[get_user_id(message)] = ""
        _su.write(json.dumps(sudos))
    return True


def rm_super_user(message) -> bool:
    """删除超级管理员"""
    rsu = open(SUPERUSER_FILE, "r")
    sr = rsu.read()
    if not sr:
        return False
    sudos = json.loads(sr)
    try:
        sudos.pop(get_user_id(message))
    except KeyError:
        return False
    _su = open(SUPERUSER_FILE, "w")
    _su.write(json.dumps(sudos))
    return True


def is_super_user(event) -> bool:
    """判断`event`所指向的用户是否为超级管理员"""
    su = False
    with open(SUPERUSER_FILE, "r") as _su:
        sr = _su.read()
        if not sr:
            sudos = {}
        else:
            sudos = json.loads(sr)
    for sudo in sudos.keys():
        if get_user_id(event) == sudo:
            su = True
            break
    return su


def get_super_users() -> List[str]:
    """捕获所有骰娘管理员"""
    su_read = SUPERUSER_FILE.read_text()
    if not su_read:
        return []

    read: Dict[str, Literal[""]] = json.loads(su_read)
    return list(read.keys())
