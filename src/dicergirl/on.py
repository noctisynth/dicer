from nonebot.plugin import on_message, on_startswith
from nonebot.rule import Rule
from nonebot.adapters import Event
from nonebot.matcher import Matcher
from infini.input import Input
from infini.loader import Loader
from diceutils.utils import format_msg
from diceutils.parser import CommandParser, Commands, Optional, Bool

import json
import importlib
import sys


class Interceptor:
    __slots__ = ("msg", "ignorecase")

    def __init__(self, msg: str = "", ignorecase: bool = False):
        self.msg = msg
        self.ignorecase = ignorecase

    def __repr__(self) -> str:
        return f"Interceptor(msg={self.msg}, ignorecase={self.ignorecase})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Interceptor)
            and frozenset(self.msg) == frozenset(other.msg)
            and self.ignorecase == other.ignorecase
        )

    def __hash__(self) -> int:
        return hash((frozenset(self.msg), self.ignorecase))

    async def __call__(self) -> bool:
        return True


interceptor = on_message(Rule(Interceptor()), priority=1, block=True)
ipm = on_startswith(".ipm", priority=0, block=True)

packages = ["dicergirl"]

with Loader() as loader:
    for package in packages:
        loader.load(package)
    core = loader.into_core()


def hmr():
    global core
    importlib.invalidate_caches()

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


@ipm.handle()
async def ipm_handler(event: Event, matcher: Matcher):
    args = format_msg(event.get_plaintext(), begin=".ipm")
    commands = CommandParser(
        Commands(
            [
                Bool("hmr"),
                Optional("add", str),
                Optional("remove", str),
            ]
        ),
        args=args,
        auto=True,
    ).results

    if commands["hmr"]:
        hmr()
        return await matcher.send("Infini 热重载完毕")

    if commands["add"]:
        packages.append(commands["add"])
        hmr()
        return await matcher.send(f"规则包[{commands['add']}]挂载完成")

    if commands["remove"]:
        if commands["remove"] in packages:
            packages.remove(commands["remove"])
            return await matcher.send(f"规则包[{commands['remove']}]卸载完成")
        return await matcher.send(f"规则包[{commands['remove']}]未挂载")

    await matcher.send(
        "Infini Package Manager 版本 1.0.0-beta.1 [IPM for Infini v2.0.6]\n"
        "欢迎使用 IPM, 使用`.help ipm`查看 IPM 使用帮助."
    )


@interceptor.handle()
async def handler(event: Event, matcher: Matcher):
    nb_event_name = event.get_event_name()
    nb_event_type = event.get_type()
    nb_event_description = event.get_event_description()
    nb_event_json: dict = json.loads(event.json())

    nickname = (nb_event_json.get("user", {})).get("nickname") or (
        nb_event_json.get("sender", {})
    ).get("nickname")
    user_id = str(event.get_user_id())
    self_id = nb_event_json.get("self_id")
    group_id = str(event.group_id) if hasattr(event, "group_id") else None
    session_id = event.get_session_id()

    plain_text = event.get_plaintext()
    message = event.get_message()

    input = Input(
        plain_text,
        variables={
            "nickname": nickname,
            "user_id": user_id,
            "self_id": self_id,
            "group_id": group_id,
            "session_id": session_id,
            "nb_event_name": nb_event_name,
            "nb_event_type": nb_event_type,
            "nb_event_description": nb_event_description,
            "nb_event_json": nb_event_json,
            "message": message,
        },
    )

    for output in core.input(input):
        await matcher.send(output)
