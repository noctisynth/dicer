from botpy.message import Message
from botpy.types.message import MarkdownPayload
from botpy.api import BotAPI
from botpy.logging import get_logger
from pathlib import Path

from utils.settings import set_package, get_package
set_package("qqguild")

from dicergirl.coc.investigator import Investigator
from dicergirl.coc.coccards import cards, cache_cards, sa_handler
from dicergirl.coc.cocutils import sc, st, at, dam, en, rd0, ra, ti, li, rb, rp

from dicergirl.scp.agent import Agent
from dicergirl.scp.scpcards import scp_cards, scp_cache_cards
from dicergirl.scp.scputils import sra, scp_dam, at as sat

from dicergirl.dnd.adventurer import Adventurer
from dicergirl.dnd.dndcards import dnd_cards, dnd_cache_cards
from dicergirl.dnd.dndutils import dra

from dicergirl.utils.decorators import Commands
from dicergirl.utils.messages import help_message, version
from dicergirl.utils.utils import logger, init, is_super_user, add_super_user, rm_super_user, su_uuid, format_msg, format_str, get_handlers, get_config, modes
from dicergirl.utils.handlers import scp_set_handler, scp_show_handler, scp_del_handler, coc_set_handler, coc_show_handler, coc_del_handler, dnd_set_handler, dnd_show_handler, dnd_del_handler
from dicergirl.utils.chat import chat

import botpy
import logging
import sys

DEBUG = False
current_dir = Path(__file__).resolve().parent
config = get_config()
mode = "scp"

get_logger().setLevel(logging.CRITICAL)
logger.remove()
logger.add(
    sys.stdout,
    level = "INFO"
)
package = get_package()

@Commands(name=(".test"))
async def testhandler(api: BotAPI, message: Message, params=None):
    if not is_super_user(message):
        await message.reply(content="[Oracle] 权限不足, 拒绝执行指令.")
        return True
    logger.debug("发送消息:" + str(message.content))
    logger.debug(message.__repr__())
    msg = format_msg(message)
    if not msg:
        msg = "[]"
    if msg[-1] == "markdown":
        mp = MarkdownPayload(content="#Markdown 消息测试")
        await api.post_message(channel_id=message.channel_id, msg_id=message.id, markdown=mp)
        return True
    await message.reply(content=str(msg))
    return True

@Commands(name=(".debug"))
async def debughandler(api: BotAPI, message: Message, params=None):
    global DEBUG
    args = format_msg(message, begin=".debug")
    if not is_super_user(message):
        await message.reply(content="[Oracle] 权限不足, 拒绝执行指令.")
        return True

    if args:
        logger.debug(args)
        if args[0] == "off":
            DEBUG = False
            get_logger().setLevel(logging.INFO)
            logger.remove()
            logger.add(
                sys.stdout,
                level = "INFO"
            )
            logger.info("[cocdicer] 输出等级设置为 INFO.")
            await message.reply(content="[Oracle] DEBUG 模式已关闭.")
            return True
    else:
        DEBUG = True
        get_logger().setLevel(logging.DEBUG)
        logger.remove()
        logger.add(
            sys.stdout,
            level = "INFO"
        )
        logger.info("[cocdicer] 输出等级设置为 DEBUG.")
        await message.reply(content="[Oracle] DEBUG 模式已启动.")
        return True
    if args[0] == "on":
        DEBUG = True
        get_logger().setLevel(logging.DEBUG)
        logger.remove()
        logger.add(
            sys.stdout,
            level = "INFO"
        )
        logger.info("[cocdicer] 输出等级设置为 DEBUG.")
        await message.reply(content="[Oracle] DEBUG 模式已启动.")
    else:
        await message.reply(content="[Oracle] 错误, 我无法解析你的指令.")
    return True

