from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from .config import Config
from .on import interceptor as interceptor

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-infini",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

