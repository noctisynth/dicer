"""
存放常量的文件
"""
import pathlib

from dicergirl.reply.parser import default_templates
from dicergirl.reply.provider.provider import Provider, CustomProvider


def load_template_methods():
    """
    获取 default_templates.py 中的所有方法
    """
    methods = {}
    for name, method in vars(default_templates).items():
        if callable(method):
            methods[name] = method
    return methods


# 占位符对应的方法列表
TEMPLATE_METHODS = load_template_methods()
# Provider列表
DGI_PROVIDERS: list[Provider] = []
CUSTOM_PROVIDERS: list[CustomProvider] = []
# 家目录
HOME_PATH = pathlib.Path.home()
# dgi配置存放路径
CONFIG_PATH = f"{HOME_PATH}\\.config\\dgi"
# dgi回复配置存放路径
REPLY_FILE_PATH = f"{CONFIG_PATH}\\reply"
# 示例自定义回复文件
EXAMPLE_REPLY_FILE_PATH = f"{REPLY_FILE_PATH}\\example.yml"
# 示例模板
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