@Commands(name=(".su", ".sudo"))
async def superuser_handler(api: BotAPI, message: Message, params=None):
    args = format_str(message, begin=(".su", ".sudo"))
    arg = list(filter(None, args.split(" ")))

    if len(arg) >= 1:
        if arg[0].lower() == "exit":
            if not rm_super_user(message):
                await message.reply(content="[Oracle] 你还不是超级管理员, 无法撤销超级管理员身份.")
                return True
            await message.reply(content="[Oracle] 你已撤销超级管理员身份.")
            return True

    if is_super_user(message):
        await message.reply(content="[Oracle] 你已经是超级管理员.")
        return True

    if not args:
        logger.critical(f"超级令牌: {su_uuid}")
        await message.reply(content="[Oracle] 启动超级管理员鉴权, 鉴权令牌已在控制终端展示.")
    else:
        if not args == su_uuid:
            await message.reply(content="[Oracle] 鉴权失败!")
        else:
            add_super_user(message)
            await message.reply(content="[Oracle] 你取得了管理员权限.")
    return True
    
@Commands(name=(".coc"))
async def cochandler(api: BotAPI, message: Message, params=None):
    args = format_msg(message, begin=".coc")
    if len(args) > 1:
        logger.info("指令错误, 驳回.")
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

    if 15 <= args and args < 90:
        cache_cards.update(message, inv.__dict__, save=False)
        await message.reply(content=str(inv.output()))
    return True

@Commands(name=(".scp"))
async def scp_handler(api: BotAPI, message: Message, params=None):
    args = format_msg(message, begin=".scp")
    if len(args) > 1:
        logger.info("指令错误, 驳回.")
        await message.reply(content="[Oracle] 错误: 参数超出预计(1需要 但 %d传入), 指令驳回." % len(args))
        return True

    try:
        if len(args) == 0:
            raise ValueError
        args = int(args[0])
    except ValueError:
        await message.reply(content=f'警告: 参数 {args} 不合法, 使用默认值 20 替代.')
        args = 20

    agt = Agent()
    agt.age_check(args)
    agt.init()
    
    if 15 <= args and args < 90:
        scp_cache_cards.update(message, agt.__dict__, save=False)
        await message.reply(content=str(agt.output()))
    return True

@Commands(name=(".dnd"))
async def dnd_handler(api: BotAPI, message: Message, params=None):
    args = format_msg(message, begin=".dnd")
    if len(args) > 1:
        logger.info("指令错误, 驳回.")
        await message.reply(content="[Oracle] 错误: 参数超出预计(1需要 但 %d传入), 指令驳回." % len(args))
        return True

    try:
        if len(args) == 0:
            raise ValueError
        args = int(args[0])
    except ValueError:
        await message.reply(content=f'警告: 参数 {args} 不合法, 使用默认值 20 替代.')
        args = 20

    adv = Adventurer()
    adv.age_check(args)
    adv.init()
    
    if adv.int[0] <= 8:
        await message.reply(content="[Orcale] 很遗憾, 检定新的冒险者智力不足, 弱智是不允许成为冒险者的, 请重新进行车卡检定.")
        return True

    if 15 <= args and args < 90:
        dnd_cache_cards.update(message, adv.__dict__, save=False)
        await message.reply(content=str(adv.output()))
    return True

@Commands(name=(".show"))
async def showhandler(api: BotAPI, message: Message, params=None):
    args = format_msg(message, begin=(".show", ".display"))
    if not args:
        if mode in modes:
            try:
                sh = eval(f"{mode}_show_handler(message, args)")
            except:
                sh = [f"[Oracle] 错误: 执行指令失败, 疑似该模式不存在该指令."]
        else:
            await message.reply(content="未知的跑团模式.")
            return True

        for msg in sh:
            await message.reply(content=str(msg))
        return True

    if args[0] in modes:
        args.remove(args[0])
        sh = eval(f"{args[0]}_show_handler(message, args)")
    else:
        try:
            sh = eval(f"{mode}_show_handler(message, args)")
        except:
            sh = [f"[Oracle] 错误: 执行指令失败, 疑似该模式不存在该指令."]

    for msg in sh:
        await message.reply(content=str(msg))
    return True

