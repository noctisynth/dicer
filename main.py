import os
import re
import botpy

from dices import help_message, st, en, rd0, ra
from madness import ti, li
from investigator import Investigator
from san_check import sc
from cards import _cachepath, cards, cache_cards, set_handler, show_handler, sa_handler, del_handler
from decorator import Commands

from botpy import logging, BotAPI
from botpy.message import Message
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

def format_msg(message, begin=None):
    pattern = r'([\u4e00-\u9fff]+|\d+)'
    msg = format_str(message, begin=begin)
    msg = re.findall(pattern, msg)
    msg = [x.strip() for x in msg if x.strip()]
    return msg

def format_str(message, begin=None):
    regex = "[<](.*?)[>]"
    msg = re.sub("\s+", " ", re.sub(regex, "", str(message.content).lower())).strip(" ")
    if begin:
        if isinstance(begin, list) or isinstance(begin, tuple):
            for b in begin:
                msg = msg.replace(b, "").lstrip(" ")
        else:
            msg = msg.replace(begin, "").lstrip(" ")
    return msg

@Commands(name=(".test"))
async def testhandler(api, message: Message, params=None):
    _log.info("发送消息:" + str(message.content))
    print(message.__repr__())
    msg = format_msg(message)
    await message.reply(content=str(msg))
    return True

@Commands(name=(".coc", ".gen"))
async def cochandler(api, message: Message, params=None):
    args = format_msg(message, begin=(".coc", ".gen"))
    if len(args) > 1:
        _log.info("指令错误, 驳回.")
        await message.reply(content="错误: 参数超出预计(1需要 但 %d传入), 指令驳回." % len(args))
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


@Commands(name=(".en"))
async def enhandler(api, message: Message, params=None):
    args = format_str(message, begin=".en")
    await message.reply(content="错误: 此功能正在开发中, 暂时无法正常使用.")
    # await message.reply(content=en(args))
    return True


@Commands(name=(".ra"))
async def rahandler(api, message: Message, params=None):
    args = format_msg(message, begin=".ra")
    args = list(filter(None, args))
    await message.reply(content=ra(args, message))
    return True
    

#@Commands(name=(".rh"))
#async def rhcommandhandler(api, message: Message, params=None):
#    """
#    args = str(event.get_message())[3:].strip()
#    uid = event.get_user_id()
#    if args and not("." in args):
#        print("get here")
#        if isinstance(bot, V12Bot):
#            from nonebot.adapters.onebot.v12 import  MessageSegment
#            await bot.send_message(detail_type="private", user_id=uid, message=[MessageSegment.text(rd0(args))])
#        elif isinstance(bot, V11Bot):
#            await bot.send_private_msg(user_id=uid, message=rd0(args))
#    """

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
    await message.reply(content=sc(args, message))


@Commands(name=(".set"))
async def sethandler(api, message: Message, params=None):
    args = format_msg(message, begin=".set")
    await message.reply(content=set_handler(message, args))


@Commands(name=(".sa"))
async def sahandler(api, message: Message, params=None):
    args = format_str(message, begin=".sa")
    await message.reply(content=sa_handler(message, args))


@Commands(name=(".del"))
async def delhandler(api, message: Message, params=None):
    args = format_str(message, begin=".del")
    for msg in del_handler(message, args):
        await message.reply(content=msg)


class OracleClient(botpy.Client):
    async def on_ready(self):
        if not os.path.exists("data"):
            _log.info("[cocdicer] 数据文件夹未建立, 建立它.")
            os.makedirs("data")
        if not os.path.exists(_cachepath):
            _log.info("[cocdicer] 存储文件未建立, 建立它.")
            with open(_cachepath, "w", encoding="utf-8") as f:
                f.write("{}")
        cards.load()

    async def on_at_message_create(self, message: Message):
        # 注册指令handler
        handlers = [
            testhandler,
            rdhelphandler,
            stcommandhandler,
            enhandler,
            #rhcommandhandler,
            rahandler,
            rdcommandhandler,
            cochandler,
            ticommandhandler,
            licommandhandler,
            schandler,
            sethandler,
            showhandler,
            sahandler,
            delhandler
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message, params=None):
                return
            
intents = botpy.Intents(public_guild_messages=True)
client = OracleClient(intents=intents)
client.run(appid=test_config["appid"], token=test_config["token"])

