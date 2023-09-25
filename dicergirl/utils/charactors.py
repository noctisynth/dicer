from ..common.const import EMPTY_CHAR, EMPTY_DICT

class BaseCharactor:
    def __init__(self) -> None:
        self.name = EMPTY_CHAR
        self.sex = "女"
        self.age = 18
        self.hp = 0
        self.hp_max = 0
        self.tools = EMPTY_DICT
        self.skills = EMPTY_DICT

    def load(self, data: dict):
        self.__dict__.update(data)
        return self

class Character(BaseCharactor):
    """ 人物卡模板 """
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self):
        data = "姓名: %s\n" % self.name
        data += "性别: %s 年龄: %d\n" % (self.sex, self.age)
        data += "生命值: %d/%d" % (self.hp, self.hp_max)
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

    def rollcount(self) -> tuple:
        return (self.__count(), self.__count() + self.luc)

    def __count(self):
        return 0