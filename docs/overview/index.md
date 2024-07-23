---
next:
  link: ../getting-started/index.md
---
# 概览

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dicergirl)&nbsp;
![PyPI](https://img.shields.io/pypi/v/dicergirl)&nbsp;
![PyPI - Wheel](https://img.shields.io/pypi/wheel/dicergirl)&nbsp;
![PyPI - Downloads](https://img.shields.io/pypi/dw/dicergirl)&nbsp;
![PyPI - License](https://img.shields.io/pypi/l/dicergirl)

DicerGirl 是一个开源的、跨平台、可拓展的新一代骰娘框架。它基于 Nonebot2 搭建，具有完整的插件管理系统, 你可以在各种不同的跑团模式（如COC、DND、SCP）中自由切换。

在`DicerGirl`插件系统的支持下，你可以安装任何被支持的跑团模式。

::: warning 注意

很遗憾，`DicerGirl` (夜骰) 已经停止继续维护。经过慎重考虑和评估，我们决定将资源集中于其他战略性项目。

自即日起，我们将不再提供新的功能更新、安全补丁或技术支持。这意味着如果您继续使用 `DicerGirl`，你需要自行承担使用可能造成的任何风险，我们将不再修复任何已知漏洞。我们建议您在接下来的时间内，根据自身需求寻找替代方案或迁移您的数据和骰娘。

目前已有以下较为成熟的解决方案：

- [青果骰 OlivaDice](https://github.com/OlivOS-Team/OlivOS)
- [星骰 AstralDice](https://trpgbot.com/)

同样可以期待正在开发中的水系核心：

- [水系核心](https://github.com/HydroRoll-Team/HydroRollCore)

我们衷心感谢您在过去的时间里对本项目的支持和信任。

感谢您对夜骰的关注和支持！

:::

## 特色

### 规则包系统

DicerGirl 不像传统骰娘那样采用通配式的框架，而是允许不同的规则采用不同的业务处理方法，并允许规则包作者创建属于他们的指令。当然, 通配的默认方法也同样被 DicerGirl 所支持。我们将在下一个版本中使用 [Infini](https://github.com/HydroRoll-Team/infini/) 标准构建跑团规则包。

Infini 是由 [Noctisynth](https://github.com/noctisynth/) 与 [HydroRoll-Team](https://github.com/HydroRoll-Team/) 共同指定的新一代通用型平台机器人文本输入与文本生成标准。

### 插件管理

DicerGirl 具有完整的插件管理系统, 任何开发者都可以发布以自定义跑团模式为规则的插件，任何骰主都有权限下载安装在 Infini 发布的规则包。它不像大多数解决方案在骰主后台进行插件增删处理，而是在支持以上方法的基础上，允许用户简单的在骰娘部署的平台使用骰娘指令对插件进行增删。例如，你可以发送消息：

```bash
.bot 安装 scp
```

骰娘在接收到消息后，会在后台完成 SCP 规则包的安装。

### 自定义昵称

DicerGirl 允许骰主使用指令`.bot name [昵称]`来对骰娘设置一个自定义的昵称。

例如，你可以使用：

```bash
.bot 命名 欧若可
```

这样，你的骰娘便拥有了一个新的名称——“欧若可”。

### 开箱即用

DicerGirl 不需要复杂的配置，如果你熟悉 Nonebot2，你可以快速的使用`nb-cli`安装 DicerGirl：

```bash
nb plugin install dicergirl
```

如果你对没点计算机使用的属性，我们还对计算机使用检定失败的玩家提供了在 Windows 平台快速部署的方案。它使用 DicerGirl Installer 安装并按照指引进行配置即可使用。如果你已经决定开始使用`DicerGirl`，请移步[快速开始](../getting-started/index.md)。
