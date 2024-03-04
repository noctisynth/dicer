from diceutils.status import StatusPool
from infini.core import Core
from infini.loader import Loader
from infini.output import Output

import importlib
import sys

status = StatusPool.register("dicergirl")
core: Core


def get_core():
    return core


def hmr(output: Output = None):
    global core
    importlib.invalidate_caches()

    packages = status.get("bot", "packages") or []

    for package in packages:
        for name in [name for name in sys.modules.keys() if name.startswith(package)]:
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

    with Loader() as loader:
        for package in packages:
            loader.load(package)
        core = loader.into_core()
    
    if output:
        output.status = 0
