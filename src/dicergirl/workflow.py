from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from .utils import hmr, file_upload

pool = ThreadPoolExecutor(20)
workflows = {"echo.hmr": hmr, "echo.upload": file_upload}


def put(func: Callable):
    pool.submit(func)