@Commands(name=(".set"))
async def sethandler(api: BotAPI, message: Message, params=None):
    args = format_msg(message, begin=".set")
    if not args:
        args.append(mode)

    if args[0] in modes:
        try:
            now = args[0]
            args.remove(args[0])
            sh = eval(f"{now}_set_handler(message, args)")
        except:
            sh = [f"[Oracle] 错误: 执行指令失败, 疑似该模式不存在该指令."]
    else:
        sh = [f"[Oracle] 错误: 未知的跑团模式."]

    await message.reply(content=sh)
    return True

@Commands(name=(".help", ".h"))
async def rdhelphandler(api: BotAPI, message: Message, params=None):
    args = format_msg(message, begin=(".help", ".h"))
    if args:
        arg = args[0]
    else:
        arg = ""
    await message.reply(content=help_message(arg))
    return True

@Commands(name=(".mode", ".m"))
async def modehandler(api: BotAPI, message: Message, params=None):
    global mode
    args = format_msg(message, begin=(".mode", ".m"))
    if args:
        if args[0].lower() in modes:
            mode = args[0].lower()
            await message.reply(content=f"[Oracle] 已切换到 {mode.upper()} 跑团模式.")
            return True
        else:
            await message.reply(content="[Oracle] 未知的跑团模式, 忽略.")
            await message.reply(content=help_message("mode"))
            return True
    else:
        await message.reply(content=f"[Oracle] 当前的跑团模式为 {mode.upper()}.")
    return True

@Commands(name=(".st"))
async def stcommandhandler(api: BotAPI, message: Message, params=None):
    try:
        await message.reply(content=st())
    except:
        await message.reply(content=help_message("st"))
    return True


@Commands(name=(".at"))
async def attackhandler(api: BotAPI, message: Message, params=None):
    args = format_str(message, begin=(".at", ".attack"))
    if mode == "coc":
        await message.reply(content=at(args, message))
    elif mode == "scp":
        await message.reply(content=sat(args, message))
    return True


@Commands(name=(".dam"))
async def damhandler(api: BotAPI, message: Message, params=None):
    args = format_msg(message, begin=(".dam", ".damage"))
    if mode == "scp":
        sd = scp_dam(args, message)
    elif mode == "coc":
        sd = dam(args, message)
    else:
        await message.reply(content="未知的跑团模式.")
        return True

    await message.reply(content=sd)
    return True


@Commands(name=(".en"))
async def enhandler(api: BotAPI, message: Message, params=None):
    args = format_str(message, begin=".en")
    await message.reply(content=en(args, message))
    return True


@Commands(name=(".ra"))
async def rahandler(api: BotAPI, message: Message, params=None):
    args = format_msg(message, begin=".ra")
    if mode in ["coc", "scp", "dnd"]:
        if mode == "scp":
            await message.reply(content=sra(args, message))
        elif mode == "coc":
            await message.reply(content=ra(args, message))
        elif mode == "dnd":
            await message.reply(content=dra(args, message))
    return True

@Commands(name=(".rh"))
async def rhhandler(api: BotAPI, message: Message, params=None):
    args = format_str(message, begin=".rh")
    await message.reply(content="[Oracle] 暗骰: 命运的齿轮在转动.")
    await api.post_dms(guild_id=message.guild_id, msg_id=message.id, content=rd0(args))

@Commands(name=(".rha"))
async def rhahandler(api: BotAPI, message: Message, params=None):
    args = format_msg(message, begin=".rha")
    await message.reply(content="[Oracle] 暗骰: 命运的骰子在滚动.")
    await api.post_dms(guild_id=message.guild_id, msg_id=message.id, content=ra(args, message))

@Commands(name=(".r"))
async def rdcommandhandler(api: BotAPI, message: Message, params=None):
    args = format_str(message, begin=".r")
    if args[0] == "b":
        args = args[1:]
        await message.reply(content=rb(args))
        return
    if args[0] == "p":
        args = args[1:]
        await message.reply(content=rp(args))
        return
    try:
        await message.reply(content=rd0(args))
    except:
        await message.reply(content=help_message("r"))
    return True


