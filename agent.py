import random
from dicer import Dice

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
        attr = prop
        total = 20 - len(prop)
        dice = Dice("1d8")
        for _ in range(total):
            name = random.choice(list(prop.keys()))
            prop[name] += 1

        for p in prop.keys():
            num = prop[p]
            attr[p] = 0
            for i in range(num):
                attr[p] += dice.roll().total

        self.__dict__.update(attr)

    def age_check(self, age=20) -> str:
        if self.age != 20:
            return
        if age < 15:
            return "[scpdicer] 年龄过小, 无法担当基金会特工."
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
