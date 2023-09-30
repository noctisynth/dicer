from nonebot.adapters.onebot.v11 import MessageEvent

from ..utils.dicer import Dicer
from ..utils.docimasy import expr
from ..utils.utils import get_group_id
from ..utils.plugins import modes
from ..utils.cards import Cards
from ..utils.charactors import Character
from ..reply.manager import manager

class StatusCode:
    def __init__(self, status_code: int=1) -> None:
        self.status_code = status_code

    def __eq__(self, __value: object) -> bool:
        return __value == self.status_code

    def __bool__(self):
        if self.status_code > 0:
            return True
        else:
            return False

def __set_plus_format(args: list):
    """ `.set 技能 +x`语法解析 """
    while True:
        try:
            index = args.index("+")
        except:
            break
        args[index] = args[index] + args[index+1]
        args.pop(index+1)

    while True:
        try:
            index = args.index("-")
        except:
            break
        args[index] = args[index] + args[index+1]
        args.pop(index+1)

    return args

def __set_default(args: list, event: MessageEvent, reply: list, cards: Cards=None, module=None, attrs_dict: dict=None, cha: Character=None, qid: str=None) -> bool:
    """ 设置属性 """
    for attr, alias in attrs_dict.items():
        if args[0] in alias:
            if attr in ["名字", "性别"]:
                if attr == "性别" and not args[1] in ["男", "女"]:
                    reply.append(
                        manager.process_generic_event(
                            "BadSex",
                            event=event,
                            CharactorName="角色",
                            Value=args[1]
                        )
                    )
                    return StatusCode(-1)
                cha.__dict__[alias[0]] = args[1]
            else:
                try:
                    if not args[1].startswith(("-", "+")):
                        cha.__dict__[alias[0]] = int(args[1])
                    elif args[1].startswith("+"):
                        cha.__dict__[alias[0]] += int(args[1][1:])
                    elif args[1].startswith("-"):
                        cha.__dict__[alias[0]] -= int(args[1][1:])
                except ValueError:
                    reply.append(
                        manager.process_generic_event(
                            "ValueError",
                            event=event,
                            SkillName=args[0],
                            Value=args[1]
                        )
                    )
                    return StatusCode(0)
            cards.update(event, cha.__dict__, qid=qid)
            return StatusCode(1)

def __set_skill(args, event: MessageEvent, reply: list, cards: Cards=None, cha: Character=None, module=None, qid: str=None) -> bool:
    """ 设置技能 """
    try:
        if not args[1].startswith(("-", "+")):
            cha.skills[args[0]] = int(args[1])
        elif args[1].startswith("+"):
            cha.skills[args[0]] += int(args[1][1:])
        elif args[1].startswith("-"):
            cha.skills[args[0]] -= int(args[1][1:])
        cards.update(event, cha.__dict__, qid=qid)
        return StatusCode(1)
    except ValueError:
        reply.append(
            manager.process_generic_event(
                "ValueError",
                event=event,
                SkillName=args[0],
                Value=args[1]
            )
        )
        return StatusCode(0)

def set_handler(event: MessageEvent, args: list, at: list, mode: str=None) -> str:
    """ 兼容所有模式的`.set`指令后端方法 """
    module = modes[mode]
    cards: Cards = module.__cards__
    cache_cards: Cards = module.__cache__
    charactor: Character = module.__charactor__()
    attrs_dict: dict = module.__baseattrs__
    args: list = __set_plus_format(args)

    attr_saved = 0
    skill_saved = 0
    saved_failed = 0

    if len(at) == 1:
        qid = at[0]
    else:
        qid = ""

    if not args:
        if cache_cards.get(event, qid=qid):
            card_data = cache_cards.get(event, qid=qid)
            cards.update(event, card_data, qid=qid)
            cha = charactor.load(card_data)
            cache_cards.delete(event)
            return manager.process_generic_event(
                "CardSaved",
                event=event,
                CardDetail=cha.output()
            )
        else:
            return manager.process_generic_event(
                "CacheNotFound",
                event=event,
                ModuleName=module.__name__
            )
    else:
        if cards.get(event, qid=qid):
            card_data = cards.get(event, qid=qid)
            cha = charactor.load(card_data)
        else:
            return manager.process_generic_event(
                "CacheNotFound",
                event=event,
                ModuleName=module.__name__
            )

        if len(args) % 2 != 0:
            return manager.process_generic_event(
                "AttributeCountError",
                event=event,
                Command="set"
                )

        reply = []

        li = []
        sub_li = []
        for arg in args:
            index = args.index(arg)
            if index % 2 == 0:
                sub_li.append(arg)
            elif index % 2 == 1:
                sub_li.append(arg)
                li.append(sub_li)
                sub_li = []
            else:
                return manager.process_generic_event(
                    "AttributeCountError",
                    event=event,
                    Command="set"
                )

        for sub_li in li:
            set_default_code = __set_default(sub_li, event, reply, cards=cards, module=module, attrs_dict=attrs_dict, cha=cha, qid=qid)
            if set_default_code:
                attr_saved += 1
                continue
            elif set_default_code == -1:
                saved_failed += 1
                continue

            if __set_skill(sub_li, event, reply, cards=cards, cha=cha, module=module, qid=qid):
                skill_saved += 1
            else:
                saved_failed += 1

        if not saved_failed:
            return manager.process_generic_event(
                "OnSet",
                event=event,
                AttrSetNumber=attr_saved,
                SkillSetNumber=skill_saved,
                SkillSetFailed=saved_failed
            )
        else:
            details = ""
            for detail in reply:
                details += detail + "\n"
            details.strip("\n")

            return manager.process_generic_event(
                "OnSetWithFailure",
                event=event,
                AttrSetNumber=attr_saved,
                SkillSetNumber=skill_saved,
                SkillSetFailed=saved_failed,
                FailedDetail=details
            )

