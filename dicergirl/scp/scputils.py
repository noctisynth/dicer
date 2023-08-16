try:
    from ..utils.messages import help_messages, help_message
    from ..utils.dicer import Dice, scp_doc, expr
    from .scpcards import scp_cards
    from .attributes import all_names, scp_attrs_dict as attrs_dict, weapons, all_alias, all_alias_dict
    from .agent import Agent
    from ..utils.multilogging import multilogger
except ImportError:
    from dicergirl.utils.messages import help_messages, help_message
    from dicergirl.utils.dicer import Dice, scp_doc, expr
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
        print(upper.keys())
        print(args.upper())
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
        card["hp"] = 0
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

def sra(args, event):
    if len(args) == 0:
        return help_message("sra")
    elif len(args) > 4:
        return "[Oracle] 错误: 参数过多(最多4需要但%d给予)." % len(args)
    
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
                exp = getattr(inv, anb[args[2]])[args[2]]
                is_skill = True
            elif not is_validated_skill:
                return f"[Oracle] 错误: 基础属性 {args[0]} 不存在."
            else:
                return f"[Oracle] 错误: 技能、知识或能力 {args[2]} 不存在."
        else:
            return help_messages.sra
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

    if not is_base and not is_skill and not skill_only:
        if args[0] in inv.skills.keys():
            exp = inv.skills[args[0]]
            return expr(Dice(), int(exp))
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
    return r

def scp_en(event, args):
    if not args:
        return help_messages.en

    try:
        en = int(args[1])
        if not en:
            return f"[Oracle] 无法进行发起 {en} 点激励."
    except ValueError:
        return help_messages.en

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