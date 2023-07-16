from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from botpy import logging, BotAPI
from botpy.message import Message
from botpy.ext.cog_yaml import read
from pathlib import Path

from dices import st, en, rd0, ra, at, dam
from madness import ti, li
from investigator import Investigator
from san_check import sc
from cards import _cachepath, cards, cache_cards, set_handler, show_handler, sa_handler, del_handler
from decorators import Commands, translate_punctuation
from messages import help_message, version

import os
import re
import sys
import botpy
import threading
import time
import importlib
import logging as _logging

DEBUG = False
config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
current_dir = Path(__file__).resolve().parent
_log = logging.get_logger()

def format_msg(message, begin=None):
    msg = format_str(message, begin=begin).split(" ")
    outer = []
    for m in msg:
        m = re.split(r'([\u4e00-\u9fff]+|\d+)', m)
        m = list(filter(None, m))
        outer += m
    msg = outer
    _log.debug(msg)
    msg = list(filter(None, msg))
    _log.debug(msg)
    return msg

def format_str(message, begin=None):
    regex = "[<](.*?)[>]"
    msg = re.sub("\s+", " ", re.sub(regex, "", str(message.content).lower())).strip(" ")
    msg = translate_punctuation(msg)
    _log.debug(msg)
    if begin:
        if isinstance(begin, list) or isinstance(begin, tuple):
            for b in begin:
                msg = msg.replace(b, "").lstrip(" ")
        else:
            msg = msg.replace(begin, "").lstrip(" ")
    _log.debug(msg)
    return msg

@Commands(name=(".test"))
async def testhandler(api, message: Message, params=None):
    _log.debug("发送消息:" + str(message.content))
    _log.debug(message.__repr__())
    msg = format_msg(message)
    await message.reply(content=str(msg))
    return True

@Commands(name=(".debug"))
async def testhandler(api, message: Message, params=None):
    global DEBUG
    DEBUG = True
    _log.setLevel(_logging.DEBUG)
    _log.info("[cocdicer] 输出等级设置为 DEBUG.")
    await message.reply(content="[Oracle] 输出等级设置为DEBUG.")
    return True

@Commands(name=(".coc", ".gen"))
async def cochandler(api, message: Message, params=None):
    args = format_msg(message, begin=(".coc", ".gen"))
    if len(args) > 1:
        _log.info("指令错误, 驳回.")
        await message.reply(content="[Oracle] 错误: 参数超出预计(1需要 但 %d传入), 指令驳回." % len(args))
        return False
    try:
        if len(args) == 0:
            raise ValueError
        args = int(args[0])
    except ValueError:
        await message.reply(content=f'警告: 参数 {args} 不合法, 使用默认值 20 替代.')
        args = 20
    inv = Investigator()
    await message.reply(content=inv.age_change(args))
    if 15 <= args < 90:
        cache_cards.update(message, inv.__dict__, save=False)
        await message.reply(content=str(inv.output()))
    return True

@Commands(name=(".show", ".display"))
async def showhandler(api, message: Message, params=None):
    args = format_msg(message, begin=(".show", ".display"))
    sh = show_handler(message, args)
    for msg in sh:
        await message.reply(content=str(msg))
    return True


@Commands(name=(".help", ".h"))
async def rdhelphandler(api, message: Message, params=None):
    args = format_msg(message, begin=(".help", ".h"))
    if args:
        arg = args[0]
    else:
        arg = None
    await message.reply(content=help_message(arg))
    return True


@Commands(name=(".st"))
async def stcommandhandler(api, message: Message, params=None):
    await message.reply(content=st())
    return True


@Commands(name=(".at"))
async def attackhandler(api, message: Message, params=None):
    args = format_msg(message, begin=(".at", ".attack"))
    await message.reply(content=at(args))
    return True


@Commands(name=(".dam"))
async def damhandler(api, message: Message, params=None):
    args = format_str(message, begin=(".dam", ".damage"))
    await message.reply(content=dam(args, message))
    return True


@Commands(name=(".en"))
async def enhandler(api, message: Message, params=None):
    args = format_str(message, begin=".en")
    await message.reply(content=en(args, message))
    return True


@Commands(name=(".ra"))
async def rahandler(api, message: Message, params=None):
    args = format_msg(message, begin=".ra")
    await message.reply(content=ra(args, message))
    return True


@Commands(name=(".r"))
async def rdcommandhandler(api, message: Message, params=None):
    args = format_str(message, begin=".r")
    args = args.strip(".r")
    if args and not("." in args):
        await message.reply(content=rd0(args))
    return True


@Commands(name=(".ti"))
async def ticommandhandler(api, message: Message, params=None):
    await message.reply(content=ti())


