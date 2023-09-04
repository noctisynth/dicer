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

    def __init__(self) -> None:
        self.su = """.su Optional[str: token]  管理员鉴权
  token: 鉴权令牌
  - 鉴权令牌会在执行无参数的`.su`指令后, 在`Nonebot2`的控制终端输出, 输出模式为`CRITICAL`.
  - 需要注意此权限管理系统与`Nonebot2`的`SUPERUSER`不同.
    .su d32ab3...  管理员验证"""
        self.bot = """.bot  机器人管理
  .bot on  机器人启用
  .bot off  机器人禁用
  .bot status  机器人当前状态
  .bot exit  机器人退出群聊"""
        self.mode = """.mode [str: mode]  切换跑团模式
  mode: 跑团模式缩略式
    .mode coc  切换到 COC 跑团模式
  - 如果骰娘管理员加入了第三方跑团插件, `mode`参数应该设置为该插件中`__init__.py`的`__name__`参数, 不区分大小写.
  - 默认的跑团模式为`SCP`, 每一次机器人重启或更新后, 跑团模式都会更改为`SCP`."""
        self.coc = """.coc [age] [roll] [name] [sex] Optioanl[cache]  完成 COC 人物作成
  age: 调查员年龄
  roll: 天命次数
  name: 调查员姓名
  sex: 调查员性别
  - 以上参数均可缺省
    .coc age 20 roll 5 name 欧若可 sex 女  进行5次姓名为`欧若可`的20岁女性调查员天命
  cache: 展示已天命的人物卡
    .coc cache
  - 值得注意的是, 调查员的年龄与调查员的外貌、教育值相关."""
        self.scp = """.scp Optional[begin|reset|deal|upgrade]  完成 SCP 人物卡作成
  begin: 展示基金会基本介绍
    .scp begin
  reset Optional[hp|p|enp|rep|card]: 重置人物卡
  - 无参数的`.scp reset`指令会重置人物所有附加属性, 包括生命值、熟练值、激励点和声望, 但不会改变已升级的技能和特工等级、类别.
    hp: 重置人物卡生命值为最大生命值
      .scp reset hp
    p: 重置人物卡熟练值为最大熟练值
      .scp reset p
    enp: 重置人物卡激励点为最大激励点
      .scp reset enp
    rep: 重置人物卡声望为最大声望
      .scp reset rep
    card: 重置人物卡(请谨慎使用)
    `.scp reset card`指令会重置人物卡为初始状态, 请谨慎使用.
      .scp reset card
  deal Optional[str: weapon]  装备购买
  - 无参数的`.scp deal`指令会给出当前特工允许的购买的武器.
    weapon: 武器名称
      .scp deal 燃烧瓶  购买一个燃烧瓶
  upgrade [str: name] [int: level]  升级技能
    name: 技能名称
    level: 需要提升到的等级
      .scp upgrade 计算机 5  将计算机提升到 5 级."""
        self.dnd = """.dnd Optional[str: age]  完成 DND 人物作成
  age: 冒险者年龄(可选参数)
  - 值得注意的是, 冒险者的年龄与冒险者的外貌、教育值相关."""
        self.set = """.set [str: name] [int: data|str: data]
  name: 属性或技能名称
  - SCP 跑团中不支持设置属性, 同时设置非自定义技能也是不推荐的, 在设置前, 建议先询问主持人的意见.
  data: 目标属性值
    .set 名字 阿斯塔特  将你的名字设置`阿斯塔特`
    - 注意, 当属性或技能名称均为中文或均为英文时, 指令是强空格需求的.
    .set 计算机 80  将你的计算机技能设置为 80
    .set 幸运 +10  将你的幸运增加 10 点
在群聊中输入单独的`.set`指令, 欧若可将自动读取最近一次车卡(即人物卡作成)指令的结果进行保存.
`.set`指令支持批量设置技能来完成录卡, 例如:
  .set 名字 阿斯塔特 幸运 80 ...(将你的名字设置为 “阿斯塔特” 并将你的幸运设置为 80)
  - 值得注意的是, 录卡一般常见于 COC 跑团和 DND 跑团, SCP 模式是不需要的, 在建卡之前, 请先询问主持人是否需要进行录卡.
注意, 虽然该指令同样为弱空格指令解析, 即你不需要在参数之间键入空格, 但是这样的指令是不允许的:
  .set名字阿斯塔特
欧若可将会将该指令识别为同一个参数."""
        self.show = """.show [skill|all|str: attribute] Optional[CQ:at]  人物卡展示
  skill: 查看自身人物卡技能
  all: 查询所有存储的人物卡
  attribute: 该模式下存在的可查看参数
  - 部分参数可能并不在其它模式中支持, 如果管理员加入了第三方插件, 准允的可选参数请询问主持人、骰娘管理员或插件开发者.
  - 例如在 SCP 模式中:
    .show level  展示特工等级 
    .show ability  展示特工能力
    .show money  展示特工余额
  at: 在群聊中`@`一个玩家, `.show`指令将会指向该玩家, 该参数是可选的."""
        self.r = """.r[a|d|#|h]  投掷指令 例如:
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
        self.ra = """.ra [str: name] Optional[int: difficulty]  基础属性或技能检定
  name: 属性或技能名称
  difficulty: 事件难度(可选参数)
    .ra 命运  快速检定`命运`属性
    - 在 SCP 模式中, 还支持以下指令:
      .ra 命运 10  检定命运同时指定检定的事件难度为 10(默认为12)
      .ra 灵感/计算机 24  指定以灵感检定计算机技能, 事件难度为24
    - 值得注意的是, 在SCP跑团中, 检定难度应当在 1~25 之间, >25 的难度会直接返回致命失败."""
        self.sra = self.ra
        self.dam = """.dam Optional[check|int: dice|str: dice]
  check: 检定人物当前生命状态
    .dam check
  dice: 伤害掷骰
    .dam 1d6  人物受到`1d6`掷骰结果的伤害
    .dam 6  人物受到 6 点伤害"""
        self.at = """.at Optional[str: dice|str: weapon]
