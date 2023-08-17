# -*- coding: utf-8 -*-
from functools import wraps
from typing import Union
try:
    from .settings import get_package
except ImportError:
    from dicergirl.utils.settings import get_package

import re

qqguild_handlers = []

def translate_punctuation(string) -> str:
    punctuation_mapping = {
        '，': ',',
        '。': '.',
        '！': '!',
        '？': '?',
        '；': ';',
        '：': ':',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '（': '(',
        '）': ')',
        '【': '[',
        '】': ']',
        '《': '<',
        '》': '>',
    }
    for ch_punct, en_punct in punctuation_mapping.items():
        string = string.replace(ch_punct, en_punct)
    return string

class Commands:
    def __init__(self, name: Union[tuple, str]):
        self.commands = name
        self.regex = "[<](.*?)[>]"
    
    def _handle(self, func):
        qqguild_handlers.append(func)
        @wraps(func)
        async def decorated(*args, **kwargs):
            if get_package() == "nonebot2":
                kwargs["begin"] = self.commands
                return await func(*args, **kwargs)

            content = re.sub(self.regex, "", translate_punctuation(kwargs["message"].content.lower())).strip(" ")
            if content.startswith("/"):
                content = "." + content[1:]
            kwargs["message"].content = content
            if isinstance(self.commands, tuple):
                for command in self.commands:
                    if command in content:
                        return await func(*args, **kwargs)
            elif self.commands in content:
                return await func(*args, **kwargs)
            else:
                return False
        return decorated

    def handle(self):
        return self._handle

if __name__ == "__main__":
    chinese_string = "你好，世界！这是一个示例；请问：你是谁？"
    english_string = translate_punctuation(chinese_string)
    print(english_string)
