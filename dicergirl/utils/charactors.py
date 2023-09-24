class Character:
    """ 人物卡模板 """
    def __init__(self) -> None:
        self.name = "无名角色"
        self.age = 20
        self.sex = "女"
        self.hp = 10
        self.hp_max = 10
        self.skills = {}
        self.tools = {}

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

    def load(self, data: dict):
        self.__dict__.update(data)
        return self