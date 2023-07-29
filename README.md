# DicerGirl

## 介绍
跑团骰娘机器人欧若可, 支持 QQ频道 及 Nonebot2 部署.

## 软件架构
任何支持 Python3 环境搭建的平台, 建议使用 Python3.10 及以上的 Python 版本, DicerGirl 不支持 Python2.

## 版本特性
同时支持基于`qq-botpy`的 QQ频道机器人 以及 Nonebot2 Onebot v11. 这使得该库可以在不进行迁移修改的情况下完全兼容腾讯官方支持的 QQ频道机器人 以及功能强大的 Nonebot2.

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
pip install watchdog qq-botpy loguru
```

如果你使用 Nonebot2 模式, 你需要安装 Nonebot2:
```sh
pip install nb-cli
```

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
如果你使用 QQ频道模式, 你需要先打开根目录的 config.yaml 文件, 将其中的`appid`和`token`改成腾讯[QQ 开放平台](https://q.qq.com/)中创建 QQ 机器人所得到的 BotAppId 和 机器人令牌, 在终端中执行命令:
```sh
python run.py
```

你也可以在目录表层创建一个`.py`文件:
```python
from dicergirl.utils.settings import set_package
set_package("qqguild")

from dicer import main

main()
```

它们可以起到相同的效果.

请注意在执行指令之前依照 QQ 开放平台配置自己的机器人，并开启并创建 QQ频道.

#### Nonebot2 模式
1. 直接安装
如果你使用 Nonebot2 作为 Dicer 的引擎, 你应当先注意你是否需要激活虚拟环境, 并执行:
```sh
pip install dicergirl
```

如果你不知道如何激活虚拟环境, 且你使用了 Nonebot2 推荐的`venv`而不是`conda`, 那么你应该打开你的 Nonebot2 项目, 进入`.venv`目录中, 找到`pip`(Windows 中是 `pip.exe`), 然后进入该可执行文件的文件夹, 再执行以上命令.

2. 源文件安装
或者你也可以将克隆的仓库拷贝到: `你的Nonebot2项目目录/src` 中, 并在 pyproject.toml 中的`plugin_dirs`参数中加入`['src']`, 这与直接安装的结果是等同的, 但是这不利于你收到 DicerGirl 的最新更新.

3. 配置完毕
之后, 在终端切入你的 Nonebot2 项目目录并执行:
```sh
nb run --reload
```

## 使用
你可以在部署完成后, 在相应的 QQ 群或者 QQ 频道发送消息`.help`来查看使用方法.

目前已兼容 COC 跑团与 SCP 跑团的大部分指令.

## 声明
此项目由 Apache-2.0 协议开源, 使用代码时, 请注意遵照开源协议.