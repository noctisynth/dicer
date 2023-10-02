import abc
import re
import random

from multilogging import multilogger
from typing import List


ZERO = 0
EMPTY_STRING = ""
EMPTY_LIST = []

logger = multilogger(name="DicerGirl", payload="Dicer")


class BaseDice:
    def __init__(self, roll_string: str=EMPTY_STRING) -> None:
        self.roll_string = roll_string
        self.db = EMPTY_STRING
        self.outcome = ZERO
        self.display = EMPTY_LIST

    def __repr__(self) -> str:
        return self.db.upper()

    @abc.abstractmethod
    def parse(self) -> "BaseDice":
        raise NotImplementedError

    @abc.abstractmethod
    def roll(self) -> int:
        """ 对骰子进行投掷并给出结果 """
        raise NotImplementedError


class DigitDice(BaseDice):
    """ 数字骰 """
    def __init__(self, roll_string: str=EMPTY_STRING) -> None:
        super().__init__(roll_string=roll_string)
        if not roll_string.isdigit():
            raise ValueError

        self.parse()

    def parse(self) -> "DigitDice":
        self.a = int(self.roll_string)
        self.b = 1
        self.db = f"{self.a}"
        return self

    def roll(self) -> int:
        self.outcome = self.a
        self.display = [self.a]
        return self.outcome


class Dice(BaseDice):
    """ 多面骰 """
    def __init__(self, roll_string: str="", explode: bool=False) -> None:
        super().__init__(roll_string=roll_string)
        self.dices = EMPTY_LIST
        self.great = False
        self.explode = explode
        self.parse()

    def parse(self) -> "Dice":
        self.dices = []
        split = re.split(r"[dD]", self.roll_string)

        if split[0]:
            self.a = int(split[0])
        else:
            self.a = 1

        if split[1]:
            self.b = int(split[1])
        else:
            self.b = 100

        self.db = f"{self.a}D{self.b}"
        self.dices += [f"D{self.b}"] * self.a
        return self

    def roll(self) -> int:
        self.results = []
        self.display = []

        for _ in range(self.a):
            result = random.randint(1, self.b)

            if result == 1 and self.explode:
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
            self.display.append(result)

        self.outcome = sum(self.results)
        return self.outcome


