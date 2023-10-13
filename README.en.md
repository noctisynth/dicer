<div align="center">
    <img src="https://unvisitor.gitee.io/media/unvisitor/images/unvisitor.png" alt="Unknown Visitor" width="200" height="200"></img>
</div>

<div align="center">

# DicerGirl
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dicergirl)
[![PyPI](https://img.shields.io/pypi/v/dicergirl)](https://pypi.org/project/dicergirl/)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/dicergirl)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/dicergirl)](https://pypi.org/project/dicergirl/)
![PyPI - License](https://img.shields.io/pypi/l/dicergirl)

</div>

## Introduction
DicerGirl is a new generation cross-platform open-source TRPG (Tabletop Role-Playing Game) dice framework.

## Version Features
Deployed using `Nonebot2 Onebot v11`, supports adding and removing campaign modes.

This project currently supports custom campaign modules, see [Development](docs/develop.md) for details.

The public test QQ group number for this project is: [770386358](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hvaf8JGmEXA3N9r4SGgpghDti31aW1bR&authKey=%2Bux%2BedOIguriMYBMGe40coeOT7mx%2B99%2FVMbK0MvE2w1AsVQLLK%2B0hBO6vVB%2Bmlws&noverify=0&group_code=770386358)

## Installation Tutorial
### Windows Quick Deployment
Download the latest version of [`DicerGirl Installer` package](https://gitee.com/unvisitor/dginstaller/releases), after installation, DGI will automatically deploy DicerGirl. You can configure your QQ account in the terminal with the prompt `https://127.0.0.1:{port}/go-cqhttp/`.

Here, `{port}` is a randomly generated port number.

The web version of `go-cqhttp` is based on `nonebot-plugin-gocqhttp`.

However, it's worth noting that DGI is currently only suitable for Windows systems.

### Linux/MacOS/Other
DicerGirl can be installed on any operating system that supports Python3, including Windows.

To install `DicerGirl` using the original method, make sure you have installed `Python3` and configured the environment variables correctly.

If you already have a `Nonebot2` project, use the command in the `Nonebot2` project:

```bash
nb plugin install dicergirl
```

If you haven't created a `Nonebot2` project yet, make sure you have installed `nb-cli` correctly:

```bash
pip install nb-cli
```

And create the project using `nb-cli`:

```bash
nb create -t bootstrap
```

Select `FastAPi`, `HTTPX`, and `websockets` for the drivers, and `OneBot V11` for the adapter.

After creation, execute the following in the generated project directory:

```bash
nb plugin install dicergirl
nb run --reload
```

For more details on creating projects and adding/removing plugins in Nonebot2, refer to [Nonebot CLI](https://cli.nonebot.dev/).

## Usage Tutorial
After deployment, you can send the message `.help` in the corresponding platform to view usage instructions.

For detailed usage instructions, see [Usage](docs/usage.md).

## Campaign Module System
`DicerGirl` exists as a `Nonebot2` plugin. If you are familiar with `Nonebot2`, you can install it directly using the following method:

```bash
pip install nb-cli
nb create -t bootstrap
nb plugin install dicergirl
```

You can choose to install other DicerGirl campaign modules:

```bash
pip install dicergirl-plugin-scp
pip install dicergirl-plugin-coc
pip install dicergirl-plugin-dnd
pip install dicergirl-plugin-hsr
```

You can also install third-party plugins, but Unknown Visitor is not responsible for their stability and security.

## Cross-Platform Support
DicerGirl depends on Nonebot2, which allows it to work across different platforms. In addition to this, any communication platform supported by Onebot v11 and Nonebot2 is also supported.

```bash
nb adapter install nonebot-adapter-onebot
nb adapter install nonebot-adapter-qqguild
```

## Note
Using `DicerGirl` in `Nonebot2` is recommended without using `nonebot-plugin-helper`, as it may conflict with the `.help` command.

## Vulnerability or Suggestion Submission
If you have suggestions or find vulnerabilities in Dicergirl, please submit them in [issues](issues).

## Special Thanks
 - [Nonebot2](https://github.com/nonebot/nonebot2/) @[yanyongyu](https://github.com/yanyongyu)
 - [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) @[Mrs4s](https://github.com/Mrs4s)
 - [nonebot-plugin-cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer) @[abrahum](https://github.com/abrahum)

## Dice Girl Public Test Group

Public test QQ group number: [770386358](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=hvaf8JGmEXA3N9r4SGgpghDti31aW1bR&authKey=%2Bux%2BedOIguriMYBMGe40coeOT7mx%2B99%2FVMbK0MvE2w1AsVQLLK%2B0hBO6vVB%2Bmlws&noverify=0&group_code=770386358)

## Copyright Notice
This project is open-sourced under the Apache-2.0 license. When using the code, please be sure to comply with the open-source license.