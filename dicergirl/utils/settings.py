from pathlib import Path
from typing import List, Dict
try:
    from dicergirl.utils.multilogging import multilogger
except ImportError:
    from .multilogging import multilogger

import sys
import yaml

package: str = None
""" 目前 Dicer Girl 挂载的平台 """
allowed_packages: List[str] = ["nonebot2", "qqguild"]
""" Dicer Girl 允许挂载的平台 """
logger = multilogger(name="Dicer Girl", payload="Settings")
""" `settings.py`日志管理系统 """
status: Dict[str, bool] = {}
""" 机器人在各个群聊状态 """

def set_package(pkg: str):
    """ 设置当前挂载的平台 """
    global package
    pkg = pkg.lower()

    if pkg in allowed_packages:
        package = pkg
        return package
    else:
        try:
            raise ValueError(f"错误的包名:`{pkg}`, 支持的包: {allowed_packages}")
        except Exception as error:
            logger.exception(error)
        sys.exit()

def get_package():
    """ 获得当前挂载的平台 """
    return package

def setconfig(appid, token, path=Path.home()/".dicergirl", filename="config.yaml"):
    """ 在`QQGuild`模式中设置频道机器人`appid`以及`token`. """
    if package == "nonebot2":
        raise AttributeError("你无法在 Nonebot2 模式下创建配置文件, 请确保你在调用`setconfig`函数之前已经执行了`set_package('qqguild').")
    configfile = open(path / filename, "w")
    data = {
            "appid": appid,
            "token": token
            }
    yaml.dump(data, configfile, sort_keys = False)
    return data

def getconfig(path=Path.home()/".dicergirl", filename="config.yaml"):
    """ 获取`QQGuild`模式中频道机器人的`appid`以及`token`. """
    configfile = open(path / filename, "r")
    config = yaml.safe_load(configfile.read())
    return config

def change_status(var) -> bool:
    """ 录入新的`status`内容 """
    global status
    status = var
    return True

def load_status_settings():
    """ 导出当前机器人在各群聊的状态 """
    return status

if __name__ == "__main__":
    set_package("?")