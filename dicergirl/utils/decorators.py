# -*- coding: utf-8 -*-
from functools import wraps
from typing import Union

import re

def translate_punctuation(string):
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

    def __call__(self, func):
        @wraps(func)
        async def decorated(*args, **kwargs):
            api = kwargs["api"]
            message = kwargs["message"]
            content = re.sub(self.regex, "", translate_punctuation(message.content.lower())).strip(" ")
            if content.startswith("/"):
                content = "." + content[1:]
            message.content = content
            if isinstance(self.commands, tuple):
                for command in self.commands:
                    if command in content:
                        params = content.split(command)[1].strip()
                        return await func(api=api, message=message, params=params)
            elif self.commands in content:
                params = content.split(self.commands)[1].strip()
                return await func(api=api, message=message, params=params)
            else:
                return False

        return decorated

if __name__ == "__main__":
    chinese_string = "你好，世界！这是一个示例；请问：你是谁？"
    english_string = translate_punctuation(chinese_string)
    print(english_string)
