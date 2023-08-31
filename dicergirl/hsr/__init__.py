from .trailblazer import Trailblazer
from .nbhandlers import commands
from .hsrcards import hsr_cards

hsr_cards.load()

__type__ = "plugin"
__charactor__ = Trailblazer
__name__ = "hsr"
__cname__ = "开拓者"
__nbhandler__ = nbhandlers
__nbcommands__ = commands
__description__ = "HSR 模式是以游戏 崩坏：星穹铁道(Honkai: Star Rail) 为背景的 TRPG 跑团模式."