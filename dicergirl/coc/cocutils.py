from dicergirl.utils.docimasy import expr
from dicergirl.utils.messages import temporary_madness, madness_end, phobias, manias
from dicergirl.utils.dicer import Dicer
from multilogging import multilogger
from .coccards import coc_cards, coc_attrs_dict
from .investigator import Investigator

import random

logger = multilogger(name="Dicer Girl", payload="COCUtil")

def sc(arg, event):
    """ COC 疯狂检定 """
    reply = []
    try:
        args = arg.split(" ")
        args = list(filter(None, args))
        using_card = False
        s_and_f = args[0].split("/")
        success = Dicer().parse(s_and_f[0])
        success.roll()
        success = success.calc()
        failure = Dicer().parse(s_and_f[1])
        failure.roll()
        failure = failure.calc()
        if len(args) > 1:
            card = {"san": int(args[1]), "name": "未指定调查员"}
            reply.append("[Oracle] 用户指定了应当检定的 SAN 值, 这会使得本次检定不会被记录.")
            using_card = False
        else:
            card = coc_cards.get(event)
            using_card = True
        r = Dicer().roll().calc()
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
            coc_cards.update(event, card)
        return reply
    except:
        return "[Oracle] 产生了未知的错误, 你可以使用`.help sc`指令查看指令使用方法.\n如果你确信这是一个错误, 建议联系开发者获得更多帮助.\n如果你是具有管理员权限, 你可以使用`.debug on`获得更多信息."

def coc_at(event, args):
    """ COC 伤害检定 """
    inv = Investigator().load(coc_cards.get(event))
    method = "+"

    if args:
        d = Dicer().parse(args).roll()
    else:
        d = Dicer().parse("1d6").roll()

    if "d" in inv.db():
        db = Dicer(inv.db()).roll()
        dbtotal = db.outcome
        db = db.db
    else:
        db = int(inv.db())
        dbtotal = db
        if db < 0:
            method = ""

    return f"[Oracle] 投掷 {d.db}{method}{db}=({d.outcome}+{dbtotal})\n造成了 {d.outcome+dbtotal}点 伤害."

def coc_dam(event, args):
    """ COC 承伤检定 """
    card = coc_cards.get(event)
    if not card:
        return "[Oracle] 未找到缓存数据, 请先使用`.coc`指令进行车卡生成角色卡并`.set`进行保存."
    max_hp = card["con"] + card["siz"]
    try:
        arg = int(args[0])
        card["hp"] -= arg
        r = f"[Orcale] {card['name']} 失去了 {arg}点 生命"
    except:
        d = Dicer().parse("1d6").roll()
        card["hp"] -= d.outcome
        r = "[Oracle] 投掷 1D6={d}\n受到了 {d}点 伤害".format(d=d.calc())
    if card["hp"] <= 0:
        card["hp"] = 0
        r += f", 调查员 {card['name']} 已死亡."
    elif (max_hp * 0.8) <= card["hp"] and (card["hp"] < max_hp):
        r += f", 调查员 {card['name']} 具有轻微伤."
    elif (max_hp * 0.6 <= card["hp"]) and (card["hp"] <= max_hp * 0.8):
        r += f", 调查员 {card['name']} 进入轻伤状态."
    elif (max_hp * 0.2 <= card["hp"]) and (card["hp"] <= max_hp * 0.6):
        r += f", 调查员 {card['name']} 身负重伤."
    elif max_hp * 0.2 >= card["hp"]:
        r += f", 调查员 {card['name']} 濒死."
    else:
        r += "."
    coc_cards.update(event, card)
    return r

def coc_ra(event, args):
    """ COC 技能检定 """
    if len(args) == 0:
        return "[Oracle] 错误: 检定技能需要给入技能名称.\n使用`.help ra`指令查看指令使用方法."
    if len(args) > 2:
        return "[Oracle] 错误: 参数过多(最多2需要但%d给予)." % len(args)

    card_data = coc_cards.get(event)
    if not card_data:
        if len(args) == 1:
            return "[Oracle] 你尚未保存人物卡, 请先执行`.coc`车卡并执行`.set`保存.\n如果你希望快速检定, 请执行`.ra [str: 技能名] [int: 技能值]`."

        return str(expr(Dicer(), args[1]))

    inv = Investigator().load(card_data)

    is_base = False
    exp = None
    for _, alias in coc_attrs_dict.items():
        if args[0] in alias:
            exp = int(getattr(inv, alias[0]))
            is_base = True
            break

    if not is_base:
        for skill in inv.skills:
            if args[0] == skill:
                exp = inv.skills[skill]
                break
            else:
                exp = False

    if not exp:
        if len(args) == 1:
            return "[Oracle] 你没有这个技能, 如果你希望快速检定, 请执行`.ra [str: 技能名] [int: 技能值]`."

        if not args[1].isdigit():
            return "[Oracle] 技能值应当为整型数, 使用`.help ra`查看技能检定指令使用帮助."

        return str(expr(Dicer(), int(args[1])))
    elif exp and len(args) > 1:
        if not args[1].isdigit():
            return "[Oracle] 技能值应当为整型数, 使用`.help ra`查看技能检定指令使用帮助."

        reply = [f"[Oracle] 你已经设置了技能 {args[0]} 为 {exp}, 但你指定了检定值, 使用指定检定值作为替代."]
        reply.append(str(expr(Dicer(), int(args[1]))))
        return reply

    time = 1
    r = expr(Dicer(), exp)

    for _ in range(time-1):
        r += expr(Dicer(), exp)

    return r.detail

def ti():
    """ COC 临时疯狂检定 """
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
    """ COC 总结疯狂检定 """
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

def coc_en(event, args):
    """ COC 技能成长检定 """
    if not args:
        return "[Oracle] 错误: 检定技能需要给入技能名称.\n使用`.help ra`指令查看指令使用方法."

    try:
        arg = int(args[1])
    except ValueError:
        return "[Oracle] 错误: 给定需要消耗的激励点应当为整型数.\n使用`.help ra`指令查看指令使用方法."

    check = random.randint(1, 100)

    if check > arg or check > 95:
        plus = random.randint(1, 10)
        r = "判定值%d, 判定成功, 技能成长%d+%d=%d" % (check, arg, plus, arg+plus)
        return r + "\n温馨提示: 如果技能提高到90%或更高, 增加2D6理智点数。"
    else:
        return "判定值%d, 判定失败, 技能无成长。" % check