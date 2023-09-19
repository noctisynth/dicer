"""
存放常量的文件
"""
import pathlib

from ruamel.yaml import YAML

REPLY_YAML = YAML()
""" ruamel.yaml的YAML对象实例化 """
HOME_PATH = pathlib.Path.home()
""" 主目录 """
DG_FOLDER_PATH = HOME_PATH / ".dicergirl"
""" DicerGirl 数据文件夹路径 """
REPLY_FOLDER_PATH = DG_FOLDER_PATH / "reply"
""" Dicergirl 自定义回复文件夹路径 """
EXAMPLE_REPLY_FILE_PATH = REPLY_FOLDER_PATH / "example.yml"
""" 示例自定义回复文件路径 """
IS_ONE_TIME_MATCH = False
""" 自定义是否只匹配一次 """

EXAMPLE_TEMPLATE = """\
# 是否启用
enable: true
# 作者
author: "佚名"
# 自定义规则列表
items: 
    - default.example:
        # 是否启用
        enable: true
        # 发送内容
        send_text: "你好，现在是北京时间{time}！"
        # 匹配字段
        match_field: "/example time"
        # EXACT_MATCH(完全匹配),PARTIAL_MATCH(部分匹配),REGEX_MATCH(正则匹配),FUNCTION_MATCH(方法匹配)
        match_type: EXACT_MATCH 
# 版本号
version: 1.0
# 自定义功能描述
description: "示例模板"
"""