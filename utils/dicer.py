import logging
import re
import random

_log = logging.getLogger()

class Dice:
    def __init__(self, roll_string="", explode=False):
        self.roll_string = roll_string
        self.dices = []
        self.parse(roll_string=self.roll_string, explode=explode)
        self.results = []
        self.total = 0
        self.great = False

    def parse(self, roll_string="", explode=False):
        self.explode = explode
        if roll_string:
            self.roll_string = roll_string
        
        if not self.roll_string:
            self.a = 1
            self.b = 100
            self.x = 0
            self.db = f"{self.a}D{self.b}"
            self.dices += [f"D{self.b}"] * self.a
            return self

        pattern = r'(\d+)d(\d+)([+\-])?(\d+)?'
        match = re.match(pattern, self.roll_string)

        if match:
            self.a = int(match.group(1))
            self.b = int(match.group(2))
            self.method = match.group(3) if match.group(3) else "+"
            self.x = int(match.group(4)) if match.group(4) else 0
            self.db = f"{self.a}D{self.b}"
            self.dices += [f"D{self.b}"] * self.a
        else:
            try:
                self.a = 1
                self.b = int(self.roll_string)
                self.x = 0
                self.db = f"{self.a}D{self.b}"
                self.dices += [f"D{self.b}"] * self.a
            except:
                return "[ChatGPT] Invalid roll string format. Use aDb+x format, where a, b, and x are integers."
        return self

    def roll(self):
        if self.b == 0:
            self.results = 0
            self.total = 0
            return self
        self.results = []
        for _ in range(self.a):
            result = random.randint(1, self.b)
            if result == 1:
                result -= 1
            if self.explode and self.b == 8:
                if result == 1:
                    result -= 1
                self.dices.append("D10")
                result2 = random.randint(1, 10)
                if result2 == 1:
                    result -= 1
                result += result2
                if result2 == 10:
                    self.dices.append("D12")
                    result3 = random.randint(1, 12)
                    if result3 == 1:
                        result -= 1
                    result += result3
                    if result3 == 12:
                        self.dices.append("D20")
                        result4 = random.randint(1, 20)
                        if result4 == 1:
                            result -= 1
                        result += result4
                        if result4 == 20:
                            self.great = True
            self.results += [result]

        if self.method == "+":
            self.total = sum(self.results) + self.x
        else:
            self.total = sum(self.results) - self.x
        return self

    def detail_expr(self):
        return str(self.get_results())
    
    def get_results(self):
        return self.results
    
    def calc(self):
        return self.get_total()
    
    def get_total(self):
        return self.total
    
    def __str__(self):
        return self.db

def expr(d, anum):
    d.roll()
    result = d.calc()
    s = f"{d}={(d.detail_expr())}={result}"
    _log.debug(d.detail_expr())
    if anum:
        s += "\n"
        if result == 100:
            s += "大失败！"
        elif anum < 50 and result > 95:
            s += f"{result}>95 大失败！"
        elif result == 1:
            s += "大成功！"
        elif result <= anum // 5:
            s += f"检定值{anum} {result}≤{anum//5} 极难成功"
        elif result <= anum // 2:
            s += f"检定值{anum} {result}≤{anum//2} 困难成功"
        elif result <= anum:
            s += f"检定值{anum} {result}≤{anum} 成功"
        else:
            s += f"检定值{anum} {result}>{anum} 失败"
    return s

def scp_doc(result, difficulty, agent=None, great=False):
    if not agent:
        agent = "该特工"
    r = f"事件难度: {difficulty}\n"
    if difficulty > 25:
        r += f"检定数据: {random.randint(1, 25)}"
        r += f"检定结果: 致命失败.\n检定结论: {agent} 在试图挑战数学、挑战科学、挑战真理, 尝试达成一个不可能事件, {agent} 毫无疑问获得了 致命失败."
        return r
    r += f"检定数据: {result}\n"
    if great:
        r += "检定结果: 关键成功.\n"
        if result <= difficulty:
            r += "检定结论: 有时候, 一次普通的成功或许会大幅度的牵扯到整个未来, 但这并不是一件太过于值得高兴的事情, 因为它不见得是一个好的开始."
        else:
            r += "检定结论: 被 Administrator 所眷顾的人, 毫无疑问这是一次完美的成功, 但是你或许会面对更加绝望的未来."
    elif result > difficulty:
        r += "检定结果: 成功.\n"
        r += "检定结论: 命运常常给予人们无声的嗤笑, 一次成功当然是好事, 但也要警惕这是否是步入深渊的开始."
    elif result < (difficulty/2):
        r += "检定结果: 致命失败.\n"
        r += "检定结论: 努力或许的确有用处, 但是努力只是提高运气的一种手段. 在低劣的运气面前, 任何努力都是没有用的."
    elif result < difficulty:
        r += "检定结果: 失败.\n"
        r += "检定结论: 人类从来都生活在饱含恐惧与绝望的危险之中, 失败是一件稀松平常的事情, 小心, 错误的决定或许会让你步入深渊."
    else:
        result = random.randint(0, 1)
        if result:
            r += "检定结果: 成功.\n"
            r += "检定结论: 小心, 你的成功完全是一次偶然, 不要试图去将这样的偶然当做希望."
        else:
            r += "检定结果: 失败.\n"
            r += "检定结论: 成功与失败宛如山顶与深渊, 无论是哪一种都是可能的, 相反, 在这个世界落入深渊是一件更加合理的事情."
    return r

if __name__ == "__main__":
    try:
        roll_string = "1d6"
        dice = Dice().parse("1d6").roll()
        print(f"{roll_string}={dice.detail_expr()}={dice.calc()}")
    except ValueError as e:
        print(e)