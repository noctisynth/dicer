# CocDicer

## 介绍
基于 QQ 频道的COC跑团骰娘机器人.

## 软件架构
任何支持 Python3 环境搭建的平台, 建议使用 Python3.10 及以上的 Python 版本, CocDicer 不支持 Python2.

## 安装教程

###1. 安装 Python 环境
#### Windows 系统
[Python NPM镜像源国内下载](https://registry.npmmirror.com/-/binary/python/3.11.4/python-3.11.4-amd64.exe)
注意，在安装过程中，请注意选择将 Python 加入环境变量(Path)中.

#### Ubuntu/Debian/Kali Linux
```
apt install python3 -y
```

#### CentOS
```
yum install python3 -y
```

打开系统终端(Windows 中打开 cmd.exe 或 Powershell), 输入`python -V`和`pip -V`, 显示版本信息即代表安装成功.

###2. 安装依赖库
首先升级 pip 到最新版:
```
python -m pip install --upgrade pip
pip install wheel setuptools --upgrade
```

其次安装 CocDicer 所需要的依赖库, 在终端中键入:
`pip install watchdog qq-botpy`

###3. 配置 QQBot
打开根目录的 config.yaml 文件, 将其中的`appid`和`token`改成腾讯[QQ 开放平台](https://q.qq.com/)中创建 QQ 机器人所得到的 BotAppId 和 机器人令牌, 在终端中执行命令:
```
python main.py
```

请注意在执行指令之前依照 QQ 开放平台配置自己的机器人，并开启并创建 QQ频道.

## 声明
此项目由 Apache-2.0 协议开源, 使用代码时, 请注意遵照开源协议.