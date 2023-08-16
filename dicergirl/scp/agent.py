try:
    from ..utils.dicer import Dice
    from .attributes import scp_attrs_dict, ability_data, knowledge_data, skills_data
except ImportError:
    from dicergirl.utils.dicer import Dice
    from dicergirl.scp.attributes import scp_attrs_dict, knowledge_data, skills_data, ability_data

import random

class Agent(object):
    def __init__(self) -> None:
        self.name = "无名特工"
        self.age = 20
        self.sex = "女"
        self.level = 1
        self.hp_max = 0
        self.hp = 0
        self.enp = 0
        self.rep = 0
        self.ach = 0
        self.dices = {}
        self.en = {}
        self.money = 200
        self.agentclass = "E"
        self.knowledge = {knowledge: 0 for knowledge in knowledge_data.keys()}
        self.skills = {skill: 0 for skill in skills_data.keys()}
        self.ability = {ability: 0 for ability in ability_data.keys()}
        self.p = {
            "knowledge": 17,
            "skills": 14,
            "ability": 10
        }
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
        attr = {p: 1 for p in prop}
        self.en = {p: 0 for p in prop}
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
        self.reset_hp()
        self.reset_enp()
        self.reset_p()
        self.reset_rep()
    
    def reset(self):
        self.reset_hp()
        self.reset_enp()
        self.reset_p()
        self.reset_rep()

    def reset_card(self):
        self.reset()
        self.money = 200
        self.agentclass = "E"
        self.knowledge = {knowledge: 0 for knowledge in knowledge_data.keys()}
        self.skills = {skill: 0 for skill in skills_data.keys()}
        self.ability = {ability: 0 for ability in ability_data.keys()}
        self.p = {
            "knowledge": 17,
            "skills": 14,
            "ability": 10
        }
        self.tools = {}
        self.ach = 0
        self.level = 1

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
    
    def reset_p(self):
        self.p = {
            "knowledge": 17,
            "skills": 14,
            "ability": 10
        }
        self.p["knowledge"] += (self.__count("D10", self.dices["int"]) + self.__count("D10", self.dices["per"])) * 5
        self.p["skills"] += (self.__count("D10", self.dices["str"]) + self.__count("D10", self.dices["dex"])) * 5
        self.p["ability"] += (self.__count("D10", self.dices["chr"]) + self.__count("D10", self.dices["wil"])) * 5
    
    def reset_rep(self):
        self.rep = 0
        for i in self.dices["fte"]:
            if i == "D8":
                self.rep += 1
            elif i == "D10":
                self.rep += 3

    def __count(self, string, list):
        count = 0
        for item in list:
            if string == item:
                count += 1
        return count

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
        data += "强度: %s 命运: %s\n" % (self.__dices_format("str"), self.__dices_format("fte"))
        data += "感知: %s 魅力: %s\n" % (self.__dices_format("per"), self.__dices_format("chr")) 
        data += "灵巧: %s 情报: %s\n" % (self.__dices_format("dex"), self.__dices_format("int"))
        data += "健康: %s 意志: %s\n" % (self.__dices_format("hth"), self.__dices_format("wil"))
        data += "熟练值:\n"
        data += "  知识: %s " % self.p["knowledge"]
        data += "技能: %s " % self.p["skills"]
        data += "能力: %s\n" % self.p["ability"]
        data += "声望: %s\n" % (self.rep)
        data += "激励点: %d\n" % (self.enp)
        data += "生命: %d/%d" % (self.hp, self.hp_max)
        return data
    
    def __dices_format(self, prop):
        d8 = 0
        d10 = 0
        d12 = 0
        d20 = 0

        for dice in self.dices[prop]:
            if dice == "D8":
                d8 += 1
            elif dice == "D10":
                d10 += 1
            elif dice == "D12":
                d12 += 1
            elif dice == "D20":
                d20 += 1

        d8 = f"{d8}D8"
        d10 = f"+{d10}D10" if d10 != 0 else ""
        d12 = f"+{d12}D12" if d12 != 0 else ""
        d20 = f"+{d20}D20" if d20 != 0 else ""
        return d8 + d10 + d12 + d20

    def skills_output(self) -> str:
        if not self.skills and not self.knowledge and not self.ability:
            return "%s 当前无任何技能数据。" % self.name

        r = "\n" + self.__skill_output_format("知识", self.knowledge.items()) + "\n"
        r += "\n" + self.__skill_output_format("技巧", self.skills.items()) + "\n"
        r += "\n" + self.__skill_output_format("能力", self.ability.items())

        return r
    
    def __skill_output_format(self, name, items):
        r = f"{self.name} {name}"
        count = 0
        for k, v in items:
            if count % 2 == 0:
                line = "\n"
                tab = " "
            else:
                line = ""
                tab = ""

            r += f"{line}{k}: {v}{tab}"
            count += 1
        return r

    def output(self) -> str:
        return self.__repr__()
    
    def all_not_base(self):
        nbs = {k: "skills" for k, v in self.skills.items()}
        nbk = {k: "knowledge" for k, v in self.knowledge.items()}
        nba = {k: "ability" for k, v in self.ability.items()}
        anb = {}
        anb.update(nbs)
        anb.update(nbk)
        anb.update(nba)
        return anb

    def out_allskills(self):
        return self.skills_output()

    def out_knowledge(self):
        return self.__skill_output_format("知识", self.knowledge.items()).strip("\n") if self.knowledge else "%s 当前无任何知识数据." % self.name

    def out_skills(self):
        return self.__skill_output_format("技能", self.skills.items()).strip("\n") if self.skills else "%s 当前无任何能力数据." % self.name

    def out_ability(self):
        return self.__skill_output_format("能力", self.ability.items()).strip("\n") if self.ability else "%s 当前无任何能力数据." % self.name

    def out_hp(self):
        return "当前生命值: %d/%d" % (self.hp, self.hp_max)

    def out_enp(self):
        return f"当前剩余激励点: {self.enp}"

    def out_rep(self):
        return f"当前声望: {self.rep}"

    def out_p(self):
        out =  "当前熟练值:\n"
        out += "  知识: %d" % self.p["knowledge"]
        out += "  技能: %d" % self.p["skills"]
        out += "  能力: %d" % self.p["ability"]
        return out

    def out_exp(self):
        return self.out_p()

    def out_money(self):
        return f"当前余额: {self.money}"

    def out_class(self):
        return f"当前特工类别: {self.agentclass}"

    def out_level(self):
        return f"当前特工权限: {self.level}"

    def out_en(self):
        out = "当前激励状态:"
        for en in self.en.keys():
            ability = None
            for attr in scp_attrs_dict.keys():
                if scp_attrs_dict[attr][0] == en:
                    ability = attr

            if not ability:
                return f"[Orcale] 错误: 已经被激励的技能 {en} 不存在!"

            out += f"\n  {ability}: {self.en[en]} 点激励."

        return out

    def load(self, data: dict):
        self.__dict__.update(data)
        return self