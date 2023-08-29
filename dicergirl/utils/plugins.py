from pathlib import Path
from multilogging import multilogger

import sys
import importlib

logger = multilogger(name="Dicer Girl", payload="Plugin")

loaded = False
""" 首次加载标识, 防止nb指令重复注册 """
def modules():
    global loaded
    if loaded:
        return modes

    modules_dict = {}
    sys.path.append(Path(__file__).resolve().parent.parent.__str__())
    for folder in Path(__file__).resolve().parent.parent.iterdir():
        if Path(folder).is_dir() and (Path(folder) / "__init__.py").exists():
            try:
                module = importlib.import_module(folder.name)
            except Exception as error:
                logger.exception(error)
                logger.error(f"插件 {folder.name} 导入失败.")

            if not hasattr(module, "__type__"):
                continue

            if module.__type__ != "plugin":
                continue

            if hasattr(module, "__nbcommands__"):
                commands: dict = module.__nbcommands__
            else:
                commands = {}

            if commands and not hasattr(module, "__nbhandler__"):
                logger.error(f"插件 {folder.name} 配置异常, 导入失败.")
                continue

            handlers = module.__nbhandler__
            for command, handler in commands.items():
                try:
                    getattr(handlers, command)(getattr(handlers, handler))
                except AttributeError:
                    logger.error(f"插件 {folder.name} 中 Nonebot2 指令配置异常, 导入失败.")
                    continue
                except Exception as error:
                    logger.error("未知错误:")
                    logger.exception(error)

            modules_dict[module.__name__] = module
            logger.success(f"插件 {folder.name.upper()} 导入完成.")
    sys.path.pop(-1)
    loaded = True
    return modules_dict

modules_dict = modules()
modes: dict = {module.split(".")[-1]: modules_dict[module] for module in modules_dict}
""" 已导入的跑团模块 """