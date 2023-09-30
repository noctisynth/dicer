from pathlib import Path
from multilogging import multilogger
from ..common.const import PLUGINS_PATH

import sys
import importlib

logger = multilogger(name="Dicer Girl", payload="Plugin")

loaded = False
""" 首次加载标识, 防止nb指令重复注册 """
def modules():
    global loaded
    if loaded:
        return modes

    modes_dict = {}
    library_dict = {}
    sys.path.append(PLUGINS_PATH.__str__())

    for folder in PLUGINS_PATH.iterdir():
        if Path(folder).is_dir() and (Path(folder) / "__init__.py").exists():
            try:
                module = importlib.import_module(folder.name)
            except Exception as error:
                logger.exception(error)
                logger.error(f"插件 {folder.name} 导入失败.")
                continue

            if not hasattr(module, "__type__"):
                continue

            if module.__type__ not in ("plugin", "library"):
                continue
            else:
                if module.__type__ == "plugin":
                    module_type = "插件"
                elif module.__type__ == "library":
                    module_type = "库"

            if hasattr(module, "__nbcommands__"):
                commands: dict = module.__nbcommands__
            else:
                commands = {}

            if commands and not hasattr(module, "__nbhandler__"):
                logger.error(f"{module_type} {folder.name} 配置异常, 导入失败.")
                continue

            if hasattr(module, "__nbhandler__"):
                handlers = module.__nbhandler__
            else:
                handlers = {}

            for command, handler in commands.items():
                try:
                    getattr(handlers, command)(getattr(handlers, handler))
                except AttributeError:
                    logger.error(f"{module_type} {folder.name} 中 Nonebot2 指令配置异常, 导入失败.")
                    continue
                except Exception as error:
                    logger.error("未知错误:")
                    logger.exception(error)

            if module.__type__ == "plugin":
                modes_dict[module.__name__] = module
            elif module.__type__ == "library":
                library_dict[module.__name__] = module
            
            logger.success(f"{module_type} {folder.name.upper()} 导入完成.")

    sys.path.pop(-1)
    loaded = True
    return modes_dict, library_dict

modules_dict, library_dict = modules()

modes: dict = {module.split(".")[-1]: modules_dict[module] for module in modules_dict}
""" 已导入的跑团模块 """
library: dict = {module.split(".")[-1]: library_dict[module] for module in library_dict}