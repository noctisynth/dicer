import string
from dicergirl.reply.provider.provider import Provider, CustomProvider, MatchType
from dicergirl.reply.parser.parser import MessageParser
from dicergirl.reply.parser.matcher import TextMatcher
from dicergirl.common import const


class GenericResponseHandler:
    """
    自定义回复处理器
    """

    def __init__(self):
        self.matcher = TextMatcher()
        self.parser = MessageParser()

    def handle(self, key: string, *args, **kwargs):
        """
        原生 DicerGirl 或 DicerGirl 插件的处理方法
        """
        for provider in const.HARDCODED_PROVIDERS:
            if provider.key == key:
                return self.parser.replacement(provider.value, **kwargs)

    def custom_handle(self, text) -> list[string]:
        """
        匹配并处理，并返回匹配文本
        Args:
            text 用户发送的文本
        Return:
            保存多次匹配后处理的待发送文本
        """
        text_list = []
        for provider in const.KEYWORD_PROVIDERS:
            if self.matcher.match(text, provider.value, provider.matchType):
                if provider.enable:
                    tmp = self.__custom_handle(text, provider)
                    if tmp is not None:
                        text_list.append(tmp)
                    if const.IS_ONE_TIME_MATCH:
                        return text_list
                else:
                    return []
        return text_list

    def __custom_handle(self, text: string, custom_provider: CustomProvider):
        """
        [内部方法]自定义回复的处理方法
        """
        for provider in const.KEYWORD_PROVIDERS:
            if provider.key == custom_provider.key:
                return self.parser.custom_replacement(text, custom_provider)
