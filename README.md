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
DicerGirl 新一代跨平台开源 TRPG 骰娘框架.

## 版本特性
使用`Nonebot2 Onebot v11`部署, 支持增删跑团模式.

此项目目前已支持自定义跑团模块, 详见[开发](docs/develop.md).

## 安装教程
### Windows 快速部署
下载最新版的[`Dicergirl Installer`安装包](https://gitee.com/unvisitor/dginstaller/releases), 安装完成后 DGI 会自动部署 DicerGirl, 你可以在终端中提示的`https://127.0.0.1:{port}/go-cqhttp/`中配置 QQ 账号.

其中, `{port}`为随机的端口号.

网页版`go-cqhttp`基于`nonebot-plugin-gocqhttp`.

但值的注意的是, DGI 目前仅适用于 Windows 系统.

## 使用教程
你可以在部署完成后, 在相应的平台中发送消息`.help`来查看使用方法.

详细的使用方法见[使用](docs/usage.md).

## 跑团模块系统
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
你同样可以安装第三方插件, 但未知访客不对其稳定性和安全性负责.

## 跨平台支持
DicerGirl 依赖于 Nonebot2, 这使得它可以跨平台工作. 除此之外, Onebot v11 以及 Nonebot2 支持的任何通讯平台都被支持.
```bash
nb adapter install nonebot-adapter-onebot
nb adapter install nonebot-adapter-qqguild
```

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