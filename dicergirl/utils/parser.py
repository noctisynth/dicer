from typing import Dict, List, Any
from ..common.errors.parseerror import NoneTypeCommandError, CommandRequired, TooManyAliasCommandError

class Optional:
    """ 可选指令 """
    def __init__(self, key: str, cls: type, default: Any=None):
        if not key:
            raise NoneTypeCommandError("Optional parameter must not be `None`.")

        if isinstance(key, str):
            key = [key, ]

        self.key = key
        self.cls = cls
        self.default = default

    def __str__(self):
        return self.key[0]

class Required:
    """ 必选指令 """
    def __init__(self, key, cls: type, default: Any=None):
        if not key:
            raise NoneTypeCommandError("Required parameter must not be `None`.")

        if isinstance(key, str):
            key = [key, ]

        self.key = key
        self.cls = cls
        self.default = default

    def __str__(self):
        return self.key[0]

class Only:
    """ 布尔指令 """
    def __init__(self, key, default: bool=None):
        if not key:
            raise NoneTypeCommandError("Bool parameter must not be `None`.")

        if isinstance(key, str):
            key = [key, ]

        self.key = key
        self.default = default

    def __str__(self):
        return self.key[0]

class Positional:
    """ 定位指令 """
    def __init__(self, key, cls: type, default: Any=None):
        if not key:
            raise NoneTypeCommandError("Postional parameter must not be `None`.")

        if isinstance(key, str):
            key = [key, ]

        self.key = key
        self.cls = cls
        self.default = default

    def __str__(self):
        return self.key[0]

class Commands(list):
    """ 指令集合 """
    def __init__(self, *args, **kwargs):
        super(Commands, self).__init__(*args, **kwargs)

    def __required__(self) -> List[Required]:
        return [required for required in self if isinstance(required, Required)]

    def __optional__(self) -> List[Optional]:
        return [optional for optional in self if isinstance(optional, Optional)]

    def __positional__(self) -> List[Positional]:
        return [positional for positional in self if isinstance(positional, Positional)]

    def get_plain_required(self) -> List[str]:
        return [str(required) for required in self if isinstance(required, Required)]

    def get_plain_optional(self) -> List[str]:
        return [str(optional) for optional in self if isinstance(optional, Optional)]

    def get_plain_positional(self) -> List[str]:
        return [str(positional) for positional in self if isinstance(positional, Positional)]

    def get_plain_commands(self) -> List[str]:
        return [str(command) for command in self]

def required(commands: Commands):
    return commands.__required__()

def optional(commands: Commands):
    return commands.__optional__()

def positional(commands: Commands):
    return commands.__positional__()

class CommandParser:
    """指令解析类
    示例:
        ```python
        cp = CommandParser(
            Commands([Optional("optional"), Required("required"), Only("bool"), ...]),
            args = ["required", "valueofrequired", "bool"],
            auto = True # 自动解析指令, `auto=True`时, `args`不得为空
            ).results
        print(cp["optional"]) # 输出为`None`
        print(cp["required"]) # 输出为`valueofrequired`
        print(cp["bool"]) # 输出为`True`
        ```
    """
    def __init__(self, commands: Commands=None, args: List[str]=None, auto: bool=False):
        self.results: Dict[str, str] = {}

        if not isinstance(commands, Commands):
            raise TypeError("指令槽必须为类`Commands`.")
        if args and not isinstance(args, (list, tuple)):
            raise TypeError("参数槽必须为列或数组.")

        self.commands = commands
        self.args = args
        self.nothing = False

        if auto:
            self.shlex()

    def shlex(self, args: List[str]=None):
        """ 开始拆析指令集合 """
        if not args:
            args = self.args
        iter_args = [arg for arg in args]

        if not isinstance(args, (list, tuple)):
            raise TypeError("指令切片必须传入列或数组.")

        results: Dict[str, str] = {}
        nothing: bool = True

        for command in self.commands:
            key = list(set(command.key) & set(args))
            if len(key) > 1:
                raise TooManyAliasCommandError("Too many alias parameters.")

            if isinstance(command, Only):
                if key:
                    results[command.key[0]] = True
                    iter_args.remove(key[0])
                    nothing = False
                else:
                    results[command.key[0]] = False
                continue

            if key:
                index = args.index(key[0])
                iter_index = iter_args.index(key[0])
                if len(args) > index + 1:
                    try:
                        value = command.cls(args[index+1])
                    except ValueError:
                        raise TypeError(f"Value type of {command.key} is mismatch, {command.key} required but {type(args[index+1])} was given.")
                    results[command.key[0]] = value
                    iter_args.pop(iter_index)
                    iter_args.pop(iter_index)
                    nothing = False
                else:
                    results[command.key[0]] = command.default
            else:
                if isinstance(command, Required):
                    raise CommandRequired(f"Required parameter `{command.key[0]}` not found.")

                results[command.key[0]] = command.default

        positional_commands = positional(self.commands)
        str_positionals = self.commands.get_plain_positional()
        for positional_command in positional_commands:
            if len(iter_args) == 0:
                break

            index = str_positionals.index(str(positional_command))
            if len(iter_args) >= index+1:
                try:
                    value = positional_command.cls(iter_args[index])
                except ValueError:
                    raise TypeError(f"Value type of {positional_command.key} is mismatch, {positional_command.key} required but {type(iter_args[index])} was given.")
                results[str(positional_command)] = value

        self.results = results
        self.nothing = nothing

    def __iter__(self):
        return iter(self.results.items())

if __name__ == "__main__":
    cp = CommandParser(
        Commands([Positional("roll", int), Only("cache"), Positional("test", int), Optional("age", int), Optional(("name", "n"), str, "欧若可"), Optional("sex", str)]),
        )
    cp.args = ["cache", "age", "20", "n", "先生", "7", "10"]
    cp.shlex()
    print(cp.results)
    print(type(cp.results["roll"]))