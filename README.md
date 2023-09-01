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
跑团骰娘机器人欧若可, 支持所有 Onebot v11 标准的平台.

## 版本特性
`Nonebot2 Onebot v11`部署, 支持增删跑团模式.

此项目目前已支持自定义跑团模块, 详见[开发](docs/develop.md).

## 安装教程
### Windows 快速部署
下载最新版的[`Dicergirl Installer`安装包](https://gitee.com/unvisitor/dginstaller/releases), 安装完成后安装程序会自动部署 DicerGirl, 你可以在终端中提示的`https://127.0.0.1:{port}/go-cqhttp/`中配置 QQ 账号.

其中, `{port}`为随机的端口号.

网页版`go-cqhttp`基于`nonebot-plugin-gocqhttp`.

## 使用教程
你可以在部署完成后, 在相应的平台中发送消息`.help`来查看使用方法.

详细的使用方法见[使用](docs/usage.md).

## 注意
在`Nonebot2`中使用`Dicer Girl`建议不要使用`nonebot-plugin-helper`, 这可能使得`.help`指令与其冲突.

## 漏洞或建议提交
如果你对于 Dicergirl 有建议或发现漏洞, 请在[issues](issues)中提交你的建议.

## 特别鸣谢
 - [Nonebot2](https://github.com/nonebot/nonebot2/) @[yanyongyu](https://github.com/yanyongyu)
 - [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) @[Mrs4s](https://github.com/Mrs4s)
 - [nonebot-plugin-cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer) @[abrahum](https://github.com/abrahum)

## 版权声明
此项目以 Apache-2.0 协议开源, 使用代码时, 请注意遵照开源协议.