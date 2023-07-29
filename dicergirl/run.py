from loguru import logger
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from multiprocessing import Process, freeze_support
try:
    from .utils.settings import package
except ImportError:
    from utils.settings import package

import sys
import runpy
import time
import os

current_dir = Path(__file__).resolve().parent
exec_dir = current_dir / "main.py"
MODULE_TO_RELOAD = 'main'

if package == "nonebot2":
    logger.critical(
        "模块`run.py`仅允许在`QQGuild`模式下运行, 如果你的确在`QQGuild`运行, 请在你之前导入:\n"
        "    from dicer.utils.settings import set_package\n"
        "并执行:\n"
        "    set_package('qqguild')"
        )
    sys.exit()

class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self):
        super(FileModifiedHandler, self).__init__()
        self.is_modified: bool = False
        self.modified_module: str = None

    def on_modified(self, event):
        if not event.is_directory:
            split = os.path.basename(event.src_path).split(".")
            if len(split) == 1:
                return
            if split[1] == "py":
                self.is_modified = True
                self.modified_module = split[0]

def monitor_folder(folder_path, target=None):
    thread = Process(target=target)
    thread.daemon = True

    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()
    logger.info("文件监视器已启动, `QQGuild`机器人已开启热重载模式.")
    logger.info(f"监视目录: {folder_path}")

    thread.start()
    logger.info("开始启动`QQGuild`机器人...")

    try:
        while True:
            if event_handler.is_modified:
                event_handler.is_modified = False
                if target:
                    if thread.is_alive():
                        logger.info(f"模块`{event_handler.modified_module}`被更改, 开始终止主程序.")
                        thread.terminate()
                        thread.join()
                    logger.info("主线程已终止, 重启中.")
                    thread = Process(target=target)
                    thread.daemon = True
                    thread.start()
                else:
                    raise ValueError("监视线程未传入.")
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("用户要求结束任务, 程序退出.")
        sys.exit()

def run():
    sys.path.insert(0, str(current_dir))
    runpy.run_module(MODULE_TO_RELOAD, run_name="__main__", alter_sys=True)
 
def main():
    freeze_support()
    try:
        monitor_folder(current_dir, target=run)
    except KeyboardInterrupt:
        logger.info("用户要求退出.")
        sys.exit()
    except Exception as e:
        logger.exception(e)

    sys.exit()

if __name__ == "__main__":
    main()