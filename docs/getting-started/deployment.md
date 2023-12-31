---
prev:
  link: ./installation.md
next:
  link: ./using-dicergirl.md
---
# 部署

在进行部署之前，请确保你已经正确安装`DicerGirl`，否则请先移步[安装](./installation.md)。

## 使用`nb-cli`启动

请在正确安装了`DicerGirl`的`Nonebot2`项目文件夹处执行指令：

```bash
nb run --reload --reload-delay 2
```

我们使用`nb-cli`启动，其中`--reload`与`--reload-delay`允许在`DicerGirl`插件增删或版本更新后自动重启服务并重新挂载规则包。然而，在生产环境下，热重载功能可能同样会为你的服务器增加一些未知的问题。如果你希望规避它，请使用以下指令替代：

```bash
nb run
```

在不使用`--reload`参数的情况下，`DicerGirl`的热更新无法正常使用，这意味着在插件增删后你仍然需要启动`DicerGirl`来使你的更改生效，所以我们依然建议你采用热重载。

如果你需要更多对`nb-cli`的支持，请移步[Nonebot CLI](https://cli.nonebot.dev/)。
