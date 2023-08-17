from typing import Dict, List, Any

class Optional:
    def __init__(self, key, cls: type=None, default: Any=None):
        if not key:
            raise ValueError("Optional parameter must not be `None`.")

        self.key = key
        self.cls = cls
        self.default = default

    def __str__(self):
        return self.key

class Required:
    def __init__(self, key, cls: type=None, default: Any=None):
        if not key:
            raise ValueError("Required parameter must not be `None`.")

        self.key = key
        self.cls = cls
        self.default = default

    def __str__(self):
        return self.key

class Only:
    def __init__(self, key, default: bool=None):
        if not key:
            raise ValueError("Bool parameter must not be `None`.")

        self.key = key
        self.default = default

    def __str__(self):
        return self.key

class Commands(list):
    def __init__(self, *args, **kwargs):
        super(Commands, self).__init__(*args, **kwargs)

    def __required__(self) -> List[Required]:
        return [required for required in self if isinstance(required, Required)]

    def __optional__(self) -> List[Optional]:
        return [optional for optional in self if isinstance(optional, Optional)]

    def get_plain_required(self) -> List[str]:
        return [str(required) for required in self if isinstance(required, Required)]

    def get_plain_optional(self) -> List[str]:
        return [str(optional) for optional in self if isinstance(optional, Optional)]

    def get_plain_commands(self) -> List[str]:
        return [str(command) for command in self]

def required(commands: Commands):
    return commands.__required__()

def optional(commands: Commands):
    return commands.__optional__()

class CommandParser:
    def __init__(self, commands: Commands=None, args: List[str]=None, auto: bool=False):
        self.results: Dict[str, str] = {}

        if not isinstance(commands, Commands):
            raise ValueError("指令槽必须为类`Commands`.")
        if args and not isinstance(args, (list, tuple)):
            raise ValueError("参数槽必须为列.")

        self.commands = commands
        self.args = args

        if auto:
            self.shlex()

    def shlex(self, args: List[str]=None):
        if not args:
            args = self.args

        if not isinstance(args, (list, tuple)):
            raise ValueError("指令切片必须传入列或数组.")

        results: Dict[str, str] = {}

        for command in self.commands:
            if isinstance(command, Only):
                if command.key in args:
                    results[command.key] = True
                else:
                    results[command.key] = False
                continue

            if command.key in args: 
                index = args.index(command.key)
                if len(args) > index + 1:
                    try:
                        value = command.cls(args[index+1])
                    except ValueError:
                        raise ValueError(f"Value type of {command.key} is mismatch, {command.key} required but {type(args[index+1])} was given.")
                    results[command.key] = value
                else:
                    results[command.key] = command.default
            else:
                if isinstance(command, Required):
                    raise ValueError(f"Required parameter `{command.key}` not found.")

                results[command.key] = command.default
        self.results = results

    def __iter__(self):
        return iter(self.results.items())

if __name__ == "__main__":
    cp = CommandParser(
        Commands([Only("cache"), Optional("age", int), Optional("name", str, "欧若可"), Optional("sex", str), Optional("roll", int)]),
        )
    cp.args = ["cache", "age", "20"]
    cp.shlex()
    print(cp.results)
    cp = CommandParser(
        Commands([Only("cache"), Required("test", int)])
    )
    cp.args = ["cache", "test", "222"]
    cp.shlex()
    print(dict(cp))