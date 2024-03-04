from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from .utils import hmr

pool = ThreadPoolExecutor(20)
workflows = {"echo.hmr": hmr}


def put(func: Callable):
    pool.submit(func)
