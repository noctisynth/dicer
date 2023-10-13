import os
from enum import unique, Enum
from typing import List, Dict

from multilogging import multilogger
from ruamel.yaml import CommentedMap, CommentedSeq

from dicergirl.common import const
from dicergirl.common.const import DEFAULT_GROUP_NAME as NAME
from dicergirl.common.response import GenericResponse, ConditionResponse
from dicergirl.reply.data import GenericData, ConditionData
from dicergirl.reply.parsers.matcher import MatchType

logger = multilogger(name="DicerGirl", payload="ReplyRegistry")


@unique
class ReplyType(Enum):
    """
    事件类型

    - DEFAULT: 默认回复事件，对应值为0。
    - CUSTOM: 自定义回复事件，对应值为1。
    - CONDITION: 条件回复事件，对应值为2。
    """
    DEFAULT = 0,
    CUSTOM = 1,
    CONDITION = 2


class ReplyRegistry:
    """
    ReplyRegistry 负责存储所有需要交由用户自定义的事件。

    通用回复和特定条件回复的自定义无需手动注册，请使用 dicergirl.reply.init 下的 init 方法。

    Attributes:
        _instance (ReplyRegistry): ReplyRegistry 的实例对象。
        _default_generic_data (dict): 存储默认回复的字典。
        _custom_generic_data (dict): 存储自定义通用回复的字典。
        _condition_specific_data (dict): 存储条件回复的字典。

    Methods:
        register_container: 注册数据到相应的容器中
        register_event: 注册事件
        remove_event: 销毁事件
        enable_event: 启用事件
        disable_event: 禁用事件
        toggle_event: 切换事件状态
        generic_event_names: 获取所有默认事件的事件
        custom_event_names: 获取所有自定义事件的事件名
        message_event_names: 获取所有消息事件的事件名
        all_event_names: 获取所有事件的事件名

    Private Methods:
        _register_default_generic_event: 注册默认回复事件
        _register_custom_generic_event: 注册自定义通用回复事件
        _register_condition_specific_event: 注册条件回复事件
        _remove_default_generic_event: 从默认通用数据容器中删除指定事件
        _remove_custom_generic_event: 从自定义通用数据容器中删除指定事件，并从文件中擦除相关数据
        _remove_condition_specific_event: 从条件数据容器中删除指定事件，并从文件中擦除相关数据
        _add_data_in_file: 将数据添加到文件中
        _erase_data_in_file: 从文件中擦除数据

    Usage:
        registry.register_event("common.sayhi", "你好{user}!")  # 注册默认通用回复
        registry.register_event("common.sayhi", "你好{user}!现在是北京时间{time}!", is_custom=True)  # 注册自定义通用回复
        registry.register_event("common.sayhi", "你好{user}！", "你好", MatchType.EXACT_MATCH)  # 注册特定条件下的自定义回复
    """
    _instance = None
    _default_generic_data: Dict[str, GenericData] = {}
    _custom_generic_data: Dict[str, GenericData] = {}
    _condition_specific_data: Dict[str, ConditionData] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._default_generic_data[NAME] = GenericData(NAME, "0.1")
            cls._custom_generic_data[NAME] = GenericData(f"dg-{NAME}", "0.1")
            cls._condition_specific_data[NAME] = ConditionData(NAME, "0.1")
            cls._instance = object.__new__(cls)
        return cls._instance

    def disable_event(self, event_name: str, is_message_event: bool = False, group_name: str = NAME):
        """
        禁用事件

        Args:
            event_name (str): 待禁用事件的事件名
            is_message_event (bool, optional): 是否为消息事件，用于标识特定条件下的回复事件。默认值为 False。
            group_name (str, optional): 数据组的名称。默认值为 NAME。

        Returns:
            bool: 当前事件的状态
        """
        try:
            if is_message_event:
                container = self._condition_specific_data[NAME]
                filename = f"{group_name}.yml"
                cache = const.CONDITION_SPECIFIC_REPLY_FILE_CACHE
            else:
                container = self._custom_generic_data[f"dg-{group_name}"]
                filename = f"dg-{group_name}.yml"
                cache = const.GENERIC_REPLY_FILE_CACHE
            response = container.disable(event_name)
            if not response:
                logger.info(f"没有找到{event_name}对应的Response实例")
                return None
            self._add_data_in_file(filename, cache, response, True)
            return container.is_enable(event_name)
        except KeyError as e:
            logger.error(
                f"请确保您的回复配置文件包含了正确的键和相应的值。如果您不确定如何正确配置文件，请参考文档或向管理员寻求帮助。")
            logger.error(f"Error: {e}")
            return None

    def enable_event(self, event_name: str, is_message_event: bool = False, group_name: str = NAME):
        """
        启用事件

        Args:
            event_name (str): 待启用事件的事件名
            is_message_event (bool, optional): 是否为消息事件，用于标识特定条件下的回复事件。默认值为 False。
            group_name (str, optional): 数据组的名称。默认值为 NAME。
        Returns:
            bool: 当前事件的状态
        """
        try:
            if is_message_event:
                container = self._condition_specific_data[group_name]
                filename = f"{group_name}.yml"
                cache = const.CONDITION_SPECIFIC_REPLY_FILE_CACHE
            else:
                container = self._custom_generic_data[f"dg-{group_name}"]
                filename = f"dg-{group_name}.yml"
                cache = const.GENERIC_REPLY_FILE_CACHE
            response = container.enable(event_name)
            if not response:
                logger.info(f"没有找到{event_name}对应的Response实例")
                return None
            self._add_data_in_file(filename, cache, response, True)
            return container.is_enable(event_name)
        except KeyError as e:
            logger.error(
                f"请确保您的回复配置文件包含了正确的键和相应的值。如果您不确定如何正确配置文件，请参考文档或向管理员寻求帮助。")
            logger.error(f"Error: {e}")
            return None

    def toggle(self, event_name: str, is_message_event: bool = False, group_name: str = NAME):
        """
        切换事件状态

        Args:
            event_name (str): 待切换的事件名
            is_message_event (bool, optional): 是否为消息事件，用于标识特定条件下的回复事件。默认值为 False。
            group_name (str, optional): 数据组的名称。默认值为 NAME。
        Returns:
            bool: 当前事件的状态
        """
        try:
            if is_message_event:
                container = self._condition_specific_data[group_name]
                filename = f"{group_name}.yml"
                cache = const.CONDITION_SPECIFIC_REPLY_FILE_CACHE
            else:
                container = self._custom_generic_data[f"dg-{group_name}"]
                filename = f"dg-{group_name}.yml"
                cache = const.GENERIC_REPLY_FILE_CACHE
            response = container.toggle(event_name)
            if not response:
                logger.info(f"没有找到{event_name}对应的Response实例")
                return None
            self._add_data_in_file(filename, cache, response, True)
            return container.is_enable(event_name)
        except KeyError as e:
            logger.error(
                f"请确保您的回复配置文件包含了正确的键和相应的值。如果您不确定如何正确配置文件，请参考文档或向管理员寻求帮助。")
            logger.error(f"Error: {e}")
            return None

    def register_container(self, data: GenericData) -> bool:
        """
        注册数据到相应的容器中

        Args:
            data (GenericData): 要注册的数据对象

        Returns:
            bool: 如果注册成功，则返回 True；否则返回 False。
        """
        if isinstance(data, ConditionData):
            container = self._condition_specific_data
        elif isinstance(data, GenericData):
            container = self._custom_generic_data
        else:
            logger.warning(f"回复文件'{data.group_name.upper()}'注册失败")
            return False
        container[data.group_name] = data
        if data.group_name in container:
            logger.debug(f"自定义回复文件'{data.group_name.upper()}'注册成功")
            return True
        else:
            logger.warning(f"回复文件'{data.group_name.upper()}'注册失败")
            return False

    def register_event(self,
                       event_name: str,
                       send_text: str,
                       match_field: str = None,
                       match_type: MatchType = None,
                       enable: bool = True,
                       is_custom: bool = False) -> bool:
        """
        注册事件:
        若只向 event_name, send_text 传参，则向 _default_generic_data 注册。
        若 match_field 和 match_type 不为空, 则向 _condition_specific_data 注册。
        若以上条件不皆满足, 且自定义标识为 True, 则向 _custom_generic_data 注册。

        Args:
            event_name (str): 事件名
            send_text (str): 事件对应的响应文本
            match_field (str): 匹配字段，例如: "<[^>]*>"
            match_type (MatchType): 匹配类型:相等、包含、正则、函数
            enable (bool): 是否启用响应事件
            is_custom (bool): 标记，是否为用户自定义事件

        Returns:
            bool: 如果事件成功注册到相关容器中，则返回 True；否则返回 False。
        """
        if match_field and match_type:
            return self._register_condition_specific_event(event_name, send_text, match_field, match_type, enable)
        elif is_custom:
            return self._register_custom_generic_event(event_name, send_text, enable)
        else:
            return self._register_default_generic_event(event_name, send_text, enable)

    def remove_event(self, event_name: str,
                     group_name: str = NAME,
                     reply_type: ReplyType = ReplyType.CUSTOM) -> bool:
        """
        销毁事件

        Args:
            event_name (str): 要删除的事件的名称。
            group_name (str, optional): 数据组的名称。默认值为 NAME。
            reply_type (ReplyType, optional): 事件类型。默认值为 ReplyType。

        Returns:
            bool: 如果成功删除事件，则返回 True；否则返回 False。
        """
        if reply_type is ReplyType.CUSTOM:
            return self._remove_custom_generic_event(event_name, f"dg-{group_name}")
        elif reply_type is ReplyType.CONDITION:
            return self._remove_condition_specific_event(event_name, group_name)
        elif reply_type is ReplyType.DEFAULT:
            return self._remove_default_generic_event(event_name, group_name)
        else:
            logger.error(f"错误的回复类型: {str(reply_type)}")
            return False

    def _register_default_generic_event(self,
                                        event_name: str,
                                        send_text: str,
                                        enable: bool = True) -> bool:
        """
        注册默认回复事件

        Args:
            event_name (str):  事件名
            send_text (str): 事件对应的响应文本
            enable (bool): 是否启用事件

        Returns:
            bool: 如果事件成功注册到_default_generic_data中，则返回 True；否则返回 False。
        """
        container = self._default_generic_data[NAME]
        response_type = "DicerGirl默认回复"

        response = GenericResponse(event_name, send_text, enable)
        container.add(response)

        if container.get_response(event_name):
            logger.debug(f"{response_type}'{event_name}'注册成功")
            return True
        else:
            logger.warning(f"{response_type}'{event_name}'注册失败")
            return False

    def _register_custom_generic_event(self,
                                       event_name: str,
                                       send_text: str,
                                       enable: bool = True) -> bool:
        """
        注册自定义通用回复事件

        Args:
            event_name (str):  事件名
            send_text (str): 事件对应的响应文本
            enable (bool): 是否启用事件

        Returns:
            bool: 如果事件成功注册到_custom_generic_data中，则返回 True；否则返回 False。
        """
        container = self._custom_generic_data[f"dg-{NAME}"]
        response_type = "自定义通用回复"
        filename = f"dg-{NAME}.yml"
        cache = const.GENERIC_REPLY_FILE_CACHE

        response = GenericResponse(event_name, send_text, enable)
        container.add(response)

        self._add_data_in_file(filename, cache, response)

        if container.get_response(event_name):
            logger.debug(f"{response_type}'{event_name}'注册成功")
            return True
        else:
            logger.warning(f"{response_type}'{event_name}'注册失败")
            return False

    def _register_condition_specific_event(self, event_name: str,
                                           send_text: str,
                                           match_field: str,
                                           match_type: MatchType,
                                           enable: bool = True) -> bool:
        """
        注册条件回复事件

        Args:
            event_name (str): 事件名
            send_text (str): 事件对应的响应文本
            match_field (str): 匹配字段，例如: "<[^>]*>"
            match_type (MatchType): 匹配类型:相等、包含、正则、函数
            enable (bool): 是否启用响应事件

        Returns:
            bool: 如果事件成功注册到_condition_specific_data中，则返回 True；否则返回 False。
        """
        container = self._condition_specific_data[NAME]
        response_type = "自定义条件回复"
        filename = f"{NAME}.yml"
        cache = const.CONDITION_SPECIFIC_REPLY_FILE_CACHE

        response = ConditionResponse(event_name, send_text, match_field, match_type, enable)
        container.add(response)

        self._add_data_in_file(filename, cache, response)

        if container.get_response(event_name):
            logger.debug(f"{response_type}'{event_name}'注册成功")
            return True
        else:
            logger.warning(f"{response_type}'{event_name}'注册失败")
            return False

    def _remove_default_generic_event(self, event_name, group_name: str = NAME):
        """
          从默认通用数据容器中删除指定事件。

          Args:
              event_name (str): 要删除的事件的名称。
              group_name (str, optional): 数据组的名称。默认值为 NAME。

          Returns:
              bool: 如果成功删除事件，则返回 True；否则返回 False。
          """
        container = self._default_generic_data[group_name]
        container.remove(event_name)
        if not container.get_response(event_name):
            logger.debug(f"回复事件'{event_name}'销毁成功")
            return True
        else:
            logger.warning(f"回复事件'{event_name}'销毁失败")
            return False

    def _remove_custom_generic_event(self, event_name, group_name: str = NAME):
        """
        从自定义通用数据容器中删除指定事件，并从文件中擦除相关数据。

        Args:
            event_name (str): 要删除的事件的名称。
            group_name (str, optional): 数据组的名称。默认值为 NAME。

        Returns:
            bool: 如果成功删除事件，则返回 True；否则返回 False。
        """
        filename = f"{group_name}.yml"
        cache = const.GENERIC_REPLY_FILE_CACHE

        container = self._custom_generic_data[group_name]
        container.remove(event_name)
        self.erase_data_in_file(filename, event_name, cache)
        if not container.get_response(event_name):
            logger.debug(f"回复事件'{event_name}'销毁成功")
            return True
        else:
            logger.warning(f"回复事件'{event_name}'销毁失败")
            return False

    def _remove_condition_specific_event(self, event_name, group_name: str = NAME):
        """
        从条件数据容器中删除指定事件，并从文件中擦除相关数据。

        Args:
            event_name (str): 要删除的事件的名称。
            group_name (str, optional): 数据组的名称。默认值为 NAME。

        Returns:
            bool: 如果成功删除事件，则返回 True；否则返回 False。
        """
        filename = f"{group_name}.yml"
        cache = const.CONDITION_SPECIFIC_REPLY_FILE_CACHE

        container = self._condition_specific_data[group_name]
        container.remove(event_name)

        self.erase_data_in_file(filename, event_name, cache)
        self.erase_data_in_file(filename, event_name, cache)

        if not container.get_response(event_name):
            logger.debug(f"回复事件'{event_name}'销毁成功")
            return True
        else:
            logger.warning(f"回复事件'{event_name}'销毁失败")
            return False

    @staticmethod
    def _add_data_in_file(filename, cache, response: GenericResponse, is_update=False) -> bool:
        """
        将数据添加到文件中。

        Args:
            filename (str): 文件名
            cache (dict): 缓存数据的字典
            response (GenericResponse): 响应对象

        Returns:
            bool: 如果成功将数据添加到文件中，则返回 True；否则返回 False。

        Raises:
            Exception: 捕获读写YAML文件时产生的未知异常。
        """
        try:
            event_name = response.event_name
            for filepath, data in cache.items():
                if os.path.basename(filepath) == filename:
                    save_data = response.to_dict()
                    tmp = data["items"]
                    if isinstance(tmp, CommentedSeq):
                        found = False
                        for item in list(tmp):
                            if isinstance(item, CommentedMap):
                                for name, content in item.items():
                                    if name == event_name:
                                        item[name] = save_data
                                        found = True
                                        break
                        if not found and not is_update:
                            data["items"].append({event_name: save_data})
                        with open(file=filepath, mode='wb') as drf:
                            const.REPLY_YAML.dump(data=data, stream=drf)
                            break
        except Exception as e:
            logger.error(f"数据持久化异常")
            logger.error(f"Error: {e}")
            return False

    @staticmethod
    def erase_data_in_file(filename, event_name, cache) -> bool:
        """
            从文件中擦除数据。

        Args:
            filename (str): 文件名。
            event_name (str): 事件名称。
            cache (dict): 缓存数据的字典。

        Returns:
            bool: 如果成功从文件中擦除数据，则返回 True；否则返回 False。

        Raises:
            Exception: 捕获读写YAML文件时产生的未知异常。
        """
        try:
            if filename and cache:
                for filepath, data in cache.items():
                    if os.path.basename(filepath) == filename:
                        tmp = data["items"]
                        if isinstance(tmp, CommentedSeq):
                            for item in list(tmp):
                                if isinstance(item, CommentedMap):
                                    tmp_map = CommentedMap()
                                    for name, content in item.items():
                                        if name != event_name:
                                            tmp_map[name] = content
                                    tmp.remove(item)
                                    tmp.append(tmp_map)
                        with open(file=filepath, mode='wb') as drf:
                            const.REPLY_YAML.dump(data=data, stream=drf)
                            break

        except Exception as e:
            logger.error(f"数据擦除异常")
            logger.error(f"Error: {e}")
            return False

    @property
    def generic_event_names(self) -> List[str]:
        """
        获取所有默认事件的事件名

        Returns:
            List[str]: 包含所有默认事件的名称列表
        """
        return [response.event_name for data in self._default_generic_data.values() for response in data.items.values()]

    @property
    def custom_event_names(self) -> List[str]:
        """
        获取所有自定义通用事件的事件名

        Returns:
            List[str]: 包含所有自定义通用事件的名称列表
        """
        return [response.event_name for data in self._custom_generic_data.values() for response in data.items.values()]

    @property
    def message_event_names(self) -> List[str]:
        """
        获取所有消息事件的事件名

        Returns:
            List[str]: 包含所有消息事件的名称列表
        """
        return [response.event_name for data in self._condition_specific_data.values() for response in
                data.items.values()]

    @property
    def all_event_names(self) -> List[str]:
        """
        获取所有事件的事件名

        Returns:
            List[str]: 包含所有事件的事件名称的列表。
        """
        return self.generic_event_names + self.message_event_names + self.custom_event_names
