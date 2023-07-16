from messages import help_messages
from cards import cards
from botpy import logging
from dicer import Dice

_log = logging.get_logger()

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
