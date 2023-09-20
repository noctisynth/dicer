from nonebot.adapters.onebot.v12 import GroupMessageEvent
from ..utils.dicer import Dicer
from ..utils.docimasy import expr
from ..utils.utils import get_group_id
from ..utils.plugins import modes
from ..reply.manager import manager

manager.register_event("SetDefault", "[{SenderCard}]设置{CharactorName} {Property} 为: {Value}")
manager.register_event("SetDefaultFailed", "基础数据 {Property} 要求正整数数据, 但你传入了 {Value}.")
manager.register_event("SetSkill", "[{SenderCard}]设置{CharactorName}技能 {Property} 为: {Value}")
manager.register_event("SetSkillFailed", "技能数据 {Property} 要求正整数数据, 但你传入了 {Value}.")
manager.register_event("CardInUse", "[{SenderCard}]使用中人物卡: \n{CardDetail}")
manager.register_event("CardInCache", "[{SenderCard}]已暂存人物卡: \n{CardDetail}")
manager.register_event("CardSaved", "[{SenderCard}]成功从缓存保存人物卡属性: \n{CardDetail}")
manager.register_event("CardDeleted", "[{SenderCard}]已删除使用中的人物卡！")
manager.register_event("BadRollString", "诶, 出错了, 请检查你的掷骰表达式.\n使用`.help roll`获得掷骰指令使用帮助.")
manager.register_event("MultipleRollStringError", "参数错误, `#`提示符前应当跟随整型数.")
manager.register_event("BadSex", "{BotName}拒绝将{CharactorName}性别将设置为 {Value}, 这是对物种的侮辱.")
manager.register_event("AttributeCountError", "参数错误, 这是由于传输的数据数量错误, {BotName}只接受为偶数的参数数量, 这看起来不像是来源于我的错误.\n使用`.help {Command}`查看使用帮助.")
manager.register_event("CardCleared", "[{SenderCard}]已清空暂存人物卡数据.")
manager.register_event("UnknownError", "诶, 貌似发生了未知的错误?")
manager.register_event("SkillDeleted", "[{SenderCard}]已删除技能 {SkillName}, 唔, 真是可惜.")
manager.register_event("ShootDocimasy", "[{SenderCard}]进行射击检定:\n{DiceDescription}\n检定命中了 {OnShoot}.")

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

def __set_default(args: list, event, cards=None, module=None, attrs_dict=None, cha=None, qid=None) -> bool:
    """ 技能或属性设置 """
    for attr, alias in attrs_dict.items():
        if args[0] in alias:
            if attr in ["名字", "性别"]:
                if attr == "性别" and not args[1] in ["男", "女"]:
                    return manager.process_generic_event(
                        "BadSex",
                        CharactorName=module.__cname__,
                        Value=args[1]
                    )
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
                    return manager.process_generic_event(
                        "SetDefaultFailed",
                        Property=args[0],
                        Value=args[1]
                        )
            cards.update(event, cha.__dict__, qid=qid)
            return manager.process_generic_event(
                "SetDefault",
                CharactorName=module.__cname__,
                Property=attr,
                Value=cha.__dict__[alias[0]]
                )

def __set_skill(args, event, reply: list, cards=None, cha=None, module=None, qid=None):
    """ 设置技能 """
    try:
        if not args[1].startswith(("-", "+")):
            cha.skills[args[0]] = int(args[1])
        elif args[1].startswith("+"):
            cha.skills[args[0]] += int(args[1][1:])
        elif args[1].startswith("-"):
            cha.skills[args[0]] -= int(args[1][1:])
        cards.update(event, cha.__dict__, qid=qid)
        reply.append(manager.process_generic_event(
            "SetSkill",
            CharactorName=module.__cname__,
            Property=args[0],
            Value=cha.skills[args[0]]
        ))
    except ValueError:
        reply.append(manager.process_generic_event(
            "SetSkillFailed",
            Property=args[0],
            Value=args[1]
        ))
    finally:
        return reply

