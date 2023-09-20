from enum import unique, Enum
from typing import Dict

from multilogging import multilogger

from dicergirl.common.const import DEFAULT_GROUP_NAME as NAME
from dicergirl.common.response import GenericResponse, ConditionResponse
from dicergirl.reply.data import GenericData, ConditionData
from dicergirl.reply.parsers.matcher import MatchType

logger = multilogger(name="DicerGirl", payload="ReplyRegistry")


@unique
class ReplyType(Enum):
    DEFAULT = 0,
    CUSTOM = 1,
    CONDITION = 2


class ReplyRegistry(object):
    """
    ReplyRegistry 负责存储所有需要交由用户自定义的事件。
    通用回复和特定条件回复的自定义无需手动注册, 请使用 dicergirl.reply.init 下的 init 方法

    Attributes:
        _instance - ReplyRegistryManager 的实例对象
        _default_generic_data - 存储通用回复
        _custom_generic_response - 存储自定义通用回复
        _condition_specific_data - 存储条件回复

    Usage:
        registry.register_event("common.sayhi", "你好{user}!") # 注册默认通用回复
        registry.register_event("common.sayhi", "你好{user}!现在是北京时间{time}!", is_custom = True) # 注册自定义通用回复
        registry.register_event("common.sayhi", "你好{user}！","你好", MatchType.EXACT_MATCH) # 注册特定条件下的自定义回复
    """
    _instance = None
    _default_generic_data: Dict[str, GenericData] = {}
    _custom_generic_data: Dict[str, GenericData] = {}
    _condition_specific_data: Dict[str, ConditionData] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._default_generic_data[NAME] = GenericData(NAME, "0.1")
            cls._custom_generic_data[NAME] = ConditionData(NAME, "0.1")
            cls._condition_specific_data[NAME] = ConditionData(NAME, "0.1")
            cls._instance = object.__new__(cls)
        return cls._instance

    def register_container(self, data: GenericData):
        if isinstance(data, ConditionData):
            container = self._condition_specific_data
            container[data.group_name] = data
        elif isinstance(data, GenericData):
            container = self._custom_generic_data
            container[data.group_name] = data
        else:
            logger.warning(f"错误的注册类型: {data}")
            return False
        if data.group_name in container.keys():
            logger.info(f"自定义回复文件'{data.group_name.upper()}'注册成功")
            return True
        else:
            logger.warning(f"回复文件'{data.group_name.upper()}'注册失败")
            return True

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
        若只向 event_name, send_text 传参，则向 _default_generic_data 注册。
        若 match_field 和 match_type 不为空, 则向 _condition_specific_data 注册。
        若以上条件不皆满足, 且自定义标识为 True, 则向 _custom_generic_data 注册。

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
        is_condition_specific_data = False
        if match_field and match_type:
            container = self._condition_specific_data[NAME]
            is_condition_specific_data = True
            response_type = "自定义条件回复"
        elif is_custom:
            container = self._custom_generic_data[NAME]
            self._custom_generic_data[NAME].add(GenericResponse(event_name, send_text))
            response_type = "自定义通用回复"
        else:
            container = self._default_generic_data[NAME]
            response_type = "DicerGirl默认回复"
        if is_condition_specific_data:
            container.add(ConditionResponse(event_name, send_text, match_field, match_type, enable))
        else:
            container.add(GenericResponse(event_name, send_text, enable))
        if container.get_response(event_name):
            logger.info(f"{response_type}'{event_name}'注册成功")
            return True
        else:
            logger.warning(f"{response_type}'{event_name}'注册失败")
            return False

    def remove_event(self, event_name: str, reply_type: ReplyType = ReplyType.CONDITION):
        """
        注销事件: 若自定义标识为 True，则只移除 _custom_generic_data 的 Response。

        Parameters:
            event_name - 注销事件的名称
            is_custom - 是否为用户自定义
        """
        if reply_type is ReplyType.CUSTOM:
            container = self._custom_generic_data[NAME]
        elif reply_type is ReplyType.CONDITION:
            container = self._condition_specific_data[NAME]
        elif reply_type is ReplyType.DEFAULT:
            container = self._default_generic_data[NAME]
        else:
            logger.error(f"错误的回复类型: {str(reply_type)}")
            return False
        container.remove(event_name)
        if container.get_response(event_name):
            logger.info(f"回复事件'{event_name}'销毁成功")
            return True
        else:
            logger.warning(f"回复事件'{event_name}'销毁失败")
            return False

    @property
    def generic_event_names(self):
        """
        获取通用事件的所有事件名
        """
        return [v2.event_name for v1 in self._default_generic_data.values() for v2 in v1.items.values()]

    @property
    def custom_event_names(self):
        """
        获取用户自定义过事件的事件名
        """
        return [v2.event_name for v1 in self._custom_generic_data.values() for v2 in v1.items.values()]

    @property
    def message_event_name(self):
        """
        获取消息事件的所有事件名
        """
        return [v2.event_name for v1 in self._condition_specific_data.values() for v2 in v1.items.values()]

    @property
    def all_event_names(self):
        """
        获取所有事件的事件名
        """
        return self.generic_event_names + self.message_event_name
