from loguru._logger import Logger, Core
from typing import Union
import sys
import re

def multilogger(
        sink = sys.stdout,
        name: str = "UV Attack",
        payload: str = "",
        format: str = "<!time>[<level>{level}</level>] <cyan><!name></cyan> | <!payload><!module><level>{message}</level>",
        colorize: bool = True,
        level: str = "INFO",
        notime: bool = False,
        *args,
        **kwargs
) -> Logger:
    module = "" if level != "DEBUG" else "<cyan>{module}</cyan>.<cyan>{name}</cyan>:{line} | "
    payload = f"<red>{payload}</red> | " if payload else ""
    time = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> " if not notime else ""

    for match in re.findall(r"(<!.*?>)", format):
        value = re.match(r"^<!(.*?)>$", match)[1]
        format = re.sub(match, eval(value), format)

    logger_instance = Logger(
        core=Core(),
        exception=None,
        depth=0,
        record=False,
        lazy=False,
        colors=False,
        raw=False,
        capture=True,
        patchers=[],
        extra={},
    )
    logger_instance.configure(handlers=[
        {
            "sink": sink,
            "format": format,
            "colorize": colorize,
            "level": level,
        },
    ])
    return logger_instance

if __name__ == "__main__":
    log = multilogger()
    log.info("hhh")
    log2 = multilogger(payload="ARP", notime=False)
    log2.info("hhhhh")
    log.info("hh")