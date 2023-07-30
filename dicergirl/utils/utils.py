from pathlib import Path
from loguru import logger
from typing import Union

try:
    from dicergirl.utils.decorators import translate_punctuation
    from dicergirl.utils.settings import package, setconfig, getconfig
except ImportError:
    from .decorators import translate_punctuation
    from .settings import package, setconfig, getconfig

if package == "nonebot2":
    class Message:
        pass
    try:
        from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent
    except ModuleNotFoundError:
        logger.warning("未找到依赖`Nonebot2`, 请检查你的配置.")
        class MessageEvent:
            pass
        class GroupMessageEvent:
            pass
elif package == "qqguild":
    class MessageEvent:
        pass
    class GroupMessageEvent:
        pass
    try:
        from botpy.message import Message
    except ModuleNotFoundError:
        logger.warning("未找到依赖`qq-botpy`, 请检查你的配置.")
        class Message:
            pass

import json
import os
import uuid
import re
import inspect

current_dir = Path(__file__).resolve().parent
dicer_girl_dir = Path.home() / ".dicergirl"
data_dir = dicer_girl_dir / "data"
_coc_cachepath = data_dir / "coc_cards.json"
_scp_cachepath = data_dir / "scp_cards.json"
_super_user = data_dir / "super_user.json"
_log = logger
su_uuid = (str(uuid.uuid1()) + str(uuid.uuid4())).replace("-", "")
version = "3.0.4"

def init():
    if not dicer_girl_dir.exists():
        _log.info("Dicer Girl 文件夹未建立, 建立它.")
        dicer_girl_dir.mkdir()
    if not data_dir.exists():
        _log.info("Dicer Girl 数据文件夹未建立, 建立它.")
        data_dir.mkdir()
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

def set_config(appid, token):
    return setconfig(appid, token, path=dicer_girl_dir, filename="config.yaml")

def get_config() -> dict:
    return getconfig(path=dicer_girl_dir, filename="config.yaml")

def format_msg(message, begin=None):
    msg = format_str(message, begin=begin).split(" ")
    outer = []
    for m in msg:
        m = re.split(r'(\d+)|([a-zA-Z]+)|([\u4e00-\u9fa5]+)', m)
        m = list(filter(None, m))
        outer += m
    msg = outer
    msg = list(filter(None, msg))
    _log.debug(msg)
    return msg

def format_str(message: Union[Message, str], begin=None):
    regex = "[<](.*?)[>]"
    content = message.content if isinstance(message, Message) else message
    msg = re.sub("\s+", " ", re.sub(regex, "", str(content).lower())).strip(" ")
    msg = translate_punctuation(msg)
    _log.debug(msg)
    if begin:
        if isinstance(begin, list) or isinstance(begin, tuple):
            for b in begin:
                msg = msg.replace(b, "").lstrip(" ")
        else:
            msg = msg.replace(begin, "").lstrip(" ")
    _log.debug(msg)
    return msg

def get_handlers(main):
    commands_functions = []

    for _, obj in vars(main).items():
        if inspect.isfunction(obj) and hasattr(obj, '__annotations__'):
            annotations = obj.__annotations__
            if annotations.get('message') is Message:
                commands_functions.append(obj)

    return commands_functions

def get_group_id(event):
    try:
        if package == "nonebot2":
            return str(event.group_id)
        elif package == "qqguild":
            return 
    except KeyError:
        return "0"

def get_user_id(event: Union[Message, MessageEvent, GroupMessageEvent]):
    if isinstance(event, Message):
        return eval(str(event.author))["id"]
    else:
        return str(event.get_user_id())

def add_super_user(message):
    with open(_super_user, "w+") as _su:
        sr = _su.read()
        if not sr:
            sudos = {}
        else:
            sudos = json.loads(sr)
        sudos[get_user_id(message)] = ""
        _su.write(json.dumps(sudos))
    return True

def rm_super_user(message):
    rsu = open(_super_user, "r")
    sr = rsu.read()
    if not sr:
        return False
    sudos = json.loads(sr)
    try:
        sudos.pop(get_user_id(message))
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
        if get_user_id(message) == sudo:
            su = True
            break
    return su
