from pathlib import Path
from datetime import datetime
from nonebot.plugin import PluginMetadata
from typing import Dict
from .utils.settings import set_package, get_package
from .utils.multilogging import multilogger

import nonebot

__plugin_meta__ = PluginMetadata(
    name="欧若可骰娘",
    description="完善的可拓展跑团机器人, 支持 COC/DND/SCP 等跑团模式.",
    usage="安装即可使用.",
    type="application",
    homepage="https://gitee.com/unvisitor/dicer",
    supported_adapters={"~onebot.v11"},
)
__author__ = "苏向夜 <fu050409@163.com>"

logger = multilogger(name="Dicer Girl", payload="Nonebot2")
try:
    driver = nonebot.get_driver()
    set_package("nonebot2")
except ValueError:
    set_package("qqguild")

from .utils.utils import version as __version__

import logging
import sys
import random
import re
import asyncio
import json

DEBUG = False
current_dir = Path(__file__).resolve().parent
mode = "scp"
package = get_package()

if package == "nonebot2":
    from .coc.investigator import Investigator
    from .coc.coccards import coc_cards, coc_cache_cards, coc_rolls
    from .coc.cocutils import sc, st, at, coc_dam, coc_en, ra, ti, li, rb, rp

    from .scp.agent import Agent
    from .scp.scpcards import scp_cards, scp_cache_cards
    from .scp.scputils import sra, scp_dam, scp_en, at as sat, deal, begin
    from .scp.attributes import all_alias_dict

    from .dnd.adventurer import Adventurer
    from .dnd.dndcards import dnd_cards, dnd_cache_cards
    from .dnd.dndutils import dra

    from .utils.decorators import Commands, translate_punctuation
    from .utils.messages import help_message, version
    from .utils.utils import init, is_super_user, add_super_user, rm_super_user, su_uuid, format_msg, format_str, modes, get_mentions
    from .utils.utils import get_loggers, loggers, add_logger, log_dir, get_group_id
    from .utils.parser import CommandParser, Commands, Only, Optional, Required
    from .utils.handlers import show_handler, set_handler, del_handler, roll
    from .utils.chat import chat

    from nonebot.rule import Rule
    from nonebot.matcher import Matcher
    from nonebot.plugin import on_startswith, on_message, on
    from nonebot.adapters import Bot as Bot
    from nonebot.adapters.onebot.v11 import Bot as V11Bot
    from nonebot.consts import STARTSWITH_KEY

    if driver._adapters.get("OneBot V12"):
        from nonebot.adapters.onebot.v12 import MessageEvent, GroupMessageEvent, MessageSegment, Event
    else:
        from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, MessageSegment, Event

    class StartswithRule:
        __slots__ = ("msg", "ignorecase")

        def __init__(self, msg, ignorecase=False):
            self.msg = msg
            self.ignorecase = ignorecase

        def __repr__(self) -> str:
            return f"Startswith(msg={self.msg}, ignorecase={self.ignorecase})"

        def __eq__(self, other: object) -> bool:
            return (
                isinstance(other, StartswithRule)
                and frozenset(self.msg) == frozenset(other.msg)
                and self.ignorecase == other.ignorecase
            )

        def __hash__(self) -> int:
            return hash((frozenset(self.msg), self.ignorecase))

        async def __call__(self, event, state) -> bool:
            try:
                text = translate_punctuation(event.get_plaintext()).strip()
            except Exception:
                return False
            if match := re.match(
                f"^(?:{'|'.join(re.escape(prefix) for prefix in self.msg)})",
                text,
                re.IGNORECASE if self.ignorecase else 0,
            ):
                state[STARTSWITH_KEY] = match.group()
                return True
            return False

    def startswith(msg, ignorecase=True):
        if isinstance(msg, str):
            msg = (msg,)

        return Rule(StartswithRule(msg, ignorecase))

    def on_startswith(commands, priority=0, block=True):
        if isinstance(commands, str):
            commands = (commands, )

        if get_package() == "nonebot2":
            return on_message(startswith(commands, True), priority=priority, block=block, _depth=1)
        elif get_package() == "qqguild":
            return Commands(name=commands)

    testcommand = on_startswith(".test", priority=2, block=True)
    debugcommand = on_startswith(".debug", priority=2, block=True)
    superusercommand = on_startswith((".su", ".sudo"), priority=2, block=True)
    botcommand = on_startswith(".bot", priority=1, block=True)
    logcommand = on_startswith(".log", priority=1, block=True)
    loghandlercommand = on_startswith("", priority=1, block=False)
    selflogcommand = on("message_sent", priority=1, block=False)
    coccommand = on_startswith(".coc", priority=1, block=True)
    scpcommand = on_startswith(".scp", priority=1, block=True)
    dndcommand = on_startswith(".dnd", priority=1, block=True)
    showcommand = on_startswith((".show", ".display"), priority=2, block=True)
    setcommand = on_startswith((".set", ".st"), priority=2, block=True)
    helpcommand = on_startswith((".help", ".h"), priority=2, block=True)
    modecommand = on_startswith((".mode", ".m"), priority=2, block=True)
    stcommand = on_startswith(".sht", priority=2, block=True)
    attackcommand = on_startswith((".at", ".attack"), priority=2, block=True)
    damcommand = on_startswith((".dam", ".damage"), priority=2, block=True)
    encommand = on_startswith((".en", ".encourage"), priority=2, block=True)
    racommand = on_startswith(".ra", priority=2, block=True)
    rhcommand = on_startswith(".rh", priority=2, block=True)
    rhacommand = on_startswith(".rha", priority=1, block=True)
    rollcommand = on_startswith((".r", ".roll"), priority=3, block=True)
    ticommand = on_startswith(".ti", priority=2, block=True)
    licommand = on_startswith(".li", priority=2, block=True)
    sccommand = on_startswith(".sc", priority=2, block=True)
    delcommand = on_startswith((".del", ".delete"), priority=2, block=True)
    chatcommand = on_startswith(".chat", priority=2, block=True)
    versioncommand = on_startswith((".version", ".v"), priority=2, block=True)

    @driver.on_startup
    async def _():
        global DEBUG
        logger.info("欧若可骰娘初始化中...")
        if DEBUG:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.remove()
            logger.add(
                sys.stdout,
                level = "DEBUG"
            )
            logger.info("DEBUG 模式已启动.")
        init()
        coc_cards.load()
        scp_cards.load()
        dnd_cards.load()
        logger.success("欧若可骰娘初始化完毕.")

    @testcommand.handle()
    async def testhandler(matcher: Matcher, event: MessageEvent):
        if not is_super_user(event):
            await matcher.send("[Oracle] 权限不足, 拒绝执行测试指令.")
            return

        logger.info("收到消息:" + str(event.get_message()))
        msg = format_msg(event.get_message(), begin=".test")

        if not msg:
            msg = "[]"

        if msg[-1] == "markdown":
            mp = ""
            await matcher.send(group_id=event.group_id, message=mp)
            return

        await matcher.finish(str(msg))


    @debugcommand.handle()
    async def debughandler(matcher: Matcher, event: MessageEvent):
        global DEBUG
        args = format_msg(event.get_message(), begin=".debug")
        if not is_super_user(event):
            await matcher.send("[Oracle] 权限不足, 拒绝执行指令.")
            return

        if args:
            logger.debug(args)
            if args[0] == "off":
                DEBUG = False
                logging.getLogger().setLevel(logging.INFO)
                logger.remove()
                logger.add(
                    sys.stdout,
                    level = "INFO"
                )
                logger.info("[cocdicer] 输出等级设置为 INFO.")
                await matcher.send("[Oracle] DEBUG 模式已关闭.")
                return
        else:
            DEBUG = True
            logging.getLogger().setLevel(logging.DEBUG)
            logger.remove()
            logger.add(
                sys.stdout,
                level = "INFO"
            )
            logger.info("[cocdicer] 输出等级设置为 DEBUG.")
            await matcher.send("[Oracle] DEBUG 模式已启动.")
            return

        if args[0] == "on":
            DEBUG = True
            logging.getLogger().setLevel(logging.DEBUG)
            logger.remove()
            logger.add(
                sys.stdout,
                level = "INFO"
            )
            logger.info("[cocdicer] 输出等级设置为 DEBUG.")
            await matcher.send("[Oracle] DEBUG 模式已启动.")
        else:
            await matcher.send("[Oracle] 错误, 我无法解析你的指令.")

    @superusercommand.handle()
    async def superuser_handler(matcher: Matcher, event: MessageEvent):
        args = format_str(event.get_message(), begin=(".su", ".sudo"))
        arg = list(filter(None, args.split(" ")))

        if len(arg) >= 1:
            if arg[0].lower() == "exit":
                if not rm_super_user(event):
                    await matcher.send("[Oracle] 你还不是超级管理员, 无法撤销超级管理员身份.")
                    return
                await matcher.send("[Oracle] 你已撤销超级管理员身份.")
                return

        if is_super_user(event):
            await matcher.send("[Oracle] 你已经是超级管理员.")
            return

        if not args:
            logger.critical(f"超级令牌: {su_uuid}")
            await matcher.send("[Oracle] 启动超级管理员鉴权, 鉴权令牌已在控制终端展示.")
        else:
            if not args == su_uuid:
                await matcher.send("[Oracle] 鉴权失败!")
            else:
                add_super_user(event)
                await matcher.send("[Oracle] 你取得了管理员权限.")

    @botcommand.handle()
    async def bothandler(bot: V11Bot, matcher: Matcher, event: GroupMessageEvent):
        args = format_msg(event.get_message(), begin=".bot")
        if not is_super_user(event):
            await matcher.send("[Oracle] 你没有管理员权限, 请先执行`.su`开启权限鉴定.")
            return
        if len(args) == 1:
            if args[0] in ["exit", "out", "leave"]:
                print("退出群聊.")
                await matcher.send("[Oracle] 欧若可离开群聊.")
                await bot.set_group_leave(group_id=event.group_id)
            elif args[0] in ["on", "run", "start"]:
                await matcher.send("[Oracle] 我运行在非 systemd 平台上, 我将保持启动.")
            elif args[0] in ["off", "down", "shutdown"]:
                await matcher.send("[Oracle] 我运行在非 systemd 平台上, 我将保持启动.")
            else:
                await matcher.send("[Oracle] 错误的指令.")
        else:
            await matcher.send(help_message("bot"))

    @logcommand.handle()
    async def loghandler(matcher: Matcher, event: Event):
        args = format_msg(event.get_message(), begin=".log")
        commands = CommandParser(
            Commands([
                Only("show"),
                Only("add"),
                Optional("name", str),
                Optional("stop", int),
                Optional("start", int),
                Optional("remove", int)
                ]),
            args=args,
            auto=True
            ).results

        if commands["show"]:
            #if not str(event.group_id) in saved_loggers.keys():
            #    await matcher.send("该群组暂无日志.")
            #    saved_loggers[event.group_id] = {}
            #    return

            gl = get_loggers(event)
            if len(gl) == 0:
                await matcher.send("暂无存储的日志.")
                return

            reply = "该群聊所有日志:\n"
            for i in range(len(gl)):
                reply += f"序列 {i} : {gl[i]}\n"
            reply.strip("\n")

            await matcher.send(reply)
            return

        if commands["add"]:
            if commands["name"]:
                logname = str(log_dir/(commands["name"]+".trpg.log"))
            else:
                logname = str(log_dir/(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".trpg.log"))

            new_logger = multilogger(name="DG Msg Logger", payload="TRPG")
            new_logger.remove()
            new_logger.add(logname, encoding='utf-8', format="{message}", level="INFO")
            if not get_group_id(event) in loggers.keys():
                loggers[get_group_id(event)] = {}

            keys = loggers[get_group_id(event)].keys()
            if len(keys) == 0:
                index = 1
            else:
                index = max(keys) + 1

            loggers[get_group_id(event)][index] = [new_logger, logname]
            if not add_logger(event, logname):
                raise IOError("无法新增日志.")
            await matcher.send(f"[Oracle] 新增日志序列: {index}\n日志文件: {logname}")
            return

        if commands["stop"]:
            if not get_group_id(event) in loggers.keys():
                await matcher.send("该群组从未设置过日志.")
                loggers[get_group_id(event)] = {}
                return

            if not commands["stop"] in loggers[get_group_id(event)]:
                await matcher.send("目标日志不存在.")
                return

            loggers[get_group_id(event)][commands["stop"]][0].remove()
            await matcher.send(f"日志序列 {commands['stop']} 已停止记录.")
            return

        if commands["remove"]:
            gl = get_loggers(event)
            if not get_group_id(event) in loggers.keys():
                await matcher.send("该群组从未设置过日志.")
                loggers[get_group_id(event)] = {}
                return

            #if not commands["remove"] in loggers[get_group_id(event)]:
            #    await matcher.send("目标日志不存在.")
            #    return

            loggers[get_group_id(event)][commands["remove"]][0].remove()
            Path(loggers[get_group_id(event)][commands["remove"]][1]).unlink()
            loggers[get_group_id(event)].pop([commands["remove"]])
            await matcher.send(f"日志序列 {commands['remove']} 已删除.")
            return

        await matcher.send("骰娘日志管理系统, 使用`.help log`指令详细信息.")

    def trpg_log(event):
        if not get_group_id(event) in loggers.keys():
            return

        for log in loggers[get_group_id(event)].keys():
            if isinstance(event, GroupMessageEvent):
                message = event.get_user_id() + ": " + event.get_message()
            elif isinstance(event, Event):
                message = "Oracle: " + event.raw_message
            loggers[get_group_id(event)][log][0].info(message)

    @selflogcommand.handle()
    @loghandlercommand.handle()
    def loggerhandler(event: Event):
        trpg_log(event)

    @coccommand.handle()
    async def cochandler(matcher: Matcher, event: GroupMessageEvent):
        args = format_msg(event.get_message(), begin=".coc", zh_en=True)
        qid = event.get_user_id()
        commands = CommandParser(
            Commands([
                Only("cache", False),
                Optional("set", int),
                Optional("age", int, 20),
                Optional("name", str),
                Optional("sex", str, "女"),
                Optional("roll", int, 1)
                ]),
            args=args,
            auto=True
            ).results
        toroll = commands["roll"]

        if commands["set"]:
            coc_cards.update(event, coc_rolls[qid][commands["set"]], save=True)
            inv = Investigator().load(coc_rolls[qid][commands["set"]])
            await matcher.send(f"使用序列 {commands['set']} 卡:\n{inv.output()}")
            coc_rolls[qid] = {}
            return

        age = commands["age"]
        name = commands["name"]

        if not (15 <= age and age < 90):
            await matcher.send(Investigator().age_change(age))
            return

        reply = ""
        if qid in coc_rolls.keys():
            rolled = len(coc_rolls[qid].keys())
        else:
            coc_rolls[qid] = {}
            rolled = 0

        for i in range(toroll):
            inv = Investigator()
            inv.age_change(age)
            inv.sex = commands["sex"]

            if name:
                inv.name = name

            coc_rolls[qid][rolled+i] = inv.__dict__
            count = inv.rollcount()
            reply += f"天命编号: {rolled+i}\n"
            reply += inv.output() + "\n"
            reply += f"共计: {count[0]}/{count[1]}\n"

        if toroll == 1:
            coc_cache_cards.update(event, inv.__dict__, save=False)

        reply.rstrip("\n")
        await matcher.send(reply)

    @scpcommand.handle()
    async def scp_handler(matcher: Matcher, event: GroupMessageEvent):
        args = format_msg(event.get_message(), begin=".scp", zh_en=True)
        at = get_mentions(event)

        if at and not is_super_user(event):
            return "[Oracle] 权限不足, 无法指定玩家修改人物卡."

        if at:
            qid = at[0]
        else:
            qid = ""

        if len(args) != 0:
            if args[0] in ["begin", "start"]:
                for des in begin():
                    await matcher.send(des)
                    await asyncio.sleep(2)
                return
            elif args[0] in ["level", "levelup", "lu"]:
                agt = Agent().load(scp_cards.get(event, qid=qid))

                if agt.ach >= 10:
                    agt.ach -= 10
                    agt.level += 1
                    scp_cards.update(event, inv_dict=agt.__dict__, save=True)
                    await matcher.send(f"[Oracle] {agt.name} 特工权限提升至 {agt.level} 级.")
                    return
                else:
                    await matcher.send(f"[Oracle] 特工 {agt.name} 功勋不足, 无法申请提升权限等级.")
                    return
            elif args[0] in ["reset", "r"]:
                if not is_super_user(event):
                    await matcher.send("[Oracle] 权限不足, 拒绝执行人物卡重置指令.")
                    return

                agt = Agent().load(scp_cards.get(event, qid=qid))

                if len(args) == 2:
                    try:
                        exec(f"agt.reset_{args[1]}()")
                        scp_cards.update(event, agt.__dict__, qid=qid, save=True)
                        await matcher.send(f"[Oracle] 已重置指定人物卡属性: {args[1]}.")
                    except:
                        await matcher.send("[Oracle] 指令看起来不存在.")
                    finally:
                        return

                agt.reset()
                scp_cards.update(event, agt.__dict__, qid=qid, save=True)
                await matcher.send(f"[Oracle] 人物卡 {agt.name} 属性已重置.")
                return
            elif args[0] in ["upgrade", "u", "up", "study", "learn"]:
                agt = Agent().load(scp_cards.get(event, qid=qid))
                anb = agt.all_not_base()

                if args[1] in all_alias_dict.keys():
                    key_name = all_alias_dict[args[1]]
                    oldattr = getattr(agt, anb[key_name])
                    level = int(oldattr[key_name])

                    if len(args) <= 2:
                        up = level + 1
                    else:
                        try:
                            up = int(args[2])
                        except ValueError:
                            await matcher.send(help_message("scp"))
                            return

                    if level >= up:
                        await matcher.send(f"[Oracle] 你的 {args[1]} 技能的等级已经是 {level} 级了.")
                        return

                    required = int(up * (up + 1) / 2 - level * (level + 1) / 2)
                    if agt.p[anb[key_name]] < required:
                        await matcher.send(f"[Oracle] 你的熟练值不足以支撑你将 {args[1]} 提升到 {up} 级.")
                        return

                    agt.p[anb[key_name]] -= required

                    flt = random.randint(1, 10)

                    if flt == 10:
                        flt = 0

                    oldattr[key_name] = float(up) + flt/10
                    setattr(agt, anb[key_name], oldattr)
                    scp_cards.update(event, agt.__dict__, qid=qid, save=True)
                    await matcher.send(f"[Oracle] 你的 {args[1]} 升级到 {up} 级.\n该技能的熟练度为 {oldattr[key_name]}.")
                    return
                else:
                    await matcher.send(f"[Oracle] 自定义技能 {args[1]} 无法被升级.")
                    return
            elif args[0] in ["deal", "d", "buy", "b"]:
                args_for_deal = args[1:]
                await matcher.send(deal(event, args_for_deal))
                return 
            else:
                await matcher.send(f"[Oracle] 指令 {args[0]} 看起来似乎不存在.")
                return

        agt = Agent()
        agt.init()

        scp_cache_cards.update(event, agt.__dict__, save=False)
        await matcher.send(str(agt.output()))

    @dndcommand.handle()
    async def dnd_handler(matcher: Matcher, event: GroupMessageEvent):
        args = format_msg(event.get_message(), begin=".dnd")
        if len(args) > 1:
            logger.warning("指令错误, 驳回.")
            await matcher.send("[Oracle] 错误: 参数超出预计(1需要 但 %d传入), 指令驳回." % len(args))
            return True

        try:
            if len(args) == 0:
                raise ValueError
            args = int(args[0])
        except ValueError:
            await matcher.send(f'警告: 参数 {args} 不合法, 使用默认值 20 替代.')
            args = 20

        adv = Adventurer()
        adv.age_check(args)
        adv.init()
        
        if adv.int[0] <= 8:
            await matcher.send("[Orcale] 很遗憾, 检定新的冒险者智力不足, 弱智是不允许成为冒险者的, 请重新进行车卡检定.")
            return True

        if 15 <= args and args < 90:
            dnd_cache_cards.update(event, adv.__dict__, save=False)
            await matcher.send(str(adv.output()))
        return True

    @showcommand.handle()
    async def showhandler(matcher: Matcher, event: GroupMessageEvent):
        args = format_msg(event.get_message(), begin=(".show", ".display"))
        at = get_mentions(event)

        if mode in modes:
            try:
                sh = show_handler(event, args, at, mode=mode)
            except Exception as error:
                logger.exception(error)
                sh = [f"[Oracle] 错误: 执行指令失败, 疑似该模式不存在该指令."]
        else:
            await matcher.send("未知的跑团模式.")
            return True

        for msg in sh:
            await matcher.send(str(msg))
        return

    @setcommand.handle()
    async def sethandler(matcher: Matcher, event: GroupMessageEvent):
        args = format_msg(event.get_message(), begin=(".set", ".st"))
        at = get_mentions(event)

        if at and not is_super_user(event):
            await matcher.send("[Oracle] 权限不足, 拒绝执行指令.")
            return

        try:
            sh = set_handler(event, args, at, mode=mode)
        except Exception as error:
            logger.exception(error)
            sh = [f"[Oracle] 错误: 执行指令失败, 疑似模式 {mode} 不存在该指令."]

        await matcher.send(sh)
        return


    @helpcommand.handle()
    async def rdhelphandler(matcher: Matcher, event: MessageEvent):
        args = format_msg(str(event.get_message()), begin=(".help", ".h"))
        if args:
            arg = args[0]
        else:
            arg = ""
        print(arg)
        await matcher.send(help_message(arg))


    @modecommand.handle()
    async def modehandler(matcher: Matcher, event: MessageEvent):
        global mode
        args = format_msg(event.get_message(), begin=(".mode", ".m"))
        if args:
            if args[0].lower() in modes:
                mode = args[0].lower()
                await matcher.send(f"[Oracle] 已切换到 {mode.upper()} 跑团模式.")
                return True
            else:
                await matcher.send("[Oracle] 未知的跑团模式, 忽略.")
                await matcher.send(help_message("mode"))
                return True
        else:
            await matcher.send(f"[Oracle] 当前的跑团模式为 {mode.upper()}.")

    @stcommand.handle()
    async def stcommandhandler(matcher: Matcher, event: GroupMessageEvent):
        try:
            await matcher.send(st())
        except:
            await matcher.send(help_message("st"))


    @attackcommand.handle()
    async def attackhandler(matcher: Matcher, event: GroupMessageEvent):
        args = format_str(event.get_message(), begin=(".at", ".attack"))
        if mode == "coc":
            await matcher.send(at(args, event))
        elif mode == "scp":
            await matcher.send(sat(args, event))


    @damcommand.handle()
    async def damhandler(matcher: Matcher, event: GroupMessageEvent):
        args = format_msg(event.get_message(), begin=(".dam", ".damage"))
        if mode == "scp":
            sd = scp_dam(args, event)
        elif mode == "coc":
            sd = coc_dam(args, event)
        else:
            await matcher.send("未知的跑团模式.")
            return

        await matcher.send(sd)

    @encommand.handle()
    async def enhandler(matcher: Matcher, event: GroupMessageEvent):
        args = format_msg(event.get_message(), begin=".en")
        at = get_mentions(event)

        if at and not is_super_user(event):
            await matcher.send("[Oracle] 权限不足, 拒绝执行指令.")
            return

        try:
            en = eval(f"{mode}_en(event, args)")
        except:
            en = f"[Oracle] 错误: 执行指令失败, 疑似模式 {mode.upper()} 不存在该指令."

        await matcher.send(en)


    @racommand.handle()
    async def rahandler(matcher: Matcher, event: GroupMessageEvent):
        args = format_msg(event.get_message(), begin=".ra")
        if mode in ["coc", "scp", "dnd"]:
            if mode == "scp":
                await matcher.send(str(sra(args, event)))
            elif mode == "coc":
                await matcher.send(str(ra(args, event)))
            elif mode == "dnd":
                await matcher.send(str(dra(args, event)))
        return

    @rhcommand.handle()
    async def rhhandler(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
        args = format_str(event.get_message(), begin=".rh")
        await matcher.send("[Oracle] 暗骰: 命运的骰子在滚动.")
        await bot.send_private_msg(user_id=event.get_user_id(), message=roll(args))

    @rhacommand.handle()
    async def rhahandler(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
        args = format_msg(event.get_message(), begin=".rha")
        await matcher.send("[Oracle] 暗骰: 命运的骰子在滚动.")
        await bot.send_private_msg(user_id=event.get_user_id(), message=ra(args, event))

    @rollcommand.handle()
    async def rollhandler(matcher: Matcher, event: MessageEvent):
        args = format_msg(event.get_message(), begin=(".r", ".roll"))
        if not args:
            await matcher.send(roll(["1", "d", "100"]))
            return

        if args[0] == "b":
            await matcher.send(rb(args[1:]))
            return
        elif args[0] == "p":
            await matcher.send(rp(args[1:]))
            return

        try:
            await matcher.send(roll(args))
        except:
            await matcher.send(help_message("r"))


    @ticommand.handle()
    async def ticommandhandler(matcher: Matcher, event: GroupMessageEvent):
        try:
            await matcher.send(ti())
        except:
            await matcher.send(help_message("ti"))


    @licommand.handle()
    async def licommandhandler(matcher: Matcher, event: GroupMessageEvent):
        try:
            await matcher.send(li())
        except:
            await matcher.send(help_message("li"))


    @sccommand.handle()
    async def schandler(matcher: Matcher, event: GroupMessageEvent):
        args = format_str(event.get_message(), begin=".sc")
        scrs = sc(args, event)

        if isinstance(scrs, list):
            for scr in scrs:
                await matcher.send(scr)
        else:
            await matcher.send(scrs)

    @delcommand.handle()
    async def delhandler(matcher: Matcher, event: GroupMessageEvent):
        args = format_str(event.get_message(), begin=(".del", ".delete"))
        at = get_mentions(event)

        if at and not is_super_user(event):
            await matcher.send("[Oracle] 权限不足, 拒绝执行指令.")
            return

        if mode in modes:
            for msg in del_handler(event, args, at, mode=mode):
                await matcher.send(msg)

    @chatcommand.handle()
    async def chathandler(matcher: Matcher, event: MessageEvent):
        args = format_str(event.get_message(), begin=".chat")
        if not args:
            await matcher.send("[Oracle] 空消息是不被允许的.")
            return
        await matcher.send(chat(args))


    @versioncommand.handle()
    async def versionhandler(matcher: Matcher, event: MessageEvent):
        args = format_str(event.get_message(), begin=(".version", ".v"))
        await matcher.send(f"欧若可骰娘 版本 {version}, 未知访客开发, 以Apache-2.0协议开源.\nCopyright © 2011-2023 Unknown Visitor. Open source as protocol Apache-2.0.")
        return
elif package == "qqguild":
    pass
else:
    logger.critical(f"未知的包模式: {package}!")
    sys.exit()