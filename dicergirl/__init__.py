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
import platform
import psutil
import html

DEBUG = False
current_dir = Path(__file__).resolve().parent
package = get_package()

if package == "nonebot2":
    from .utils.messages import help_message, version
    from .utils.utils import (
        init, on_startswith,
        get_group_id, get_mentions, get_user_card,
        is_super_user, add_super_user, rm_super_user, su_uuid,
        format_msg, format_str,
        get_mode, set_mode,
        get_loggers, loggers, add_logger, remove_logger, log_dir,
        get_status, boton, botoff,
        rolekp, roleob,
        run_shell_command, get_latest_version
        )
    from .utils.plugins import modes
    from .utils.parser import CommandParser, Commands, Only, Optional, Required
    from .utils.handlers import show_handler, set_handler, del_handler, roll, shoot
    from .utils.cards import Cards
    from .utils.chat import chat

    from nonebot.matcher import Matcher
    from nonebot.plugin import on
    from nonebot.adapters import Bot as Bot
    from nonebot.adapters.onebot.v11 import Bot as V11Bot
    from nonebot.internal.matcher.matcher import Matcher

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
    loghandlercommand = on_startswith("", priority=1, block=False)
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
    chatcommand = on_startswith(".chat", priority=2, block=True)
    versioncommand = on_startswith((".version", ".v"), priority=2, block=True)

    # 定时任务
    scheduler = nonebot.require("nonebot_plugin_apscheduler").scheduler

    @driver.on_startup
    async def _() -> None:
        """ `Nonebot2`核心加载完成后的初始化方法 """
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
        logger.success("欧若可骰娘初始化完毕.")

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
            await matcher.send("[Oracle] 权限不足, 拒绝执行测试指令.")
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
        """ 超级用户管理指令 """
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
        """ 机器人管理指令 """
        args = format_msg(event.get_message(), begin=".bot")
        commands = CommandParser(
            Commands([
                Only(("version", "v", "bot")),
                Only(("exit", "bye", "leave")),
                Only(("on", "run", "start")),
                Only(("off", "down", "shutdown")),
                Only(("upgrade", "up")),
                Only(("status"))
            ]),
            args=args,
            auto=True
        )

        if commands.nothing or commands.results["version"]:
            return await versionhandler(matcher=matcher)
        else:
            commands = commands.results

        if commands["exit"]:
            if not is_super_user(event):
                await matcher.send("[Oracle] 你没有管理员权限, 请先执行`.su`开启权限鉴定.")
                return

            logger.info(f"欧若可退出群聊: {event.group_id}")
            await matcher.send("[Oracle] 欧若可离开群聊.")
            await bot.set_group_leave(group_id=event.group_id)
            return

        if commands["on"]:
            boton(event)
            await matcher.send("[Oracle] 欧若可已开放指令限制.")
            return

        if commands["off"]:
            botoff(event)
            await matcher.send("[Oracle] 欧若可已开启指令限制.")
            return

        if commands["status"]:
            try:
                system = platform.freedesktop_os_release()["PRETTY_NAME"]
            except:
                system = platform.platform()

            memi = psutil.Process().memory_info()
            rss = memi.rss / 1024 / 1024
            total = psutil.virtual_memory().total / 1024 / 1024

            reply = f"欧若可骰娘 {version}, {'正常运行' if get_status(event) else '指令限制'}\n"
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
                upgrade = await run_shell_command(f"{sys.executable} -m pip install dicergirl -i https://pypi.org/simple --upgrade")

                if upgrade["returncode"] != 0:
                    logger.error(upgrade['stderr'])
                    await matcher.send("更新失败! 请查看终端输出以获取错误信息, 或者你可以再次尝试.")
                    return

                await matcher.send(f"欧若可骰娘已更新为版本 {'.'.join(map(str, newest_version))}.")

            await matcher.send("我已经是最新版本的欧若可了!")
            return

        await matcher.send("[Oracle] 未知的指令, 使用`.help bot`获得机器人管理指令使用帮助.")

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

            await matcher.send(f"[Oracle] 新增日志序列: {index}\n日志文件: {logname}")
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
            await matcher.send(f"[Oracle] 日志序列 {commands['start']} 重新启动.")
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
        import json
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
                message = "[欧若可]: " + html.unescape(event.message)

            loggers[get_group_id(event)][log][0].info(message)

    @selflogcommand.handle()
    @loghandlercommand.handle()
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
                sh = [f"[Oracle] 错误: 执行指令失败, 疑似模式 {mode} 不存在该指令."]
        else:
            await matcher.send("未知的跑团模式.")
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

        if at and not is_super_user(event):
            await matcher.send("[Oracle] 权限不足, 拒绝执行指令.")
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
                sh = [f"[Oracle] 错误: 执行指令失败, 疑似模式 {mode} 不存在该指令."]
        else:
            await matcher.send("未知的跑团模式.")
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
        print(arg)
        await matcher.send(help_message(arg))

    @modecommand.handle()
    async def modehandler(bot: V11Bot, matcher: Matcher, event: MessageEvent):
        """ 跑团模式切换指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=(".mode", ".m"))
        if args:
            if args[0].lower() in modes:
                set_mode(event, args[0].lower())

                for user in await bot.get_group_member_list(group_id=event.group_id):
                    card: Cards = modes[get_mode(event)].__cards__
                    user_id: int = user['user_id']
                    got = card.get(event, qid=str(user_id))

                    if isinstance(got, dict):
                        if "name" not in got.keys():
                            got = ""

                    name = got['name'] if got else ""
                    await bot.set_group_card(group_id=event.group_id, user_id=user_id, card=name)

                await matcher.send(f"[Oracle] 已切换到 {args[0].upper()} 跑团模式.")
                return True
            else:
                await matcher.send("[Oracle] 未知的跑团模式, 忽略指令.")
                return True
        else:
            reply = "当前已正确安装的跑团插件:\n"
            for plugin in modes.keys():
                reply += f"{plugin.upper()} 模式: {plugin}.\n"

            reply += f"[Oracle] 当前的跑团模式为 {get_mode(event).upper()}."
            await matcher.send(reply)

    @shootcommand.handle()
    async def shoothandler(matcher: Matcher, event: GroupMessageEvent):
        """ 射击检定指令 """
        if not get_status(event) and not event.to_me:
            return

        await matcher.send(shoot())

    @attackcommand.handle()
    async def attackhandler(matcher: Matcher, event: GroupMessageEvent):
        """ 伤害检定指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_str(event.get_message(), begin=(".at", ".attack"))
        mode = get_mode(event)
        if mode in modes:
            if not hasattr(modes[mode], "__commands__"):
                await matcher.send(f"[Oracle] 跑团模式 {mode.upper()} 未设置标准指令.")
                return

            if not "at" in modes[mode].__commands__.keys():
                await matcher.send(f"[Oracle] 跑团模式 {mode.upper()} 不支持伤害检定指令.")
                return

            handler = modes[mode].__commands__["at"]
            await matcher.send(handler(event, args))
        else:
            await matcher.send("[Oracle] 未知的跑团模式.")

    @damcommand.handle()
    async def damhandler(matcher: Matcher, event: GroupMessageEvent):
        """ 承伤检定指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=(".dam", ".damage"))
        mode = get_mode(event)
        if mode in modes:
            if not hasattr(modes[mode], "__commands__"):
                await matcher.send(f"[Oracle] 跑团模式 {mode.upper()} 未设置标准指令.")
                return

            if not "at" in modes[mode].__commands__.keys():
                await matcher.send(f"[Oracle] 跑团模式 {mode.upper()} 不支持承伤检定指令.")
                return

            handler = modes[mode].__commands__["dam"]
            await matcher.send(handler(event, args))
        else:
            await matcher.send("[Oracle] 未知的跑团模式.")

    @encommand.handle()
    async def enhandler(matcher: Matcher, event: GroupMessageEvent):
        """ 属性或技能激励指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=".en")
        mode = get_mode(event)
        if mode in modes:
            if not hasattr(modes[mode], "__commands__"):
                await matcher.send(f"[Oracle] 跑团模式 {mode.upper()} 未设置标准指令.")
                return

            if not "at" in modes[mode].__commands__.keys():
                await matcher.send(f"[Oracle] 跑团模式 {mode.upper()} 不支持激励指令.")
                return

            handler = modes[mode].__commands__["en"]
            await matcher.send(handler(event, args))
        else:
            await matcher.send("[Oracle] 未知的跑团模式.")

    @racommand.handle()
    async def rahandler(matcher: Matcher, event: GroupMessageEvent):
        """ 属性或技能检定指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=".ra")
        mode = get_mode(event)
        if mode in modes:
            if not hasattr(modes[mode], "__commands__"):
                await matcher.send(f"[Oracle] 跑团模式 {mode.upper()} 未设置标准指令.")
                return

            if not "ra" in modes[mode].__commands__.keys():
                await matcher.send(f"[Oracle] 跑团模式 {mode.upper()} 不支持技能检定指令.")
                return

            handler = modes[mode].__commands__["ra"]
            replies = handler(event, args)
            if isinstance(replies, list):
                for reply in replies:
                    await matcher.send(reply)
                return

            await matcher.send(replies)
        else:
            await matcher.send("[Oracle] 未知的跑团模式.")

    @rhcommand.handle()
    async def rhhandler(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
        """ 暗骰指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_str(event.get_message(), begin=".rh")
        await matcher.send("[Oracle] 暗骰: 命运的骰子在滚动.")
        await bot.send_private_msg(user_id=event.get_user_id(), message=roll(args))

    @rhacommand.handle()
    async def rhahandler(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
        """ 暗骰技能检定指令 """
        if not get_status(event) and not event.to_me:
            return

        args = format_msg(event.get_message(), begin=".rha")
        mode = get_mode()
        await matcher.send("[Oracle] 暗骰: 命运的骰子在滚动.")
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
            await matcher.send("[Oracle] 未知错误, 可能是掷骰语法异常.\nBUG提交: https://gitee.com/unvisitor/issues")

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
            await matcher.send("[Oracle] 权限不足, 拒绝执行指令.")
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
        await matcher.send("[Oracle] 身份组设置为主持人 (KP).")

    @roleobcommand.handle()
    async def roleobhandler(bot: V11Bot, matcher: Matcher, event: GroupMessageEvent):
        """ OB 身份组认证 """
        import json
        roleob(event)

        if json.loads(event.json())['sender']['card'] == "ob":
            await bot.set_group_card(group_id=event.group_id, user_id=event.get_user_id())
            await matcher.send("[Oracle] 取消旁观者 (OB) 身份.")
        else:
            await bot.set_group_card(group_id=event.group_id, user_id=event.get_user_id(), card="ob")
            await matcher.send("[Oracle] 身份组设置为旁观者 (OB).")

    @sncommand.handle()
    async def snhandler(bot: V11Bot, matcher: Matcher, event: GroupMessageEvent):
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
            await matcher.send("[Oracle] 空消息是不被允许的.")
            return
        await matcher.send(chat(args))

    @versioncommand.handle()
    async def versionhandler(matcher: Matcher):
        """ 骰娘版本及开源声明指令 """
        await matcher.send(f"欧若可骰娘 版本 {version}, 未知访客开发, 以Apache-2.0协议开源.\nCopyright © 2011-2023 Unknown Visitor. Open source as protocol Apache-2.0.")
        return
elif package == "qqguild":
    pass
else:
    logger.critical(f"未知的包模式: {package}!")
    sys.exit()