def show_handler(event: MessageEvent, args, at, mode=None):
    """ 兼容所有模式的`.show`指令后端方法 """
    module = modes[mode]
    cards: Cards = module.__cards__
    cache_cards: Cards = module.__cache__
    charactor: Character = module.__charactor__()

    if len(at) == 1:
        qid = at[0]
    else:
        qid = ""

    r = []
    if not args:
        if cards.get(event, qid=qid):
            card_data = cards.get(event, qid=qid)
            cha = charactor.load(card_data)
            data = manager.process_generic_event(
                "CardInUse",
                event=event,
                CardDetail=cha.output()
            )
            r.append(data)
        if cache_cards.get(event, qid=qid):
            card_data = cache_cards.get(event, qid=qid)
            cha = charactor.load(card_data)
            data = manager.process_generic_event(
                "CardInCache",
                event=event,
                CardDetail=cha.output()
            )
            r.append(data)
    elif args[0] in ["detail", "de", "details"]:
        if cards.get(event, qid=qid):
            card_data = cards.get(event, qid=qid)
            cha = charactor.load(card_data)
            r.append(cha.skills_output())
    elif args[0] == "all":
        cd = cards.data[get_group_id(event)]
        for data in cd:
            cha = charactor.load(cd[data])
            d = cha.output() + "\n"
            d += cha.skills_output()
            r.append(d)
    else:
        if cards.get(event, qid=qid):
            card_data = cards.get(event, qid=qid)
            cha = charactor.load(card_data)
            if hasattr(cha, "out_"+args[0]):
                try:
                    r.append(getattr(cha, "out_"+args[0])())
                except:
                    r.append("查询时出现异常, 可能你想要查询的内容不存在?")
            else:
                r.append("错误的查询方式.")

    if not r:
        r.append("未查询到保存或暂存信息.")

    return r

def del_handler(event: MessageEvent, args, at, mode=None):
    """ 兼容所有模式的`.del`指令后端方法 """
    module = modes[mode]
    cache_cards = module.__cache__
    cards = module.__cards__

    if len(at) == 1:
        qid = at[0]
    else:
        qid = ""

    r = []
    for arg in args:
        if not arg:
            pass
        elif arg == "cache":
            if cache_cards.get(event, qid=qid):
                if cache_cards.delete(event, save=False):
                    r.append(manager.process_generic_event(
                        "CacheCardCleared",
                        event=event,
                    ))
                else:
                    r.append(manager.process_generic_event(
                        "UnknownError",
                        event=event,
                    ))
            else:
                r.append("暂无缓存人物卡数据.")
        elif arg == "card":
            if cards.get(event):
                if cards.delete(event):
                    r.append(manager.process_generic_event(
                        "CardDeleted",
                        event=event,
                    ))
                else:
                    r.append(manager.process_generic_event(
                        "UnknownError",
                        event=event,
                    ))
            else:
                r.append("暂无使用中的人物卡.")
        else:
            if cards.delete_skill(event, arg):
                r.append(manager.process_generic_event(
                        "SkillDeleted",
                        event=event,
                        SkillName=arg
                    ))

    if not r:
        r.append("使用`.help del`获得指令使用帮助.")

    return r

def roll(args: str, name: str=None) -> str:
    """ 标准掷骰指令后端方法 """
    time = 1
    if "#" in args:
        args = args.split("#")

        try:
            time = int(args[0].strip())
            if time > 20:
                return manager.process_generic_event(
                        "BadMultipleRollString",
                        SenderCard=name
                    )
        except ValueError:
            return manager.process_generic_event(
                "MultipleRollStringError",
                SenderCard=name
            )

        if len(args) == 1:
            args = "1d100"
        else:
            args = args[1]
    else:
        args = args.strip()

    try:
        d = Dicer(args)
        r = expr(d, None, name=name)

        for _ in range(time-1):
            r += expr(d, None, name=name)

        return r.detail
    except ValueError:
        return manager.process_generic_event(
            "BadRollString",
            SenderCard=name
        )

def shoot(event: MessageEvent):
    dice = Dicer("1d20").roll()
    result = dice.outcome

    if result < 4:
        rstr = "右腿"
    elif result < 7:
        rstr = "左腿"
    elif result < 11:
        rstr = "腹部"
    elif result < 16:
        rstr = "胸部"
    elif result < 18:
        rstr = "右臂"
    elif result < 20:
        rstr = "左臂"
    elif result < 21:
        rstr = "头部"

    return manager.process_generic_event(
        "ShootDocimasy",
        event=event,
        DiceDescription=dice.description(),
        OnShoot=rstr
    )