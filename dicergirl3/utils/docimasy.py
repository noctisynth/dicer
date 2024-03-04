from dicergirl.utils.dicer import Dicer
from dicergirl.reply.manager import manager
from nonebot.adapters import Event


class Docimasy:
    """
    检定结果解析类
    """

    judge_dict = {
        "critical success": 4,
        "very hard success": 3,
        "hard success": 2,
        "success": 1,
        "fail": 0,
        "fatal fail": -1,
    }

    def __init__(self, detail="", judge: str | int = None):
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
                if self.detail:
                    self.detail = self.detail.strip("\n") + "\n" + toadd
                else:
                    self.detail = toadd
        elif isinstance(toadd, int):
            self.judge += toadd
        elif isinstance(toadd, Docimasy):
            self.detail += "\n" + toadd.detail
        else:
            raise NotImplementedError
        return self

    def __int__(self):
        return self.judge

    def __repr__(self):
        return self.detail

    def __str__(self):
        return self.detail


def judger(
    event: Event, dice: Dicer, exp: int, name: str = None, reason: str = None
) -> Docimasy:
    """类 COC 模式技能检定结果"""
    result = dice.roll().calc()
    docimasy = Docimasy()

    if isinstance(exp, int):
        if result == 100:
            judge = "大失败!"
            docimasy.set_judge("fatal fail")
        elif exp < 50 and result > 95:
            judge = "大失败!"
            docimasy.set_judge("fatal fail")
        elif result == 1:
            judge = "大成功!"
            docimasy.set_judge("critical success")
        elif result <= exp // 5:
            judge = "极难成功"
            docimasy.set_judge("very hard success")
        elif result <= exp // 2:
            judge = "困难成功"
            docimasy.set_judge("hard success")
        elif result <= exp:
            judge = "成功"
            docimasy.set_judge("success")
        else:
            judge = "失败"
            docimasy.set_judge("fail")

    if reason and not isinstance(exp, int):
        docimasy += manager.process_generic_event(
            "utils.docimasy.reason",
            event=event,
            Reason=reason,
            DiceDescription=dice.description(),
        )
    elif not reason and isinstance(exp, int):
        docimasy += manager.process_generic_event(
            "utils.docimasy.skill",
            event=event,
            SkillName=name,
            Value=exp,
            DiceDescription=dice.description(),
            Docimasy=judge,
        )
    else:
        docimasy += manager.process_generic_event(
            "utils.docimasy",
            event=event,
            DiceDiscription=dice.description(),
        )

    return docimasy
