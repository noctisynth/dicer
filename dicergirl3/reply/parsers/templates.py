"""
该文件用于存储文本中可替换的变量
"""
import datetime


def time() -> str:
    current_time = datetime.datetime.now()
    return current_time.strftime("%H:%M:%S")


def date() -> str:
    current_date = datetime.datetime.now()
    return current_date.strftime("%Y-%m-%d")
