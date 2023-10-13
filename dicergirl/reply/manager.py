import inspect
from dataclasses import dataclass
from typing import Callable, Dict, Type, Tuple, Any, List

from multilogging import multilogger

from dicergirl.common import const
from dicergirl.common.const import DEFAULT_GROUP_NAME as NAME
from dicergirl.common.response import GenericResponse
from dicergirl.reply.data import GenericData, ConditionData
from dicergirl.reply.parsers.parser import parser
from dicergirl.reply.registry import ReplyRegistry

logger = multilogger(name="DicerGirl", payload="ReplyRegistryManager")


@dataclass
class MethodInfo:
    """
     用于存储可调用对象及其参数信息的数据类

     Attributes:
         callable (Callable): 任意方法
         parameters (Dict[str, Type]): 参数信息的字典，其中键为参数名称，值为参数类型
     """
    callable: Callable
    parameters: Dict[str, Type]


class ReplyRegistryManager(ReplyRegistry):
    """
    ReplyRegistryManager 类用于管理全局方法、全局变量和处理消息事件等功能。

    Attributes:
        global_method (Dict[str, MethodInfo]): 用于存储全局方法的字典
        global_variable (Dict[str, Tuple[Type, Any]]): 用于存储全局变量的字典

    Methods:
        register_method: 注册全局方法
        remove_method: 删除全局方法
        register_variable: 注册全局变量
        remove_variable: 删除全局变量
        process_generic_event: 处理通用事件
        process_message_event: 处理消息事件
        call_method: 调用全局方法

    Private Methods:
        _handle_generic_event: 处理通用事件的内部方法
        _handle_placeholders: 处理占位符的内部方法
        _prepare_arguments: 准备方法参数的内部方法
        _filter_arguments: 过滤不匹配参数的内部方法
        _check_argument_types: 检查参数类型的内部方法
        _handle_condition_event: 处理条件事件的内部方法
        _execute_method: 执行方法的内部方法
    """
    _inspect_empty = inspect.signature(ReplyRegistry).empty
    global_method: Dict[str, MethodInfo] = {}
    global_variable: Dict[str, Tuple[Type, Any]] = {}

    def register_method(self, method: Callable, method_name: str = None):
        """
        注册全局方法

        Args:
            method (Callable): 待注册的方法
            method_name (str, optional): 方法的名称。如果未提供，默认使用方法的名称。
        """
        if method_name is None:
            method_name = method.__name__
        self.global_method[method_name] = MethodInfo(method, {name: parameter.annotation
                                                              for name, parameter in
                                                              inspect.signature(method).parameters.items()})
        logger.debug(f"注册全局方法: {method}")

    def remove_method(self, method_name: str) -> bool:
        """
        删除全局方法

        Args:
            method_name (str): 待移除的方法名

        Returns:
            bool: 如果成功删除方法返回 True；否则返回 False。
        """
        if method_name in self.global_method:
            del self.global_method[method_name]
            logger.debug(f"销毁全局方法: {method_name}")
            return True
        return False

    def register_variable(self, **kwargs):
        """
        注册全局变量

        Args:
            **kwargs: 待注册的全局变量
        """
        for key, value in kwargs.items():
            self.global_variable[key] = (type(value), value)
            logger.debug(f"注册全局变量: {key}")

    def remove_variable(self, variable_name: str) -> bool:
        """
        删除全局变量

        Args:
            variable_name (str): 待删除的全局变量名

        Returns:
            bool: 如果成功删除变量，则返回 True；否则返回 False。
        """
        if variable_name in self.global_variable:
            logger.debug(f"销毁全局变量: {variable_name}")
            del self.global_variable[variable_name]
            return True
        return False

    def process_generic_event(self, event_name: str, **kwargs):
        """
        删除全局变量

        Args:
            event_name (str): 待处理的事件名
            **kwargs: 附加参数

        Returns:
            bool: 如果成功删除变量，则返回 True；否则返回 False。
        """
        for container in self._custom_generic_data.values():
            response = container.get_response(event_name)
            if response:
                is_enable = container.is_enable(event_name)
                if response and is_enable:
                    result = self._handle_generic_event(response, **kwargs)
                    if result:
                        return result
                    else:
                        break
        response = self._default_generic_data[NAME].get_response(event_name)
        result = self._handle_generic_event(response, **kwargs)
        if not result:
            logger.warning(f"{event_name}执行结果为: {result}")
        return result

    def process_message_event(self, message: str):
        """
        处理消息事件并返回匹配字段的消息文本

        Args:
            message (str): 用户发送的文本消息

        Returns:
            str | None: 匹配字段的消息文本，如果没有匹配则返回 None。
        """
        result = self._handle_condition_event(message)
        if len(result) == 0:
            return None
        return result

    def call_method(self, method_name: str, **kwargs):
        """
        调用全局方法。

        Args:
          method_name (str): 待调用的方法名
          **kwargs: 方法所需参数

        Returns:
          Any | None: 方法的执行结果，如果发生错误则返回 None。
        """
        method_info = self.global_method[method_name]
        if method_info is not None:
            kwargs = self._prepare_arguments(method_name, kwargs)
            if kwargs is not None:
                return self._execute_method(method_info.callable, kwargs)
        else:
            logger.warning(f"未找到全局方法 '{method_name}'。")
        return None

    def _handle_generic_event(self,
                              response: GenericResponse,
                              **kwargs) -> str | None:
        if not response:
            return None
        kwargs = self._handle_placeholders(response.send_text, **kwargs)
        return parser.replacement(response.send_text, **kwargs)

    def _handle_placeholders(self, send_text, *args, **kwargs):
        for placeholder in parser.get_placeholders(send_text):
            if placeholder not in kwargs:
                if placeholder in self.global_variable:
                    kwargs[placeholder] = self.global_variable[placeholder][1]
                elif placeholder in self.global_method:
                    kwargs[placeholder] = self.call_method(placeholder, **kwargs)
        return kwargs

    def _prepare_arguments(self, method_name, kwargs):
        method_info = self.global_method[method_name]
        parameters = method_info.parameters
        if set(kwargs.keys()) != set(parameters.keys()):
            kwargs = self._filter_arguments(parameters, kwargs)
        if set(kwargs.keys()) != set(parameters.keys()):
            logger.warning(
                f"方法 '{method_name}' 需要拥有参数 {list(parameters.keys())} ，"
                f"但仅提供了 {list(kwargs.keys())}。"
            )
            return None
        kwargs = self._check_argument_types(method_name, kwargs, parameters)
        return kwargs

    def _filter_arguments(self, parameters, kwargs):
        kwargs = {k: v for k, v in kwargs.items() if k in parameters}

        kwargs.update({k: v[1] for k, v in self.global_variable.items() if
                       k not in kwargs and k in parameters and (
                               parameters[k] is v[0] or parameters[k] is self._inspect_empty)})
        return kwargs

    def _check_argument_types(self, method_name, kwargs, parameters):
        for parameter_name, parameter in kwargs.items():
            if (not isinstance(parameter, parameters[parameter_name]) and
                    parameters[parameter_name] is not self._inspect_empty):
                logger.warning(
                    f"方法 '{method_name}' 的参数 '{parameter_name}' 传递的类型错误。 "
                    f"期望的类型为：{parameters[parameter_name]}，但实际类型为：{type(parameter)}。"
                )
                return None
        return kwargs

    def _handle_condition_event(self, message: str) -> List[str]:
        tmp_dict = {}
        messages = []
        is_one_time_match = const.IS_ONE_TIME_MATCH
        for container in self._condition_specific_data.values():
            responses = container.get_responses(message)
            tmp_dict.update(responses)
        for container, response in tmp_dict.items():
            if container.is_enable(response.event_name):
                kwarg = self._handle_placeholders(response.send_text)
                result = parser.replacement(response.send_text, **kwarg)
                if result is not None:
                    messages.append(result)
                if is_one_time_match:
                    break
        return messages

    @staticmethod
    def _execute_method(method: Callable, kwargs):
        try:
            return method(**kwargs)
        except Exception as e:
            logger.warning(f"执行方法 '{method.__name__}' 时发生错误：{str(e)}")
            return None


manager = ReplyRegistryManager()
