import string
from dicergirl.reply.parser.message_parser import MessageParser
from dicergirl.reply.parser.text_matcher import TextMatcher
from dicergirl.common import const


class ReplyHandler:
    """
    自定义回复处理器
    """

    def __init__(self):
        self.matcher = TextMatcher()
        self.parser = MessageParser()

    async def handle(self, key: string, *args, **kwargs):
        """
        原生Dice Girl或Dice Girl插件的处理方法
        """
        for provider in const.DGI_PROVIDERS:
            if provider.key == key:
                return self.parser.replacement(provider.value, **kwargs)

    async def custom_handle(self, message) -> string:
        """
        匹配并处理文本
        """
        for provider in const.CUSTOM_PROVIDERS:
            if self.matcher.match(message, provider.value, provider.matchType):
                if provider.enable:
                    return self.__custom_handle(provider.key)
                else:
                    return None

    async def __custom_handle(self, key: string, *args, **kwargs):
        """
        [内部方法]自定义回复的处理方法
        """
        for provider in const.CUSTOM_PROVIDERS:
            if provider.key == key:
                return self.parser.replacement(provider.value, **kwargs)
