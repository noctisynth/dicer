import random

from typing import Optional
from messages import help_messages, help_message
from cards import cards, attrs_dict, Investigator, expr
from dicer import Dice
from botpy import logging

_log = logging.get_logger()

class Mylist(list):
    def next(self, index: int):
        if index < self.__len__()-1:
            return self[index+1]
        else:
            return ""

def dhr(t, o):
    if t == 0 and o == 0:
        return 100
    else:
        return t*10+o


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
    d = Dice().parse("1d6").roll()
    return "[Oracle] 投掷 1D6={d}\n造成了 {d}点 伤害.".format(d=d.calc())

def dam(args, message):
    card = cards.get(message)
    max_hp = cards["con"] + cards["siz"]
    try:
        arg = int(args[0])
        card["hp"] -= arg
        r = f"[Orcale] {card['name']} 失去了 {arg}点 生命"
    except:
        d = Dice().parse("1d6").roll()
        card["hp"] -= d.total
        r = "[Oracle] 投掷 1D6={d}\n受到了 {d}点 伤害".format(d=d.calc())
    if cards["hp"] <= 0:
        cards["hp"] = 0
        r += f", 调查员 {cards['name']} 已死亡."
    elif max_hp * 0.8 <= card["hp"] < max_hp:
        r += f", 调查员 {cards['name']} 具有轻微伤."
    elif max_hp * 0.6 <= cards["hp"] <= max_hp * 0.8:
        r += f", 调查员 {cards['name']} 进入轻伤状态."
    elif max_hp * 0.2 <= cards["hp"] <= max_hp * 0.6:
        r += f", 调查员 {cards['name']} 身负重伤."
    elif max_hp * 0.2 >= card["hp"]:
        r += f", 调查员 {cards['name']} 濒死."
    else:
        r += "."
    cards.update(message, card)
        

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


def rd0(arg: str) -> str:
    _log.debug(str(arg))
    args = arg.lower().split(" ")
    d_str = args.pop(0).split("#")
    _log.debug(str(d_str))
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
    if len(args) > 2:
        return "错误: 参数过多(2需要 %d给予)." % len(args)

    card_data = cards.get(event)
    if not card_data:
        return "在执行参数检定前, 请先完成车卡并保存."
    inv = Investigator().load(card_data)
    is_base = False
    for attr, alias in attrs_dict.items():
        if args[0] in alias:
            v = int(eval("inv.{prop}".format(prop=alias[0])))
            is_base = True
            break
    if not is_base:
        for skill in inv.skills:
            if args[0] == skill:
                v = inv.skills[skill]
                break
    if len(args) == 1:
        t = 100
    else:
        t = args[-1]

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

    
