try:
    from .docimasy import expr
    from ..utils.utils import get_group_id
    from ..coc.coccards import coc_cache_cards, coc_cards, coc_attrs_dict
    from ..scp.scpcards import scp_cache_cards, scp_cards
    from ..scp.attributes import scp_attrs_dict
    from ..dnd.dndcards import dnd_cache_cards, dnd_cards, dnd_attrs_dict
    from .. import coc, scp, dnd
    from .dicer import Dice
except ImportError:
    from dicergirl.utils.docimasy import expr
    from dicergirl.utils.utils import get_group_id
    from dicergirl.coc.coccards import coc_cache_cards, coc_cards, coc_attrs_dict
    from dicergirl.scp.scpcards import scp_cache_cards, scp_cards
    from dicergirl.scp.attributes import scp_attrs_dict
    from dicergirl.dnd.dndcards import dnd_cache_cards, dnd_cards, dnd_attrs_dict
    from dicergirl import coc, scp, dnd
    from dicergirl.utils.dicer import Dice

def __set_plus_format(args: list):
    """ `.set 技能 +3`语法解析 """
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
                    return f"[Oracle] 欧若可拒绝将{module.__cname__}性别将设置为 {args[1]}, 这是对物种的侮辱."
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
                    return "基础数据 %s 要求正整数数据, 但你传入了 %s." % (args[0], args[1])
            cards.update(event, cha.__dict__, qid=qid)
            return "[Oracle] 设置%s %s 为: %s" % (module.__cname__, attr, cha.__dict__[alias[0]])

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
        reply.append("设置%s %s 技能为: %s." % (module.__cname__, args[0], cha.skills[args[0]]))
    except ValueError:
        reply.append("技能 %s 要求正整数数据, 但你传入了 %s." % (args[0], args[1]))
    finally:
        return reply

def set_handler(message, args, at, mode=None):
    """ 兼容所有模式的`.set`指令后端方法 """
    cards = eval(f"{mode}_cards")
    cache_cards = eval(f"{mode}_cache_cards")
    charactor = eval(mode).__charactor__
    attrs_dict = eval(f"{mode}_attrs_dict")
    module = eval(mode)
    args = __set_plus_format(args)

    if len(at) == 1:
        qid = at[0]
    else:
        qid = ""

    if not args:
        if cache_cards.get(message, qid=qid):
            card_data = cache_cards.get(message, qid=qid)
            cards.update(message, inv_dict=card_data, qid=qid)
            inv = charactor().load(card_data)
            return "[Oracle] 成功从缓存保存人物卡属性: \n" + inv.output()
        else:
            return f"[Oracle] 未找到缓存数据, 请先使用无参数的`.{module.__name__}`指令进行车卡生成角色卡."
    else:
        if cards.get(message, qid=qid):
            card_data = cards.get(message, qid=qid)
            inv = charactor().load(card_data)
        else:
            return f"[Oracle] 未找到缓存数据, 请先使用无参数的`.{module.__name__}`指令进行车卡生成角色卡."

        if len(args) % 2 != 0:
            return "[Oracle] 参数错误, 这是由于传输的数据数量错误, 我只接受为偶数的参数数量.\n此外, 这看起来不像是来源于我的错误."

        elif len(args) == 2:
            sd = __set_default(args, message, cards=cards, module=module, attrs_dict=attrs_dict, cha=inv, qid=qid)
            if sd:
                return sd
            
            return __set_skill(args, message, [], cards=cards, cha=inv, module=module, qid=qid)[0]
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
                    return "[Oracle] 参数错误, 这是由于传输的数据数量错误, 我只接受为偶数的参数数量.\n此外, 这看起来不像是来源于我的错误."

            for sub_li in li:
                sd = __set_default(sub_li, message, cards=cards, module=module, attrs_dict=attrs_dict, cha=inv, qid=qid)
                if sd:
                    continue

                reply = __set_skill(sub_li, message, reply, cards=cards, cha=inv, module=module, qid=qid)

            rep = "[Oracle]\n"
            for r in reply:
                rep += r + "\n"
            return rep.rstrip("\n")
        else:
            return "[Oracle] 参数错误, 可能是由于传输的数据数量错误.\n此外, 这看起来不像是来源于我的错误."

def show_handler(message, args, at, mode=None):
    """ 兼容所有模式的`.show`指令后端方法 """
    cards = eval(f"{mode}_cards")
    cache_cards = eval(f"{mode}_cache_cards")
    charactor = eval(mode).__charactor__

    if len(at) == 1:
        qid = at[0]
    else:
        qid = ""

    r = []
    if not args:
        if cards.get(message, qid=qid):
            card_data = cards.get(message, qid=qid)
            inv = charactor().load(card_data)
            data = "[Oracle] 使用中人物卡: \n" 
            data += inv.output()
            r.append(data)
        if cache_cards.get(message, qid=qid):
            card_data = cache_cards.get(message, qid=qid)
            inv = charactor().load(card_data)
            r.append("[Oracle] 已暂存人物卡: \n" + inv.output())
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
            try:
                r.append(getattr(cha, "out_"+args[0])())
            except:
                r.append("[Oracle] 查询时出现异常, 可能你想要查询的内容不存在?")

    if not r:
        r.append("[Oracle] 未查询到保存或暂存信息.")

    return r

def del_handler(message, args, at, mode=None):
    """ 兼容所有模式的`.del`指令后端方法 """
    cache_cards = eval(f"{mode}_cache_cards")
    cards = eval(f"{mode}_cards")

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
                    r.append("[Oracle] 已清空暂存人物卡数据.")
                else:
                    r.append("[Oracle] 错误: 未知错误.")
            else:
                r.append("[Oracle] 暂无缓存人物卡数据.")
        elif arg == "card":
            if cards.get(message):
                if cards.delete(message):
                    r.append("[Oracle] 已删除使用中的人物卡！")
                else:
                    r.append("[Oracle] 错误: 未知错误.")
            else:
                r.append("[Oracle] 暂无使用中的人物卡.")
        else:
            if cards.delete_skill(message, arg):
                r.append(f"已删除技能 {arg}.")

    if not r:
        r.append("[Oracle] 使用`.help del`获得指令使用帮助.")

    return r

def roll(args: str) -> str:
    """ 标准掷骰指令后端方法 """
    time = 1
    if "#" in args:
        args = args.split("#")

        try:
            time = int(args[0].strip())
        except ValueError:
            return "[Oracle] 参数错误, `#`提示符前应当跟随整型数."

        if len(args) == 1:
            args = "1d100"
        else:
            args = args[1]
    else:
        args = args.strip()

    try:
        d = Dice(args)
        r = expr(d, None)

        for _ in range(time-1):
            r += expr(d, None)

        return r.detail
    except ValueError:
        return "[Oracle] 出现错误, 请检查你的掷骰表达式.\n使用`.help r`获得掷骰指令使用帮助."