- 无参数的`.at`指令会进行该模式默认的近战伤害检定
  dice: 掷骰伤害检定
  - SCP 模式中不支持该语法.
    .at 1d6  人物造成`1d6`掷骰结果的伤害
  weapon: 使用武器进行伤害检定
  - 该语法仅在 SCP 模式中支持.
  .at 燃烧瓶  使用燃烧瓶进行伤害检定"""
        self.sc = """.sc [int: success]/[int: failure] Optional[int: SAN]  COC 疯狂检定
  success: 判定成功降低san值, 支持aDb语法(a、b与x为数字)
  failure: 判定失败降低san值, 支持aDb语法(a、b与x为数字)
  SAN: 指定检定的 SAN 值(可选参数)
  - 缺省该参数则会自动使用该用户已保存的人物卡数据."""
        self.ti = ".ti  对调查员进行临时疯狂检定"
        self.li = ".li  对调查员进行总结疯狂检定"
        self.en = """.en [str: attribute] [int: encourage]  属性激励
  attribute: 技能名
  encourage: 消耗激励点
    .en 强度 2  激励属性`强度`2 点"""
        self.delele = """.del [cache|card|str: talent]
  cache: 删除暂存数据
  card: 删除使用中的人物卡(谨慎使用)
  talent: 删除指定的自定义技能
  - 删除自定义技能时, 支持多个参数, 可以一次指定多个技能名."""
        self.log = """.log [add|remove|start|stop|clear] [str: name]
  add: 新增日志
    name: 指定日志文件名
  remove: 删除日志
  start: 启动停止记录的日志
  stop: 中止正在记录的日志
  clear: 删除所有日志(慎用)"""

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