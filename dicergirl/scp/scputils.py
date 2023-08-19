try:
    from ..utils.docimasy import expr, scp_doc
    from ..utils.dicer import Dice
    from .scpcards import scp_cards
    from .attributes import all_names, scp_attrs_dict as attrs_dict, weapons, all_alias, all_alias_dict
    from .agent import Agent
    from ..utils.multilogging import multilogger
except ImportError:
    from dicergirl.utils.docimasy import expr, scp_doc
    from dicergirl.utils.dicer import Dice
    from dicergirl.scp.scpcards import scp_cards
    from dicergirl.scp.attributes import all_names, scp_attrs_dict as attrs_dict, weapons, all_alias, all_alias_dict
    from dicergirl.scp.agent import Agent
    from dicergirl.utils.multilogging import multilogger

import random

logger = multilogger(name="Dicer Girl", payload="SCPUtil")

def at(args, event):
    card = scp_cards.get(event)
    agt = Agent().load(card)
    all_dices = []

    if not args:
        dices = [dice for dice in agt.dices["str"]]

        if len(dices) > 4:
            while len(all_dices) != 4:
                choice = random.choice(dices)
                all_dices.append(choice)
                dices.remove(choice)
        elif len(dices) <= 4:
            all_dices = dices

        results = []
        for dice in all_dices:
            dice = Dice("1"+dice.lower()).roll()
            results.append(dice.total)

        result = max(results)

        if len(results) > 1:
            results.remove(result)
            result += max(results)

        return f"[Oracle] 特工发起近战格斗伤害检定, 检定造成了 {result} 点 伤害."
    else:
        args = "".join(args)

        upper = {name.upper(): [tool, name] for name, tool in agt.tools.items()}
        if not args.upper() in upper.keys():
            return f"[Oracle] 看起来该特工并未购置 {args.upper()}."

        return f"[Oracle] 特工使用 {upper[args.upper()][1]} 发起攻击, 检定造成了 {Dice(upper[args.upper()][0]['base']).roll().calc()} 点 伤害."

def deal(event, args):
    if len(args) > 0:
        args = "".join(args).upper()

    card = scp_cards.get(event)
    level = card["level"]
    reply = ""

    if not args:
        reply += f"特工权限: {level}\n"

        for lvl in range(level):
            reply += f"Level {lvl+1} 准允购置的装备:"
            for weapon in weapons[lvl+1].keys():
                reply += f"\n  {weapon}: {weapons[lvl+1][weapon]['price']}￥"

            reply += "\n"

        return reply
    
    allowed_upper = {}
    for lvl in weapons.keys():
        allowed_upper.update({allow.upper(): [lvl, weapon, allow] for allow, weapon in weapons[lvl].items()})

    if args in allowed_upper.keys():
        real_name = allowed_upper[args][2]
        if allowed_upper[args][1]['price'] > card['money']:
            return f"[Oracle] 该特工囊中羞涩, 无法购置装备 {args}.\n贫穷是人类社会生存中的重大危机, 很高兴, 你距离危险更近了一步."

        card['money'] -= allowed_upper[args][1]['price']
        agt = Agent().load(card)
        agt.tools[real_name] = allowed_upper[args][1]
        scp_cards.update(event, agt.__dict__, save=True)
        return f"[Oracle] 特工购置了 1 件 {real_name}."
    else:
        return f"[Oracle] 装备 {real_name} 不存在或特工权限不足."

