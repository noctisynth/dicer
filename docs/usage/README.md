# Dicergirl 使用
```
此骰娘基于腾讯 QQ频道(qq-botpy) 及 Nonebot2 搭建.
最终版本由未知访客团队(Unknow Visitor, 原左旋联盟)完成.
感谢 灵冬-老孙 提供相关技术支持.
感谢 @Github: abrahum, 本项目中 COC 模式有部分移植了 @Github: abrahum 的 nonebot_plugin_cocdicer 项目.

.help	帮助信息
.su	进行超级管理员鉴权
.bot	机器人管理
.mode	切换当前跑团模式
.coc	进行车卡, 完成 COC 角色作成
.scp	进行车卡, 完成 SCP 角色作成
.dnd	进行车卡, 完成 DND 角色作成
.set	角色卡设定
.show	角色卡查询
.r	掷骰检定指令
.dam	调查员或特工承伤检定
.at	调查员或特工伤害检定
.sc	疯狂检定
.ti	临时疯狂症状
.li	总结疯狂症状
.en	技能成长
.del	删除数据
输入`.help [指令名]`获取该指令的详细信息
注1: 以上的 "aDb" 格式(例如10D100)的内容, 表示模拟投掷100面骰子, 投掷10次, 结果小于检定值则检定通过.
注2: 该骰娘使用正则表达式对指令解析, 指令参数传递为弱空格需求.
注3: 该骰娘会对英文大小写及中文字符转换, 指令及指令参数为弱大小写和弱中英文区分需求.
注4: 指令帮助内容中`Optional[...]`代表参数可选, `[command]`表示该参数为指令且必须为`command`, `[str: ...]`表示参数为字符串, `[int: ...]`表示参数为数字, `[a|b]`表示参数多选.

欧若可骰娘 版本 {version}, 未知访客开发, 以Apache-2.0协议开源.
Copyright © 2011-2023 Unknown Visitor. Open source as protocol Apache-2.0.
```
如果你需要得到详细的帮助, 建议在群聊中发送`.help [指令名]`来获取该指令的详细信息.

例如你想要详细了解`.scp`指令:
```
.help scp
```