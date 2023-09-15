"""
初始化DGI_PROVIDERS与CUSTOM_PROVIDERS数组
"""
import os
import re

from dicergirl.common import const
from multilogging import multilogger
from dicergirl.reply.provider.provider import Provider, CustomProvider

logger = multilogger(name="DicerGirl", payload="ReplyFile")


def init():
    """
        初始化方法
    """
    if not os.path.exists(const.REPLY_FOLDER_PATH):
        os.makedirs(const.REPLY_FOLDER_PATH)
    __init_example_provider()
    __init_provider()


def __init_provider():
    """
    加载reply文件数组中
    """
    for filename in os.listdir(const.REPLY_FOLDER_PATH):
        pattern = re.compile(r'^dg-.*\.yml$')
        file_path = os.path.join(const.REPLY_FOLDER_PATH, filename)
        logger.info(f"载入{filename},完整路径[{file_path}]")
        if os.path.isfile(file_path):
            if pattern.match(filename):
                with (open(file_path, "rb") as file):
                    data = const.REPLY_YAML.load(file)
                    items = data["items"]
                    # logger.info(items)
                    for item in items:
                        for key, value in item.items():
                            const.DG_PROVIDERS.append(
                                Provider(
                                    key=key,
                                    value=value
                                )
                            )
            elif filename.endswith(".yml"):
                with (open(file_path, "rb") as file):
                    data = const.REPLY_YAML.load(file)
                    enable = data["enable"]
                    if not enable:
                        continue
                    items = data["items"]
                    # logger.info(items)
                for item in items:
                    for key, value in item.items():
                        const.CUSTOM_PROVIDERS.append(
                            CustomProvider(
                                key=key,
                                value=value["value"],
                                message=value["message"],
                                matchType=value["matchType"],
                                enable=value["enable"]
                            )
                        )


def __init_example_provider():
    """
    示例文件初始化
    """
    if not os.path.exists(const.EXAMPLE_REPLY_FILE_PATH):
        with open(file=const.EXAMPLE_REPLY_FILE_PATH, mode='wb') as drf:
            raw_data = const.REPLY_YAML.load(const.EXAMPLE_TEMPLATE)
            const.REPLY_YAML.dump(data=raw_data, stream=drf)


# 测试用例
# init()
# for provider in const.DG_PROVIDERS:
#     logger.info(f"Key:{provider.key},Value:{provider.value}")
#
# for provider in const.CUSTOM_PROVIDERS:
#     logger.info(f"Key:{provider.key},Value:{provider.value},Message:{provider.message}MatchType: {provider.matchType},Enable:{provider.enable}")
