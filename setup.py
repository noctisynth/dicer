from dicergirl.utils.utils import version

import setuptools

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name = "dicergirl",
    version = version,
    author = "Night Resurgent <fu050409@163.com>",
    author_email = "fu050409@163.com",
    description = "新一代跨平台开源 TRPG 骰娘框架",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitee.com/unvisitor/dicer",
    project_urls = {
        "Bug Tracker": "https://gitee.com/unvisitor/dicer/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license = "Apache-2.0",
    packages = setuptools.find_packages(),
    install_requires = [
        'nonebot2',
        'nonebot-adapter-onebot',
        'loguru',
        'pyyaml',
        'openai',
        'multilogging',
        'psutil',
        'nonebot_plugin_apscheduler',
        'pypi-simple',
        'httpx',
        'dicergirl-plugin-scp',
    ],
    python_requires=">=3",
)