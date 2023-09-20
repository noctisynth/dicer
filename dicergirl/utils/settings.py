from typing import List, Dict
from multilogging import multilogger

package: str = None
""" 目前 Dicer Girl 挂载的平台 """
allowed_packages: List[str] = ["nonebot2", "qqguild"]
""" Dicer Girl 允许挂载的平台 """
logger = multilogger(name="Dicer Girl", payload="Settings")
""" `settings.py`日志管理系统 """
status: Dict[str, bool] = {}
""" 机器人在各个群聊状态 """
DEBUG = False
""" 漏洞监测模式 """

def change_status(var) -> bool:
    """ 录入新的`status`内容 """
    global status
    status = var
    return True

def load_status_settings():
    """ 导出当前机器人在各群聊的状态 """
    return status