try:
    from dicergirl.utils.multilogging import multilogger
except ImportError:
    from .multilogging import multilogger

import re
import random

logger = multilogger(name="Dicer Girl", payload="Dicer")

class Dice:
    def __init__(self, roll_string="", explode=False):
        self.roll_string = roll_string
        self.dices = []
        self.method = "+"
        self.results = []
        self.add = []
        self.parse(roll_string=self.roll_string, explode=explode)
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

        pattern = r'^(\d+)d(\d+)([+\-])?(\d+)?d?(\d+)?$'
        match = re.match(pattern, self.roll_string)

        if match:
            self.a = int(match.group(1))
            self.b = int(match.group(2))
            self.method = match.group(3) if match.group(3) else "+"
            if match.group(4) and match.group(5):
                xd = Dice(f"{match.group(4)}d{match.group(5)}").roll()
                self.x = xd.calc()
                self.db = f"{self.a}D{self.b}{self.method}{match.group(4)}D{match.group(5)}"
                self.add = xd.results
                logger.debug(xd.results)
            else:
                self.x = int(match.group(4)) if match.group(4) else 0
                if self.x:
                    self.db = f"{self.a}D{self.b}{self.method}{self.x}"
                else:
                    self.db = f"{self.a}D{self.b}"
                self.add = [self.x] if self.x else None
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
        if self.add:
            add = sum(self.add)
        else:
            add = 0

        for _ in range(self.a):
            result = random.randint(1, self.b)

            if result == 1:
                if self.explode:
                    result -= 1

            if self.explode and self.b == 8:
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
            self.total = sum(self.results) + add
        else:
            self.total = sum(self.results) - add
        
        if self.add:
            self.results.append(self.add)

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

def expr(d: Dice, anum):
    d.roll()
    result = d.calc()
    s = f"掷骰: {d.db}\n"
    s += f"{d.db}={(d.detail_expr())}={result}"

    if anum:
        s += "\n"
        if result == 100:
            s += "大失败！"
        elif anum < 50 and result > 95:
            s += f"{result}>95 大失败！"
        elif result == 1:
            s += "大成功！"
        elif result <= anum // 5:
            s += f"检定值: {anum} {result}≤{anum//5}\n"
            s += "检定结果: 极难成功."
        elif result <= anum // 2:
            s += f"检定值: {anum} {result}≤{anum//2}\n"
            s += "检定结果: 困难成功."
        elif result <= anum:
            s += f"检定值: {anum} {result}≤{anum}\n"
            s += "检定结果: 成功."
        else:
            s += f"检定值: {anum} {result}>{anum}\n"
            s += "检定结果: 失败."
    return s

def scp_doc(result, difficulty, encourage=None, agent=None, great=False):
    if not agent:
        agent = "该特工"

    r = f"事件难度: {difficulty}\n"

    if difficulty > 25:
        r += f"检定数据: {random.randint(1, 25)}"
        r += f"检定结果: 致命失败.\n"
        r += f"检定结论: {agent} 在试图挑战数学、挑战科学、挑战真理, 尝试达成一个不可能事件, {agent} 毫无疑问获得了 致命失败."
        return r
    
    if encourage:
        r += f"肾上腺素: {encourage}\n"
        r += f"检定数据: {result}+{encourage}\n"
        result += encourage
    else:
        r += f"检定数据: {result}\n"

    if great:
        r += "检定结果: 关键成功.\n"
        if result <= difficulty:
            r += "检定结论: 有时候, 一次普通的成功或许会大幅度的牵扯到整个未来, 但这并不是一件太过于值得高兴的事情, 因为它不见得是一个好的开始."
        else:
            r += "检定结论: 被 Administrator 所眷顾的人, 毫无疑问这是一次完美的成功, 但是你或许会面对更加绝望的未来."
    elif result >= (difficulty*2):
        r += "检定结果: 关键成功.\n"
        r += "检定结论: 绝境之中的人常常能够爆发出无尽的潜力, 疯狂是人类最强大的武器, 用疯狂去嗤笑命运吧."
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

def dnd_doc(result, dc, adventurer=None):
    if not adventurer:
        adventurer = "该冒险者"
    r = f"事件难度: {dc}\n"
    r += f"检定数据: {result}\n"
    if result >= 20:
        r += "检定结果: 大成功.\n"
        r += "检定结论: 被命运眷顾的幸运者, 这毫无疑问是一次完美的成功."
    elif result > dc:
        r += "检定结果: 成功.\n"
        r += "检定结论: 前进吧, 冒险者, 异世的诗篇还在等着你."
    elif result <= dc / 2:
        r += "检定结果: 大失败.\n"
        r += "检定结论: 冒险不是自寻死路, 有时候, 放弃也是一个好的选择."
    elif result < dc:
        r += "检定结果: 失败.\n"
        r += "检定结论: 成功与失败总是相辅相成, 不要让一次失败打倒你."
    else:
        result = random.randint(0, 1)
        if result:
            r += "检定结果: 成功.\n"
            r += "检定结论: 小心, 你的成功完全是一次偶然, 不要认为这样的偶然稀松平常, 冷静与冲动并存, 才是一个合格的冒险者."
        else:
            r += "检定结果: 失败.\n"
            r += "检定结论: 成功与失败由于一体两面, 无论是哪一种都是可能的, 但是你不必气馁, 失败与成功都是冒险的一部分."
    return r

if __name__ == "__main__":
    try:
        roll_string = "2d1-2"
        dice = Dice().parse(roll_string).roll()
        print(f"{dice.db}={dice.detail_expr()}={dice.calc()}")
    except ValueError as e:
        print(e)