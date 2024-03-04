from typing import Dict, Literal
from multilogging import multilogger

logger = multilogger(name="Dicer Girl", payload="Settings")
""" `settings.py`日志管理系统 """
status: Dict[str, bool] = {}
""" 机器人在各个群聊状态 """
DEBUG = False
""" 漏洞监测模式 """


def change_status(var) -> bool:
    """录入新的`status`内容"""
    global status
    status = var
    return True


def load_status_settings() -> bool:
    """导出当前机器人在各群聊的状态"""
    return status


def is_debug() -> Literal[False]:
    return DEBUG


def debugon() -> Literal[True]:
    global DEBUG
    DEBUG = True


def debugoff() -> Literal[True]:
    global DEBUG
    DEBUG = False
