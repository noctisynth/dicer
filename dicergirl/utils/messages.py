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
        "日志": ["log", "logger", "日志管理", "日志系统", "日志"]
    }
    main = """Unvisitor DicerGirl 版本 {version} [Python {py_version} For Nonebot2 {nonebot_version}]
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
   plgup (pluginup, 升级) [名称]    升级特定插件
   install (add, 安装) [名称]      安装插件
   remove (del, rm, 删除, 卸载) [名称]    删除插件
   mode (list, 已安装)             列出已安装的插件
   store (plugins, 商店)           显示商店中可用的插件
   search (搜索) [名称]            在商店中搜索插件
示例：
   .bot version
   .bot install 插件名称
   .bot remove 插件名称"""
    mode = """用法：.mode [模式名称]
描述：
   切换跑团模式
示例：
   .mode coc  切换到 COC 跑团模式
注意：
   - 如果骰娘管理员加入了第三方跑团插件, `mode`参数应该设置为该插件中`__init__.py`的`__name__`参数, 不区分大小写.
   - 默认的跑团模式为`SCP`, 每一次机器人重启或更新后, 跑团模式都会更改为`SCP`."""
    set = """用法：.set (.st) <指令> [属性名称] [属性值] ...
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
   - 请确保在录卡之前执行无参数的`.set(.st)`指令保存人物卡。
   - 在保存人物卡之前请先确保当前模式与车卡模式相同.
   - 部分跑团模式(如SCP)中不支持设置属性, 同时设置非自定义技能也是不推荐的, 在设置前, 建议先询问主持人的意见.
   - 在群聊中输入单独的`.set`指令, 欧若可将自动读取最近一次车卡(即人物卡作成)指令的结果进行保存.
   - 当属性或技能名称均为中文或均为英文时, 指令是强空格需求的.
   - 录卡一般常见于类似 COC 跑团和 DND 跑团的跑团模式, 部分模式(如SCP模式)是不需要的, 在建卡之前, 请先询问主持人是否需要进行录卡."""
    show = """.show [skill|all|str: attribute] Optional[CQ:at]  人物卡展示
  skill: 查看自身人物卡技能
  all: 查询所有存储的人物卡
  attribute: 该模式下存在的可查看参数
  - 部分参数可能并不在其它模式中支持, 如果管理员加入了第三方插件, 准允的可选参数请询问主持人、骰娘管理员或插件开发者.
  - 例如在 SCP 模式中:
    .show level  展示特工等级 
    .show ability  展示特工能力
    .show money  展示特工余额
  at: 在群聊中`@`一个玩家, `.show`指令将会指向该玩家, 该参数是可选的."""
    roll = """.r[a|d|#|h]  投掷指令 例如:
    .r 10 100 (10D100)
  d  指定骰子面数
    .r 10d100 (10D100)
    - 值得注意的是, `.r 10d100`与`.r 10 100`的效果是等同的.
  a [str: 属性或技能名] [int: 检定难度]  基础属性或技能检定
    .ra 幸运
    在 SCP 模式中, 还支持以下指令:
      .ra 命运 10  检定命运同时指定检定的事件难度为 10(默认为12)
      .ra 灵感/计算机 24  指定以灵感检定计算机技能, 事件难度为24
      - 值得注意的是, 在SCP跑团中, 检定难度应当在 1~25 之间, >25 的难度会直接返回致命失败.
  h  暗骰
    .rh  发起一次`1d100`的暗骰
  #  多轮检定
  b|p  奖励骰 | 惩罚骰
    .rb 4  奖励骰掷骰 4 次
  +|-  附加计算
  .r 1d10+2d6  结果为`1d10`与`2d6`结果的和
  .r 1d8-2  结果为`1d8`与`2`的差
  - 除`.r`指令外, 其它需要进行掷骰的指令均支持附加计算."""
    ra = """.ra [str: name] Optional[int: difficulty]  基础属性或技能检定
  name: 属性或技能名称
  difficulty: 事件难度(可选参数)
    .ra 命运  快速检定`命运`属性
    - 在 SCP 模式中, 还支持以下指令:
      .ra 命运 10  检定命运同时指定检定的事件难度为 10(默认为12)
      .ra 灵感/计算机 24  指定以灵感检定计算机技能, 事件难度为24
    - 值得注意的是, 在SCP跑团中, 检定难度应当在 1~25 之间, >25 的难度会直接返回致命失败."""
    dam = """.dam Optional[check|int: dice|str: dice]
  check: 检定人物当前生命状态
    .dam check
  dice: 伤害掷骰
    .dam 1d6  人物受到`1d6`掷骰结果的伤害
    .dam 6  人物受到 6 点伤害"""
    at = """.at Optional[str: dice|str: weapon]
- 无参数的`.at`指令会进行该模式默认的近战伤害检定
  dice: 掷骰伤害检定
  - SCP 模式中不支持该语法.
    .at 1d6  人物造成`1d6`掷骰结果的伤害
  weapon: 使用武器进行伤害检定
  - 该语法仅在 SCP 模式中支持.
  .at 燃烧瓶  使用燃烧瓶进行伤害检定"""
    en = """.en [str: attribute] [int: encourage]  属性激励
  attribute: 技能名
  encourage: 消耗激励点
    .en 强度 2  激励属性`强度`2 点"""
    delele = """.del [cache|card|str: talent]
  cache: 删除暂存数据
  card: 删除使用中的人物卡(谨慎使用)
  talent: 删除指定的自定义技能
  - 删除自定义技能时, 支持多个参数, 可以一次指定多个技能名."""
    log = """用法：.log <指令> [选项]
描述：
   执行与管理日志相关的各种任务。
指令：
   show          显示所有日志
   add (new) [名称]   添加一个新日志，可选择提供一个名称
   stop [ID]     停止特定 ID 的日志记录
   start [ID]    启动特定 ID 的日志记录
   remove (rm) [ID]  删除特定 ID 的日志记录
   download (load) [ID] 下载特定 ID 的日志记录
示例：
   .log show
   .log add 日志名称
   .log stop 日志ID
注意：
   - 使用 'add' 指令而不带参数以创建一个未命名的日志。"""

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

def regist(name, message, alias=[]):
    if not alias:
        alias = [name, ]

    messages.keys[name] = alias
    setattr(messages, alias[0], message)

if __name__ == "__main__":
    regist("test", "测试指令", alias=["test", "测试指令"])
    print(help_message("test"))
    print(help_message("支持"))