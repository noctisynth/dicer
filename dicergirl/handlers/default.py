from dicergirl.utils.dicer import Dicer
from dicergirl.utils.docimasy import expr
from dicergirl.utils.cards import Cards
from typing import Any, Dict, List

class DefaultCommand:
    def __init__(self, name: str, cards: Cards, cache: Cards, charactor, attrs_dict: Dict[str, List[str]]) -> None:
        self.name = name
        self.cards = cards
        self.cache = cache
        self.charactor = charactor
        self.attrs_dict = attrs_dict

class DefaultRA(DefaultCommand):
    def __init__(self, name: str, cards: Cards, cache: Cards, charactor, attrs_dict: Dict[str, List[str]]) -> None:
        super().__init__(name, cards, cache, charactor, attrs_dict)

    def __call__(self, event, args: list) -> str:
        if len(args) == 0:
            return "你在整什么活? 检定技能需要给入技能名称.\n使用`.help ra`指令查看指令使用方法."
        if len(args) > 2:
            return "给入参数过多(最多2需要但%d给予)." % len(args)
        
        card_data = self.cards.get(event)
        if not card_data:
            if len(args) == 1:
                return f"你尚未保存人物卡, 请先执行`.{self.name}`车卡并执行`.set`保存.\n如果你希望快速检定, 请执行`.ra [str: 技能名] [int: 技能值]`."

            return str(expr(Dicer(), int(args[1])))
        
        inv = self.charactor().load(card_data)

        is_base = False
        exp = None
        for _, alias in self.attrs_dict.items():
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

class DefaultAT(DefaultCommand):
    def __init__(self, roll: str="1d6") -> None:
        self.roll = roll

    def __call__(self, event, args) -> str:
        rd = Dicer(self.roll).roll()
        return f"进行伤害检定:\n{rd.description()}\n造成了 {rd.outcome} 点伤害!"

class DefaultDAM(DefaultCommand):
    def __init__(self, roll: str="1d6") -> None:
        self.roll = roll

    def __call__(self, event, args) -> str:
        rd = Dicer(self.roll).roll()
        return f"进行承伤检定:\n{rd.description()}\n受到了 {rd.outcome} 点伤害!"