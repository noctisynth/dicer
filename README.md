<div align="center">
    <img src="https://unvisitor.gitee.io/media/unvisitor/images/unvisitor.png" alt="未知访客" width="200" height="200"></img>
</div>

<div align="center">

# DicerGirl

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dicergirl)
[![PyPI](https://img.shields.io/pypi/v/dicergirl)](https://pypi.org/project/dicergirl/)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/dicergirl)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/dicergirl)](https://pypi.org/project/dicergirl/)
![PyPI - License](https://img.shields.io/pypi/l/dicergirl)

</div>

## 介绍

Noctisynth DicerGirl 是新一代跨平台开源 TRPG 骰娘框架, 公测 QQ 群号：[770386358](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hvaf8JGmEXA3N9r4SGgpghDti31aW1bR&authKey=%2Bux%2BedOIguriMYBMGe40coeOT7mx%2B99%2FVMbK0MvE2w1AsVQLLK%2B0hBO6vVB%2Bmlws&noverify=0&group_code=770386358).

## 安装

### `Nonebot2`原生安装

所有支持 Python3 的操作系统(包括 Windows)均可以安装 DicerGirl.

在使用原始方法安装`DicerGirl`, 请先确保你已经安装了`Python3`并正确配置环境变量.

如果你已有`Nonebot2`项目, 请在`Nonebot2`项目中使用指令:

```bash
nb plugin install dicergirl
```

如果你尚未创建`Nonebot2`项目, 请先确保你已正确安装`nb-cli`:

```bash
pip install nb-cli
```

并使用`nb-cli`创建项目:

```bash
nb create -t bootstrap
```

适配器与驱动器的选择参考你希望使用的适配器，例如`OneBot V11`的驱动器请选择`FastAPI`、`HTTPX`与`websockets`, `QQ`适配器请选择`HTTPX`、`websockets`与`AIOHTTP`.

创建完成后, 在生成的项目目录中执行:

```bash
nb plugin install dicergirl
nb run --reload --reload-delay 2
```

Nonebot2 的项目创建与插件增删详见[Nonebot CLI](https://cli.nonebot.dev/).

### Windows 快速部署

下载最新版的[`Dicergirl Installer`安装包](https://gitee.com/unvisitor/dginstaller/releases), 安装完成后 DGI 会自动部署 DicerGirl, 你可以在终端中提示的`https://127.0.0.1:{port}/go-cqhttp/`中配置 QQ 账号.

其中, `{port}`为随机的端口号.

网页版`go-cqhttp`基于`nonebot-plugin-gocqhttp`.

但值的注意的是, DGI 目前仅适用于 Windows 系统, 且它目前正在加急适配`QQ`协议中.

## 使用教程

你可以在部署完成后, 在相应的平台中发送消息`.help`或`/help`(QQ 协议)来查看使用方法.

详细的使用方法见[使用](docs/usage.md).

## 跑团模块系统

### 支持的跑团模式

|          COC           |          DND           |          SCP           |
| :--------------------: | :--------------------: | :--------------------: |
| `dicergirl-plugin-coc` | `dicergirl-plugin-dnd` | `dicergirl-plugin-scp` |
|           ✅           |           ✅           |           ✅           |

`DicerGirl`作为`Nonebot2`插件存在, 如果你熟悉`Nonebot2`, 你可以使用如下方法直接安装:

```bash
pip install nb-cli
nb create -t bootstrap
nb plugin install dicergirl
```

你可以选择安装其它 DicerGirl 跑团模块:

```bash
pip install dicergirl-plugin-scp
pip install dicergirl-plugin-coc
pip install dicergirl-plugin-dnd
pip install dicergirl-plugin-hsr
```

你同样可以安装第三方插件, 但 Noctisynth 不对其稳定性和安全性负责.

## 跨平台支持

DicerGirl 依赖于`Nonebot2`, 这使得它可以跨平台工作. 除此之外,`Nonebot2`支持的大多平台都 DicerGirl 被支持.

```bash
nb adapter install nonebot-adapter-onebot  # 使用Onebot协议
nb adapter install nonebot-adapter-qqguild  # 使用QQ协议
```

## 注意

在 Nonebot2 中使用 DicerGirl 建议不要使用`nonebot-plugin-helper`, 这可能使得`.help`指令与其冲突.

## 漏洞或建议提交

如果你对于 DicerGirl 有建议或发现漏洞, 请在[issues](issues)中提交你的建议.

## 特别鸣谢

- [Nonebot2](https://github.com/nonebot/nonebot2/) @[yanyongyu](https://github.com/yanyongyu)
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) @[Mrs4s](https://github.com/Mrs4s)
- [nonebot-plugin-cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer) @[abrahum](https://github.com/abrahum)

## 骰娘公测群

公测 QQ 群号：[770386358](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hvaf8JGmEXA3N9r4SGgpghDti31aW1bR&authKey=%2Bux%2BedOIguriMYBMGe40coeOT7mx%2B99%2FVMbK0MvE2w1AsVQLLK%2B0hBO6vVB%2Bmlws&noverify=0&group_code=770386358)

## 发电作者

作者前几天刚弄的[爱发电](https://afdian.net/a/obliviated)，如果你和作者一样穷困潦倒（x），就给这个项目送个 Star 吧！

## 版权声明

此项目以 Apache-2.0 协议开源, 使用代码时, 请注意遵照开源协议.
