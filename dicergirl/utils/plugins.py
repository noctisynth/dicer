from .. import coc, scp, dnd
import sys

modes = {module.split(".")[-1]: sys.modules[module] for module in sys.modules if hasattr(sys.modules[module], "__type__")}
""" 已导入的跑团模块 """