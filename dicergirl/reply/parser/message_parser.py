import re
import string
from dicergirl.common import const
from dicergirl.reply import init_reply


class MessageParser:
    """
    消息解析类
    """

    def __init__(self):
        self.regex = r'%([^%]+)%'

    def replacement(self, text, *args, **kwargs):
        """
        替换基本元素
        """
        text = self.process_message(text)

        def replace(match):
            key = match.group(1)
            return str(kwargs.get(key, match.group(0)))

        # replace方法的返回值有类型限定
        return re.sub(self.regex, replace, text)

    def get_placeholders(self, text):
        """
        提取消息中的%内的文本
        """
        return re.findall(self.regex, text)

    def process_message(self, text):
        """
        处理消息并替换%方法名%
        """
        placeholders = self.get_placeholders(text)
        for placeholder in placeholders:
            if self.__check_method_exists(placeholder):
                method = const.TEMPLATE_METHODS[placeholder]
                replacement = method()
                text = text.replace(f'%{placeholder}%', replacement)
        return text

    @staticmethod
    def __check_method_exists(method_name):
        """
        判断是否有对应的方法
        """
        return method_name in const.TEMPLATE_METHODS