@Commands(name=(".ti"))
async def ticommandhandler(api: BotAPI, message: Message, params=None):
    try:
        await message.reply(content=ti())
    except:
        await message.reply(content=help_message("ti"))
    return True


@Commands(name=(".li"))
async def licommandhandler(api: BotAPI, message: Message, params=None):
    try:
        await message.reply(content=li())
    except:
        await message.reply(content=help_message("li"))
    return True


@Commands(name=(".sc"))
async def schandler(api: BotAPI, message: Message, params=None):
    args = format_str(message, begin=".sc")
    scrs = sc(args, message)

    if isinstance(scrs, list):
        for scr in scrs:
            await message.reply(content=scr)
    else:
        await message.reply(content=scrs)
    return True

@Commands(name=(".sa"))
async def sahandler(api: BotAPI, message: Message, params=None):
    args = format_str(message, begin=".sa")
    await message.reply(content=sa_handler(message, args))

@Commands(name=(".del", ".delete"))
async def delhandler(api: BotAPI, message: Message, params=None):
    args = format_str(message, begin=(".del", ".delete"))
    if mode in modes:
        for msg in eval(f"{mode}_del_handler(message, args)"):
            await message.reply(content=msg)
    return True

@Commands(name=(".chat"))
async def chathandler(api: BotAPI, message: Message, params=None):
    args = format_str(message, begin=".chat")
    if not args:
        await message.reply(content="[Oracle] 空消息是不被允许的.")
        return True
    await message.reply(content=chat(args))
    return True

@Commands(name=(".version", ".v"))
async def versionhandler(api: BotAPI, message: Message, params=None):
    args = format_str(message, begin=(".version", ".v"))
    await message.reply(content=f"欧若可骰娘 版本 {version}, 未知访客版权所有.\nCopyright © 2011-2023 Unknown Visitor. All Rights Reserved.")
    return True

class OracleClient(botpy.Client):
    handlers = get_handlers(__import__(__name__))

    async def on_ready(self):
        global DEBUG
        if DEBUG:
            get_logger().setLevel(logging.DEBUG)
            logger.remove()
            logger.add(
                sys.stdout,
                level = "DEBUG"
            )
            logger.info("DEBUG 模式已启动.")
        init()
        cards.load()
        scp_cards.load()
        dnd_cards.load()
        logger.success("机器人启动成功, 将进行心跳维持链接.")

    async def on_at_message_create(self, message: Message):
        is_command = False
        for handler in self.handlers:
            if await handler(api=self.api, message=message, params=None):
                isbot = "玩家" if message.author.bot == False else "机器人"
                logger.info(f"[dicer] 执行指令: {message.content} 指令来源: {message.channel_id} : {message.author.id} : {message.author.username} : {isbot}")
                is_command = True
                break
        valid = message.content.startswith(".") and len(message.content) >= 2
        if not is_command and valid:
            await message.reply(content="[Oracle] 不是合格的指令, 请检查你的输入.")

    async def on_message_create(self, message: Message):
        is_command = False
        if message.mentions:
            return
        for handler in self.handlers:
            if await handler(api=self.api, message=message, params=None):
                isbot = "玩家" if message.author.bot == False else "机器人"
                logger.info(f"[dicer] 执行指令: {message.content} 指令来源: {message.channel_id} : {message.author.id} : {message.author.username} : {isbot}")
                is_command = True
                break
        valid = message.content.startswith(".") and len(message.content) >= 2
        if not is_command and valid:
            await message.reply(content="[Oracle] 不是合格的指令, 请检查你的输入.")

def main():
    intents = botpy.Intents.all()
    client = OracleClient(intents=intents)
    run = lambda: client.run(appid=config["appid"], token=config["token"])
    logger.info("启动`QQGuild`机器人服务中...")
    run()

if __name__ == "__main__":
    main()
