from typing import Dict, List

import Levenshtein

def similar(str1, str2):
    distance = Levenshtein.distance(str1, str2)
    return 1 - (distance / max(len(str1), len(str2)))

class Messages:
    """ 骰娘帮助信息 """
    keys: Dict[str, List[str]] = {
        "帮助": ["main", "", None, "帮助"],
        "指令": ["commands", "command", "cmd", "指令"],
        "管理": ["admin", "管理"],
        "支持": ["supports", "support", "spt", "支持"],
    }
    main = """Unvisitor DicerGirl 版本 {version} [ Python {py_version} For Nonebot2 {nonebot_version} ]
.help/.h  展示此帮助信息
.help 指令  查看指令帮助
.help 管理  查看骰娘管理指令
.help 支持  获取开发者支持
使用`.help [模式名称]`以获取该跑团模式的帮助.

Unvisitor DicerGirl 版本 {version}, 以 Apache-2.0 协议开源.
Copyright © 2011-2023 Unknown Visitor, org.
This project is open source under the Apache-2.0 license."""
    commands = """Unvisitor DicerGirl 版本 {version}
角色卡设定或模式切换后骰娘会自动修改群名片, 在保存新的人物卡时同样会更改群名片.
所有指令允许大小写混用.
.mode/.m  切换和查询跑团模式
.set/.st  角色卡设定
.show/.st show  角色卡查询
.r  掷骰指令
.ra  属性或技能检定
.at/.attack  角色伤害检定
.dam/.damage  角色承伤检定
.en/.encourage  成长检定
.del/.st del  删除数据
.kp  进入主持人席位
.ob  进入旁观者席位
.log  日志管理
使用`.help [指令名]`获取该指令的详细信息
"""
    admin = """Unvisitor DicerGirl 版本 {version}
骰娘管理指令, 如果你是骰主或开发者, 请注意 DicerGirl 的管理员与 Nonebot2 不同.
.su/.sudo  进行骰娘管理员鉴权
.bot  机器人管理
使用`.help [指令名]`获取该指令的详细信息
"""
    supports = """Unvisitor DicerGirl 版本 {version}
开发团队: Unknown Visitor Hacker Union
DicerGirl 主页:
  1. Gitee: https://gitee.com/unvisitor/dicer
  2. Github: https://github.com/unvisitor/dicer
BUG 提交: https://gitee.com/unvisitor/dicer/issues
功能建议: https://gitee.com/unvisitor/dicer/issues
公测 QQ 群: 770386358
项目负责人: 1264983312
"""

    def get(self, key) -> None | str:
        for _, alias in self.keys.items():
            if key in alias:
                return self.__getattribute__(alias[0])

        return

messages = Messages()

def help_message(args: str) -> str:
    """ `.help`指令后端方法 """
    similarcmd = {}
    got = messages.get(args)
    if got:
        return got

    for key, alias in messages.keys.items():
        relation = []
        for alia in alias:
            if alia:
                relation.append(similar(alia, args))

        similarcmd[key] = max(relation)

    related = []
    most_related = ["", 0]
    for cmd, similarity in similarcmd.items():
        if similarity > 0.8:
            related.append(cmd)

        if most_related[1] < similarity:
            most_related = [cmd, similarity]

    if not related:
        return "{name}没有找到相关帮助, 你是否是指: %s?" % (most_related[0])

    i = 1
    reply = "{name}没有找到相关帮助, 你是否是指:\n"
    for relate in related:
        reply += f"{i}. {relate}\n"
    reply += "使用.help [以上参数]来获得相关帮助内容."
    return reply 

if __name__ == "__main__":
    print(help_message("支持"))