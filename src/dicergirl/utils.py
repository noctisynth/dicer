from nonebot.adapters import Bot
from pathlib import Path
from diceutils.status import StatusPool
from infini.core import Core
from infini.loader import Loader
from infini.output import Output

import importlib
import sys
import asyncio

status = StatusPool.register("dicergirl")
core: Core


def get_core():
    return core


def hmr(output: Output = None):
    global core
    importlib.invalidate_caches()

    packages = status.get("bot", "packages") or []

    with Loader() as loader:
        for package in packages:
            for name in [
                name for name in sys.modules.keys() if name.startswith(package)
            ]:
                sys.modules[name] = (
                    importlib.reload(sys.modules[name])
                    if name in sys.modules
                    else importlib.import_module(name)
                )
            sys.modules[package] = (
                importlib.reload(sys.modules[package])
                if package in sys.modules
                else importlib.import_module(package)
            )

            loader.load(package)
        core = loader.into_core()

    if output:
        output.status = 0


def file_upload(bot: Bot, filepath: Path, output: Output):
    asyncio.run(
        bot.call_api(
            "upload_group_file",
            **{
                "group_id": output.variables["group_id"],
                "file": str(filepath),
                "name": filepath.name,
            },
        )
    )
    output.status = 0
