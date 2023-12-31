---
prev:
  link: ./index.md
next:
  link: ./builtins.md
---
# 管理指令

::: tip
`DicerGirl`的管理员权限所有体系与`Nonebot2`的管理员（`SUPERUSER`）不同，它独立于`Nonebot2`存在。我们将会在下个版本中对接 Infini 标准，当前仍然采用 DicerGirl 原生管理系统。
:::

骰娘管理指令是用于处理骰娘与世界主或骰主之间业务的指令体系，包括鉴权系统、权限隔离等。

## `.sudo`指令

::: tip
别名指令与原指令完全等效。
:::

>
> 别名： `.su`
>

该指令用于进行管理员鉴权，使得用户获得骰娘的管理员权限。

你可以简单的执行裸指令来发起一次管理员鉴权：

```bash
.sudo
```

指令发送后，鉴权令牌会在`Nonebot2`的控制终端输出，输出模式为`CRITICAL`。鉴权令牌应当是类似这样的：

```txt
7d571ca69a4711ee8c7b01ee66fa82b19312fb83fba049b39e351a51a5a01b98
```

将鉴权令牌完整复制之后，执行以下指令：

```txt
.sudo 7d571ca69a4711ee8c7b01ee66fa82b19312fb83fba049b39e351a51a5a01b98
```

骰娘将会回复：

```bash
[用户]你成功取得了管理员权限.
```

注意，如果多个鉴权请求同时被发起，那么将只有较晚的鉴权请求会被保留，其它的请求会话会被释放。DicerGirl 鉴权令牌使用`uuid1`与`uuid4`算法生成，它可以保证不会出现令牌的唯一性和安全性。

## `.dismiss`指令
>
> 用法：.dismiss
>

它是指令`.bot exit`的别名。

参考：[`.bot`指令](#bot指令) > [`exit`选项](#exit选项)

## `.bot`指令
>
> 用法：`.bot <指令> [参数]`
>

该指令用于执行与管理插件和机器人设置相关的各种任务。裸指令将会输出机器人相关信息。

### `version`选项
>
> 别名：v, bot, 版本
>

显示机器人版本。

示例：

```bash
.bot version
```

### `exit`选项

::: tip
`.bot exit`为了兼容其它现有骰系，特别新增了`.dismiss`为其别名。`.dismiss`与`.bot exit`是等效的。
:::

>
> 别名：bye, leave, 离开
>

要求机器人退出群聊。为了适配 QQ 平台第三方协议时保证机器人的账号安全，`.bot exit`没有权限要求，任何用户均可以要求骰娘离开群聊。

::: warning
该指令在 QQ 适配器下无效。
:::

### `on`选项
>
> 别名：run, start, 启动
>

关闭指令限制状态并使得机器人进入活跃状态。

::: warning
该指令在 QQ 适配器下无效。
:::

### `off`选项
>
> 别名：down, shutdown, 关闭
>

::: warning
该指令对与`DicerGirl`同级安装的其它插件无效。
:::

开启机器人指令限制，除管理指令外，机器人不再响应任何指令。

::: warning
该指令在 QQ 适配器下无效。
:::

### `upgrade`选项
>
> 别名：up, 更新
>

要求机器人自动升级。

### `downgrade`选项
>
> 别名：降级
> 用法：`.bot downgrade [版本号]`
>

::: warning
强烈不建议使用！你的 DicerGirl 在版本回退后可能无法再次还原，甚至可能遇到不可挽回的问题！

我们强烈建议使你的 DicerGirl 保持最新的版本。
:::

将机器人降级到特定版本。

### `name` 选项
>
> 别名：命名
> 用法：`.bot name [名称]`
>

为你的骰娘命名。

### `status`选项
>
> 别名：状态
>

显示机器人当前运行状态。

### `plgup`选项

::: warning DEPRECATED
将在下一个版本被`.dpm`指令替代。
:::

>
> 别名：pluginup, 升级
> 用法：`.bot plgup <插件名>`
>

升级特定插件。

### `install`选项

::: warning DEPRECATED
将在下一个版本被`.dpm`指令替代。
:::

>
> 别名：add, 安装
> 用法：`.bot install <插件名>`
>

安装新的插件。

### `remove`选项

::: warning DEPRECATED
将在下一个版本被`.dpm`指令替代。
:::

>
> 别名：del, rm, 删除, 卸载
> 用法：`.bot install <插件名>`
>

删除已安装的插件。

### `mode`选项

>
> 别名：list, 已安装
>

列出已安装的插件。

### `store`选项

::: warning DEPRECATED
将在下一个版本被`.dpm`指令替代。
:::

>
> 别名：plugins, 商店
>

显示商店中可用的插件。
