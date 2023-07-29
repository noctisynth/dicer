try:
    from ..utils.utils import _coc_cachepath, _scp_cachepath, logger as _log, get_group_id
    from ..utils.dicer import Dice, expr
    from ..utils.messages import help_messages
    from ..coc.investigator import Investigator
    from ..coc.coccards import cache_cards, cards, attrs_dict
    from ..scp.agent import Agent
    from ..scp.scpcards import scp_cache_cards, scp_cards, scp_attrs_dict
except ImportError:
    from dicergirl.utils.utils import _coc_cachepath, _scp_cachepath, logger as _log, get_group_id
    from dicergirl.utils.dicer import Dice, expr
    from dicergirl.utils.messages import help_messages
    from dicergirl.coc.investigator import Investigator
    from dicergirl.coc.coccards import cache_cards, cards, attrs_dict
    from dicergirl.scp.agent import Agent
    from dicergirl.scp.scpcards import scp_cache_cards, scp_cards, scp_attrs_dict

def set_handler(message, args):
    if not args:
        if cache_cards.get(message):
            card_data = cache_cards.get(message)
            cards.update(message, inv_dict=card_data)
            inv = Investigator().load(card_data)
            return "[Oracle] 成功从缓存保存人物卡属性: \n" + inv.output()
        else:
            return "[Oracle] 未找到缓存数据, 请先使用coc指令进行车卡生成角色卡."
    else:
        if cards.get(message):
            card_data = cards.get(message)
            inv = Investigator().load(card_data)
        else:
            return "[Oracle] 未找到已保存数据, 请先使用空白set指令保存角色数据."
        if len(args) % 2 != 0:
            return "[Oracle] 参数错误, 这是由于传输的数据数量错误, 我只接受为偶数的参数数量, 因为我无法连接到OpenAI, 这使得我无法使用 GPT-4 作为神经网络引擎, 我使用 TensorFlow 作为替代.\n此外, 这看起来不像是来源于我的错误."
        elif len(args) == 2:
            for attr, alias in attrs_dict.items():
                if args[0] in alias:
                    if attr in ["名字", "性别"]:
                        if attr == "性别" and not args[1] in ["男", "女"]:
                            return "[Oracle] 欧若可拒绝将调查员性别将设置为 {sex}, 这是对物种的侮辱.".format(sex=args[1])
                        inv.__dict__[alias[0]] = args[1]
                    else:
                        try:
                            inv.__dict__[alias[0]] = int(args[1])
                        except ValueError:
                            return "[Oracle] 请输入正整数属性数据"
                    cards.update(message, inv.__dict__)
                    return "[Oracle] 设置调查员%s为: %s" % (attr, args[1])
            try:
                inv.skills[args[0]] = int(args[1])
                cards.update(message, inv.__dict__)
                return "[Oracle] 设置调查员 %s 技能为: %s." % (args[0], args[1])
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
                    return "[Oracle] 参数错误, 可能是 Python 解释器的错误, 请检查该服务的 Python 版本, 我无法解析到我当前承载的服务器状态, 因为开发者并未给我提供 API 接口.\n此外, 这看起来不像是来源于我的错误."
            for sub_li in li:
                has_set = False
                for attr, alias in attrs_dict.items():
                    if sub_li[0] in alias:
                        if attr in ["名字", "性别"]:
                            if attr == "性别" and not sub_li[1] in ["男", "女"]:
                                return "[Oracle] 欧若可拒绝将调查员性别将设置为 {sex}, 这是对物种的侮辱.".format(sex=sub_li[1])
                            inv.__dict__[alias[0]] = sub_li[1]
                        else:
                            try:
                                inv.__dict__[alias[0]] = int(sub_li[1])
                            except ValueError:
                                reply.append("基础数据 %s 要求正整数数据, 但你传入了 %s." % (sub_li[0], sub_li[1]))
                                continue
                        cards.update(message, inv.__dict__)
                        reply.append("设置调查员基础数据 %s 为: %s" % (attr, sub_li[1]))
                        has_set = True
                if has_set:
                    continue
                try:
                    inv.skills[sub_li[0]] = int(sub_li[1])
                    cards.update(message, inv.__dict__)
                    reply.append("设置调查员 %s 技能为: %s." % (sub_li[0], sub_li[1]))
                except ValueError:
                    reply.append("技能 %s 要求正整数数据, 但你传入了 %s." % (sub_li[0], sub_li[1]))
            rep = "[Oracle]\n"
            for r in reply:
                rep += r + "\n"
            return rep.rstrip("\n")
        else:
            return "[Oracle] 参数错误, 可能是由于传输的数据数量错误, 此外, 这看起来不像是来源于我的错误."


