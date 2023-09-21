from pathlib import Path
from datetime import datetime
from multilogging import multilogger

from .reply.manager import manager

from .utils.utils import (
    version, init, on_startswith,
    get_group_id, get_mentions, get_user_card,
    is_super_user, add_super_user, rm_super_user, make_uuid, get_uuid,
    format_msg, format_str,
    get_mode, set_mode,
    get_loggers, loggers, add_logger, remove_logger, log_dir,
    get_status, boton, botoff, set_name, get_name,
    rolekp, roleob,
    run_shell_command, get_latest_version
)
from .utils.plugins import modes
from .utils.parser import CommandParser, Commands, Only, Optional, Required, Positional
from .utils.cards import Cards
from .utils.chat import chat

from .handlers.general import show_handler, set_handler, del_handler, roll, shoot

from .plugins.parse import get_plugins
from .plugins.operation import install, remove, upgrade as plgupgrade
from .errors.pluginerror import PluginExistsError, PluginInstallFailedError, PluginNotFoundError, PluginUninstallFailedError

from .common.messages import help_message
from .common.registers import regist_all

from nonebot.matcher import Matcher
from nonebot.plugin import on, PluginMetadata
from nonebot.adapters import Bot as Bot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.internal.matcher.matcher import Matcher

import logging
import sys
import platform
import psutil
import html
import nonebot
import re
import json

__version__ = version
__plugin_meta__ = PluginMetadata(
    name="DicerGirl",
    description="新一代跨平台开源 TRPG 骰娘框架",
    usage="开箱即用",
    type="application",
    homepage="https://gitee.com/unvisitor/dicer",
    supported_adapters={"~onebot.v11"},
)
__author__ = "苏向夜 <fu050409@163.com>"

DEBUG = False
logger = multilogger(name="Dicer Girl", payload="Nonebot2")
current_dir = Path(__file__).resolve().parent

try:
    driver = nonebot.get_driver()
    initalized = True
except ValueError:
    initalized = False

