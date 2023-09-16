import string
from dicergirl.reply.parser.matcher import MatchType


class Provider:
    """
    :argument key 注册名，用于检索对应的键值
    :argument value 待发送的文本或其他格式
    """
    def __init__(self, key: string, value: string):
        self.key = key
        self.value = value


class CustomProvider(Provider):
    """
    :argument key 注册名，用于检索对应的键值
    :argument value 字符/正则/函数体
    :argument message 匹配成功后，将发送的文本或待执行的函数
    :argument matchType 匹配类型
    :argument enable 是否启用该参数
    """
    def __init__(self, key: string,
                 value: string,
                 message: string,
                 matchType: MatchType,
                 enable=True):
        super().__init__(key, value)
        self.matchType = matchType
        self.message = message
        self.enable = enable
