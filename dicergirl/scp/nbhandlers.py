from .agent import Agent
from .scpcards import scp_cards, scp_cache_cards
from .scputils import deal, begin
from .attributes import all_alias_dict

try:
    from dicergirl.utils.utils import format_msg, get_status, get_mentions, is_super_user, on_startswith
    from dicergirl.utils.parser import CommandParser, Commands, Only, Optional, Required
except ImportError:
    from ..utils.utils import format_msg, get_status, get_mentions, is_super_user, on_startswith
    from ..utils.parser import CommandParser, Commands, Only, Optional, Required

from nonebot.matcher import Matcher
from nonebot.adapters import Bot as Bot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.internal.matcher.matcher import Matcher
from nonebot.adapters.onebot.v11 import GroupMessageEvent

import asyncio
import random

scpcommand = on_startswith(".scp", priority=1, block=True).handle()

async def scp_handler(matcher: Matcher, event: GroupMessageEvent):
    """ SCP 车卡指令 """
    if not get_status(event):
        return

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
                        await matcher.send("[Oracle] 需要提升的等级应当为整型数, 请检查你的指令.\n使用`.help scp`查看 SCP 车卡指令使用方法.")
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

commands = {"scpcommand": "scp_handler"}