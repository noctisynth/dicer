from loguru import logger
from pathlib import Path

import sys
import yaml

package = "qqguild"
allowed_packages = ["nonebot2", "qqguild"]

def set_package(pkg: str):
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

def setconfig(appid, token, path=Path.home()/".dicergirl", filename="config.yaml"):
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
    configfile = open(path / filename, "r")
    config = yaml.safe_load(configfile.read())
    return config

if __name__ == "__main__":
    set_package("?")