def show_handler(message, args):
    r = []
    if not args:
        if cards.get(message):
            card_data = cards.get(message)
            inv = Investigator().load(card_data)
            data = "[Oracle] 使用中人物卡: \n" 
            data += inv.output() + "\n"
            data += inv.skills_output()
            r.append(data)
        if cache_cards.get(message):
            card_data = cache_cards.get(message)
            inv = Investigator().load(card_data)
            r.append("[Oracle] 已暂存人物卡: \n" + inv.output())
    elif args[0] in ["skill", "s", "skills"]:
        if cards.get(message):
            card_data = cards.get(message)
            inv = Investigator().load(card_data)
            r.append(inv.skills_output())
    elif args[0] == "all":
        cd = cards.data[get_group_id(message)]
        for data in cd:
            inv = Investigator().load(cd[data])
            d = inv.output() + "\n"
            d += inv.skills_output()
            r.append(d)
    else:
        r.append("[Oracle] 参数异常.")
    if not r:
        r.append("[Oracle] 未查询到保存或暂存信息.")
    return r

def del_handler(message, args: str):
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

def scp_set_handler(message, args):
    if not args:
        if scp_cache_cards.get(message):
            card_data = scp_cache_cards.get(message)
            scp_cards.update(message, inv_dict=card_data)
            inv = Agent().load(card_data)
            return "[Oracle] 成功从缓存保存人物卡属性: \n" + inv.output()
        else:
            return "[Oracle] 未找到缓存数据, 请先使用`.scp`指令进行车卡生成角色卡."
    else:
        if scp_cards.get(message):
            card_data = scp_cards.get(message)
            inv = Agent().load(card_data)
        else:
            return "[Oracle] 未找到已保存数据, 请先使用空白`.set`指令保存角色数据."
        if len(args) % 2 != 0:
            return "[Oracle] 参数错误, 这是由于传输的数据数量错误, 我只接受为偶数的参数数量, 因为我无法连接到OpenAI, 这使得我无法使用 GPT-4 作为神经网络引擎, 我使用 TensorFlow 作为替代.\n此外, 这看起来不像是来源于我的错误."
        elif len(args) == 2:
            for attr, alias in scp_attrs_dict.items():
                if args[0] in alias:
                    if attr in ["名字", "性别"]:
                        if attr == "性别" and not args[1] in ["男", "女"]:
                            return "[Oracle] 欧若可拒绝将基金会特工性别将设置为 {sex}, 这是对物种的侮辱.".format(sex=args[1])
                        inv.__dict__[alias[0]] = args[1]
                    else:
                        try:
                            inv.__dict__[alias[0]] = int(args[1])
                        except ValueError:
                            return "[Oracle] 请输入正整数属性数据"
                    scp_cards.update(message, inv.__dict__)
                    return "[Oracle] 设置基金会特工 %s 为: %s" % (attr, args[1])
            try:
                inv.skills[args[0]] = int(args[1])
                scp_cards.update(message, inv.__dict__)
                return "[Oracle] 设置基金会特工 %s 技能为: %s." % (args[0], args[1])
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
                    return "[Oracle] 参数错误, 可能是 Python 解释器的错误, 请检查该服务的 Python 版本, 我无法解析到我当前承载的服务器状态, 因为开发者并未给我提供 API 接口.\n此外, 这看起来不像是来源于我的错误."
            for sub_li in li:
                has_set = False
                for attr, alias in scp_attrs_dict.items():
                    if sub_li[0] in alias:
                        if attr in ["名字", "性别"]:
                            if attr == "性别" and not sub_li[1] in ["男", "女"]:
                                return "[Oracle] 欧若可拒绝将基金会特工性别将设置为 {sex}, 这是对物种的侮辱.".format(sex=sub_li[1])
                            inv.__dict__[alias[0]] = sub_li[1]
                        else:
                            try:
                                inv.__dict__[alias[0]] = int(sub_li[1])
                            except ValueError:
                                reply.append("基础数据 %s 要求正整数数据, 但你传入了 %s." % (sub_li[0], sub_li[1]))
                                continue
                        scp_cards.update(message, inv.__dict__)
                        reply.append("设置基金会特工基础数据 %s 为: %s" % (attr, sub_li[1]))
                        has_set = True
                if has_set:
                    continue
                try:
                    inv.skills[sub_li[0]] = int(sub_li[1])
                    scp_cards.update(message, inv.__dict__)
                    reply.append("设置基金会特工 %s 技能为: %s." % (sub_li[0], sub_li[1]))
                except ValueError:
                    reply.append("技能 %s 要求正整数数据, 但你传入了 %s." % (sub_li[0], sub_li[1]))
            rep = "[Oracle]\n"
            for r in reply:
                rep += r + "\n"
            return rep.rstrip("\n")
        else:
            return "[Oracle] 参数错误, 可能是由于传输的数据数量错误, 此外, 这看起来不像是来源于我的错误."

