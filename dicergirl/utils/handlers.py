from loguru import logger
try:
    from ..utils.utils import _coc_cachepath, _scp_cachepath, logger as _log, get_group_id
    from ..utils.dicer import Dice, expr
    from ..utils.messages import help_messages
    from ..coc.coccards import coc_cache_cards, coc_cards, attrs_dict
    from ..scp.scpcards import scp_cache_cards, scp_cards, scp_attrs_dict
    from ..dnd.dndcards import dnd_cache_cards, dnd_cards, dnd_attrs_dict
    from .. import coc, scp, dnd
except ImportError:
    from dicergirl.utils.utils import _coc_cachepath, _scp_cachepath, logger as _log, get_group_id
    from dicergirl.utils.dicer import Dice, expr
    from dicergirl.utils.messages import help_messages
    from dicergirl.coc.coccards import cache_cards, cards, attrs_dict
    from dicergirl.scp.scpcards import scp_cache_cards, scp_cards, scp_attrs_dict
    from dicergirl.dnd.dndcards import dnd_cache_cards, dnd_cards, dnd_attrs_dict
    from dicergirl import coc, scp, dnd

def set_handler(message, args, at, mode=None):
    cards = eval(f"{mode}_cards")
    cache_cards = eval(f"{mode}_cache_cards")
    charactor = eval(mode).__charactor__
    module = eval(mode)

    if not args:
        if cache_cards.get(message):
            card_data = cache_cards.get(message)
            cards.update(message, inv_dict=card_data)
            inv = charactor().load(card_data)
            return "[Oracle] 成功从缓存保存人物卡属性: \n" + inv.output()
        else:
            return f"[Oracle] 未找到缓存数据, 请先使用无参数的`.{module.__name__}`指令进行车卡生成角色卡."
    else:
        if cards.get(message):
            card_data = cards.get(message)
            inv = charactor().load(card_data)
        else:
            return f"[Oracle] 未找到缓存数据, 请先使用无参数的`.{module.__name__}`指令进行车卡生成角色卡."
        if len(args) % 2 != 0:
            return "[Oracle] 参数错误, 这是由于传输的数据数量错误, 我只接受为偶数的参数数量.\n此外, 这看起来不像是来源于我的错误."
        elif len(args) == 2:
            for attr, alias in scp_attrs_dict.items():
                if args[0] in alias:
                    if attr in ["名字", "性别"]:
                        if attr == "性别" and not args[1] in ["男", "女"]:
                            return f"[Oracle] 欧若可拒绝将{module.__cname__}性别将设置为 {args[1]}, 这是对物种的侮辱."
                        inv.__dict__[alias[0]] = args[1]
                    else:
                        try:
                            inv.__dict__[alias[0]] = int(args[1])
                        except ValueError:
                            return "[Oracle] 请输入正整数属性数据."
                    cards.update(message, inv.__dict__)
                    return "[Oracle] 设置%s %s 为: %s" % (module.__cname__, attr, args[1])
            try:
                inv.skills[args[0]] = int(args[1])
                cards.update(message, inv.__dict__)
                return "[Oracle] 设置%s %s 技能为: %s." % (module.__cname__, args[0], args[1])
            except ValueError:
                return "[Oracle] 请输入正整数技能数据."
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
                has_set = False
                for attr, alias in scp_attrs_dict.items():
                    if sub_li[0] in alias:
                        if attr in ["名字", "性别"]:
                            if attr == "性别" and not sub_li[1] in ["男", "女"]:
                                return f"[Oracle] 欧若可拒绝将{module.__cname__}性别将设置为 {args[1]}, 这是对物种的侮辱."
                            inv.__dict__[alias[0]] = sub_li[1]
                        else:
                            try:
                                inv.__dict__[alias[0]] = int(sub_li[1])
                            except ValueError:
                                reply.append("基础数据 %s 要求正整数数据, 但你传入了 %s." % (sub_li[0], sub_li[1]))
                                continue
                        cards.update(message, inv.__dict__)
                        reply.append("设置%s基础数据 %s 为: %s" % (module.__cname__, attr, sub_li[1]))
                        has_set = True
                if has_set:
                    continue
                try:
                    inv.skills[sub_li[0]] = int(sub_li[1])
                    cards.update(message, inv.__dict__)
                    reply.append("设置%s %s 技能为: %s." % (module.__cname__, sub_li[0], sub_li[1]))
                except ValueError:
                    reply.append("技能 %s 要求正整数数据, 但你传入了 %s." % (sub_li[0], sub_li[1]))
            rep = "[Oracle]\n"
            for r in reply:
                rep += r + "\n"
            return rep.rstrip("\n")
        else:
            return "[Oracle] 参数错误, 可能是由于传输的数据数量错误.\n此外, 这看起来不像是来源于我的错误."

