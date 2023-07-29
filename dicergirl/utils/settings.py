from loguru import logger

import sys

package = "qqguild"
allowed_packages = ["nonebot2", "qqguild"]

def set_package(pkg: str):
    global package
    pkg = pkg.lower()

    if pkg in allowed_packages:
        package = pkg
        return package
    else:
        try:
            raise ValueError(f"错误的包名:`{pkg}`, 支持的包: {allowed_packages}")
        except Exception as error:
            logger.exception(error)
        sys.exit()

if __name__ == "__main__":
    set_package("?")