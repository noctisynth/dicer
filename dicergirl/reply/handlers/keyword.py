from typing import List

from dicergirl.reply.parsers.matcher import TextMatcher

from dicergirl.common import const
from dicergirl.reply.parsers.parser import MessageParser
from dicergirl.reply.response import ConditionResponse


class KeywordResponseHandler:

    def custom_handle(self, text) -> List[str]:
        """
        匹配并处理，并返回匹配文本

        Parameters:
            text - 用户发送的文本
        Returns:
            保存多次匹配后处理的待发送文本
        """
        text_list = []
        for provider in const.KEYWORD_RESPONSES:
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

    def __custom_handle(self, text: str, response: ConditionResponse):
        """
        [内部方法]自定义回复的处理方法
        """
        for provider in const.KEYWORD_RESPONSES:
            if provider.key == response.key:
                return self.parser.custom_replacement(text, response)
