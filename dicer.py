from botpy import logging

import re
import random

_log = logging.get_logger()

class Dice:
    def __init__(self, roll_string="", explode=False):
        self.roll_string = roll_string
        self.parse(roll_string=self.roll_string, explode=explode)
        self.results = []
        self.total = 0

    def parse(self, roll_string="", explode=False):
        self.explode = explode
        if roll_string:
            self.roll_string = roll_string
        
        if not self.roll_string:
            self.a = 1
            self.b = 100
            self.x = 0
            self.db = f"{self.a}D{self.b}"
            return self

        pattern = r'(\d+)d(\d+)([+\-]\d+)?'
        match = re.match(pattern, self.roll_string)

        if match:
            self.a = int(match.group(1))
            self.b = int(match.group(2))
            self.x = int(match.group(3)) if match.group(3) else 0
            self.db = f"{self.a}D{self.b}"
        else:
            try:
                self.a = 1
                self.b = int(self.roll_string)
                self.x = 0
                self.db = f"{self.a}D{self.b}"
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
                result2 = random.randint(1, 10)
                if result2 == 1:
                    result -= 1
                result += result2
                if result2 == 10:
                    result3 = random.randint(1, 12)
                    if result3 == 1:
                        result -= 1
                    result += result3
                    if result3 == 12:
                        result4 = random.randint(1, 20)
                        if result4 == 1:
                            result -= 1
                        result += result4
            self.results += [result]

        self.total = sum(self.results) + self.x
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

if __name__ == "__main__":
    try:
        roll_string = "1d6"
        dice = Dice().parse("1d6").roll()
        print(f"{roll_string}={dice.detail_expr()}={dice.calc()}")
    except ValueError as e:
        print(e)