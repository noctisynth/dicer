from cocmessages import help_messages, temporary_madness, madness_end, phobias, manias, help_message
from botpy import logging
from dicer import Dice, scp_doc
from typing import Optional
from scpcards import scp_cards, attrs_dict, Agent

import random

_log = logging.get_logger()

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

def at(args):
    if args:
        d = Dice().parse(args).roll()
    else:
        d = Dice().parse("1d6").roll()
    return f"[Oracle] 投掷 {d.db}={d.total}\n造成了 {d.total}点 伤害."

def dam(args, message):
    card = scp_cards.get(message)
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
    elif max_hp * 0.8 <= card["hp"] < max_hp:
        r += f", 调查员 {card['name']} 具有轻微伤."
    elif max_hp * 0.6 <= card["hp"] <= max_hp * 0.8:
        r += f", 调查员 {card['name']} 进入轻伤状态."
    elif max_hp * 0.2 <= card["hp"] <= max_hp * 0.6:
        r += f", 调查员 {card['name']} 身负重伤."
    elif max_hp * 0.2 >= card["hp"]:
        r += f", 调查员 {card['name']} 濒死."
    else:
        r += "."
    scp_cards.update(message, card)
    return r

def sra(args, event):
    if len(args) > 2:
        return "错误: 参数过多(最多2需要但%d给予)." % len(args)
    
    if len(args) == 2:
        difficulty = int(args[1])
    else:
        difficulty = 12

    card_data = scp_cards.get(event)
    if not card_data:
        return "在执行参数检定前, 请先完成`.scp`车卡并`.sset`保存."
    inv = Agent().load(card_data)
    is_base = False
    for attr, alias in attrs_dict.items():
        if args[0] in alias:
            dices: list = eval("inv.dices['{prop}']".format(prop=alias[0]))
            is_base = True
            break
    if not is_base:
        for skill in inv.skills:
            if args[0] == skill:
                v = inv.skills[skill]
                break
    result = 0
    all_dices = []
    if len(dices) > 4:
        while True:
            if len(all_dices) == 4:
                break
            choice = random.choice(dices)
            all_dices.append(choice)
            dices.remove(choice)
    elif len(dices) <= 4:
        all_dices = dices
    
    great = False
    for dice in all_dices:
        dice = Dice("1"+dice.lower()).roll()
        result += dice.total
        if dice.great == True:
            great = True
    r = scp_doc(result, difficulty, agent=inv.name, great=great)
    return r


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
