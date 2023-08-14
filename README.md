# DicerGirl
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dicergirl)
[![PyPI](https://img.shields.io/pypi/v/dicergirl)](https://pypi.org/project/dicergirl/)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/dicergirl)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/dicergirl)](https://pypi.org/project/dicergirl/)
![PyPI - License](https://img.shields.io/pypi/l/dicergirl)

## 介绍
跑团骰娘机器人欧若可, 支持 QQ频道 及 Nonebot2 部署.

## 软件架构
任何支持 Python3 环境搭建的平台, 建议使用 Python3.10 及以上的 Python 版本, DicerGirl 不支持 Python2.

## 版本特性
同时支持基于`qq-botpy`的 QQ频道机器人 以及 `Nonebot2 Onebot v11`. 这使得该库可以在不进行迁移修改的情况下完全兼容腾讯官方支持的 QQ频道机器人 以及功能强大的 Nonebot2.

此项目目前已支持`Nonebot2`模式下自定义跑团模块, 详见[开发](#开发).

### QQ频道 以及 Nonebot2 的区别
QQ 频道机器人仅支持在 QQ频道 中运行, 你需要创建一个 QQ频道, 这个方案是安全的且被腾讯官方推荐的, 但是它会受到诸多限制, 譬如禁止机器人发送未经审核的链接、禁止机器人发送未经审核的图片等, 同时, QQ频道机器人还存在单日的消息推送上限. 你在使用 QQ 频道机器人模式之前, 需要先前往 [QQ 开放平台](https://q.qq.com/) 注册账号并创建机器人.

基于 [Nonebot2](https://github.com/nonebot/nonebot2)、[Onebot v11](https://github.com/botuniverse/onebot) 以及 [Go-CQHTTP](https://github.com/Mrs4s/go-cqhttp) 实现的 QQ 机器人则不存在任何限制, 你甚至可以像使用 QQ 软件一样调用所有你在软件中能够发送的消息类型的 API. 然而, 这并不是一个安全的方案, 因为腾讯对于采用非官方 API 的 QQ 机器人似乎是深恶痛绝的, 所以你可能会常常遭到腾讯的风控甚至封号, 即便设置了 QSign 的老账号也有可能遭到封号, 不过当你被系统封号一次并完成实名认证之后, 腾讯一般不会再进行封号处理.

## 安装教程

### 1. 安装 Python 环境
#### Windows 系统
[Python3.11.4 官方下载地址](https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe) , 由于 python.org 在国内的访问速度问题, 该下载地址可能会耗时较长.

[Python3.11.4 NPM镜像源](https://registry.npmmirror.com/-/binary/python/3.11.4/python-3.11.4-amd64.exe) 国内下载地址. 

注意，在安装过程中，请注意选择将 Python 加入环境变量(Path)中.

#### Ubuntu/Debian/Kali Linux
```sh
apt install python3 python3-pip -y
```

#### CentOS
```sh
yum install python3 python3-devel python3-pip -y
```

打开系统终端(Windows 中打开 cmd.exe 或 Powershell), 输入`python -V`和`pip -V`, 显示版本信息即代表安装成功.

### 2. 安装依赖库
首先升级 pip 到最新版:
```sh
python -m pip install --upgrade pip
pip install wheel setuptools --upgrade
```

如果你使用 QQ频道模式, 你需要安装 Dicer 所需要的依赖库, 在终端中键入:
```sh
pip install dicergirl
```

如果你使用 Nonebot2 模式, 你需要安装 Nonebot2:
```sh
pip install nb-cli
```
如果你在更新`pip`之后, 你的设备安装`nb-cli`依旧出现错误, 在安装 Dicer Girl 的时候, 你可以采用 Python Nonebot2 原生的`bot.py`模式, 来取代`nb run`指令.

如果你同时部署这两者, 你可以直接采取:
```sh
pip install -r requirements.txt
```

这会安装 Dicer 所需要的所有依赖库.

对于 Nonebot2 与 Go-CQHTTP 的配置和使用, 这里不进行过多赘述.

### 3. 安装 DicerGirl
使用以下指令安装 DicerGirl:
```sh
pip install dicergirl
```

#### 频道模式
如果你使用 QQ频道模式, 你需要穿件一个`.py`文件并写入以下内容
```python
from dicergirl.utils.utils import init, set_config
from dicergirl.utils.settings import set_package
from dicergirl.run import main

init() # 初始化 Dicer Girl
set_package("qqguild") # 声明使用`qqguild`模式
set_config("1020*****", "RiFuHMFembccObW*****************") # 分别填入你的 BotAppID 和机器人令牌

if __name__ == "__main__":
    main()
```

请注意在执行指令之前依照 QQ 开放平台配置自己的机器人，并开启并创建 QQ频道.

#### Nonebot2 模式
1. 安装 Dicer Girl
##### 直接安装
如果你使用 Nonebot2 作为 Dicer 的引擎, 你应当先注意你是否需要激活虚拟环境, 并执行:
```sh
pip install dicergirl
```
使用`nb-cli`创建的 Nonebot2 项目是推荐使用虚拟环境的, 不过你在执行`nb create`之后, 是否创建虚拟环境这一选项是可选的.

如果你不知道如何激活虚拟环境, 且你使用了 Nonebot2 默认的`venv`而不是`conda`, 那么你应该打开你的 Nonebot2 项目, 进入`.venv`目录中, 找到`pip`(Windows 中是 `pip.exe`), 然后进入该可执行文件的文件夹, 再执行以上命令.

如果你使用`conda`作为虚拟环境, 你应当执行:
```sh
conda activate [venv] 
```
其中`[venv]`应该被替换为你设定的 conda 虚拟环境名称.

#### `nb-cli`安装
```sh
nb plugin install dicergirl
```

##### 源文件安装
或者你也可以将克隆的仓库拷贝到: `你的Nonebot2项目目录/src` 中, 并在 pyproject.toml 中的`plugin_dirs`参数中加入`['src']`, 这与直接安装的结果是等同的, 但是这不利于你收到 DicerGirl 的最新更新.

2. 启动项目
##### 使用`nb-cli`启动
之后, 在终端切入你的 Nonebot2 项目目录并执行:
```sh
nb run --reload
```
其中, `--reload`意味着你启用了 Nonebot2 自带的热重载模式, 它使得你可以在你修改某些 Nonebot2、Dicer Girl 或者你自行加入的第三方依赖库之后, 在不手动终止程序的情况下让 Nonebot2 自行判断是否需要重载项目.

值得注意的是, `Nonebot2`官方提供的`nb-cli`可能有延迟, 所以近期`nb plugin install dicergirl`指令可能不能奏效, 请使用`pip`直接安装或者使用源文件安装.

##### 使用`bot.py`原生启动
如果你无法成功通过`pip`安装`nb-cli`, 你使用安装`nonebot2`来替代:
```sh
pip install nonebot2 nonebot-adapter-onebot nonebot2[fastapi] nonebot2[httpx] nonebot2[websockets]
```
安装成功后, 新建一个文件夹, 并创建`bot.py`、`pyproject.toml`、`.env.prod`三个文件, 以及一个空文件`README.md`.

分别写入以下内容:

bot.py
```python
#!/bin/python
# 文件: bot.py
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_builtin_plugins('echo')
nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()
```
pyproject.toml
```toml
# 文件: pyproject.toml
[project]
name = "oracle-dicer"
version = "0.1.0"
description = "oracle-dicer"
readme = "README.md"
requires-python = ">=3.8, <4.0"

[tool.nonebot]
adapters = [
    { name = "OneBot V11", module_name = "nonebot.adapters.onebot.v11" }
]
plugins = ['dicergirl']
plugin_dirs = ['src']
builtin_plugins = ["echo"]
```
.env.prod
```toml
DRIVER=~fastapi+~httpx+~websockets
```
完成后, 打开终端, 执行:
```
python3 bot.py
```
如果你是 Windows 系统, 请使用`python`来替代`python3`:
```
python bot.py
```

## 使用
你可以在部署完成后, 在相应的 QQ 群或者 QQ 频道发送消息`.help`来查看使用方法.

目前已完全支持 COC/SCP/DND 跑团.

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

## 插件开发
### 1. 配置
首先, 创建一个`__init__.py`, 配置以下内容, 这里以 SCP 模式为例:
```python
from .agent import Agent

__type__ = "plugin"
__charactor__ = Agent
__name__ = "scp"
__cname__ = "特工"
```
其中`__type__`声明该库为依赖于`Dicer Girl`的插件, 内容必须为`plugin`.

`__charactor__`为人物卡专有类, 详见[建立一个角色卡](#x-建立一个角色卡).

`__name__`声明该库的模式名称, 该名称必须是唯一的且为小写英文, 不应当有特殊字符.

`__cname__`为角色卡的默认称呼, 例如 SCP 模式中称呼人物为`特工`, COC 模式中称呼人物为`调查员`.

### 2. 建立一个角色卡
新建一个`charactor.py`(也可以为其它名字), 写入以下内容:
```python
class Charactor:
    def __init__(self):
        self.name = "默认人物名"
        self.age = 20 # 默认人物年龄
        # ...其它自定义内容
        self.skills = {}

    # ...其它你的自定义方法

    def __str__(self) -> str: # 也可以是__repr__, 这两者是等效的
        return str # 返回一个人物基本属性描述
    
    def output(self) -> str:
        return str # 返回一个详细的人物卡
    
    def skills_output(self) -> str:
        return str # 返回一个详细的人物技能数据

    def out_age(self) -> str: # 这里为`our_age`, 你可以使用`.show age`指令来得到它的返回值, 同样, 你可以将`age`设置为其它值
        return f"角色年龄为: {self.age}"
    
    # ...其它`.show`输出内容

    def load(self, data: dict): # 这里也可以加入特定操作, 这里是为了导入人物卡
        self.__dict__.update(data)
        return self
```

## 注意
在`Nonebot2`中使用`Dicer Girl`建议不要使用`nonebot-plugin-helper`, 这可能使得`.help`指令与其冲突.

## 特别鸣谢
 - [Nonebot2](https://github.com/nonebot/nonebot2/) @[yanyongyu](https://github.com/yanyongyu)
 - [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) @[Mrs4s](https://github.com/Mrs4s)
 - [nonebot-plugin-cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer) @[abrahum](https://github.com/abrahum)

## 版权声明
此项目以 Apache-2.0 协议开源, 使用代码时, 请注意遵照开源协议.