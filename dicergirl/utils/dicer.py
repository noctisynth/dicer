try:
    from dicergirl.utils.multilogging import multilogger
except ImportError:
    from .multilogging import multilogger

import re
import random

logger = multilogger(name="Dicer Girl", payload="Dicer")

def is_digit(number):
    try:
        int(number)
        return True
    except:
        return False

class Dice:
    def __init__(self, roll_string="", explode=False, first=True):
        self.roll_string = roll_string
        self.dices = []
        self.a = 1
        self.b = 100
        self.method = "+"
        self.premethod = ""
        self.x = 0
        self.results = []
        self.add = []
        self.to_rolls = []
        self.total = 0
        self.great = False
        self.parse(roll_string=self.roll_string, explode=explode, first=first)

    def parse(self, roll_string="", explode=False, first=True):
        self.is_farther = first
        self.explode = explode
        if roll_string:
            self.roll_string = roll_string

        if not self.roll_string:
            self.a = 1
            self.b = 100
            self.x = 0
            self.db = f"1D100"
            self.dices += [f"D{self.b}"] * self.a
            return self

        if self.is_farther:
            logger.debug(f"初始骰字符串: {roll_string}")
            pattern = r'^(\d+d\d+|\d+|d\d+)([+\-])?(.*?)?$'
        else:
            pattern = r'^([+-]?\d+d\d+|[+-]?\d+|d\d+)([+\-])?(.*?)?$'

        sub_match = re.match(pattern, self.roll_string)

        if not sub_match:
            raise ValueError(f"[Oracle] 错误的投掷指令: {self.roll_string}.")
        if self.is_farther and sub_match.group(1).startswith(("+", "-")):
            raise ValueError(f"[Oracle] 错误的投掷指令: {self.roll_string}.")
        elif not self.is_farther:
            self.premethod = sub_match.group(1)[0]
        else:
            self.premethod = ""

        logger.debug(f"指令 {self.roll_string} 符合正则表达式.")
        logger.debug(f"捕获到基础骰: {sub_match.group(1)}")

        if is_digit(sub_match.group(1)):
            logger.debug(f"基础骰 {sub_match.group(1)} 为数字骰.")
            if sub_match.group(1).startswith(("+", "-")):
                self.a = int(sub_match.group(1)[1:])
            else:
                self.a = int(sub_match.group(1))

            self.b = 1
            self.x = 0
            self.db = self.premethod + str(self.a)
            self.is_num = True
        else:
            this_roll_string = sub_match.group(1)[1:] if sub_match.group(1).startswith(("+", "-")) else sub_match.group(1)
            logger.debug(f"基础骰 {this_roll_string} 为标准骰.")
            regex = r'^(\d+)?d?(\d+)?$'
            match = re.match(regex, this_roll_string)

            if not match:
                raise ValueError(f"[Oracle] 错误的投掷指令: {self.roll_string}.")

            self.is_num = False

        if not self.is_num:
            if match.group(2):
                if not is_digit(match.group(2)):
                    raise ValueError(f"[Oracle] 错误的投掷指令: {self.roll_string}.")
            if match.group(1):
                if not is_digit(match.group(1)):
                    raise ValueError(f"[Oracle] 错误的投掷指令: {self.roll_string}.")

            self.a = int(match.group(1)) if match.group(1) else 1
            self.b = int(match.group(2))
            self.db = f"{self.a}D{self.b}"
            self.dices += [f"D{self.b}"] * self.a

        self.method = sub_match.group(2) if sub_match.group(2) else "+"

        if sub_match.group(3):
            if not re.match(pattern, sub_match.group(3)):
                raise ValueError(f"[Oracle] 附加骰不符合标准: {sub_match.group(3)}.")

            logger.debug(f"计算模式: {self.method}")
            addon = self.method + sub_match.group(3)
            logger.debug(f"附加骰: {addon}")
            xd = Dice(addon, first=False).roll()
            self.x = xd.calc()
            logger.debug(f"附加骰结果: {self.x}")
            self.db = f"{self.db}{self.method}{sub_match.group(3).upper()}"
            self.add = xd.results
        else:
            self.x = 0
            self.add = None

        return self

    def __get_sum(self, list_to_sum: list) -> int:
        total = 0
        for index in range(len(list_to_sum)):
            sub = list_to_sum[index]

            if isinstance(sub, list):
                total += self.__get_sum(sub)
                continue

            total += sub
        return total

    def roll(self):
        self.results = []

        if self.add:
            add = self.__get_sum(self.add)
            add = -add if add < 0 else add
            logger.debug(f"掷骰时附加结果: {self.method}{add}")
        else:
            add = 0

        rolla = self.a if self.a > 0 else -self.a
        for _ in range(rolla):
            if self.b == 1:
                break

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

            self.results.append(result)
        
        if self.b == 1:
            self.results = [int(self.premethod + str(self.a))]

        self.total = sum(self.results)
        
        if self.premethod == "-":
            self.total = -self.total

        if self.method == "+":
            self.total += add
        else:
            self.total -= add

        if self.add:
            self.results.append(self.add)

        return self

    def description(self):
        results = self.get_results()
        length = 0
        for result in results:
            if isinstance(result, int):
                length += 1
                continue

            length += len(result)

        if length > 10:
            results = [...]

        return f"{self.db}={results}={self.total}"

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

if __name__ == "__main__":
    roll_strings = {
        "1": 1,
        "10": 10,
        "100": 100,
        "1d1": 1,
        "10d1": 10,
        "100d1": 100,
        "10d1+10d1": 20,
        "10d1-10d1": 0,
        "10d1+10d1+10d1": 30,
        "10d1-10d1+10d1": 10,
        "10d1-10d1-10d1": -10,
    }
    for roll_string in roll_strings.keys():
        try:
            dice = Dice().parse(roll_string).roll()
            if dice.total != roll_strings[roll_string]:
                print(dice.description())
                raise ValueError(f"对于 {roll_string} dice.toal={dice.total} 但期待 {roll_strings[roll_string]}")
        except ValueError as error:
            logger.exception(error)

    try:
        roll_string = "1d100+10-10"
        dice = Dice().parse(roll_string).roll()
        print(dice.description())
    except ValueError as error:
        logger.exception(error)