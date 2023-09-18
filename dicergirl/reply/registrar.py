from typing import Dict

from dicergirl.reply import handle
from dicergirl.reply.parsers.matcher import MatchType
from dicergirl.reply.response import GenericResponse, ConditionResponse


class ReplyRegistrar(object):
    """
    回复事件注册器。
    负责存储所有需要交由用户自定义的事件，或由用户自定义匹配机制以及回复内容。
    用户自定义通用回复和条件回复无需手动初始化，Usage 1、3仅作为示例。

    Attributes:
        _instance - ReplyRegistrar的实例
        _generic_responses - 存储通用回复
        _custom_generic_response - 存储自定义通用回复
        _condition_responses - 存储条件回复
    Usage 1:
        print(registrar.register("common.sayhi", "你好{user}！", is_custom=True))# 注册自定义通用回复
        # TIPS: 注册自定义通用回复前，需先注册默认通用回复(见`Usage 2`)。否则无法注册，将返回False。
    Output 1:
        False
    Usage 2:
        registrar.register("common.sayhi", "你好{user}!你好{text}!") # 注册默认通用回复
        result = registrar.process_event("common.sayhi",text="世界") # 处理事件并接收文本
        print(result)
    Output 2:
        你好李华!你好世界!
    Usage 3:
        registrar.register("common.sayhi", "你好{user}！","你好", MatchType.EXACT_MATCH) # 注册特定条件下的自定义回复
        print()
    Output 3:
        你好李华!
    """
    _instance = None
    _generic_responses: Dict = {}
    _custom_generic_responses: Dict[str, GenericResponse] = {}
    _condition_responses: Dict[str, ConditionResponse] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, name="registrar"):
        """
        Parameters:
            name - 注册器命名
        """
        self.name = name

    def register(self,
                 event_name: str,
                 send_text: str,
                 match_field: str = None,
                 match_type: MatchType = None,
                 enable: bool = True,
                 is_custom: bool = False,
                 ) -> bool:
        """
        注册事件:
        若只向 event_name, send_text 传参，则向 _generic_responses 注册。
        若 match_field 和 match_type 不为空, 则向 _condition_responses 注册。
        若以上条件不皆满足, 且自定义标识为 True, 则向 _custom_responses 注册。

        Parameters:
            event_name - 事件名
            send_text - 事件对应的响应文本
            match_field - 匹配字段，例如: "<[^>]*>"
            match_type - 匹配类型:相等、包含、正则、特定方法
            enable - 是否启用响应事件
            is_custom - 是否为自定义
        Returns:
            事件注册的是否成功
        """
        if event_name in self._generic_responses or event_name in self._condition_responses:
            return False
        else:
            if match_field is not None and match_type is not None:
                self._condition_responses[event_name] = ConditionResponse(event_name, send_text, match_field,
                                                                          match_type,
                                                                          enable)
            elif is_custom:
                if event_name in self._generic_responses:
                    self._custom_generic_responses[event_name] = GenericResponse(event_name, send_text)
                else:
                    return False
            else:
                self._generic_responses[event_name] = GenericResponse(event_name, send_text)
            return True

    def remove(self, event_name: str, is_custom=False):
        """
        注销事件: 若自定义标识为 True，则只移除 _custom_generic_responses 的 Response。

        Parameters:
            event_name - 注销事件的名称
            is_custom - 是否为用户自定义
        """
        if is_custom:
            if event_name in self._custom_generic_responses:
                del self._custom_generic_responses[event_name]
            return
        if event_name in self._generic_responses:
            del self._generic_responses[event_name]
        if event_name in self._condition_responses:
            del self._condition_responses[event_name]

    def process_event(self, event_name: str, *args, **kwargs):
        custom_result = handle.generic_handle(event_name, self._custom_generic_responses, **kwargs)
        if custom_result is not None:
            return custom_result
        default_result = handle.generic_handle(event_name, self._generic_responses, **kwargs)
        if default_result is not None:
            return default_result
        return None

    def process_message_event(self, message: str):
        """
        根据传入的消息匹配，并返回匹配字段的消息文本

        Parameters:
            message - 用户发送的文本
        """
        pass

    @property
    def generic_event_names(self):
        """
        获取通用事件的所有事件名
        """
        return list(self._generic_responses.keys())

    @property
    def custom_event_names(self):
        """
        获取用户自定义过事件的事件名
        """
        return list(self._custom_generic_responses.keys())

    @property
    def message_event_name(self):
        """
        获取消息事件的所有事件名
        """
        return list(self._condition_responses.keys())

    @property
    def all_event_names(self):
        """
        获取所有事件的事件名
        """
        return self.generic_event_names + self.message_event_name