class AwardDice(BaseDice):
    """ 奖励骰 """
    def __init__(self, roll_string: str="") -> None:
        super().__init__(roll_string=roll_string)
        self.parse()

    def parse(self) -> "AwardDice":
        split = re.split(r"[bB]", self.roll_string)

        if split[0]:
            self.a = int(split[0])
        else:
            self.a = 1

        self.b = int(split[1])
        self.db = f"{self.a}B{self.b}"
        return self

    def roll(self) -> int:
        self.results = []
        self.display = []

        for _ in range(self.a):
            ten = []
            for _ in range(self.b):
                outcome = Dice("1d10").roll()
                outcome = outcome if outcome != 10 else 0
                ten.append(outcome)

            result = Dice("1d100").roll()
            ten.append(result//10)
            minten = min(ten)
            ten.remove(result//10)
            outcome = minten*10 + (result % 10)
            self.results.append(outcome)
            self.display.append([result, ten])

        self.outcome = sum(self.results)
        return self.outcome


class PunishDice(BaseDice):
    """ 惩罚骰 """
    def __init__(self, roll_string: str="") -> None:
        super().__init__(roll_string=roll_string)
        self.parse()

    def parse(self) -> "PunishDice":
        split = re.split(r"[pP]", self.roll_string)

        if split[0]:
            self.a = int(split[0])
        else:
            self.a = 1

        self.b = int(split[1])
        self.db = f"{self.a}P{self.b}"
        return self

    def roll(self) -> int:
        self.results = []
        self.display = []

        for _ in range(self.a):
            ten = []
            for _ in range(self.b):
                outcome = Dice("1d10").roll()
                outcome = outcome if outcome != 10 else 0
                ten.append(outcome)

            result = Dice("1d100").roll()
            ten.append(result//10)
            maxten = max(ten)
            ten.remove(result//10)
            outcome = maxten*10 + (result % 10)
            self.results.append(outcome)
            self.display.append([result, ten])

        self.outcome = sum(self.results)
        return self.outcome


class Dicer:
    """掷骰类
    参数:
        roll_string: 标准掷骰表达式
        explode: 是否启用爆炸骰
    示例:
        ```python
        dice = Dice("1d10")
        dice.roll()
        print(dice.outcome) # 输出`1d10`投掷结果
        ```
    """
    def __init__(self, roll_string: str=EMPTY_STRING, explode: bool=False) -> None:
        self.roll_string: str = roll_string
        self.explode: bool = explode
        self.calc_list: List[str | Dice | DigitDice | AwardDice | PunishDice] = []
        self.results: List[int] = []
        self.display: List[int | List[int]] = []
        self.outcome: int = ZERO
        self.great: bool = False
        self.dices: List[str] = []

    def parse(self, roll_string: str=EMPTY_STRING, explode: bool=False):
        self.roll_string = roll_string if roll_string else self.roll_string
        self.calc_list = []
        self.db = EMPTY_STRING
        matches: List[str] = re.findall(r'\d*[a-zA-Z]\w*|\d+|[-+*/]', self.roll_string)

        for match in matches:
            if match in ("+", "-", "*", "/", "(", ")"):
                self.calc_list.append(match)
                self.db += match
            elif re.match(r"\d*[dD]\d*", match):
                self.calc_list.append(Dice(match, explode=explode))
                self.db += match.upper()
            elif re.match(r"\d*[bB]\d+", match):
                self.calc_list.append(AwardDice(match))
                self.db += match.upper()
            elif re.match(r"\d*[pP]\d+", match):
                self.calc_list.append(PunishDice(match))
                self.db += match.upper()
            elif re.match(r"\d+", match):
                self.calc_list.append(DigitDice(match))
                self.db += match.upper()
            else:
                raise ValueError(f"骰 {match} 不符合规范.")

        if not matches:
            self.calc_list.append(Dice("1d100"))
            self.db = "1D100"

        return self

    def roll(self):
        self.parse(roll_string=self.roll_string, explode=self.explode)
        self.dices = []
        self.display = []
        for index, calc in enumerate(self.calc_list):
            if calc in ("+", "-", "*", "/", "(", ")"):
                continue

            outcome = calc.roll()
            self.calc_list[index] = outcome
            self.results.append(outcome)
            self.display += calc.display

            if isinstance(calc, Dice) and self.explode:
                if calc.great:
                    self.great = True
                
                self.dices += calc.dices

        self.outcome = eval("".join(map(str, self.calc_list)))
        return self

    def description(self):
        def count_integers(lst) -> int:
            count = 0
            for item in lst:
                if isinstance(item, int):
                    count += 1
                elif isinstance(item, list):
                    count += count_integers(item)
            return count

        results = self.display
        len_display = count_integers(self.display)
        len_results = count_integers(self.results)

        if len_display <= 10:
            results = self.display
        elif len_results <= 10:
            results = self.results
        else:
            results = [...]

        return f"{self.db}={results}={self.outcome}"

    def get_results(self):
        return self.results

    def detail_expr(self):
        return str(self.results)

    def calc(self):
        return self.outcome

    def __repr__(self):
        return self.db

if __name__ == "__main__":
    # text = "-10/d2/1d10+2d2-22/2+3p2+2b10-p4/b2/d2"
    # dice = Dicer(text)
    # print(dice.calc_list)
    # dice.roll()
    # print(dice.calc_list)
    # print(dice.results)
    # print(dice.outcome)
    roll_strings = {
        "1": 1,
        "10": 10,
        "100": 100,
        "-1": -1,
        "-10": -10,
        "-100": -100,
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
            dice = Dicer().parse(roll_string).roll().roll()
            if dice.outcome != roll_strings[roll_string]:
                print(dice.description())
                raise ValueError(f"对于 {roll_string} dice.toal={dice.outcome} 但期待 {roll_strings[roll_string]}")
        except ValueError as error:
            logger.exception(error)

    try:
        roll_string = "d"
        dice = Dicer(roll_string).roll()
        print(dice.description())
    except ValueError as error:
        logger.exception(error)