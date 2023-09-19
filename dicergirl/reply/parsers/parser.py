import re


class MessageParser:
    """
    消息解析类
    """

    def __init__(self):
        self.regex = '{([^{}]+)}'

    def replacement(self, text, **kwargs):
        """
        替换基本元素
        """
        def replace(match):
            key = match.group(1)
            return str(kwargs.get(key, match.group(0)))

        # replace方法的返回值有类型限定
        return re.sub(self.regex, replace, text)

    def get_placeholders(self, send_text):
        """
        提取消息中的{}内的文本
        """
        return re.findall(self.regex, send_text)


parser = MessageParser()
