"""
存放常量的文件
"""
import inspect
import pathlib

from ruamel.yaml import YAML
from dicergirl.reply.parser import templates
from dicergirl.reply.provider.provider import Provider, CustomProvider


def load_template_methods():
    """
    获取 templates.py 中的所有方法
    """
    methods = {}
    for name, method in vars(templates).items():
        if callable(method) and not inspect.signature(method).parameters:
            methods[name] = method
    return methods


REPLY_YAML = YAML()
""" ruamel.yaml的YAML对象实例化 """
TEMPLATE_METHODS = load_template_methods()
""" 占位符对应的方法列表 """
HARDCODED_PROVIDERS: list[Provider] = []
""" Provider 列表 """
KEYWORD_PROVIDERS: list[CustomProvider] = []
""" 自定义 Provider """
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
enable: false
# 作者
author: "佚名"
# 自定义规则列表
items: 
    - default.example:
        # 是否启用
        enable: true
        # 匹配字段
        value: "笨蛋！"
        # 发送内容
        message: "不许说笨蛋！"
        # EXACT_MATCH(完全匹配),PARTIAL_MATCH(部分匹配),REGEX_MATCH(正则匹配),FUNCTION_MATCH(方法匹配)
        matchType: EXACT_MATCH 
# 版本号
version: 1.0
# 自定义功能描述
description: "示例模板"
"""