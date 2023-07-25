from pathlib import Path
from botpy import logging

import json
import os
import uuid

current_dir = Path(__file__).resolve().parent
_coc_cachepath = current_dir.parent / "data" / "coc_cards.json"
_scp_cachepath = current_dir.parent / "data" / "scp_cards.json"
_super_user = current_dir.parent / "data" / "super_user.json"
logger = logging.get_logger()
_log = logger
su_uuid = (str(uuid.uuid1()) + str(uuid.uuid4())).replace("-", "")

def init():
    if not current_dir / "data":
        _log.info("[cocdicer] 数据文件夹未建立, 建立它.")
        os.makedirs("data")
    if not os.path.exists(_coc_cachepath):
        _log.info("[cocdicer] COC存储文件未建立, 建立它.")
        with open(_coc_cachepath, "w", encoding="utf-8") as f:
            f.write("{}")
    if not os.path.exists(_scp_cachepath):
        _log.info("[cocdicer] SCP存储文件未建立, 建立它.")
        with open(_scp_cachepath, "w", encoding="utf-8") as f:
            f.write("{}")
    if not os.path.exists(_super_user):
        _log.info("[cocdicer] 超级用户存储文件未建立, 建立它.")
        with open(_super_user, "w", encoding="utf-8") as f:
            f.write("{}")

def get_group_id(message):
    return message.channel_id

def add_super_user(message):
    with open(_super_user, "w+") as _su:
        sr = _su.read()
        if not sr:
            sudos = {}
        else:
            sudos = json.loads(sr)
        sudos[message.author.id] = ""
        _su.write(json.dumps(sudos))
    return True

def rm_super_user(message):
    rsu = open(_super_user, "r")
    sr = rsu.read()
    if not sr:
        return False
    sudos = json.loads(sr)
    try:
        sudos.pop(message.author.id)
    except KeyError:
        return False
    _su = open(_super_user, "w")
    _su.write(json.dumps(sudos))
    return True

def is_super_user(message):
    su = False
    with open(_super_user, "r") as _su:
        sr = _su.read()
        if not sr:
            sudos = {}
        else:
            sudos = json.loads(sr)
    for sudo in sudos.keys():
        if message.author.id == sudo:
            su = True
            break
    return su