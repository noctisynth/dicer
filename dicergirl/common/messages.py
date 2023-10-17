from typing import Dict, List
from ..reply.manager import manager

import Levenshtein

manager.register_event(
    "HelpNotFoundRelated", "{BotName}没有找到相关帮助, 你是否是指: {MostRelated}?"
)
manager.register_event(
    "HelpNotFoundSomeRelated",
    "{BotName}没有找到相关帮助, 你是否是指:\n{MostRelated}\n使用.help [以上参数]来获得相关帮助内容.",
)


def similar(str1, str2):
    distance = Levenshtein.distance(str1, str2)
    return 1 - (distance / max(len(str1), len(str2)))


class Messages:
    """骰娘帮助信息"""

    keys: Dict[str, List[str]] = {
        "帮助": ["main", "", None, "帮助"],
        "指令": ["commands", "command", "cmd", "指令"],
        "管理": ["admin", "管理"],
        "支持": ["supports", "support", "spt", "支持"],
        "管理员鉴权": ["sudo", "su", "管理员鉴权", "鉴权"],
        "模式": ["mode", "m", "模式"],
        "机器人管理": ["bot", "manage", "机器人管理"],
        "录卡": ["set", "st", "录卡"],
        "展示": ["show", "展示"],
        "掷骰": ["roll", "r", "rd", "掷骰"],
        "检定": ["ra", "技能检定", "检定"],
        "承伤": ["dam", "damage", "承伤检定", "承伤检定"],
        "伤害": ["at", "attack", "伤害检定", "伤害"],
        "激励": ["en", "激励检定", "激励检定"],
        "删除": ["delete", "del", "remove", "rm", "删除"],
        "日志": ["log", "logger", "日志管理", "日志系统", "日志"],
        "消息": ["regist", "reg", "消息事件", "回复", "消息"],
    }
    main = """Unvisitor DicerGirl 版本 {version} [Python {py_version} For Nonebot2 {nonebot_version}]
.help (.h)  展示此帮助信息
.help 指令  查看指令帮助
.help 管理  查看骰娘管理指令
.help 支持  获取开发者支持
使用`.help [模式名称]`以获取该跑团模式的帮助.
此项目以 Apache-2.0 协议开源.
Copyright 2011-2023 Unknown Visitor, org."""
    commands = """Unvisitor DicerGirl 版本 {version}
角色卡设定或模式切换后骰娘会自动修改群名片, 在保存新的人物卡时同样会更改群名片.
所有指令允许大小写混用.
.mode (.m)  切换和查询跑团模式
.set (.st)  角色卡设定
.show (.st show)  角色卡查询
.roll (.r)  掷骰指令
.ra  属性或技能检定
.at (.attack)  角色伤害检定
.dam (.damage)  角色承伤检定
.en (.encourage)  成长检定
.del (.st del)  删除数据
.kp  进入主持人席位
.ob  进入旁观者席位
.log  日志管理
.reg (.regist)  消息事件注册
使用`.help [指令名]`获取该指令的详细信息"""
    admin = """Unvisitor DicerGirl 版本 {version}
骰娘管理指令, 如果你是骰主或开发者, 请注意 DicerGirl 的管理员与 Nonebot2 不同.
.su/.sudo  进行骰娘管理员鉴权
.bot  机器人管理
使用`.help [指令名]`获取该指令的详细信息"""
    supports = """Unvisitor DicerGirl 版本 {version}
开发团队: 未知访客黑客联盟
团队官网: https://www.unvisitor.site/
DicerGirl 主页: https://dicer.unvisitor.site/
DicerGirl 项目主页:
  1. Gitee: https://gitee.com/unvisitor/dicer
  2. Github: https://github.com/unvisitor/dicer
BUG 提交: https://gitee.com/unvisitor/dicer/issues
功能建议: https://gitee.com/unvisitor/dicer/issues
公测 QQ 群: 770386358
项目负责人: 1264983312"""
    sudo = """用法：.su [鉴权令牌]
描述：
    进行管理员鉴权, 获得骰娘的管理员权限。
示例:
    .su d32ab3...
注意：
    - 鉴权令牌会在执行无参数的`.su`指令后, 在`Nonebot2`的控制终端输出, 输出模式为`CRITICAL`.
    - 需要注意此权限管理系统与`Nonebot2`的`SUPERUSER`不同."""
    bot = """用法：.bot <指令> [参数]
描述：
    执行与管理插件和机器人设置相关的各种任务。
指令：
    version (v, bot, 版本)          显示机器人版本
    exit (bye, leave, 离开)         退出机器人
    on (run, start, 启动)           启动机器人
    off (down, shutdown, 关闭)      关闭机器人
    upgrade (up, 更新)              升级机器人
    downgrade (降级)                降级机器人
    name (命名) <名称>              设置或显示机器人名称
    status (状态)                   显示机器人当前状态
    plgup (pluginup, 升级) <名称>    升级特定插件
    install (add, 安装) <名称>      安装插件
    remove (del, rm, 删除, 卸载) <名称>    删除插件
    mode (list, 已安装)             列出已安装的插件
    store (plugins, 商店)           显示商店中可用的插件
    search (搜索) <名称>            在商店中搜索插件
示例：
    .bot version
    .bot install 插件名称
    .bot remove 插件名称"""
    mode = """用法：.mode (.m) [模式名称]
描述：
    切换跑团模式。
示例：
    .mode coc  切换到 COC 跑团模式
注意：
    - 如果骰娘管理员加入了第三方跑团插件, `mode`参数应该设置为该插件中`__init__.py`的`__name__`参数, 不区分大小写."""
    set = """用法：.set (.st) <指令> [属性名称] [属性值] ... [CQ:at]
描述：
    设置角色卡信息。
指令：
    show (=.show)    显示角色卡信息
    del (=.del)     删除角色卡
    clear    清空所有角色卡信息
示例：
    .set 毁灭人类 99 打爆地球 99
    .set 幸运 +10
    .set show
    .set del 毁灭人类
    .set clear
注意：
    - 在保存人物卡之前请先确保当前模式与车卡模式相同.
    - 部分跑团模式(如SCP)中不支持设置属性, 同时设置非自定义技能也是不推荐的, 在设置前, 建议先询问主持人的意见.
    - 在群聊中输入单独的`.set`指令, 欧若可将自动读取最近一次车卡(即人物卡作成)指令的结果进行保存.
    - 当属性或技能名称均为中文或均为英文时, 指令是强空格需求的, 或者你也可以使用引号规避指令解析问题.
    - 录卡一般常见于类似 COC 跑团和 DND 跑团等跑团模式, 部分模式(如SCP模式)是不需要的, 在建卡之前, 请先询问主持人是否需要进行录卡.
    - `[CQ:at]`指在群聊中`@`一个玩家, `.set`指令将会指向该玩家, 该参数是可选的."""
    show = """.show (.st show) [选项] [CQ:at]
描述：
    展示人物卡
指令：
    [键值]   该模式下存在的可查看键值
    skill   查看自身人物卡技能
    all     查询所有存储的人物卡
注意：
    - 部分键值可能并不在其它模式中支持, 如果管理员加入了第三方插件, 准允的可选键值请询问主持人、骰娘管理员或插件开发者.
    - 官方插件的键值可在插件主页查看
    - `[CQ:at]`指在群聊中`@`一个玩家, `.show`指令将会指向该玩家, 该参数是可选的."""
    roll = """.roll (.r) [掷骰表达式]
描述：
    标准掷骰指令。
指令：
    [掷骰表达式]    掷骰表达式
示例：
    .r 1d100    掷骰1d100
    .r 1d20+1d6-3d10    复杂掷骰计算
    .r (1d6+2d10)/2-3d6*2     复合掷骰运算
备注：
    - 掷骰表达式兼容常用的OneDice标准.
    - 空的掷骰表达式默认为`1d100`.
"""
    ra = """.ra <属性/技能名> [检定值]
描述：
    基础属性或技能检定。
指令：
    <属性/技能名>   人物卡中包含的基础属性或技能名称
    [检定值]      一般是指定属性/技能值或检定难度
示例：
    .ra 命运    快速检定`命运`属性
    .ra 毁灭人类 99     检定技能值为99的毁灭人类技能"""
    dam = """.dam (.damage) [选项] [掷骰表达式]
描述：
    角色承伤检定。
指令：
    [掷骰表达式]    掷骰表达式
    check   检定人物当前生命状态
示例：
    .dam check
    .dam 1d6+2  人物受到`1d6+2`掷骰结果的伤害
    .dam 6  人物受到 6 点伤害
注意：
    - 无参数的`.dam`指令会进行该模式默认的伤害承受检定."""
    at = """.at (.attack) [掷骰表达式] [参数]
描述：
    角色伤害检定。
指令：
    [掷骰表达式]    掷骰表达式
    [参数]      一般为检定工具伤害
示例：
    .at 1d6     人物造成`1d6`掷骰结果的伤害
    .at 燃烧瓶      使用燃烧瓶进行伤害检定
注意：
    - 无参数的`.at`指令会进行该模式默认的近战伤害检定.
    - 部分模式可能不支持掷骰表达式或语法."""
    en = """.en (.encourage) <属性/技能名> [激励点]
描述：
    角色(临时)属性激励。
指令：
    <属性/技能名>   角色属性或技能名
    [激励点]        激励点
示例：
    .en 强度 2  激励属性`强度`2 点
    .en 毁灭人类    激励技能`毁灭人类`
注意：
    - 部分模式可能不需要给入激励点."""
    delele = """.del (.delete) [选项] [参数]
描述：
    删除数据。
指令：
    cache   删除暂存数据
    card    删除使用中的人物卡(谨慎使用)
    [技能]  删除指定的自定义技能
注意：
    - 删除自定义技能时, 支持多个参数, 可以一次指定多个技能名."""
    log = """用法：.log <指令> [选项]
描述：
    执行与管理日志相关的各种任务。
指令：
    show          显示所有日志
    add (new) [名称]   添加一个新日志，可选择提供一个名称
    stop <ID>     停止特定 ID 的日志记录
    start <ID>    启动特定 ID 的日志记录
    remove (rm) <ID>  删除特定 ID 的日志记录
    download (load) <ID> 下载特定 ID 的日志记录
示例：
    .log show
    .log add 日志名称
    .log stop 日志ID
注意：
    - 使用 'add' 指令而不带参数以创建一个未命名的日志。"""
    regist = """用法：.regist (.reg) [事件名] [消息内容] [指令]
描述：
    用户自定义回复文本。
指令：
    remove (rm, delete, del) [事件名]   注销自定义消息事件
    enable [事件名]      启用被禁用的消息事件
    disable [事件名]     禁用自定义消息事件
示例：
    .regist ModeChanged 已切换跑团模式为{Mode}.     将默认`ModeChanged`事件回复内容修改
    .regist remove ModeChanged      返回默认消息内容"""

    def get(self, key) -> None | str:
        for _, alias in self.keys.items():
            if key in alias:
                return self.__getattribute__(alias[0])

        return


messages = Messages()


def help_message(args: str) -> str:
    """`.help`指令后端方法"""
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
        return manager.process_generic_event(
            "HelpNotFoundRelated", MostRelated=most_related[0]
        )

    i = 1
    reply = ""
    for relate in related:
        reply += f"{i}. {relate}\n"
        i += 1

    reply = manager.process_generic_event("HelpNotFoundSomeRelated", MostRelated=reply)
    return reply


def regist(name, message, alias=[]):
    if not alias:
        alias = [
            name,
        ]

    messages.keys[name] = alias
    setattr(messages, alias[0], message)


if __name__ == "__main__":
    regist("test", "测试指令", alias=["test", "测试指令"])
    print(help_message("test"))
    print(help_message("支持"))
