"""
存放常量的文件
"""
from pathlib import Path
from typing import Any, Dict

from ruamel.yaml import YAML

EMPTY_CHAR = ""
EMPTY_ARRAY = []
EMPTY_DICT = {}
NONE = None


VERSION = "3.4.0"
""" Dicer Girl 版本号 """
HOME_PATH = Path.home()
""" 主目录 """
DICERGIRL_DATA_PATH = HOME_PATH / ".dicergirl"
""" DicerGirl 数据文件夹路径 """
CURRENT_DIR = Path(__file__).resolve().parent
""" Dicer Girl 当前目录 """
SAVED_DATA_PATH = DICERGIRL_DATA_PATH / "data"
""" 人物卡数据存储文件夹 """
DICERGIRL_LOGS_PATH = DICERGIRL_DATA_PATH / "log"
""" 日志数据存储文件夹 """
BOT_STATUS_FILE = SAVED_DATA_PATH / "status.json"
""" 机器人启用状态存储文件 """
SUPERUSER_FILE = SAVED_DATA_PATH / "super_user.json"
""" 管理员鉴权文件 """
LOGGERS_CACHE_FILE = SAVED_DATA_PATH / "loggers.json"
""" 日志信息存储文件 """
BOT_MODES_FILE = SAVED_DATA_PATH / "modes.json"
""" 跑团模式存储文件 """
BLACKLIST_FILE = SAVED_DATA_PATH / "blacklist.yml"
""" 黑名单存储文件 """
DEFAULT_GROUP_NAME = "default"
""" 默认消息事件组名 """
REPLY_YAML = YAML()
""" `ruamel.yaml`的YAML对象实例化 """
REPLY_FOLDER_PATH = DICERGIRL_DATA_PATH / "reply"
""" DicerGirl 自定义回复文件夹路径 """
GENERIC_REPLY_FILE_PATH = REPLY_FOLDER_PATH / "dg-default.yml"
""" 自定义通用回复配置文件默认路径 """
CONDITION_SPECIFIC_REPLY_FILE_PATH = REPLY_FOLDER_PATH / "default.yml"
""" 特定条件下回复配置文件默认路径 """
EXAMPLE_CONDITION_SPECIFIC_REPLY_FILE_PATH = REPLY_FOLDER_PATH / "example.yml"
""" 特定条件下回复的示例配置文件路径 """
IS_ONE_TIME_MATCH = False
""" 自定义是否只匹配一次 """
GENERIC_REPLY_FILE_CACHE: Dict[str, Any] = {}
""" 自定义通用回复配置文件缓存 """
CONDITION_SPECIFIC_REPLY_FILE_CACHE: Dict[str, Any] = {}
""" 特定条件下回复配置文件缓存 """
CUSTOM_GENERIC_TEMPLATE = """\
enable: true
author: "默认"
# 版本号
version: 1.0
# 自定义功能描述
description: "默认文件"
# 自定义规则列表
items: []
"""
CONDITION_SPECIFIC_TEMPLATE = """\
enable: true
author: "默认"
# 版本号
version: 1.0
# 自定义功能描述
description: "默认文件"
# 自定义规则列表
items: []
"""
EXAMPLE_CONDITION_SPECIFIC_TEMPLATE = """\
# 是否启用
enable: true
# 作者
author: "佚名"
# 版本号
version: 1.0
# 自定义功能描述
description: "示例模板"
# 自定义规则列表
items: 
    - default.example:
        # 是否启用
        enable: false
        # 发送内容
        send_text: "你好，现在是北京时间{time}！"
        # 匹配字段
        match_field: "/example time"
        # EXACT_MATCH(完全匹配),PARTIAL_MATCH(部分匹配),REGEX_MATCH(正则匹配),FUNCTION_MATCH(方法匹配)
        match_type: EXACT_MATCH 
"""