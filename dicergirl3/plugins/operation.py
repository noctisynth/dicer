from ..utils.version import run_shell_command
from ..common.exceptions.pluginerror import (
    PluginNotFoundError,
    PluginExistsError,
    PluginInstallFailedError,
    PluginUninstallFailedError,
)
from ..utils.plugins import modes
from .parse import get_plugins_mixed
from multilogging import multilogger

import sys


logger = multilogger(name="DicerGirl", payload="plugins.operation")
""" `plugins.operation`日志 """


async def install(name):
    plugins = await get_plugins_mixed()

    if name not in plugins.keys():
        return PluginNotFoundError
    elif name in modes.keys():
        return PluginExistsError

    rsc = await run_shell_command(
        f"\"{sys.executable}\" -m pip install {plugins[name]['package']} -i https://pypi.org/simple"
    )
    if rsc["returncode"] != 0:
        logger.error(rsc["stderr"])
        return PluginInstallFailedError

    return True


async def remove(name):
    plugins = await get_plugins_mixed()

    if name in plugins.keys():
        package = plugins[name]["package"]
    else:
        package = name

    rsc = await run_shell_command(f'"{sys.executable}" -m pip uninstall {package} -y')

    if rsc["returncode"] != 0:
        logger.error(rsc["stderr"])
        return PluginUninstallFailedError

    return True


async def upgrade(name):
    plugins = await get_plugins_mixed()

    if name not in plugins.keys():
        return PluginNotFoundError

    rsc = await run_shell_command(
        f"\"{sys.executable}\" -m pip install {plugins[name]['package']} -i https://pypi.org/simple --upgrade"
    )
    if rsc["returncode"] != 0:
        logger.error(rsc["stderr"])
        return PluginInstallFailedError

    return True