if initalized:
    if driver._adapters.get("OneBot V12"):
        from nonebot.adapters.onebot.v12 import MessageEvent, GroupMessageEvent, Event, MessageSegment
    else:
        from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Event, MessageSegment

    # 指令装饰器实例化
    testcommand = on_startswith(".test", priority=2, block=True)
    debugcommand = on_startswith(".debug", priority=2, block=True)
    superusercommand = on_startswith((".su", ".sudo"), priority=2, block=True)
    botcommand = on_startswith(".bot", priority=1, block=True)
    logcommand = on_startswith(".log", priority=1, block=True)
    messagemonitor = on_startswith("", priority=1, block=False)
    selflogcommand = on("message_sent", priority=1, block=False)
    showcommand = on_startswith((".show", ".display"), priority=2, block=True)
    setcommand = on_startswith((".set", ".st"), priority=2, block=True)
    helpcommand = on_startswith((".help", ".h"), priority=2, block=True)
    modecommand = on_startswith((".mode", ".m"), priority=2, block=True)
    shootcommand = on_startswith((".sht", ".shoot"), priority=2, block=True)
    attackcommand = on_startswith((".at", ".attack"), priority=2, block=True)
    damcommand = on_startswith((".dam", ".damage"), priority=2, block=True)
    encommand = on_startswith((".en", ".encourage"), priority=2, block=True)
    racommand = on_startswith(".ra", priority=2, block=True)
    rhcommand = on_startswith(".rh", priority=2, block=True)
    rhacommand = on_startswith(".rha", priority=1, block=True)
    rollcommand = on_startswith((".r", ".roll"), priority=3, block=True)
    delcommand = on_startswith((".del", ".delete"), priority=2, block=True)
    rolekpcommand = on_startswith(".kp", priority=2, block=True)
    roleobcommand = on_startswith(".ob", priority=2, block=True)
    sncommand = on_startswith(".sn", priority=2, block=True)
    registcommand = on_startswith((".regist", ".reg"), priority=2, block=True)
    chatcommand = on_startswith(".chat", priority=2, block=True)
    versioncommand = on_startswith((".version", ".v"), priority=2, block=True)

    # 定时任务
    scheduler = nonebot.require("nonebot_plugin_apscheduler").scheduler

    @driver.on_startup
    async def _() -> None:
        """ `Nonebot2`核心加载完成后的初始化方法 """
        global DEBUG
        logger.info(f"DicerGirl 版本 {version} 初始化中...")
        if DEBUG:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.remove()
            logger.add(
                sys.stdout,
                level = "DEBUG"
            )
            logger.info("DEBUG 模式已启动.")
        regist_all()
        init()
        logger.success("DicerGirl 初始化完毕.")

    @testcommand.handle()
    async def testhandler(matcher: Matcher, event: MessageEvent):
        """ 测试指令 """
        args = format_msg(event.get_message(), begin=".test")
        cp = CommandParser(
            Commands([
                Only("all"),
                Only("split"),
                Only("markdown")
            ]),
            args=args,
            auto=True
        )

        if not is_super_user(event):
            await matcher.send(manager.process_generic_event(
                "PermissionDenied",
                event=event
            ))
            return

        reply = ""
        if cp.nothing or cp.results["all"]:
            import json
            reply += f"收到消息: {event.get_message()}\n"
            reply += f"消息来源: {event.group_id} - {event.get_user_id()}\n"
            reply += f"消息拆析: {args}\n"
            reply += f"指令拆析: {cp.results}\n"
            reply += f"消息原始内容: {event.get_plaintext()}\n"
            reply += f"消息json数据: {event.json()}\n"
            reply += f"消息发送者json信息: {json.loads(event.json())['sender']}\n"
            reply += f"发送者昵称: {json.loads(event.json())['sender']['nickname']}"
            await matcher.send(reply)
            return

        logger.debug("收到消息:" + str(event.get_message()))

        if not msg:
            msg = "[]"

        if msg[-1] == "markdown":
            mp = ""
            await matcher.send(group_id=event.group_id, message=mp)
            return

        await matcher.send(None)

    @debugcommand.handle()
    async def debughandler(matcher: Matcher, event: MessageEvent):
        """ 漏洞检测指令 """
        global DEBUG
        args = format_msg(event.get_message(), begin=".debug")
        if not is_super_user(event):
            await matcher.send(manager.process_generic_event(
                "PermissionDenied",
                event=event
            ))
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
                logger.info("输出等级设置为 INFO.")
                await matcher.send(manager.process_generic_event(
                    "DebugOff",
                    event=event
                ))
                return
        else:
            DEBUG = True
            logging.getLogger().setLevel(logging.DEBUG)
            logger.remove()
            logger.add(
                sys.stdout,
                level = "INFO"
            )
            logger.info("输出等级设置为 DEBUG.")
            await matcher.send(manager.process_generic_event(
                "DebugOn",
                event=event
            ))
            return

        if args[0] == "on":
            DEBUG = True
            logging.getLogger().setLevel(logging.DEBUG)
            logger.remove()
            logger.add(
                sys.stdout,
                level = "INFO"
            )
            logger.info("输出等级设置为 DEBUG.")
            await matcher.send(manager.process_generic_event(
                "DebugOn",
                event=event
            ))
        else:
            await matcher.send("错误, 我无法解析你的指令.")

    @superusercommand.handle()
    async def superuser_handler(matcher: Matcher, event: MessageEvent):
        """ 超级用户管理指令 """
        args = format_str(event.get_message(), begin=(".su", ".sudo"))
        arg = list(filter(None, args.split(" ")))

        if len(arg) >= 1:
            if arg[0].lower() == "exit":
                if not rm_super_user(event):
                    await matcher.send(manager.process_generic_event(
                        "NotManagerYet",
                        event=event
                    ))
                    return

                await matcher.send(manager.process_generic_event(
                    "ManagerExit",
                    event=event
                ))
                return

        if is_super_user(event):
            await matcher.send(manager.process_generic_event(
                "AlreadyManager",
                event=event
            ))
            return

        if not args:
            logger.critical(f"超级令牌: {make_uuid()}")
            await matcher.send(manager.process_generic_event(
                "AuthenticateStarted",
                event=event
            ))
        else:
            if not args == get_uuid():
                await matcher.send(manager.process_generic_event(
                    "AuthenticateFailed",
                    event=event
                ))
                add_super_user(event)
                await matcher.send(manager.process_generic_event(
                    "AuthenticateSuccess",
                    event=event
                ))

    @botcommand.handle()
    async def bothandler(bot: V11Bot, matcher: Matcher, event: MessageEvent):
        """ 机器人管理指令 """
        if get_mentions(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=".bot", zh_en=True)
        commands = CommandParser(
            Commands([
                Only(("version", "v", "bot", "版本")),
                Only(("exit", "bye", "leave", "离开")),
                Only(("on", "run", "start", "启动")),
                Only(("off", "down", "shutdown", "关闭")),
                Only(("upgrade", "up", "更新")),
                Optional(("downgrade", "降级"), str),
                Optional(("name", "命名"), str),
                Only(("status", "状态")),
                Optional(("plgup", "pluginup", "升级"), str),
                Optional(("install", "add", "安装"), str),
                Optional(("remove", "del", "rm", "删除", "卸载"), str),
                Only(("mode", "list", "已安装")),
                Only(("store", "plugins", "商店")),
                Optional(("search", "搜索"), str)
            ]),
            args=args,
            auto=True
        )

        if commands.nothing or commands.results["version"]:
            return await versionhandler(matcher=matcher)
        else:
            commands = commands.results

        if commands["exit"]:
            logger.info(f"{get_name()}退出群聊: {event.group_id}")
            await matcher.send(manager.process_generic_event(
                "GroupLeaveSet",
                event=event
            ))
            await bot.set_group_leave(group_id=event.group_id)
            return

        if commands["on"]:
            boton(event)
            await matcher.send(manager.process_generic_event(
                "BotOn",
                event=event
            ))
            return

        if commands["off"]:
            botoff(event)
            await matcher.send(manager.process_generic_event(
                "BotOff",
                event=event
            ))
            return

        if commands["status"]:
            try:
                system = platform.freedesktop_os_release()["PRETTY_NAME"]
            except:
                system = platform.platform()

            memi = psutil.Process().memory_info()
            rss = memi.rss / 1024 / 1024
            total = psutil.virtual_memory().total / 1024 / 1024

            reply = f"DicerGirl {version}, {'正常运行' if get_status(event) else '指令限制'}\n"
            reply += f"骰娘尊名: {get_name()}\n"
            reply += f"操作系统: {system}\n"
            reply += f"CPU 核心: {psutil.cpu_count()} 核心\n"
            reply += f"Python 版本: {platform.python_version()}\n"
            reply += "系统内存占用: %.2fMB/%.2fMB\n" % (rss, total)
            reply += f"漏洞检测模式: {'on' if DEBUG else 'off'}"
            await matcher.send(reply)
            return

        if commands["upgrade"]:
            await matcher.send("检查版本更新中...")
            newest_version = await get_latest_version("dicergirl")

            if tuple(map(int, version.split("."))) < newest_version:
                await matcher.send(f"发现新版本 dicergirl {newest_version}, 开始更新...")
                upgrade = await run_shell_command(f"\"{sys.executable}\" -m pip install dicergirl -i https://pypi.org/simple --upgrade")

                if upgrade["returncode"] != 0:
                    logger.error(upgrade['stderr'])
                    await matcher.send("更新失败! 请查看终端输出以获取错误信息, 或者你可以再次尝试.")
                    return

                await matcher.send(f"{get_name()}骰娘已更新为版本 {'.'.join(map(str, newest_version))}.")
                return

            await matcher.send(f"我已经是最新版本的{get_name()}了!")
            return

        if commands["downgrade"]:
            if not is_super_user(event):
                await matcher.send("你没有管理员权限, 请先执行`.su`开启权限鉴定.")
                return

            await matcher.send("警告! 执行降级之后可能导致无法再次自动升级!")
            await run_shell_command(f"\"{sys.executable}\" -m pip install dicergirl=={commands['downgrade']} -i https://pypi.org/simple")
            await matcher.send(f"{get_name()}已降级到 {commands['downgrade']}.")
            return

        if commands["name"]:
            if not is_super_user(event):
                await matcher.send("你没有管理员权限, 请先执行`.su`开启权限鉴定.")
                return

            sn = set_name(commands["name"])

            if isinstance(sn, bool):
                await bot.call_api(
                    "set_qq_profile",
                    **{
                        "nickname": commands["name"],
                    }
                )
                await matcher.send(manager.process_generic_event(
                    "NameSet",
                    event=event,
                    NewName=commands["name"]
                ))
            elif isinstance(sn, str):
                await matcher.send(sn)

            return

        if commands["mode"]:
            reply = "当前已正确安装的跑团插件:\n"
            for plugin in modes.keys():
                reply += f"{plugin.upper()} 模式:\n"
                if hasattr(modes[plugin], "__description__"):
                    reply += f"\t简介: {modes[plugin].__description__}\n"

                reply += f"\t切换: .mode {plugin}\n"

            reply.strip("\n")
            reply += f"当前的跑团模式为 {get_mode(event).upper()}."
            await matcher.send(reply)
            return

        if commands["store"]:
            official, community = await get_plugins()
            reply = "从商店搜索到以下插件:\n"
            reply += "Unvisitor 官方插件:\n"

            i = 1
            for name, detail in official.items():
                reply += f"  {i}. {detail['name']}[安装: .bot install {name}]\n"
                i += 1

            reply += "社区提供插件:\n"
            i = 1
            for name, detail in community.items():
                reply += f"  {i}. {detail['name']}[安装: .bot install {name}]\n"

            reply.rstrip("\n")
            await matcher.send(reply)
            return

        if commands["install"]:
            if commands["install"] in modes.keys():
                await matcher.send(f"模块 {commands['install']} 已经安装了!")
                return

            ins = await install(commands["install"])

            if ins is PluginNotFoundError:
                await matcher.send(f"包 {commands['install']} 不存在.")
                return
            elif ins is PluginInstallFailedError:
                await matcher.send(f"包 {commands['install']} 安装失败.")
                return
            elif ins == True:
                await matcher.send(f"模块 {commands['install']} 安装完毕.")
                return

            return

        if commands["remove"]:
            if not is_super_user(event):
                await matcher.send("你没有管理员权限, 请先执行`.su`开启权限鉴定.")
                return

            uns = await remove(commands["remove"])

            if uns is PluginUninstallFailedError:
                await matcher.send(manager.process_generic_event(
                    "UninstallFailed",
                    event=event
                ))
                return

            await matcher.send(f"模块 {commands['remove']} 卸载完毕.")
            return

        if commands["plgup"]:
            up = await plgupgrade(commands["plgup"])

            if up is PluginNotFoundError:
                await matcher.send(f"包 {commands['plgup']} 似乎不存在?")
                return
            elif up is PluginInstallFailedError:
                await matcher.send(f"包 {commands['plgup']} 更新失败了.")
                return
            elif up == True:
                await matcher.send(f"插件 {commands['plgup']} 更新完毕.")
                return

            return

        await matcher.send("未知的指令, 使用`.help bot`获得机器人管理指令使用帮助.")

    @logcommand.handle()
    async def loghandler(bot: V11Bot, matcher: Matcher, event: Event):
        """ 日志管理指令 """
        args = format_msg(event.get_message(), begin=".log")
        commands = CommandParser(
            Commands([
                Only("show"),
                Only(("add", "new")),
                Optional("name", str),
                Optional("stop", int),
                Optional("start", int),
                Optional(("remove", "rm"), int),
                Optional(("download", "load"), int)
                ]),
            args=args,
            auto=True
            ).results

        if commands["show"]:
            gl = get_loggers(event)
            if len(gl) == 0:
                await matcher.send("暂无存储的日志.")
                return

            if not get_group_id(event) in loggers.keys():
                running = []
            else:
                running = loggers[get_group_id(event)].keys()

            reply = "该群聊所有日志:\n"
            for l in gl:
                index = gl.index(l)
                reply += f"序列 {index} : {l} : {'记录中' if index in running else '已关闭'}\n"
            reply.strip("\n")

            await matcher.send(reply)
            return

        if commands["download"] or commands["download"] == 0:
            gl = get_loggers(event)
            if commands["download"] > len(gl)-1:
                await matcher.send(f"目标日志序列 {commands['download']} 不存在.")
                return

            path = Path(gl[commands["download"]])
            await bot.call_api(
                "upload_group_file",
                **{
                    "group_id": get_group_id(event),
                    "file": str(path),
                    "name": path.name
                }
            )
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

            index = len(get_loggers(event))
            loggers[get_group_id(event)][index] = [new_logger, logname]

            if not add_logger(event, logname):
                raise IOError("无法新增日志.")

            await matcher.send(f"新增日志序列: {index}\n日志文件: {logname}")
            return

        if commands["stop"] or commands["stop"] == 0:
            if not get_group_id(event) in loggers.keys():
                await matcher.send("该群组无正在运行中的日志.")
                loggers[get_group_id(event)] = {}
                return

            if not commands["stop"] in loggers[get_group_id(event)]:
                await matcher.send("目标日志不存在.")
                return

            loggers[get_group_id(event)][commands["stop"]][0].remove()
            loggers[get_group_id(event)].pop(commands["stop"])
            await matcher.send(f"日志序列 {commands['stop']} 已停止记录.")
            return

        if commands["start"] or commands["start"] == 0:
            gl = get_loggers(event)
            if commands["start"] > len(gl)-1:
                await matcher.send(f"目标日志序列 {commands['start']} 不存在.")
                return

            logname = gl[commands["start"]]
            new_logger = multilogger(name="DG Msg Logger", payload="TRPG")
            new_logger.remove()
            new_logger.add(logname, encoding='utf-8', format="{message}", level="INFO")
            if not get_group_id(event) in loggers.keys():
                loggers[get_group_id(event)] = {}

            loggers[get_group_id(event)][commands["start"]] = [new_logger, logname]
            await matcher.send(f"日志序列 {commands['start']} 重新启动.")
            return

        if commands["remove"] or commands["remove"] == 0:
            gl = get_loggers(event)
            if not gl:
                await matcher.send("该群组从未设置过日志.")
                loggers[get_group_id(event)] = {}
                return

            if commands["remove"] > len(gl)-1:
                await matcher.send(f"目标日志序列 {commands['remove']} 不存在.")
                return

            index = len(gl)
            if get_group_id(event) in loggers.keys():
                if commands["remove"] in loggers[get_group_id(event)].keys():
                    await matcher.send(f"目标日志序列 {commands['remove']} 正在运行, 开始中止...")
                    loggers[get_group_id(event)][commands["remove"]][0].remove()
                    loggers[get_group_id(event)].pop(commands["remove"])

            Path(gl[commands["remove"]]).unlink()
            remove_logger(event, commands["remove"])
            await matcher.send(f"日志序列 {commands['remove']} 已删除.")
            return

        await matcher.send("骰娘日志管理系统, 使用`.help log`指令详细信息.")

    def trpg_log(event):
        """ 外置的日志记录方法 """
        if not isinstance(event, GroupMessageEvent):
            return

        if not get_group_id(event) in loggers.keys():
            return

        for log in loggers[get_group_id(event)].keys():
            if isinstance(event, GroupMessageEvent):
                raw_json = json.loads(event.json())
                if raw_json['sender']['card']:
                    if raw_json['sender']['card'].lower() == "ob":
                        role_or_name = f"[旁观者 - {raw_json['sender']['nickname']}]"
                    elif raw_json['sender']['card'].lower() == "kp":
                        role_or_name = f"[主持人 - {raw_json['sender']['nickname']}]"
                    else:
                        role_or_name = f"[{raw_json['sender']['card']}]"
                elif raw_json['sender']['nickname']:
                    role_or_name = f"[未知访客 - {raw_json['sender']['nickname']}]"
                else:
                    role_or_name = f"[未知访客 - {str(event.get_user_id())}]"

                message = role_or_name + ": " + html.unescape(str(event.get_message()))
            elif isinstance(event, Event):
                message = f"[{get_name()}]: " + html.unescape(event.message)

            loggers[get_group_id(event)][log][0].info(message)

    @selflogcommand.handle()
    @messagemonitor.handle()
    def loggerhandler(event: Event):
        """ 消息记录日志指令 """
        trpg_log(event)

    @showcommand.handle()
    async def showhandler(matcher: Matcher, event: GroupMessageEvent, args: list=None):
        """ 角色卡展示指令 """
        if not get_status(event) and not event.to_me:
            return

        if not isinstance(args, list):
            args = format_msg(event.get_message(), begin=(".show", ".display"))
        else:
            args = args

        at = get_mentions(event)

        mode = get_mode(event)
        if mode in modes:
            try:
                sh = show_handler(event, args, at, mode=mode)
            except Exception as error:
                logger.exception(error)
                sh = [manager.process_generic_event(
                    "CommandFailed",
                    event=event
                )]
        else:
            await matcher.send(manager.process_generic_event(
                "UnknownMode",
                event=event
            ))
            return True

        for msg in sh:
            await matcher.send(str(msg))
        return

    @setcommand.handle()
    async def sethandler(bot: V11Bot, matcher: Matcher, event: GroupMessageEvent):
        """ 角色卡设置指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=(".set", ".st"))
        at = get_mentions(event)
        commands = CommandParser(
            Commands([
                Only("show"),
                Only("del"),
                Only("clear")
            ]),
            args,
            auto=True
        ).results

        if at and not get_user_card(event).upper() == "KP" and not event.to_me:
            await matcher.send(manager.process_generic_event(
                "SetPermissionDenied"
            ))
            return

        if commands["show"]:
            args.remove("show")
            return await showhandler(matcher, event, args=args)

        if commands["del"]:
            args.remove("del")
            return await delhandler(matcher, event, args=args)

        mode = get_mode(event)
        if mode in modes:
            try:
                if not args:
                    cache = modes[mode].__cache__
                    user_id: int = event.user_id
                    got = cache.get(event, qid=str(user_id))

                    if isinstance(got, dict):
                        if "name" not in got.keys():
                            got = ""

                    name = got['name'] if got else ""
                    await bot.set_group_card(group_id=event.group_id, user_id=user_id, card=name)

                sh = set_handler(event, args, at, mode=mode)
            except Exception as error:
                logger.exception(error)
                sh = [manager.process_generic_event(
                    "CommandFailed",
                    event=event
                )]
        else:
            await matcher.send(manager.process_generic_event(
                "UnknownMode",
                event=event
            ))
            return True

        await matcher.send(sh)
        return

    @helpcommand.handle()
    async def helphandler(matcher: Matcher, event: MessageEvent):
        """ 帮助指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=(".help", ".h"))
        if args:
            arg = args[0]
        else:
            arg = ""

        message = help_message(arg)
        message = re.sub(r"\{name\}", get_name(), message)
        message = re.sub(r"\{version\}", version, message)
        message = re.sub(r"\{py_version\}", platform.python_version(), message)
        message = re.sub(r"\{nonebot_version\}", nonebot.__version__, message)
        await matcher.send(message)

    @modecommand.handle()
    async def modehandler(bot: V11Bot, matcher: Matcher, event: MessageEvent):
        """ 跑团模式切换指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_str(event.get_message(), begin=(".mode", ".m"))
        if args:
            if args.lower() in modes:
                set_mode(event, args.lower())

                for user in await bot.get_group_member_list(group_id=event.group_id):
                    if not hasattr(modes[args], "__cards__"):
                        break

                    card: Cards = modes[args].__cards__
                    user_id: int = user['user_id']
                    got = card.get(event, qid=str(user_id))

                    if isinstance(got, dict):
                        if "name" not in got.keys():
                            continue
                    elif not got:
                        continue

                    name = got['name'] if got else ""
                    await bot.set_group_card(group_id=event.group_id, user_id=user_id, card=name)

                await matcher.send(manager.process_generic_event(
                    "ModeChanged",
                    event=event,
                    Mode=args.upper()
                ))
                return True
            else:
                await matcher.send(manager.process_generic_event(
                    "UnknownMode",
                    event=event
                ))
                return True
        else:
            reply = "当前已正确安装的跑团插件:\n"
            for plugin in modes.keys():
                reply += f"{plugin.upper()} 模式: {plugin}.\n"

            reply += f"当前的跑团模式为 {get_mode(event).upper()}."
            await matcher.send(reply)

    @shootcommand.handle()
    async def shoothandler(matcher: Matcher, event: GroupMessageEvent):
        """ 射击检定指令 """
        if not get_status(event) and not event.to_me:
            return

        await matcher.send(shoot(event))

    @attackcommand.handle()
    async def attackhandler(matcher: Matcher, event: GroupMessageEvent):
        """ 伤害检定指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_str(event.get_message(), begin=(".at", ".attack"))
        mode = get_mode(event)
        if mode in modes:
            if not hasattr(modes[mode], "__commands__"):
                await matcher.send(f"跑团模式 {mode.upper()} 未设置标准指令.")
                return

            if not "at" in modes[mode].__commands__.keys():
                await matcher.send(f"跑团模式 {mode.upper()} 不支持伤害检定指令.")
                return

            handler = modes[mode].__commands__["at"]
            await matcher.send(handler(event, args))
        else:
            await matcher.send(manager.process_generic_event(
                "UnknownMode",
                event=event
            ))

    @damcommand.handle()
    async def damhandler(matcher: Matcher, event: GroupMessageEvent):
        """ 承伤检定指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=(".dam", ".damage"))
        mode = get_mode(event)
        if mode in modes:
            if not hasattr(modes[mode], "__commands__"):
                await matcher.send(f"跑团模式 {mode.upper()} 未设置标准指令.")
                return

            if not "at" in modes[mode].__commands__.keys():
                await matcher.send(f"跑团模式 {mode.upper()} 不支持承伤检定指令.")
                return

            handler = modes[mode].__commands__["dam"]
            await matcher.send(handler(event, args))
        else:
            await matcher.send(manager.process_generic_event(
                "UnknownMode",
                event=event
            ))

    @encommand.handle()
    async def enhandler(matcher: Matcher, event: GroupMessageEvent):
        """ 属性或技能激励指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=".en")
        mode = get_mode(event)
        if mode in modes:
            if not hasattr(modes[mode], "__commands__"):
                await matcher.send(f"跑团模式 {mode.upper()} 未设置标准指令.")
                return

            if not "at" in modes[mode].__commands__.keys():
                await matcher.send(f"跑团模式 {mode.upper()} 不支持激励指令.")
                return

            handler = modes[mode].__commands__["en"]
            await matcher.send(handler(event, args))
        else:
            await matcher.send(manager.process_generic_event(
                "UnknownMode",
                event=event
            ))

    @racommand.handle()
    async def rahandler(matcher: Matcher, event: GroupMessageEvent):
        """ 属性或技能检定指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=".ra")
        mode = get_mode(event)
        if mode in modes:
            if not hasattr(modes[mode], "__commands__"):
                await matcher.send(f"跑团模式 {mode.upper()} 未设置标准指令.")
                return

            if not "ra" in modes[mode].__commands__.keys():
                await matcher.send(f"跑团模式 {mode.upper()} 不支持技能检定指令.")
                return

            handler = modes[mode].__commands__["ra"]
            replies = handler(event, args)
            if isinstance(replies, list):
                for reply in replies:
                    await matcher.send(reply)
                return

            await matcher.send(replies)
        else:
            await matcher.send(manager.process_generic_event(
                "UnknownMode",
                event=event
            ))

    @rhcommand.handle()
    async def rhhandler(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
        """ 暗骰指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_str(event.get_message(), begin=".rh")
        await matcher.send("暗骰: 命运的骰子在滚动.")
        await bot.send_private_msg(user_id=event.get_user_id(), message=roll(args))

    @rhacommand.handle()
    async def rhahandler(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
        """ 暗骰技能检定指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=".rha")
        mode = get_mode()
        await matcher.send("暗骰: 命运的骰子在滚动.")
        await bot.send_private_msg(user_id=event.get_user_id(), message=eval(f"{mode}_(args, event)"))

    @rollcommand.handle()
    async def rollhandler(matcher: Matcher, event: MessageEvent):
        """ 标准掷骰指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_str(event.get_message(), begin=(".r", ".roll"))
        name = get_user_card(event)
        if not args:
            await matcher.send(roll("1d100", name=name))
            return

        try:
            await matcher.send(roll(args, name=name))
        except Exception as error:
            logger.exception(error)
            await matcher.send("未知错误, 可能是掷骰语法异常.\nBUG提交: https://gitee.com/unvisitor/issues")

    @delcommand.handle()
    async def delhandler(matcher: Matcher, event: GroupMessageEvent, args: list=None):
        """ 角色卡或角色卡技能删除指令 """
        if not get_status(event) and not event.to_me:
            return

        if not isinstance(args, list):
            args = format_msg(event.get_message(), begin=(".del", ".delete"))
        else:
            args = args

        at = get_mentions(event)

        if at and not is_super_user(event):
            await matcher.send(manager.process_generic_event(
                "DeletePermissionDenied",
                event=event
            ))
            return

        mode = get_mode(event)
        if mode in modes:
            for msg in del_handler(event, args, at, mode=mode):
                await matcher.send(msg)

    @rolekpcommand.handle()
    async def rolekphandler(bot: V11Bot, matcher: Matcher, event: GroupMessageEvent):
        """ KP 身份组认证 """
        args = format_msg(event.get_message(), begin=(".kp"))
        cp = CommandParser(
            Commands([
                Optional(("time", "schedule"), int),
                Optional(("minute", "min"), int, 0)
            ]),
            args=args,
            auto=True
        ).results

        if cp["time"]:
            @scheduler.scheduled_job("cron", hour=cp["time"], minute=cp["minute"], id="timer")
            async def _():
                await bot.send_group_msg(group_id=event.group_id, message="抵达 KP 设定的跑团启动时间.")

            try:
                scheduler.start()
            except:
                pass
            await matcher.send(f"定时任务: {cp['time']}: {cp['minute'] if len(str(cp['minute'])) > 1 else '0'+str(cp['minute'])}")
            return

        rolekp(event)
        await bot.set_group_card(group_id=event.group_id, user_id=event.get_user_id(), card="KP")
        await matcher.send("身份组设置为主持人 (KP).")

    @roleobcommand.handle()
    async def roleobhandler(bot: V11Bot, matcher: Matcher, event: GroupMessageEvent):
        """ OB 身份组认证 """
        import json
        roleob(event)

        if json.loads(event.json())['sender']['card'] == "ob":
            await bot.set_group_card(group_id=event.group_id, user_id=event.get_user_id())
            await matcher.send("取消旁观者 (OB) 身份.")
        else:
            await bot.set_group_card(group_id=event.group_id, user_id=event.get_user_id(), card="ob")
            await matcher.send("身份组设置为旁观者 (OB).")

    @registcommand.handle()
    async def registhandler(matcher: Matcher, event: GroupMessageEvent):
        """ 消息事件注册指令 """
        args = format_str(event.get_message(), begin=(".regist", ".reg"), lower=False).split(" ")
        args = list(filter(None, args))
        cp = CommandParser(
            Commands([
                Positional("event_name", str),
                Positional("message", str),
                Optional(("remove", "rm", "delete", "del"), str),
                Optional("enable", str),
                Optional("disable ", str),
            ]),
            args=args,
            auto=True
        ).results

        event_name = cp["event_name"]
        message = cp["message"]
        if not event_name or not message:
            await matcher.send("消息事件注册参数不全, 使用`.help regist`获取帮助信息.")
            return

        message = html.unescape(message)
        manager.register_event(event_name, message.replace("\\n", "\n"), is_custom=True)
        await matcher.send(f"消息事件 {event_name} 已被更改为 {message}.")

    @sncommand.handle()
    async def snhandler(bot: V11Bot, matcher: Matcher, event: GroupMessageEvent):
        """ 群名片修改指令 """
        card: Cards = modes[get_mode(event)].__cards__
        user_id: int = event.get_user_id()
        got = card.get(event, qid=str(user_id))

        if isinstance(got, dict):
            if "name" not in got.keys():
                got = ""

        name = got['name'] if got else ""
        await bot.set_group_card(group_id=event.group_id, user_id=user_id, card=name)

    @chatcommand.handle()
    async def chathandler(matcher: Matcher, event: MessageEvent):
        """ chatGPT 对话指令 """
        args = format_str(event.get_message(), begin=".chat")
        if not args:
            await matcher.send("空消息是不被允许的.")
            return
        await matcher.send(chat(args))

    @versioncommand.handle()
    async def versionhandler(matcher: Matcher):
        """ 骰娘版本及开源声明指令 """
        await matcher.send(f"Unvisitor DicerGirl 版本 {version} [Python {platform.python_version()} For Nonebot2 {nonebot.__version__}]\n此项目以Apache-2.0协议开源.\nThis project is open source under the Apache-2.0 license.\n欢迎使用 DicerGirl, 使用`.help 指令`查看指令帮助.")
        return
else:
    logger.warning("Nonebot2 初始化失败, DicerGirl 无法启动!")