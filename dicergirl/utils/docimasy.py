import random
try:
    from .dicer import Dice
except ImportError:
    from dicergirl.utils.dicer import Dice

class Docimasy:
    """
        检定结果类
    """
    judge_dict = {
        "critical success": 4,
        "very hard success": 3,
        "hard success": 2,
        "success": 1,
        "fail": 0,
        "fatal fail": -1,
    }
    def __init__(self, detail, judge: str | int=None):
        self.detail = detail

        if isinstance(judge, int):
            self.judge = judge

        if judge:
            self.judge = self.judge_dict[judge]
        else:
            self.judge = None

    def set_judge(self, judge):
        if isinstance(judge, int):
            self.judge = judge

        self.judge = self.judge_dict[judge]

    def __bool__(self):
        if self.judge > 0:
            return True
        else:
            return False

    def __add__(self, toadd):
        if isinstance(toadd, str):
            toadd = toadd.lstrip("\n")
            if toadd:
                self.detail += "\n" + toadd
        elif isinstance(toadd, int):
            self.judge += toadd
        return self

    def __int__(self):
        return self.judge

    def __repr__(self):
        return self.detail

    def __str__(self):
        return self.detail

def expr(dice: Dice, anum):
    result = dice.roll().calc()
    docimasy = Docimasy(f"掷骰: {dice.db}")
    docimasy += dice.description()

    if anum:
        if result == 100:
            docimasy += "大失败！"
            docimasy.set_judge("fatal fail")
        elif anum < 50 and result > 95:
            docimasy += f"{result}>95 大失败！"
            docimasy.set_judge("fatal fail")
        elif result == 1:
            docimasy += "大成功！"
            docimasy.set_judge("critical success")
        elif result <= anum // 5:
            docimasy += f"检定值: {anum} {result}≤{anum//5}"
            docimasy += "检定结果: 极难成功."
            docimasy.set_judge("very hard success")
        elif result <= anum // 2:
            docimasy += f"检定值: {anum} {result}≤{anum//2}"
            docimasy += "检定结果: 困难成功."
            docimasy.set_judge("hard success")
        elif result <= anum:
            docimasy += f"检定值: {anum} {result}≤{anum}"
            docimasy += "检定结果: 成功."
            docimasy.set_judge("success")
        else:
            docimasy += f"检定值: {anum} {result}>{anum}"
            docimasy += "检定结果: 失败."
            docimasy.set_judge("fail")
    return docimasy

def scp_doc(result, difficulty, encourage=None, agent=None, great=False):
    if not agent:
        agent = "该特工"

    r = Docimasy(f"事件难度: {difficulty}")

    if difficulty > 25 and result <= difficulty:
        r += f"检定数据: {result}"
        r += f"检定结果: 致命失败."
        r += f"检定结论: {agent} 在试图挑战数学、挑战科学、挑战真理, 尝试达成一个不可能事件, {agent} 毫无疑问获得了 致命失败."
        r.set_judge("fatal fail")
        return r

    if encourage:
        r += f"肾上腺素: {encourage}"
        r += f"检定数据: {result}+{encourage}"
        result += encourage
    else:
        r += f"检定数据: {result}"

    if great:
        r += "检定结果: 关键成功."
        if result <= difficulty:
            r += "检定结论: 有时候, 一次普通的成功或许会大幅度的牵扯到整个未来, 但这并不是一件太过于值得高兴的事情, 因为它不见得是一个好的开始."
        else:
            r += "检定结论: 被 Administrator 所眷顾的人, 毫无疑问这是一次完美的成功, 但是你或许会面对更加绝望的未来."
        r.set_judge("critical success")
    elif result >= (difficulty*2):
        r += "检定结果: 关键成功."
        r += "检定结论: 绝境之中的人常常能够爆发出无尽的潜力, 疯狂是人类最强大的武器, 用疯狂去嗤笑命运吧."
        r.set_judge("critical success")
    elif result > difficulty:
        r += "检定结果: 成功."
        r += "检定结论: 命运常常给予人们无声的嗤笑, 一次成功当然是好事, 但也要警惕这是否是步入深渊的开始."
        r.set_judge("success")
    elif result < (difficulty/2):
        r += "检定结果: 致命失败."
        r += "检定结论: 努力或许的确有用处, 但是努力只是提高运气的一种手段. 在低劣的运气面前, 任何努力都是没有用的."
        r.set_judge("fatal fail")
    elif result < difficulty:
        r += "检定结果: 失败."
        r += "检定结论: 人类从来都生活在饱含恐惧与绝望的危险之中, 失败是一件稀松平常的事情, 小心, 错误的决定或许会让你步入深渊."
        r.set_judge("fail")
    else:
        result = random.randint(0, 1)
        if result:
            r += "检定结果: 成功."
            r += "检定结论: 小心, 你的成功完全是一次偶然, 不要试图去将这样的偶然当做希望."
            r.set_judge("success")
        else:
            r += "检定结果: 失败."
            r += "检定结论: 成功与失败宛如山顶与深渊, 无论是哪一种都是可能的, 相反, 在这个世界落入深渊是一件更加合理的事情."
            r.set_judge("fail")
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
    print(scp_doc(10, 20, agent="Oracle"))