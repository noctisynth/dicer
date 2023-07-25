# CocDicer

## Introduction
COC Dicer robot based on QQ Guild.

## Software architecture
Python3.10 or later is recommended for any platform that supports the Python3 environment. Python2 is not supported by CocDicer.

## Installation tutorial

1. Install the Python environment
#### Windows
[Python3.11.4 official download address](https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe), because the access speed of python.org in domestic problems, the download address may take a longer time in China.

[Python3.11.4 NPM mirror source](https://registry.npmmirror.com/-/binary/python/3.11.4/python-3.11.4-amd64.exe) download address in China.

Note that during the installation process, be careful to add Python to the environment variable (Path).

#### Ubuntu/Debian/Kali Linux
```
apt install python3 -y
```

#### CentOS
```
yum install python3 -y
```

Open the system terminal (open cmd.exe or Powershell in Windows System), enter 'python -V' and 'pip -V', and the version information is displayed, indicating that the installation is successful.

### 2. Install dependency libraries
First upgrade pip to the latest version:
```
python -m pip install --upgrade pip
pip install wheel setuptools --upgrade
```

Second, install the dependencies required by CocDicer, type in the terminal:
```
pip install watchdog qq-botpy
```

### 3. Configure QQBot
Open the config.yaml file in the root directory, change the 'appid' and 'token' in it to the BotAppId and bot token obtained by creating QQ bot in Tencent [QQ Open Platform](https://q.qq.com/), and run the command in the terminal:
```
python main.py
```

Please note that before executing the instructions, configure your robot according to the QQ Open platform, and open and create QQ channels.

## Statement
This project is open source under the Apache-2.0 protocol, so please follow the open source protocol when using the code.