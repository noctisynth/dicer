from pathlib import Path
from typing import Union

import json
import sys
import uuid
import re
import inspect
import json

try:
    from dicergirl.utils.decorators import translate_punctuation
    from dicergirl.utils.settings import get_package, setconfig, getconfig
    from dicergirl.utils.multilogging import multilogger
    from dicergirl import coc, scp, dnd
except ImportError:
    from .decorators import translate_punctuation
    from .settings import get_package, setconfig, getconfig
    from .multilogging import multilogger
    from .. import coc, scp, dnd

package = get_package()
version = "3.1.26"
current_dir = Path(__file__).resolve().parent
dicer_girl_dir = Path.home() / ".dicergirl"
data_dir = dicer_girl_dir / "data"
_coc_cachepath = data_dir / "coc_cards.json"
_scp_cachepath = data_dir / "scp_cards.json"
_dnd_cachepath = data_dir / "dnd_cards.json"
_super_user = data_dir / "super_user.json"
logger = multilogger(name="Dicer Girl", payload="utils")
su_uuid = (str(uuid.uuid1()) + str(uuid.uuid4())).replace("-", "")
modes = {module.split(".")[-1]: sys.modules[module] for module in sys.modules if hasattr(sys.modules[module], "__type__")}

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

def init():
    if not dicer_girl_dir.exists():
        logger.info("Dicer Girl 文件夹未建立, 建立它.")
        dicer_girl_dir.mkdir()
    if not data_dir.exists():
        logger.info("Dicer Girl 数据文件夹未建立, 建立它.")
        data_dir.mkdir()
    if not _coc_cachepath.exists():
        logger.info("COC 存储文件未建立, 建立它.")
        with open(_coc_cachepath, "w", encoding="utf-8") as f:
            f.write("{}")
    if not _scp_cachepath.exists():
        logger.info("SCP 存储文件未建立, 建立它.")
        with open(_scp_cachepath, "w", encoding="utf-8") as f:
            f.write("{}")
    if not _dnd_cachepath.exists():
        logger.info("DND 存储文件未建立, 建立它.")
        with open(_dnd_cachepath, "w", encoding="utf-8") as f:
            f.write("{}")
    if not _super_user.exists():
        logger.info("超级用户存储文件未建立, 建立它.")
        with open(_super_user, "w", encoding="utf-8") as f:
            f.write("{}")

def set_config(appid, token):
    return setconfig(appid, token, path=dicer_girl_dir, filename="config.yaml")

def get_config() -> dict:
    return getconfig(path=dicer_girl_dir, filename="config.yaml")

def format_msg(message, begin=None, zh_en=False):
    msg = format_str(message, begin=begin).split(" ")
    outer = []
    regex = r'(\d+)|([a-zA-Z\u4e00-\u9fa5]+)' if not zh_en else r"(\d+)|([a-zA-Z]+)|([\u4e00-\u9fa5]+)"

    for m in msg:
        m = re.split(regex, m)
        m = list(filter(None, m))
        outer += m

    msg = outer
    msg = list(filter(None, msg))
    logger.debug(msg)
    return msg

def format_str(message: Union[Message, str], begin=None):
    regex = r"[<\[](.*?)[\]>]"
    content = message.content if isinstance(message, Message) else message
    msg = re.sub("\s+", " ", re.sub(regex, "", str(content).lower())).strip(" ")
    msg = translate_punctuation(msg)
    logger.debug(msg)

    if begin:
        if isinstance(begin, str):
            begin = [begin, ]
        elif isinstance(begin, tuple):
            begin = list(begin)

        begin.sort(reverse=True)
        for b in begin:
            msg = msg.replace(b, "").lstrip(" ")

    logger.debug(msg)
    return msg

def get_mentions(event: GroupMessageEvent):
    mentions = []
    message = json.loads(event.json())["message"]

    for mention in message:
        if mention["type"] == "at":
            mentions.append(mention["data"]["qq"])

    return mentions

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
        if package == "qqguild":
            return str(event.channel_id)
        elif package == "nonebot2":
            return str(event.group_id)
    except:
        logger.warning(f"超出预计的 package: {package}, 将 Group ID 设置为 0.")
        return "0"

def get_user_id(event):
    try:
        if package == "qqguild":
            return eval(str(event.author))["id"]
        elif package == "nonebot2":
            return str(event.get_user_id())
    except:
        logger.warning(f"超出预计的 package: {package}, 将 User ID 设置为 0.")
        return "0"

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
