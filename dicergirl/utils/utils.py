from pathlib import Path
from typing import Union, Dict, List, Callable
from loguru._logger import Logger

import json
import sys
import uuid
import re
import inspect
import json

try:
    from dicergirl.utils.decorators import translate_punctuation
    from dicergirl.utils.settings import get_package, setconfig, getconfig, change_status, load_status_settings
    from dicergirl.utils.multilogging import multilogger
    from dicergirl import coc, scp, dnd
except ImportError:
    from .decorators import translate_punctuation
    from .settings import get_package, setconfig, getconfig, change_status, load_status_settings
    from .multilogging import multilogger
    from .. import coc, scp, dnd

package = get_package()
""" 当前 Dicer Girl 运行平台 """
version = "3.1.27"
""" Dicer Girl 版本号 """
current_dir = Path(__file__).resolve().parent
""" Dicer Girl 当前目录 """
dicer_girl_dir = Path.home() / ".dicergirl"
data_dir = dicer_girl_dir / "data"
log_dir = dicer_girl_dir / "log"
_dicer_girl_status = data_dir / "status.json"
_coc_cachepath = data_dir / "coc_cards.json"
_scp_cachepath = data_dir / "scp_cards.json"
_dnd_cachepath = data_dir / "dnd_cards.json"
_hsr_cache_path = data_dir / "hsr.json"
_super_user = data_dir / "super_user.json"
_loggers_cachepath = data_dir / "loggers.json"
logger = multilogger(name="Dicer Girl", payload="utils")
""" `utils.py`日志系统 """
su_uuid = (str(uuid.uuid1()) + str(uuid.uuid4())).replace("-", "")
modes = {module.split(".")[-1]: sys.modules[module] for module in sys.modules if hasattr(sys.modules[module], "__type__")}
""" 已导入的跑团模块 """
loggers: Dict[str, Dict[int, List[Logger | str]]] = {}
""" 正在运行的日志 """
saved_loggers: Dict[str, dict]
""" 存储的日志 """

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

def init() -> None:
    """ 骰娘初始化 """
    global saved_loggers
    dirs: Dict[str, List[Path, list]] = {
        "Dicer Girl": [dicer_girl_dir, "dir"],
        "Dicer Girl 数据": [data_dir, "dir"],
        "Dicer Girl 日志": [log_dir, "dir"],
        "Dicer Girl 状态管理": [_dicer_girl_status, "file"],
        "日志管理": [_loggers_cachepath, "file"],
        "COC 存储": [_coc_cachepath, "file"],
        "SCP 存储": [_scp_cachepath, "file"],
        "DND 存储": [_dnd_cachepath, "file"],
        "HSR 存储": [_hsr_cache_path, "file"],
        "超级用户存储": [_super_user, "file"]
    }
    for name, dir in dirs.items():
        if not dir[0].exists():
            logger.info(f"{name}{'文件夹' if dir[1] == 'dir' else '文件'}未建立, 建立它.")
            if dir[1] == "dir":
                dir[0].mkdir()
            else:
                with open(dir[0], "w", encoding="utf-8") as f:
                    f.write("{}")
    saved_loggers = load_loggers()
    load_status()

def load_loggers() -> Dict[str, list]:
    """ 加载所有的已存储的日志 """
    return json.loads(open(_loggers_cachepath, "r").read())

def get_loggers(event) -> List[str]:
    """ 获取`event`所指向的群聊中所有的日志 """
    got_loggers = json.load(open(_loggers_cachepath, "r"))
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
        json.dump(saved_loggers, open(_loggers_cachepath, "w"))
        return True
    except:
        return False

def remove_logger(event: GroupMessageEvent, id: int) -> Dict[str, list]:
    """ 从存储的`loggers.json`中移除指定`logger` """
    saved_loggers[get_group_id(event)].pop(id)
    json.dump(saved_loggers, open(_loggers_cachepath, "w"))
    return saved_loggers

def set_config(appid, token) -> dict:
    """ 在`QQGuild`模式中设置频道机器人`appid`以及`token`. """
    return setconfig(appid, token, path=dicer_girl_dir, filename="config.yaml")

def get_config() -> dict:
    """ 获取`QQGuild`模式中频道机器人的`appid`以及`token`. """
    return getconfig(path=dicer_girl_dir, filename="config.yaml")

def format_msg(message, begin=None, zh_en=False) -> list:
    """ 骰娘指令拆析为`list`的方法 """
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

def format_str(message: Union[Message, str], begin=None) -> str:
    """ 骰娘指令转义及解析 """
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

def get_mentions(event: GroupMessageEvent) -> List[str]:
    """ 获取`event`指向的消息所有被`@`的用户 QQ 号 """
    mentions = []
    message = json.loads(event.json())["message"]

    for mention in message:
        if mention["type"] == "at":
            mentions.append(mention["data"]["qq"])

    return mentions

def get_handlers(main) -> List[Callable]:
    """ 获取目前所有的指令触发函数方法 """
    commands_functions = []

    for _, obj in vars(main).items():
        if inspect.isfunction(obj) and hasattr(obj, '__annotations__'):
            annotations = obj.__annotations__
            if annotations.get('message') is Message:
                commands_functions.append(obj)

    return commands_functions

def get_group_id(event) -> str:
    """ 获取`event`指向的群聊`ID` """
    try:
        if package == "qqguild":
            return str(event.channel_id)
        elif package == "nonebot2":
            return str(event.group_id)
    except:
        logger.warning(f"超出预计的 package: {package}, 将 Group ID 设置为 0.")
        return "0"

def get_user_id(event) -> str:
    """ 获取`event`指向的用户`ID` """
    try:
        if package == "qqguild":
            return eval(str(event.author))["id"]
        elif package == "nonebot2":
            return str(event.get_user_id())
    except:
        logger.warning(f"超出预计的 package: {package}, 将 User ID 设置为 0.")
        return "0"

def add_super_user(message) -> bool:
    """ 新增超级管理员 """
    with open(_super_user, "w+") as _su:
        sr = _su.read()
        if not sr:
            sudos = {}
        else:
            sudos = json.loads(sr)
        sudos[get_user_id(message)] = ""
        _su.write(json.dumps(sudos))
    return True

def rm_super_user(message) -> bool:
    """ 删除超级管理员 """
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

def is_super_user(event) -> bool:
    """ 判断`event`所指向的用户是否为超级管理员 """
    su = False
    with open(_super_user, "r") as _su:
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

def botoff(event):
    """ 机器人在`event`所指向的群聊中开启指令限制 """
    status = load_status_settings()
    status[get_group_id(event)] = False
    change_status(status)
    f = open(_dicer_girl_status, "w")
    json.dump(status, f)

def boton(event):
    """ 机器人在`event`所指向的群聊中开启完全功能 """
    status = load_status_settings()
    status[get_group_id(event)] = True
    change_status(status)
    f = open(_dicer_girl_status, "w")
    json.dump(status, f)

def get_status(event):
    """ 判断机器人在`event`所指向的群聊中是否处于完全功能状态 """
    status = load_status_settings()
    if not get_group_id(event) in status.keys():
        status[get_group_id(event)] = True
        f = open(_dicer_girl_status, "w")
        json.dump(status, f)
        return True

    return status[get_group_id(event)]

def load_status():
    """ 导入目前所存储的机器人在各群聊中状态 """
    change_status(json.load(open(_dicer_girl_status, "r")))

def rolekp(event):
    ...

def roleob(event):
    ...