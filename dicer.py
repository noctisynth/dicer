import re
import random

class Dice:
    def __init__(self, roll_string=""):
        self.roll_string = roll_string
        self.parse(self.roll_string)
        self.db = self.roll_string.upper()
        self.results = []
        self.total = 0

    def parse(self, roll_string=""):
        if roll_string:
            self.roll_string = roll_string
        
        if not self.roll_string:
            self.a = 1
            self.b = 100
            self.x = 0
            return self

        pattern = r'(\d+)d(\d+)([+\-]\d+)?'
        match = re.match(pattern, self.roll_string)

        if match:
            self.a = int(match.group(1))
            self.b = int(match.group(2))
            self.x = int(match.group(3)) if match.group(3) else 0
        else:
            try:
                self.a = 1
                self.b = int(self.roll_string)
                self.x = 0
            except:
                return "[ChatGPT] Invalid roll string format. Use aDb+x format, where a, b, and x are integers."
        return self

    def roll(self):
        if self.b == 0:
            self.results = 0
            self.total = 0
            return self
        self.results = [random.randint(1, self.b) for _ in range(self.a)]
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

if __name__ == "__main__":
    try:
        roll_string = "2d4"
        dice = Dice()
        dice.parse(roll_string=roll_string)
        dice.roll()
        print(f"{roll_string}={dice.get_total()}={dice.calc()}")
    except ValueError as e:
        print(e)