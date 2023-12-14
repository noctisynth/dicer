---
prev: ./README.md
next: ./deployment.md
---
# 安装

## `Nonebot2`原生安装

::: warning
DicerGirl 依照最新的 PEP 要求进行编写，它遵照了最新的注释要求，然而它在低版本（Python <= 3.8）中可能无法运行。我们强烈推荐使用最新版本的 Python3。
:::

所有支持 Python3 的操作系统(包括 Windows)均可以安装 DicerGirl。

在使用原始方法安装`DicerGirl`， 请先确保你已经安装了`Python3`并正确配置环境变量.

如果你已有`Nonebot2`项目，请在`Nonebot2`项目中使用指令:

```bash
nb plugin install dicergirl
```

如果你尚未创建`Nonebot2`项目，请先确保你已正确安装`nb-cli`：

```bash
pip install nb-cli
```

`Nonebot2`官方推荐使用`pipx`替代`pip`来安装`nb-cli`：

```bash
pip install pipx
pipx install nb-cli
pipx ensurepath
```

在确保`nb-cli`被安装后，你可以执行以下指令来创建`Nonebot2`项目：

```bash
nb create -t bootstrap
```

适配器与驱动器的选择参考你希望使用的适配器，例如`OneBot V11`的驱动器请选择`FastAPI`、`HTTPX`与`websockets`, `QQ`适配器请选择`HTTPX`、`websockets`与`AIOHTTP`。

::: tip
Nonebot2 的项目创建与插件增删详见[Nonebot CLI](https://cli.nonebot.dev/)，我们建议使用`nb-cli`来安装`DicerGirl`。
:::

::: warning
DicerGirl 目前仅确保在`Onebot v11`和`QQ`适配器下正常工作，尽管它允许在任何适配器上运行并被尽可能适配，但是我们没有进行测试。在其它适配器中使用可能出现意外的异常（当然它也大概率正常工作），如果你在使用其它适配器并发现问题，请移步[BUG提交](https://github.com/noctisynth/dicer/issues)
:::

### Windows 快速部署

下载最新版的[`Dicergirl Installer`安装包](https://gitee.com/unvisitor/dginstaller/releases), 安装完成后 DGI 会自动部署 DicerGirl, 你可以在终端中提示的`https://127.0.0.1:{port}/go-cqhttp/`中配置 QQ 账号，其中, `{port}`为随机的端口号。

网页版`go-cqhttp`基于`nonebot-plugin-gocqhttp`。

::: warning
DicerGirl Installer 目前仅适用于 Windows 平台进行 `go-cqhttp` 部署，对其它平台的支持正在开发中。
:::
