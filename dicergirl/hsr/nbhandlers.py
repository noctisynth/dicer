try:
    from dicergirl.utils.utils import format_msg, get_status, get_mentions, is_super_user, on_startswith
    from dicergirl.utils.parser import CommandParser, Commands, Only, Optional, Required
except ImportError:
    from ..utils.utils import format_msg, get_status, get_mentions, is_super_user, on_startswith
    from ..utils.parser import CommandParser, Commands, Only, Optional, Required

from nonebot.matcher import Matcher
from nonebot.adapters import Bot as Bot
from nonebot.internal.matcher.matcher import Matcher
from nonebot.adapters.onebot.v11 import GroupMessageEvent

hsrcommand = on_startswith(".hsr", priority=1, block=True).handle()

async def hsr_handler(matcher: Matcher, event: GroupMessageEvent):
    """ HSR 车卡指令 """
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

    await matcher.send("[Oracle] 开发中, 请耐心等待...")

commands = {"hsrcommand": "hsr_handler"}