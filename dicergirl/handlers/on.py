from nonebot.consts import STARTSWITH_KEY
from nonebot.matcher import Matcher
from nonebot.plugin import on_message
from nonebot.rule import Rule

from ..common.decorators import translate_punctuation

import re

class StartswithRule:
    """
    自定义的指令检查方法
    允许:
        1. 无视中英文字符串
        2. 无视前后多余空字符
    """
    __slots__ = ("msg", "ignorecase")

    def __init__(self, msg, ignorecase=False):
        self.msg = msg
        self.ignorecase = ignorecase

    def __repr__(self) -> str:
        return f"Startswith(msg={self.msg}, ignorecase={self.ignorecase})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, StartswithRule)
            and frozenset(self.msg) == frozenset(other.msg)
            and self.ignorecase == other.ignorecase
        )

    def __hash__(self) -> int:
        return hash((frozenset(self.msg), self.ignorecase))

    async def __call__(self, event, state) -> bool:
        try:
            text = translate_punctuation(event.get_plaintext()).strip()
        except Exception:
            return False
        if match := re.match(
            f"^(?:{'|'.join(re.escape(prefix) for prefix in self.msg)})",
            text,
            re.IGNORECASE if self.ignorecase else 0,
        ):
            state[STARTSWITH_KEY] = match.group()
            return True
        return False


def startswith(msg, ignorecase=True) -> Rule:
    """ 实例化指令检查方法 """
    if isinstance(msg, str):
        msg = (msg,)

    return Rule(StartswithRule(msg, ignorecase))


def on_startswith(commands, priority=0, block=True) -> Matcher:
    """ 获得`Nonebot2`指令检查及参数注入方法 """
    if isinstance(commands, str):
        commands = (commands, )

    return on_message(startswith(commands, True), priority=priority, block=block, _depth=1)