def scp_dam(args, message):
    card = scp_cards.get(message)

    if not card:
        return "[Oracle] 未找到缓存数据, 请先使用`.scp`指令进行车卡生成角色卡并`.set`进行保存."

    max_hp = card["hp_max"]

    if len(args) == 1:
        if not args[0] in ["check", "c"]:
            arg = int(args[0])
            card["hp"] -= arg
            r = f"[Orcale] {card['name']} 失去了 {arg}点 生命"
        else:
            r = "检查特工状态"
    elif len(args) == 0:
        d = Dice().parse("1d6").roll()
        card["hp"] -= d.total
        r = "[Oracle] 投掷 1D6={d}\n受到了 {d}点 伤害".format(d=d.calc())
    elif len(args) == 3:
        if args[1] != "d":
            r = "[Oracle] 未知的指令格式."
        else:
            d = Dice().parse(f"{args[0]}{args[1]}{args[2]}").roll()
            card["hp"] -= d.total
            r = f"[Oracle] 投掷 {args[0]}D{args[2]}={d.calc()}\n受到了 {d.calc()}点 伤害"

    if card["hp"] <= 0:
        r += f", 特工 {card['name']} 已死亡."
    elif (max_hp * 0.8 <= card["hp"]) and (card["hp"] < max_hp):
        r += f", 特工 {card['name']} 具有轻微伤势."
    elif (max_hp * 0.6 <= card["hp"]) and (card['hp'] <= max_hp * 0.8):
        r += f", 特工 {card['name']} 具有轻微伤."
    elif (max_hp * 0.4 <= card["hp"]) and (card["hp"] <= max_hp * 0.6):
        r += f", 特工 {card['name']} 具有轻伤."
    elif (max_hp * 0.2 <= card["hp"]) and (card["hp"] <= max_hp * 0.4):
        r += f", 特工 {card['name']} 身负重伤."
    elif max_hp * 0.2 >= card["hp"]:
        r += f", 特工 {card['name']} 濒死."
    else:
        r += "."

    scp_cards.update(message, card)
    return r

def sra(args: list, event):
    if len(args) == 0:
        return "[Oracle] 错误: 检定技能需要给入技能名称.\n使用`.help ra`指令查看指令使用方法."
    elif len(args) > 4:
        return "[Oracle] 错误: 参数过多(最多4需要但%d给予).\n使用`.help ra`指令查看指令使用方法." % len(args)

    try:
        difficulty = int(args[-1])
        args.remove(args[-1])
    except ValueError:
        difficulty = 12

    card_data = scp_cards.get(event)

    if not card_data:
        return "[Oracle] 在执行参数检定前, 请先执行`.scp`车卡并执行`.set`保存."

    inv = Agent().load(card_data)

    is_base = False
    if len(args) == 1:
        for alias in attrs_dict.values():
            if args[0] in alias:
                dices = [dice for dice in inv.dices[alias[0]]]
                to_ens = [alias[0]]
                is_base = True
                break

    is_skill = False
    skill_only = False
    if not is_base and len(args) == 3:
        if args[1] in ["+", "/", "&", "*"]:
            is_validated_skill = False
            for alias in attrs_dict.values():
                if args[0] in alias:
                    dices = [dice for dice in inv.dices[alias[0]]]
                    to_ens = [alias[0]]
                    is_validated_skill = True
                    break

            anb = inv.all_not_base()
            if args[2] in anb.keys() and is_validated_skill:
                skill_name = [args[2], anb[args[2]]]
                exp = getattr(inv, anb[args[2]])[args[2]]
                is_skill = True
            elif not is_validated_skill:
                return f"[Oracle] 错误: 基础属性 {args[0]} 不存在."
            else:
                return f"[Oracle] 错误: 技能、知识或能力 {args[2]} 不存在."
        else:
            return "[Oracle] 我无法解析你的语法, 你可以使用`.help ra`指令查看指令使用方法.\n如果你确信这是一个错误, 建议联系开发者获得更多帮助.\n如果你是具有管理员权限, 你可以使用`.debug on`获得更多信息."
    elif not is_base and len(args) == 1:
        if args[0] in all_alias:
            anb = inv.all_not_base()
            key_name = all_alias_dict[args[0]]
            exp = getattr(inv, anb[key_name])[key_name]
            skill_only = True
            if anb[key_name] == "knowledge":
                to_ens = ["int", "per"]
                to_en = random.choice(to_ens)
                dices = [dice for dice in (inv.dices[to_en])]
            elif anb[key_name] == "skills":
                to_ens = ["str", "dex"]
                to_en = random.choice(to_ens)
                dices = [dice for dice in (inv.dices[to_en])]
            elif anb[key_name] == "ability":
                to_ens = ["chr", "wil"]
                to_en = random.choice(to_ens)
                dices = [dice for dice in (inv.dices[to_en])]
            else:
                skill_only = False
            skill_name = [key_name, anb[key_name]]

    if not is_base and not is_skill and not skill_only:
        if args[0] in inv.skills.keys():
            exp = inv.skills[args[0]]
            return str(expr(Dice(), int(exp)))
        else:
            return "[Oracle] 错误: 没有这个数据或技能."

    all_dices = []

    if len(dices) > 4:
        while len(all_dices) != 4:
            choice = random.choice(dices)
            all_dices.append(choice)
            dices.remove(choice)
    elif len(dices) <= 4:
        all_dices = dices

    results = []
    great = False
    for dice in all_dices:
        dice = Dice("1"+dice.lower()).roll()
        results.append(dice.total)
        if dice.great:
            great = True

    result = max(results)

    if len(results) > 1:
        results.remove(result)
        result += max(results)

    if is_skill or skill_only:
        result += exp

    encourage = None
    for en in card_data["en"]:
        if en in to_ens:
            encourage = card_data["en"][en]
            card_data["en"].pop(en)
            scp_cards.update(event, card_data)
            break

    r = scp_doc(result, difficulty, encourage=encourage, agent=inv.name, great=great)

    if is_skill or skill_only:
        if r.judge == 1:
            card_data["p"][skill_name[1]] += 0.1
        elif r.judge > 1:
            card_data["p"][skill_name[1]] += 1
        scp_cards.update(event, card_data)

    return r.detail