@Commands(name=(".li"))
async def licommandhandler(api, message: Message, params=None):
    await message.reply(content=li())


@Commands(name=(".sc"))
async def schandler(api, message: Message, params=None):
    args = format_str(message, begin=".sc")
    scrs = sc(args, message)
    if isinstance(scrs, list):
        for scr in scrs:
            await message.reply(content=scr)
    else:
        await message.reply(content=scrs)


@Commands(name=(".set"))
async def sethandler(api, message: Message, params=None):
    args = format_msg(message, begin=".set")
    await message.reply(content=set_handler(message, args))
    return True

@Commands(name=(".sa"))
async def sahandler(api, message: Message, params=None):
    args = format_str(message, begin=".sa")
    await message.reply(content=sa_handler(message, args))

@Commands(name=(".del", ".delete"))
async def delhandler(api, message: Message, params=None):
    args = format_str(message, begin=(".del", ".delete"))
    for msg in del_handler(message, args):
        await message.reply(content=msg)
    return True

@Commands(name=(".version", ".v"))
async def versionhandler(api, message: Message, params=None):
    args = format_str(message, begin=(".version", ".v"))
    await message.reply(content=f"欧若可骰娘 Version {version}")
    return True

class OracleClient(botpy.Client):
    async def on_ready(self):
        if not current_dir / "data":
            _log.info("[cocdicer] 数据文件夹未建立, 建立它.")
            os.makedirs("data")
        if not os.path.exists(_cachepath):
            _log.info("[cocdicer] 存储文件未建立, 建立它.")
            with open(_cachepath, "w", encoding="utf-8") as f:
                f.write("{}")
        cards.load()

    async def on_at_message_create(self, message: Message):
        handlers = [
            testhandler,
            rdhelphandler,
            stcommandhandler,
            enhandler,
            attackhandler,
            damhandler,
            rahandler,
            rdcommandhandler,
            cochandler,
            ticommandhandler,
            licommandhandler,
            schandler,
            delhandler,
            sethandler,
            showhandler,
            sahandler,
            versionhandler
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message, params=None):
                return

class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self):
        super(FileModifiedHandler, self).__init__()
        self.is_modified = False
        self.modified_module = None

    def on_modified(self, event):
        if not event.is_directory:
            path = os.path.basename(event.src_path)
            split = path.split(".")
            module = split[0]
            if len(split) == 1:
                return
            if split[1] == "py":
                self.is_modified = True
                self.modified_module = module

def reload_module(module_name):
    modules = {
        "cards": [
            "expr",
            "_cachepath",
            "cards",
            "cache_cards",
            "set_handler",
            "show_handler",
            "sa_handler",
            "del_handler"
        ],
        "decorators": [
            "Commands",
            "translate_punctuation"
        ],
        "san_check": ["sc"],
        "investigator": ["Investigator"],
        "dices": [
            "st",
            "en",
            "rd0",
            "ra",
            "at",
            "dam"
        ],
        "madness": ["ti", "li"],
        "messages": [
            "help_message",
            "version"
        ]
    }
    for module in modules:
        if module_name == module:
            _log.info(f"[cocdicer] 模块 {module_name} 被修改了, 重新加载负载模块.")
            funcs = modules[module]
            tmodule = sys.modules[module_name]
            im = importlib.reload(tmodule)
            for func in funcs:
                globals()[func] = eval(f"im.{func}")
                if func == "cards":
                    _log.info("[cocdicer] 人物卡模块被修改, 重新加载.")
                    globals()[func].load()
            _log.info(f"[cocdicer] 负载模块重载完成.")
            break

def monitor_folder(folder_path, target=None):
    thread = threading.Thread(target=target)
    thread.daemon = True

    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()
    _log.info("[cocdicer] 文件监视器已启动.")

    thread.start()
    _log.info("[cocdicer] QQBot信息监视器已启动.")

    try:
        while True:
            if event_handler.is_modified:
                event_handler.is_modified = False
                module = event_handler.modified_module
                if module != "main":
                    reload_module(module)
                if target != None:
                    if thread.is_alive():
                        continue
                    _log.info("[cocdicer] 主线程已终止, 重启中.")
                    thread = threading.Thread(target=target)
                    thread.daemon = True
                    thread.start()
                else:
                    raise ValueError("监视线程未传入.")
            time.sleep(0.1)
    except KeyboardInterrupt as kbi:
        _log.info("[cocdicer] 用户要求结束线程.")
        exit()

def main():
    intents = botpy.Intents(public_guild_messages=True)
    client = OracleClient(intents=intents)
    run = lambda: client.run(appid=config["appid"], token=config["token"])
    monitor_folder(current_dir, target=run)

if __name__ == "__main__":
    main()