from pathlib import Path

import sys
import importlib

def modules():
    modules_dict = {}
    sys.path.append(Path(__file__).resolve().parent.parent.__str__())
    for folder in Path(__file__).resolve().parent.parent.iterdir():
        if Path(folder).is_dir() and (Path(folder) / "__init__.py").exists():
            module = importlib.import_module(folder.name)
            print(folder.name)
            if not hasattr(module, "__type__"):
                continue            

            if hasattr(module, "__nbcommands__"):
                commands: dict = module.__nbcommands__
            else:
                commands = {}

            if commands and not hasattr(module, "__nbhandler__"):
                raise ValueError

            handlers = module.__nbhandler__
            for command, handler in commands.items():
                getattr(handlers, command)(getattr(handlers, handler))

            modules_dict[folder.name] = module
    sys.path.pop(-1)
    return modules_dict

modules_dict = modules()
modes = {module.split(".")[-1]: modules_dict[module] for module in modules_dict if hasattr(modules_dict[module], "__type__")}
""" 已导入的跑团模块 """