def scp_en(event, args):
    if not args:
        return "[Oracle] 错误: 你没有给定需要激励的基础属性.\n使用`.help en`指令查看指令使用方法."

    try:
        en = int(args[1])
        if not en:
            return f"[Oracle] 无法进行发起 {en} 点激励."
    except ValueError:
        return "[Oracle] 错误: 给定需要消耗的激励点应当为整型数.\n使用`.help en`指令查看指令使用方法."

    card_data = scp_cards.get(event)

    if card_data["enp"] < en:
        return f"[Oracle] 你仅剩的激励点无法进行发起 {en} 点激励."
    
    agt = Agent().load(card_data)

    for alias in attrs_dict.values():
        if args[0] in alias:
            to_en = alias[0]
            is_validated_skill = True
            break
    
    if not is_validated_skill:
        return f"[Oracle] 不存在的基础属性 {args[0]} 无法被激励."

    agt.enp -= en
    agt.en[to_en] = en
    scp_cards.update(event, agt.__dict__, save=True)

    return f"[Oracle] 你的 {args[0]} 受到了 {en} 点激励."

def begin():
    reply = []
    reply.append("人类到如今已经繁衍了 250000 年, 只有最近的4000 年是有意义的.")
    reply.append("所以, 我们在将近 250000 年中在干什么? ")
    reply.append("我们躲在山洞中, 围坐在小小的篝火边, 畏惧那些我们不懂得的事物——那些关于太阳如何升起的解释, 那些人头鸟身的怪物, 那些有生命的石头.")
    reply.append("所以我们称他们为“神”和“恶魔”, 并向他们祈求宽恕和祈祷拯救. ")
    reply.append("之后, 他们的数量在减少, 我们的数量在增加.")
    reply.append("当我们恐惧的事物越来越少, 我们开始更理智的看待这个世界.")
    reply.append("然而, 不能解释的事物并没有消失, 就好像宇宙故意要表现出荒谬与不可思议一样.")
    reply.append("人类不能再生活在恐惧中.")
    reply.append("没有东西能保护我们, 我们必须保护我们自己.")
    reply.append("当其他人在阳光下生活时, 我们必须在阴影中和它们战斗, 并防止它们暴露在大众眼中, 这样其他人才能生活在一个理智的, 普通的世界中.")
    reply.append("我们控制, 我们收容, 我们保护.")
    reply.append("——The Administrator")
    return reply