def set_handler(event: GroupMessageEvent, args, at, mode=None):
    """ 兼容所有模式的`.set`指令后端方法 """
    module = modes[mode]
    cards = module.__cards__
    cache_cards = module.__cache__
    charactor = module.__charactor__
    attrs_dict = module.__baseattrs__
    args = __set_plus_format(args)

    if len(at) == 1:
        qid = at[0]
    else:
        qid = ""

    if not args:
        if cache_cards.get(event, qid=qid):
            card_data = cache_cards.get(event, qid=qid)
            cards.update(event, inv_dict=card_data, qid=qid)
            inv = charactor().load(card_data)
            return manager.process_generic_event(
                "CardSaved",
                CardDetail=inv.output()
            )
        else:
            return f"未找到缓存数据, 请先使用无参数的`.{module.__name__}`指令进行车卡生成角色卡."
    else:
        if cards.get(event, qid=qid):
            card_data = cards.get(event, qid=qid)
            inv = charactor().load(card_data)
        else:
            return f"未找到缓存数据, 请先使用无参数的`.{module.__name__}`指令进行车卡生成角色卡."

        if len(args) % 2 != 0:
            return manager.process_generic_event(
                "AttributeCountError",
                Command="set"
                )

        elif len(args) == 2:
            sd = __set_default(args, event, cards=cards, module=module, attrs_dict=attrs_dict, cha=inv, qid=qid)
            if sd:
                return sd

            return __set_skill(args, event, [], cards=cards, cha=inv, module=module, qid=qid)[0]
        elif len(args) > 2:
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
                        Command="set"
                        )

            for sub_li in li:
                sd = __set_default(sub_li, event, cards=cards, module=module, attrs_dict=attrs_dict, cha=inv, qid=qid)
                if sd:
                    reply.append(sd)
                    continue

                reply = __set_skill(sub_li, event, reply, cards=cards, cha=inv, module=module, qid=qid)

            rep = ""
            for r in reply:
                rep += r + "\n"
            return rep.rstrip("\n")
        else:
            return manager.process_generic_event(
                    "AttributeCountError",
                    Command="set"
                    )

def show_handler(message, args, at, mode=None):
    """ 兼容所有模式的`.show`指令后端方法 """
    module = modes[mode]
    cards = module.__cards__
    cache_cards = module.__cache__
    charactor = module.__charactor__

    if len(at) == 1:
        qid = at[0]
    else:
        qid = ""

    r = []
    if not args:
        if cards.get(message, qid=qid):
            card_data = cards.get(message, qid=qid)
            inv = charactor().load(card_data)
            data = manager.process_generic_event(
                "CardInUse",
                CardDetail=inv.output()
            )
            r.append(data)
        if cache_cards.get(message, qid=qid):
            card_data = cache_cards.get(message, qid=qid)
            inv = charactor().load(card_data)
            data = manager.process_generic_event(
                "CardInCache",
                CardDetail=inv.output()
            )
            r.append(data)
    elif args[0] in ["detail", "de", "details"]:
        if cards.get(message, qid=qid):
            card_data = cards.get(message, qid=qid)
            inv = charactor().load(card_data)
            r.append(inv.skills_output())
    elif args[0] == "all":
        cd = cards.data[get_group_id(message)]
        for data in cd:
            inv = charactor().load(cd[data])
            d = inv.output() + "\n"
            d += inv.skills_output()
            r.append(d)
    else:
        if cards.get(message, qid=qid):
            card_data = cards.get(message, qid=qid)
            cha = charactor().load(card_data)
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

def del_handler(message, args, at, mode=None):
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
            if cache_cards.get(message, qid=qid):
                if cache_cards.delete(message, save=False):
                    r.append(manager.process_generic_event(
                        "CacheCardCleared",
                    ))
                else:
                    r.append(manager.process_generic_event(
                        "UnknownError",
                    ))
            else:
                r.append("暂无缓存人物卡数据.")
        elif arg == "card":
            if cards.get(message):
                if cards.delete(message):
                    r.append(manager.process_generic_event(
                        "CardDeleted",
                    ))
                else:
                    r.append(manager.process_generic_event(
                        "UnknownError",
                    ))
            else:
                r.append("暂无使用中的人物卡.")
        else:
            if cards.delete_skill(message, arg):
                r.append(manager.process_generic_event(
                        "SkillDeleted",
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
        except ValueError:
            return manager.process_generic_event(
                "MultipleRollStringError"
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
        )

def shoot():
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
        DiceDescription=dice.description(),
        OnShoot=rstr
    )