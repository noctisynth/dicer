from dicergirl.utils.utils import version

import setuptools

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name = "dicergirl",
    version = version,
    author = "Night Resurgent <fu050409@163.com>",
    author_email = "fu050409@163.com",
    description = "跑团骰娘机器人欧若可, 支持 QQ频道 及 Nonebot2 部署.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitee.com/unvisitor/dicer",
    project_urls = {
        "Bug Tracker": "https://gitee.com/unvisitor/dicer/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license = "Apache-2.0",
    packages = setuptools.find_packages(),
    install_requires = [
        'nb-cli',
        'nonebot2',
        'qq-botpy',
        'watchdog',
        'loguru',
        'pyyaml',
        'openai'
    ],
    python_requires=">=3",
)
