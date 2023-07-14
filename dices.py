# 参考[OlivaDiceDocs](https://oliva.dicer.wiki/userdoc)实现的nonebot2骰娘插件
import random
from typing import Optional
import diro
from messages import help_messages
from cards import cards, attrs_dict, Investigator, expr

class Mylist(list):
    def next(self, index: int):
        if index < self.__len__()-1:
            return self[index+1]
        else:
            return ""


def help_message(args: str):
    if args in help_messages.__dict__.keys():
        return help_messages.__dict__[args]
    else:
        return help_messages.main


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


def en(arg: str) -> str:
    try:
        arg = int(arg)
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
    args = arg.lower().split(" ")
    d_str = args.pop(0).split("#")
    try:
        d = diro.parse(d_str.pop(0))
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
    for attr, alias in attrs_dict.items():
        if args[0] in alias:
            v = int(eval("inv.{prop}".format(prop=alias[0])))
            break
    if len(args) == 1:
        t = 100
    else:
        t = args[-1]

    d = diro.parse("")
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

    
