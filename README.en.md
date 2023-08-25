# DicerGirl
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dicergirl)
[![PyPI](https://img.shields.io/pypi/v/dicergirl)](https://pypi.org/project/dicergirl/)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/dicergirl)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/dicergirl)](https://pypi.org/project/dicergirl/)
![PyPI - License](https://img.shields.io/pypi/l/dicergirl)

## Introduction
DicerGirl is a TRPG (Tabletop Role-Playing Game) bot that supports QQ channel and Nonebot2 deployment.

## Software Architecture
It can be deployed on any platform that supports Python3. It is recommended to use Python version 3.10 and above. DicerGirl does not support Python2.

## Version Features
DicerGirl supports both QQ channel bots based on `qq-botpy` and `Nonebot2 Onebot v11`. This makes the library fully compatible with both the officially supported QQ channel bots and the powerful features of Nonebot2.

This project currently supports custom TRPG modules under the Nonebot2 mode. See [Development](#development) for more details.

### Differences Between QQ Channel and Nonebot2
The QQ channel bot only operates in QQ channels. You need to create a QQ channel. This solution is safe and recommended by Tencent, but it comes with limitations. For example, the bot is prohibited from sending unreviewed links or images, and there is a daily limit on message sending. Before using the QQ channel bot mode, you need to register an account on [QQ Open Platform](https://q.qq.com/) and create a bot.

On the other hand, the QQ bot based on [Nonebot2](https://github.com/nonebot/nonebot2), [Onebot v11](https://github.com/botuniverse/onebot), and [Go-CQHTTP](https://github.com/Mrs4s/go-cqhttp) has no limitations. You can use all types of messages that you can send via the QQ software's API. However, this is not a safe solution, as Tencent seems to strongly disapprove of QQ bots using unofficial APIs. You may encounter restrictions or even account bans from Tencent frequently. However, once your account is banned and you complete real-name authentication, Tencent generally will not ban the account again.

## Installation Guide

### 1. Install Python Environment
#### Windows System
[Python3.11.4 Official Download](https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe) This link might take a while to load due to access speed issues from outside China.

[Python3.11.4 NPM Mirror Source](https://registry.npmmirror.com/-/binary/python/3.11.4/python-3.11.4-amd64.exe) This link provides a faster download speed from within China.

During the installation process, make sure to add Python to the system PATH.

#### Ubuntu/Debian/Kali Linux
```sh
apt install python3 python3-pip -y
```

#### CentOS
```sh
yum install python3 python3-devel python3-pip -y
```

Open your system terminal (cmd.exe or Powershell in Windows), and enter `python -V` and `pip -V` to confirm successful installation.

### 2. Install Dependencies
First, upgrade pip to the latest version:
```sh
python -m pip install --upgrade pip
pip install wheel setuptools --upgrade
```

If you're using the QQ Channel mode, you need to install the dependencies needed by Dicer. In the terminal, enter:
```sh
pip install dicergirl
```

If you're using the Nonebot2 mode, you need to install Nonebot2:
```sh
pip install nb-cli
```
If you're facing issues with `nb-cli` after updating `pip`, you can use the native `bot.py` mode of Nonebot2 for running DicerGirl, instead of using the `nb run` command.

If you're deploying both modes, you can use:
```sh
pip install -r requirements.txt
```

This will install all the required dependencies for Dicer as well.

For configuration and usage of Nonebot2 with Go-CQHTTP, I won't go into further detail here.

### 3. Install DicerGirl
Use the following command to install DicerGirl:
```sh
pip install dicergirl
```

#### QQ Channel Mode
If you're using the QQ Channel mode, you need to create a `.py` file and

 write the following content:
```python
from dicergirl.utils.utils import init, set_config
from dicergirl.utils.settings import set_package
from dicergirl.run import main

init()  # Initialize DicerGirl
set_package("qqguild")  # Declare the use of the 'qqguild' mode
set_config("1020*****", "RiFuHMFembccObW*****************")  # Replace with your BotAppID and bot token

if __name__ == "__main__":
    main()
```

Please note that before executing the command, you should configure your own bot on the QQ Open Platform and create and enable a QQ channel.

#### Nonebot2 Mode
1. Install DicerGirl
##### Direct Installation
If you're using Nonebot2 as the engine for Dicer, you should avoid using `nonebot-plugin-helper`, as it may conflict with the `.help` command.

Install DicerGirl using pip:
```sh
pip install dicergirl
```
Using `nb-cli` with Nonebot2 projects created with virtual environments is recommended. However, whether to create a virtual environment is optional when using `nb create`.

If you're unsure how to activate the virtual environment and you're using Nonebot2's default `venv` rather than `conda`, you should navigate to the `.venv` directory in your Nonebot2 project and find the `pip` executable (it's `pip.exe` on Windows). Go to the folder containing this executable and execute the command mentioned above.

If you're using `conda` for virtual environments, you should execute:
```sh
conda activate [venv]
```
Replace `[venv]` with the name of your conda virtual environment.

#### Installing `nb-cli`
```sh
nb plugin install dicergirl
```

##### Installing from Source
Alternatively, you can copy the cloned repository to the `src` directory of your Nonebot2 project and add `'src'` to the `plugin_dirs` parameter in `pyproject.toml`. This method is equivalent to direct installation, but it won't facilitate receiving updates from DicerGirl.

2. Start the Project
##### Using `nb-cli`
Afterward, navigate to your Nonebot2 project directory in the terminal and execute:
```sh
nb run --reload
```
The `--reload` option enables the hot-reloading mode of Nonebot2, allowing you to modify Nonebot2, DicerGirl, or third-party dependencies without manually restarting the program. It'll decide if a project reload is necessary automatically.

Please note that there might be some delay with the `Nonebot2` official `nb-cli`, so the recent `nb plugin install dicergirl` command might not work as expected. In such cases, use `pip` for direct installation or the source file installation.

##### Using the Native `bot.py` Start
If you're unable to successfully install `nb-cli` using `pip`, you can use the following to install `nonebot2`:
```sh
pip install nonebot2 nonebot-adapter-onebot nonebot2[fastapi] nonebot2[httpx] nonebot2[websockets]
```
After successful installation, create a folder and create `bot.py`, `pyproject.toml`, `.env.prod`, and an empty `README.md` file inside it.

Write the following content in each file:

bot.py
```python
#!/bin/python
# File: bot.py
import nonebot

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(nonebot.adapters.onebot.v11.Adapter)

nonebot.load_builtin_plugins('echo')
nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()
```
pyproject.toml
```toml
# File: pyproject.toml
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
After completing these steps, open the terminal and run:
```
python3 bot.py
```
If you're on a Windows system, replace `python3` with `python`:
```
python bot.py
```

## Usage
After deployment, you can send the message `.help` in the appropriate QQ group or QQ channel to view the usage instructions.

The project fully supports COC/SCP/DND tabletop role-playing games.

```
This bot is built on Tencent's QQ channel (qq-botpy) and Nonebot2.
The final version is developed by Unknown Visitor team (formerly known as Zuo Xuan Alliance).
Thanks to Lingdong-LaoSun for providing technical support.
Thanks to @Github: abrahum; some parts of the COC mode are adapted from @Github: abrahum's nonebot_plugin_cocdicer project.

.help	View help information
.su	Superadmin authentication
.bot	Bot management
.mode	Switch current TRPG mode
.coc	Create character sheet for Call of Cthulhu
.scp	Create character sheet for SCP
.dnd	Create character sheet for Dungeons & Dragons
.set	Set character sheet attributes
.show	Query character sheet
.r	Roll dice check
.dam	Damage check for investigator or agent
.at	Attack check for investigator or agent
.sc	Sanity check
.ti	Temporary insanity symptom
.li	Long-term insanity symptom
.en	Skill improvement
.del	Delete data
Enter `.help [command]` to get detailed information about a command.
Note 1: The "aDb" format (e.g., 10D100) indicates rolling a 100-sided die 10 times. If the result is below the target value, the check is successful.
Note 2: The bot uses regular expressions for command parsing, with weak spaces in parameters.
Note 3: The bot handles case conversion for English letters and Chinese characters, and is not case-sensitive for commands or parameters.
Note 4: In the help content of the command, `Optional[...]` represents an optional parameter, `[command]` represents a command parameter, `[str: ...]` represents a string parameter, and `[

int: ...]` represents a numerical parameter. `[a|b]` represents a multiple choice parameter.

DicerGirl TRPG Bot Version {version}, developed by Unknown Visitor, open-source under the Apache-2.0 License.
Copyright © 2011-2023 Unknown Visitor. Open source as protocol Apache-2.0.
```
If you need detailed help, it's recommended to send `.help [command]` in a group chat to get detailed information about a specific command.

For example, if you want to learn more about the `.scp` command:
```
.help scp
```

## Plugin Development
### 1. Configuration
First, create an `__init__.py` file and configure the following content, using SCP mode as an example:
```python
from .agent import Agent

__type__ = "plugin"
__charactor__ = Agent
__name__ = "scp"
__cname__ = "Agent"
```
- `__type__`: Declare this library as a plugin that depends on `Dicer Girl`. The content must be `plugin`.
- `__charactor__`: Reserved for character sheets. See [Creating a Character Sheet](#creating-a-character-sheet).
- `__name__`: Declare the name of this mode. It must be unique and in lowercase English letters without special characters.
- `__cname__`: Default name for characters. For example, in the SCP mode, characters are referred to as "Agents," and in the COC mode, they are referred to as "Investigators."

### 2. Creating a Character Sheet
Create a `charactor.py` (or any other name) file and write the following content:
```python
class Charactor:
    def __init__(self):
        self.name = "Default Character Name"
        self.age = 20  # Default character age
        # ... Other custom attributes
        self.skills = {}

    # ... Other custom methods

    def __str__(self) -> str:  # This could also be __repr__; both are equivalent
        return str  # Return a basic character attribute description
    
    def output(self) -> str:
        return str  # Return a detailed character sheet
    
    def skills_output(self) -> str:
        return str  # Return detailed character skill data

    def out_age(self) -> str:  # Here it's `our_age`; you can use `.show age` command to get its return value
        return f"Character age is: {self.age}"
    
    # ... Other `.show` output content

    def load(self, data: dict):  # You can add specific operations here; this is for importing character sheets
        self.__dict__.update(data)
        return self
```

## Note
When using `Nonebot2` with `Dicer Girl`, it's recommended to avoid using `nonebot-plugin-helper`, as it might conflict with the `.help` command.

## Special Thanks
 - [Nonebot2](https://github.com/nonebot/nonebot2/) @[yanyongyu](https://github.com/yanyongyu)
 - [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) @[Mrs4s](https://github.com/Mrs4s)
 - [nonebot-plugin-cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer) @[abrahum](https://github.com/abrahum)

## License
This project is open-source under the Apache-2.0 License. When using the code, please follow the open-source license.