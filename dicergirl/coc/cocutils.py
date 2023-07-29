from typing import Optional
try:
    from ..utils.messages import help_messages, temporary_madness, madness_end, phobias, manias, help_message
    from ..utils.dicer import Dice, expr
    from ..utils.utils import _log
    from .coccards import cards, attrs_dict
    from .investigator import Investigator
except ImportError:
    from dicergirl.utils.messages import help_messages, temporary_madness, madness_end, phobias, manias, help_message
    from dicergirl.utils.dicer import Dice, expr
    from dicergirl.utils.utils import _log
    from dicergirl.coc.coccards import cards, attrs_dict
    from dicergirl.coc.investigator import Investigator

import random
import re

def sc(arg, event):
    reply = []
    try:
        args = arg.split(" ")
        args = list(filter(None, args))
        using_card = False
        s_and_f = args[0].split("/")
        success = Dice().parse(s_and_f[0])
        success.roll()
        success = success.calc()
        failure = Dice().parse(s_and_f[1])
        failure.roll()
        failure = failure.calc()
        if len(args) > 1:
            card = {"san": int(args[1]), "name": "未指定调查员"}
            reply.append("[Oracle] 用户指定了应当检定的 SAN 值, 这会使得本次检定不会被记录.")
            using_card = False
        else:
            card = cards.get(event)
            using_card = True
        r = Dice().roll().calc()
        s = f"[Oracle] 调查员: {card['name']}\n"
        s += f"检定精神状态: {card['san']}\n"
        s += f"理智检定值: {r}, "
        if r <= card["san"]:
            down = success
            s += "检定成功.\n"
        else:
            down = failure
            s += "检定失败.\n"
        s += f"{card['name']} 理智降低了 {down} 点, "
        if down >= card["san"]:
            s += "陷入了永久性疯狂.\n"
        elif down >= (card["san"] // 5):
            s += "陷入了不定性疯狂.\n"
        elif down >= 5:
            s += "陷入了临时性疯狂.\n"
        else:
            s += "未受到严重影响.\n"
        card["san"] -= down
        if card["san"] <= 0:
            card["san"] = 0
        s += f"当前 {card['name']} 的 SAN 值为: {card['san']}"
        reply.append(s)
        if using_card:
            cards.update(event, card)
        return reply
    except:
        return help_messages.sc

def st():
    result = random.randint(1, 20)
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
    return "D20=%d: 命中了%s" % (result, rstr)

def at(args, event):
    inv = Investigator().load(cards.get(event))

    if args:
        d = Dice().parse(args).roll()
    else:
        d = Dice().parse("1d6").roll()
    db = Dice(inv.db()).roll()

    return f"[Oracle] 投掷 {d.db}+{db.db}=({d.total}+{db.total})\n造成了 {d.total+db.total}点 伤害."

def dam(args, message):
    card = cards.get(message)
    if not card:
        return "[Oracle] 未找到缓存数据, 请先使用`.coc`指令进行车卡生成角色卡并`.set`进行保存."
    max_hp = card["con"] + card["siz"]
    try:
        arg = int(args[0])
        card["hp"] -= arg
        r = f"[Orcale] {card['name']} 失去了 {arg}点 生命"
    except:
        d = Dice().parse("1d6").roll()
        card["hp"] -= d.total
        r = "[Oracle] 投掷 1D6={d}\n受到了 {d}点 伤害".format(d=d.calc())
    if card["hp"] <= 0:
        card["hp"] = 0
        r += f", 调查员 {card['name']} 已死亡."
    elif max_hp * 0.8 <= card["hp"] and card["hp"] < max_hp:
        r += f", 调查员 {card['name']} 具有轻微伤."
    elif max_hp * 0.6 <= card["hp"] and card["hp"] <= max_hp * 0.8:
        r += f", 调查员 {card['name']} 进入轻伤状态."
    elif max_hp * 0.2 <= card["hp"] and card["hp"] <= max_hp * 0.6:
        r += f", 调查员 {card['name']} 身负重伤."
    elif max_hp * 0.2 >= card["hp"]:
        r += f", 调查员 {card['name']} 濒死."
    else:
        r += "."
    cards.update(message, card)
    return r

def rd0(arg: str) -> str:
    args = arg.lower().split(" ")
    d_str = args.pop(0).split("#")
    try:
        parse = d_str.pop(0)
        d = Dice().parse(parse)
        _log.debug(str(parse))
        time = 1
        if len(d_str) > 0:
            try:
                time = int(d_str[0])
            except:
                pass
        anum: Optional[int] = None
        if len(args) > 0:
            try:
                anum = int(args[0])
            except ValueError:
                pass
        r = expr(d, anum)
        for _ in range(time-1):
            r += "\n"
            r += expr(d, anum)
        return r
    except ValueError:
        return help_messages.r

def ra(args, event):
    if len(args) == 0:
        return help_message("ra")
    if len(args) > 2:
        return "[Oracle] 错误: 参数过多(2需要 %d给予)." % len(args)

    card_data = cards.get(event)
    if not card_data:
        return "[Oracle] 在执行参数检定前, 请先完成车卡并保存."
    inv = Investigator().load(card_data)
    is_base = False
    for _, alias in attrs_dict.items():
        if args[0] in alias:
            v = int(eval("inv.{prop}".format(prop=alias[0])))
            is_base = True
            break
    if not is_base:
        for skill in inv.skills:
            if args[0] == skill:
                v = inv.skills[skill]
                break
            else:
                v = False
    if not v:
        return "[Oracle] 未知的参数或技能."
    d = Dice()
    time = 1
    if len(args) > 0:
        try:
            time = 1
        except:
            pass
    anum: Optional[int] = None
    if len(args) > 0:
        try:
            anum = int(v)
        except ValueError:
            pass
    r = expr(d, anum)
    for _ in range(time-1):
        r += "\n"
        r += expr(d, anum)
    return r

def ti():
    i = random.randint(1, 10)
    r = "临时疯狂判定1D10=%d\n" % i
    r += temporary_madness[i-1]
    if i == 9:
        j = random.randint(1, 100)
        r += "\n恐惧症状为: \n"
        r += phobias[j-1]
    elif i == 10:
        j = random.randint(1, 100)
        r += "\n狂躁症状为: \n"
        r += manias[j-1]
    r += "\n该症状将会持续1D10=%d" % random.randint(1, 10)
    return r

def li():
    i = random.randint(1, 10)
    r = "总结疯狂判定1D10=%d\n" % i
    r += madness_end[i-1]
    if i in [2, 3, 6, 9, 10]:
        r += "\n调查员将在1D10=%d小时后醒来" % random.randint(1, 10)
    if i == 9:
        j = random.randint(1, 100)
        r += "\n恐惧症状为: \n"
        r += phobias[j-1]
    elif i == 10:
        j = random.randint(1, 100)
        r += "\n狂躁症状为: \n"
        r += manias[j-1]
    return r

def rb(args):
    if args:
        match = re.match(r'([0-9]{1,2})([a-zA-Z\u4e00-\u9fa5]*)', args)
    else:
        match = None
    ten = []
    if match:
        t = int(match[1]) if match[1] else 1
        reason = f"由于 {match[2]}:\n" if match[2] else ""
    else:
        reason = ""
        t = 1
    for _ in range(t):
        _ = Dice("1d10").roll().calc()
        _ = _ if _ != 10 else 0
        ten.append(_)
    result = Dice("1d100").roll().calc()
    ten.append(result//10)
    ften = min(ten)
    ten.remove(result//10)
    return f"{reason}奖励骰:\nB{t}=(1D100={result}, {ten})={ften}{str(result)[-1]}"

def rp(args):
    if args:
        match = re.match(r'([0-9]{1,2})([a-zA-Z\u4e00-\u9fa5]*)', args)
    else:
        match = None
    ten = []
    if match:
        t = int(match[1]) if match[1] else 1
        reason = f"由于 {match[2]}:\n" if match[2] else ""
    else:
        reason = ""
        t = 1
    for _ in range(t):
        _ = Dice("1d10").roll().calc()
        _ = _ if _ != 10 else 0
        ten.append(_)
    result = Dice("1d100").roll().calc()
    ten.append(result//10)
    ften = max(ten)
    ten.remove(result//10)
    return f"{reason}惩罚骰:\nB{t}=(1D100={result}, {ten})={ften}{str(result)[-1]}"

# 未验证指令
def dhr(t, o):
    if t == 0 and o == 0:
        return 100
    else:
        return t*10+o

def en(args, message):
    try:
        arg = int(args[1])
    except ValueError:
        return help_messages.en
    check = random.randint(1, 100)
    if check > arg or check > 95:
        plus = random.randint(1, 10)
        r = "判定值%d, 判定成功, 技能成长%d+%d=%d" % (check, arg, plus, arg+plus)
        return r + "\n温馨提示: 如果技能提高到90%或更高, 增加2D6理智点数。"
    else:
        return "判定值%d, 判定失败, 技能无成长。" % check
