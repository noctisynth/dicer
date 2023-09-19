from dicergirl.reply.parsers.matcher import MatchType


class GenericResponse:
    """
    存储 DicerGirl 或 DicerGirl 插件的注册名及其回复文本

    :argument event_name 事件名
    :argument send_text 事件对应的响应文本
    """
    def __init__(self, event_name: str, send_text: str):
        self.event_name = event_name
        self.send_text = send_text


class ConditionResponse(GenericResponse):
    """
    存储用户指定条件(正则/字符串/函数体)及符合条件的回复文本

    :argument event_name 事件名
    :argument send_text 事件对应的响应文本
    :argument match_field 匹配字段，例如: "<[^>]*>"
    :argument match_type 匹配类型:相等、包含、正则、特定方法
    :argument enable 是否启用响应事件
    """
    def __init__(self, event_name: str,
                 send_text: str,
                 match_field: str,
                 match_type: MatchType,
                 enable=True):
        super().__init__(event_name, send_text)
        self.match_type = match_type
        self.match_field = match_field
        self.enable = enable
