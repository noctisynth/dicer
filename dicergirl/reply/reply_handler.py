import string
from dicergirl.reply.provider.provider import Provider, CustomProvider, MatchType
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

    def handle(self, key: string, *args, **kwargs):
        """
        原生 DicerGirl 或 DicerGirl 插件的处理方法
        """
        for provider in const.DG_PROVIDERS:
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
        for provider in const.CUSTOM_PROVIDERS:
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
        for provider in const.CUSTOM_PROVIDERS:
            if provider.key == custom_provider.key:
                return self.parser.custom_replacement(text, custom_provider)


# 测试用例
# reply_handler = ReplyHandler()
# const.DG_PROVIDERS.append(Provider("common.test.any", "测试"))
# const.DG_PROVIDERS.append(Provider("common.test.time", "你好%user%！现在的时间是:%date%-%time%"))
# const.CUSTOM_PROVIDERS.append(CustomProvider("custom.test.exact.match", "我爱你！", "你是个好人！", MatchType.EXACT_MATCH))
# const.CUSTOM_PROVIDERS.append(CustomProvider("custom.test.exact.match", "蛋", "不是蛋！", MatchType.PARTIAL_MATCH))
# const.CUSTOM_PROVIDERS.append(CustomProvider("custom.test.partial.match", "笨蛋", "哪有笨蛋！", MatchType.PARTIAL_MATCH))
# const.CUSTOM_PROVIDERS.append(
#   CustomProvider("custom.test.regex.match", r"<[^>]*>", "标签内容为：%result%",MatchType.REGEX_MATCH)
# )
# test = reply_handler.handle("common.test.any")
# test_time = reply_handler.handle("common.test.time", user="李华")
# print(f"common.test.any:{test}")
# print(f"common.test.time:{test_time}")
# custom_match1 = reply_handler.custom_handle("好蛋！")
# custom_match2 = reply_handler.custom_handle("你是笨蛋！")
# custom_regex_match = reply_handler.custom_handle("<html><a><span>")
# print("[33m消息[好蛋！]，待发送文本：[0m")
# for text in custom_match1:
#     print(text)
# print("[33m消息[你是笨蛋！]，待发送文本：[0m")
# for text in custom_match2:
#     print(text)
# print("[33m消息[<html><a><span>]，待发送文本：[0m")
# for text in custom_regex_match:
#     print(text)
# const.IS_ONE_TIME_MATCH = True
# custom_match3 = reply_handler.custom_handle("你是笨蛋！")
# print("[33m消息[你是笨蛋！]，待发送文本：[0m")
# for text in custom_match3:
#     print(text)
