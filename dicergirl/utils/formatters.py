from typing import List
from dicergirl.common.decorators import translate_punctuation
from multilogging import multilogger

import re


logger = multilogger(name="DicerGirl", payload="utils.cards")
""" `utils.cards`日志 """


def format_str(message: str, begin=None, lower=True) -> str:
    """ 骰娘指令转义及解析 """
    regex = r"[<\[](.*?)[\]>]"
    message = str(message).lower() if lower else str(message)
    msg = re.sub("\s+", " ", re.sub(regex, "", message)).strip(" ")
    msg = translate_punctuation(msg)
    logger.debug(msg)

    if begin:
        if isinstance(begin, str):
            begin = [begin, ]
        elif isinstance(begin, tuple):
            begin = list(begin)

        begin.sort(reverse=True)
        for b in begin:
            msg = msg.replace(b, "").lstrip(" ")

    logger.debug(msg)
    return msg


def format_msg(message, begin=None, zh_en=True) -> List[str]:
    """ 骰娘指令拆析为`list`的方法 """
    msgs = format_str(message, begin=begin)
    outer = []
    regex = r'([+-]?\d+)|("[^"]+")|([a-zA-Z\u4e00-\u9fa5]+)' if not zh_en else r'([+-]?\d+)|([a-zA-Z]+)|("[^"]+")|([\u4e00-\u9fa5]+)'
    msgs = list(filter(None, re.split(regex, msgs)))
    logger.debug(msgs)

    for msg in msgs:
        splited_msg = list(filter(None, re.split(regex, msg.strip(" "))))

        for i, msg in enumerate(splited_msg):
            splited_msg[i] = msg.strip('"')

        outer += splited_msg

    msgs = list(filter(None, outer))
    logger.debug(msgs)
    return msgs