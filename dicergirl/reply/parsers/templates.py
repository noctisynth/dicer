"""
该文件用于存储文本中可替换的变量
"""
import datetime
import string


def time() -> string:
    current_time = datetime.datetime.now()
    return current_time.strftime("%H:%M:%S")


def date() -> string:
    current_date = datetime.datetime.now()
    return current_date.strftime("%Y-%m-%d")