def show_handler(message, args, at, mode=None):
    cards = eval(f"{mode}_cards")
    cache_cards = eval(f"{mode}_cache_cards")
    charactor = eval(mode).__charactor__

    if at:
        return ["AT Now"]

    r = []
    if not args:
        if cards.get(message):
            card_data = cards.get(message)
            inv = charactor().load(card_data)
            data = "[Oracle] 使用中人物卡: \n" 
            data += inv.output() + "\n"
            data += inv.skills_output()
            r.append(data)
        if cache_cards.get(message):
            card_data = cache_cards.get(message)
            inv = charactor().load(card_data)
            r.append("[Oracle] 已暂存人物卡: \n" + inv.output())
    elif args[0] in ["skill", "s", "skills"]:
        if cards.get(message):
            card_data = cards.get(message)
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
        r.append("[Oracle] 参数异常.")
    if not r:
        r.append("[Oracle] 未查询到保存或暂存信息.")
    return r

def coc_del_handler(message, args: str):
    r = []
    args = args.split(" ")
    if args:
        args = list(filter(None, args))
    else:
        args = None
    for arg in args:
        if not arg:
            pass
        elif arg == "c":
            if cache_cards.get(message):
                if cache_cards.delete(message, save=False):
                    r.append("[Oracle] 已清空暂存人物卡数据.")
                else:
                    r.append("[Oracle] 错误: 未知错误.")
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
        r.append(help_messages.del_)
    return r

def scp_del_handler(message, args: str):
    r = []
    args = args.split(" ")

    if args:
        args = list(filter(None, args))
    else:
        args = None
    
    logger.info(args)
    for arg in args:
        if not arg:
            pass
        elif arg == "c":
            if scp_cache_cards.get(message):
                if scp_cache_cards.delete(message, save=False):
                    r.append("[Oracle] 已清空暂存人物卡数据.")
                else:
                    r.append("[Oracle] 错误: 未知错误.")
            r.append("[Oracle] 暂无缓存人物卡数据.")
        elif arg == "card":
            if scp_cards.get(message):
                if scp_cards.delete(message):
                    r.append("[Oracle] 已删除使用中的人物卡！")
                else:
                    r.append("[Oracle] 错误: 未知错误.")
            else:
                r.append("[Oracle] 暂无使用中的人物卡.")
        else:
            if scp_cards.delete_skill(message, arg):
                r.append(f"已删除技能 {arg}.")
    if not r:
        r.append(help_messages.del_)
    return r

def dnd_del_handler(message, args: str):
    r = []
    args = args.split(" ")
    if args:
        args = list(filter(None, args))
    else:
        args = None
    for arg in args:
        if not arg:
            pass
        elif arg == "c":
            if dnd_cache_cards.get(message):
                if dnd_cache_cards.delete(message, save=False):
                    r.append("[Oracle] 已清空暂存人物卡数据.")
                else:
                    r.append("[Oracle] 错误: 未知错误.")
            r.append("[Oracle] 暂无缓存人物卡数据.")
        elif arg == "card":
            if dnd_cards.get(message):
                if dnd_cards.delete(message):
                    r.append("[Oracle] 已删除使用中的人物卡！")
                else:
                    r.append("[Oracle] 错误: 未知错误.")
            else:
                r.append("[Oracle] 暂无使用中的人物卡.")
        else:
            if dnd_cards.delete_skill(message, arg):
                r.append(f"已删除技能 {arg}.")
    if not r:
        r.append(help_messages.del_)
    return r