def scp_show_handler(message, args):
    r = []
    if not args:
        if scp_cards.get(message):
            card_data = scp_cards.get(message)
            inv = Agent().load(card_data)
            data = "[Oracle] 使用中人物卡: \n" 
            data += inv.output() + "\n"
            data += inv.skills_output()
            r.append(data)
        if scp_cache_cards.get(message):
            card_data = scp_cache_cards.get(message)
            inv = Agent().load(card_data)
            r.append("[Oracle] 已暂存人物卡: \n" + inv.output())
    elif args[0] in ["skill", "s", "skills"]:
        if scp_cards.get(message):
            card_data = scp_cards.get(message)
            inv = Agent().load(card_data)
            r.append(inv.skills_output())
    elif args[0] == "all":
        cd = scp_cards.data[get_group_id(message)]
        for data in cd:
            inv = Agent().load(cd[data])
            d = inv.output() + "\n"
            d += inv.skills_output()
            r.append(d)
    else:
        r.append("[Oracle] 参数异常.")
    if not r:
        r.append("[Oracle] 未查询到保存或暂存信息.")
    return r

def scp_del_handler(message, args: str):
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

def sa_handler(message, args: str):
    args = args.split(" ")
    args = list(filter(None, args))
    if args:
        args = args[0]
    else:
        args = None
    if not args:
        return help_messages.sa
    elif not scp_cards.get(message):
        return "[Oracle] 请先使用`.set`指令保存人物卡后再使用快速检定功能."
    for attr, alias in attrs_dict.items():
        if args in alias:
            arg = alias[0]
            break
        else:
            arg = None
    if not arg:
        return f"[Oracle] 错误: 目标参数不在 {attrs_dict} 之内."
    card_data = scp_cards.get(message)
    dices = Dice()
    try:
        data = card_data[arg]
        if arg != "名字":
            val = int(data)
        else:
            val = None
    except KeyError:
        return f"[Oracle] 致命错误: 存储的数据 {data} 转化为数字的时候出现错误."
    if not isinstance(val, int):
        return f"[Oracle] 错误: 参数 {arg} 不可以进行快速检定, 即便它在合法指令中, 因为它没有数值.\n\
            如果你确信这是一个错误, 请尝试重新车卡或联系管理员."
    return expr(dices, val)
