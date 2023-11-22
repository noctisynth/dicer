from nonebot.adapters import Event, Bot
from multilogging import multilogger
from typing import Callable, Dict, List

from ..common.const import BOT_MODES_FILE

import inspect
import json

logger = multilogger(name="DicerGirl", payload="utils.handlers")
""" `utils.handlers`日志 """


def get_mentions(event: Event) -> List[str]:
    """获取`event`指向的消息所有被`@`的用户 QQ 号"""
    mentions = []
    try:
        message = json.loads(event.json())["message"]
    except KeyError:
        return []

    for mention in message:
        if mention["type"] == "at":
            mentions.append(mention["data"]["qq"])

    return mentions


def get_handlers(main: Callable) -> List[Callable]:
    """获取目前所有的指令触发函数方法"""
    commands_functions = []

    for _, obj in vars(main).items():
        if inspect.isfunction(obj) and hasattr(obj, "__annotations__"):
            annotations = obj.__annotations__
            if annotations.get("message") is Event:
                commands_functions.append(obj)

    return commands_functions


def get_group_id(event: Event) -> str:
    """获取`event`指向的群聊`ID`"""
    try:
        if isinstance(event, Event):
            try:
                return str(event.group_id)
            except:
                pass
            try:
                return str(event.get_session_id())
            except:
                pass
            try:
                return str(event.get_user_id())
            except:
                raise ValueError("该适配器没有user_id和group_id")
        else:
            if hasattr(event, "post_type"):
                if event.post_type == "message_sent":
                    return "botmessage"
            return "0"
    except Exception as error:
        logger.exception(error)
        return "0"


def get_user_id(event: Event) -> str:
    """获取`event`指向的用户`ID`"""
    try:
        return event.get_user_id()
    except Exception as error:
        logger.exception(error)
        return "0"


def get_user_card(event: Event) -> str:
    """获取`event`指向的用户群名片"""
    try:
        try:
            raw_json = json.loads(event.json())["sender"]
            if raw_json["card"]:
                return raw_json["card"]
            else:
                return raw_json["nickname"]
        except:
            from .plugins import modes

            cards = modes[get_mode(event)].__cards__
            got = cards.get(event, qid=get_user_id(event))
            if got:
                return got["name"]
            else:
                return "用户"
    except:
        return "未知用户"


def get_user_nickname(event: Event) -> str:
    """获取用户昵称"""
    try:
        try:
            raw_json = json.loads(event.json())["sender"]
            return raw_json["nickname"]
        except:
            from .plugins import modes

            cards = modes[get_mode(event)].__cards__
            got = cards.get(event, qid=get_user_id(event))
            if got:
                return got["name"]
            else:
                return "用户"
    except:
        return "未知用户"


async def get_friend_qids(bot: Bot) -> List[str]:
    result = []
    try:
        friends: list = await bot.get_friend_list()
        for friend in friends:
            result.append(friend["user_id"])
    except:
        pass
    return result


def load_modes() -> Dict[str, list]:
    """加载当前不同群聊的跑团模式"""
    return json.loads(open(BOT_MODES_FILE, "r").read())


def set_mode(event: Event, mode) -> bool:
    """设置当前群聊的跑团模式"""
    lm = load_modes()
    lm[get_group_id(event)] = mode
    json.dump(lm, open(BOT_MODES_FILE, "w"))


def get_mode(event) -> str:
    """获得当前群聊的跑团模式"""
    lm = load_modes()
    if not get_group_id(event) in lm.keys():
        lm[get_group_id(event)] = "coc"
        json.dump(lm, open(BOT_MODES_FILE, "w"))
        return "coc"

    return lm[get_group_id(event)]


async def get_group_member_list(bot: Bot, event: Event) -> list:
    try:
        return await bot.get_group_member_list(group_id=event.group_id)
    except:
        return []
