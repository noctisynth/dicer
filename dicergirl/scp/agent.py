import random
try:
    from ..utils.dicer import Dice
except ImportError:
    from dicergirl.utils.dicer import Dice

class Agent(object):
    def __init__(self) -> None:
        self.name = "无名特工"
        self.age = 20
        self.sex = "女"
        self.str = 0
        self.hth = 0
        self.per = 0
        self.dex = 0
        self.fte = 0
        self.chr = 0
        self.int = 0
        self.wil = 0
        self.hp_max = 0
        self.hp = 0
        self.enp = 0
        self.dices = {}
        self.skills = {}
        self.tools = {}

    def init(self):
        prop = {
            "str": 1,
            "hth": 1,
            "per": 1,
            "dex": 1,
            "fte": 1,
            "chr": 1,
            "int": 1,
            "wil": 1
        }
        attr = {
            "str": 1,
            "hth": 1,
            "per": 1,
            "dex": 1,
            "fte": 1,
            "chr": 1,
            "int": 1,
            "wil": 1
        }
        total = 20 - len(prop)
        for _ in range(total):
            name = random.choice(list(prop.keys()))
            prop[name] += 1

        for p in prop.keys():
            num = prop[p]
            dice = Dice(f"{num}d8", explode=True)
            dice.roll()
            prop[p] = dice.total
            attr[p] = dice.dices

        self.dices = attr
        self.__dict__.update(prop)
        self.reset_hp()
        self.reset_enp()

    def reset_hp(self):
        base = 10
        for d in self.dices["hth"]:
            if d == "D8":
                base += 3
            elif d == "D10":
                base += 6
            elif d == "D12":
                base += 16
        self.hp_max = base
        self.hp = base
    
    def reset_enp(self):
        base = 1
        for d in self.dices["wil"]:
            if d == "D10":
                base += 1
        self.enp = base

    def age_check(self, age=20):
        if self.age != 20:
            return
        if age < 15:
            return "[scpdicer] 年龄过小, 无法担任基金会特工."
        elif age >= 90:
            return "该特工已经被清理, 他(或者她)年龄过大, 显然是一个需要被清理的异常."
        self.age = age

    def __repr__(self) -> str:
        data = "姓名: %s\n" % self.name
        data += "性别: %s 年龄: %d\n" % (self.sex, self.age)
        data += "强度: %d 命运: %d\n" % (self.str, self.fte)
        data += "感知: %d 魅力: %d\n" % (self.per, self.chr) 
        data += "灵巧: %d 情报: %d\n" % (self.dex, self.int)
        data += "健康: %d 意志: %d\n" % (self.hth, self.wil)
        data += "激励点: %d\n" % (self.enp)
        data += "生命: %d/%d" % (self.hp, self.hp_max)
        return data

    def skills_output(self) -> str:
        if not self.skills:
            return "%s 当前无任何技能数据。" % self.name
        r = "%s技能数据: " % self.name
        for k, v in self.skills.items():
            r += "\n%s: %d" % (k, v)
        return r

    def output(self) -> str:
        return self.__repr__()

    def load(self, data: dict):
        self.__dict__.update(data)
        return self
