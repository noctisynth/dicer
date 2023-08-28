from .adventurer import Adventurer
from .dndcards import dnd_cache_cards

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

dndcommand = on_startswith(".dnd", priority=1, block=True).handle()

async def dnd_handler(matcher: Matcher, event: GroupMessageEvent):
    """ DND 车卡指令 """
    if not get_status(event):
        return

    args = format_msg(event.get_message(), begin=".dnd")
    if len(args) > 1:
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

commands = {"dndcommand": "dnd_handler"}