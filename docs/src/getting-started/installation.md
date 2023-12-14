# 安装

## `Nonebot2`原生安装

::: warning
DicerGirl 依照最新的 PEP 要求进行编写，它遵照了最新的注释要求，然而它在低版本（Python <= 3.8）中可能无法运行。我们强烈推荐使用最新版本的 Python3。
:::

所有支持 Python3 的操作系统(包括 Windows)均可以安装 DicerGirl。

在使用原始方法安装`DicerGirl， 请先确保你已经安装了`Python3`并正确配置环境变量.

如果你已有`Nonebot2`项目，请在`Nonebot2`项目中使用指令:

```bash
nb plugin install dicergirl
```

如果你尚未创建`Nonebot2`项目，请先确保你已正确安装`nb-cli`：

```bash
pip install nb-cli
```

并随后使用`nb-cli`创建项目：

```bash
nb create -t bootstrap
```

适配器与驱动器的选择参考你希望使用的适配器，例如`OneBot V11`的驱动器请选择`FastAPI`、`HTTPX`>与`websockets`, `QQ`适配器请选择`HTTPX`、`websockets`与`AIOHTTP`。

创建完成后，在生成的项目目录中执行：

```bash
nb plugin install dicergirl
nb run --reload --reload-delay 2
```

Nonebot2 的项目创建与插件增删详见[Nonebot CLI](https://cli.nonebot.dev/)。
