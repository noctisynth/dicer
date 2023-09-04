import sys
from dicergirl.utils.utils import run_shell_command
from dicergirl.errors.pluginerror import PluginNotFoundError, PluginExistsError, PluginInstallFailedError, PluginUninstallFailedError
from dicergirl.utils.plugins import modes

from .parse import get_plugins_mixed

async def install(name):
    plugins = await get_plugins_mixed()

    if name not in plugins.keys():
        return PluginNotFoundError
    elif name in modes.keys():
        return PluginExistsError

    rsc = await run_shell_command(f"{sys.executable} -m pip install {plugins[name]['package']}")
    if rsc["returncode"] != 0:
        return PluginInstallFailedError

    return True

async def remove(name):
    plugins = await get_plugins_mixed()

    if name in plugins.keys():
        package = plugins[name]['package']
    else:
        package = name

    rsc = await run_shell_command(f"{sys.executable} -m pip uninstall {package}")

    if rsc["returncode"] != 0:
        return PluginUninstallFailedError

    return True

async def upgrade(name):
    if name not in modes.keys():
        return PluginNotFoundError

    plugins = await get_plugins_mixed()

    if name not in plugins.keys() or name not in modes.keys():
        return PluginNotFoundError

    rsc = await run_shell_command(f"{sys.executable} -m pip install {plugins[name]['package']}")
    if rsc["returncode"] != 0:
        return PluginInstallFailedError

    return True