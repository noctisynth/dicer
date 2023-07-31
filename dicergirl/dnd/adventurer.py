try:
    from ..utils.dicer import Dice
except ImportError:
    from dicergirl.utils.dicer import Dice

class Adventurer(object):
    def __init__(self) -> None:
        self.name = "无名冒险者"
        self.age = 20
        self.sex = "女"
        self.str = 0
        self.dex = 0
        self.con = 0
        self.int = 0
        self.fel = 0
        self.chr = 0
        self.hp_max = 0
        self.hp = 0
        self.dices = {}
        self.skills = {}
        self.tools = {}

    def init(self):
        prop = {
            "str": 0,
            "dex": 0,
            "con": 0,
            "int": 0,
            "fel": 0,
            "chr": 0,
        }
        attr = {key : value for key, value in prop.items()}

        for p in prop.keys():
            outcome = []
            for _ in range(6):
                outcome.append(Dice("1d6").roll().calc())
            d1 = max(outcome)
            outcome.remove(d1)
            d2 = max(outcome)
            outcome.remove(d2)
            d3 = max(outcome)
            outcome.remove(d3)
            if p != "con":
                result, _ = self.__correct(d1 + d2 + d3)
            else:
                result, self.correct = self.__correct(d1 + d2 + d3)
            prop[p] = result

        self.__dict__.update(prop)
        self.reset_hp()

    def __correct(self, result):
        correct = (result - 10) // 2
        return result + correct, correct

    def reset_hp(self):
        base = Dice("1d10").roll().calc() + self.correct
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
        data += "力量: %d 智力: %d\n" % (self.str, self.int)
        data += "敏捷: %d 感知: %d\n" % (self.dex, self.fel)
        data += "体质: %d 魅力: %d\n" % (self.con, self.chr)
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