from typing import Dict

from multilogging import multilogger
from dicergirl.common.response import GenericResponse, ConditionResponse
from dicergirl.reply.parsers.matcher import MatchType

logger = multilogger(name="DicerGirl", payload="ReplyRegistry")


class ReplyRegistry(object):
    """
    ReplyRegistry 负责存储所有需要交由用户自定义的事件。
    通用回复和特定条件回复的自定义无需手动注册, 请使用 dicergirl.reply.init 下的 init 方法

    Attributes:
        _instance - ReplyRegistryManager 的实例对象
        _default_generic_responses - 存储通用回复
        _custom_generic_response - 存储自定义通用回复
        _condition_specific_responses - 存储条件回复

    Usage:
        registry.register_event("common.sayhi", "你好{user}!") # 注册默认通用回复
        registry.register_event("common.sayhi", "你好{user}!现在是北京时间{time}!", is_custom = True) # 注册自定义通用回复
        registry.register_event("common.sayhi", "你好{user}！","你好", MatchType.EXACT_MATCH) # 注册特定条件下的自定义回复
    """
    _instance = None
    _default_generic_responses: Dict = {}
    _custom_generic_responses: Dict[str, GenericResponse] = {}
    _condition_specific_responses: Dict[str, ConditionResponse] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def register_event(self,
                       event_name: str,
                       send_text: str,
                       match_field: str = None,
                       match_type: MatchType = None,
                       enable: bool = True,
                       is_custom: bool = False,
                       ) -> bool:
        """
        注册事件:
        若只向 event_name, send_text 传参，则向 _default_generic_responses 注册。
        若 match_field 和 match_type 不为空, 则向 _condition_specific_responses 注册。
        若以上条件不皆满足, 且自定义标识为 True, 则向 _custom_generic_responses 注册。

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
        if event_name in self._default_generic_responses or event_name in self._condition_specific_responses:
            return False
        else:
            if match_field is not None and match_type is not None:
                self._condition_specific_responses[event_name] = ConditionResponse(event_name, send_text, match_field,
                                                                                   match_type,
                                                                                   enable)
                logger.info(f"载入自定义条件回复: {event_name}")
            elif is_custom:
                self._custom_generic_responses[event_name] = GenericResponse(event_name, send_text)
                logger.info(f"载入自定义回复: {event_name}")
            else:
                self._default_generic_responses[event_name] = GenericResponse(event_name, send_text)
                logger.info(f"注册回复事件: {event_name}")
            return True

    def remove_event(self, event_name: str, is_custom=False):
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
        if event_name in self._default_generic_responses:
            del self._default_generic_responses[event_name]
        if event_name in self._condition_specific_responses:
            del self._condition_specific_responses[event_name]

    @property
    def generic_event_names(self):
        """
        获取通用事件的所有事件名
        """
        return list(self._default_generic_responses.keys())

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
        return list(self._condition_specific_responses.keys())

    @property
    def all_event_names(self):
        """
        获取所有事件的事件名
        """
        return self.generic_event_names + self.message_event_name
