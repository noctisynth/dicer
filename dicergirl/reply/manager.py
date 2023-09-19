import inspect
from dataclasses import dataclass
from typing import Callable, Dict, Type, Tuple, Any, List

from multilogging import multilogger

from dicergirl.common import const
from dicergirl.common.response import GenericResponse
from dicergirl.reply.parsers.matcher import matcher
from dicergirl.reply.parsers.parser import parser
from dicergirl.reply.registry import ReplyRegistry

logger = multilogger(name="DicerGirl", payload="ReplyRegistryManager")


@dataclass
class MethodInfo:
    callable: Callable
    parameters: Dict[str, Type]


class ReplyRegistryManager(ReplyRegistry):
    _inspect_empty = inspect.signature(ReplyRegistry).empty
    global_method: Dict[str, MethodInfo] = {}
    global_variable: Dict[str, Tuple[Type, Any]] = {}

    def register_method(self, method: Callable):

        parameter_type_list = [param.annotation for param in inspect.signature(method).parameters.values()]
        self.global_method[method.__name__] = MethodInfo(method, {name: parameter.annotation
                                                                  for name, parameter in
                                                                  inspect.signature(method).parameters.items()})
        logger.info(f"注册全局方法: {method}")

    def remove_method(self, method_name: str) -> bool:
        if method_name in self.global_method:
            del self.global_method[method_name]
            logger.info(f"销毁全局方法: {method_name}")
            return True
        return False

    def register_variable(self, *arg, **kwargs):
        for key, value in kwargs.items():
            self.global_variable[key] = (type(value), value)
            logger.info(f"注册全局变量: {key}")

    def remove_variable(self, variable_name: str) -> bool:
        if variable_name in self.global_variable:
            logger.info(f"销毁全局变量: {variable_name}")
            del self.global_variable[variable_name]
            return True
        return False

    def process_generic_event(self, event_name: str, *args, **kwargs):
        custom_result = self._handle_generic_event(event_name, self._custom_generic_responses, **kwargs)
        if custom_result is not None:
            return custom_result
        default_result = self._handle_generic_event(event_name, self._default_generic_responses, **kwargs)
        if default_result is not None:
            return default_result
        return None

    def process_message_event(self, message: str):
        """
        根据传入的消息匹配，并返回匹配字段的消息文本

        Parameters:
            message - 用户发送的文本
        """
        result = self._handle_condition_event(message)
        if len(result) == 0:
            return None
        return result

    def call_method(self, method_name: str, *args, **kwargs):
        method_info = self.global_method[method_name]
        if method_info is not None:
            kwargs = self._prepare_arguments(method_name, kwargs)
            if kwargs is not None:
                return self._execute_method(method_info.callable, kwargs)
        else:
            logger.warning(f"Global method '{method_name}' not found.")
        return None

    def _handle_generic_event(self,
                              event_name: str,
                              response_dict: Dict[str, GenericResponse],
                              *args,
                              **kwargs) -> str | None:

        if event_name not in response_dict:
            return None
        send_text = response_dict[event_name].send_text
        kwargs = self._handle_placeholders(send_text, **kwargs)
        return parser.replacement(send_text, **kwargs)

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
                f"Method '{method_name}' expects arguments with keys {list(parameters.keys())}, "
                f"but keys {list(kwargs.keys())} were provided."
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
                    f"Argument '{parameter_name}' for method '{method_name}' has an unexpected type. "
                    f"Expected type: {parameters[parameter_name]}, but got type: {type(parameter)}."
                )
                return None
        return kwargs

    def _handle_condition_event(self, message: str) -> List[str]:
        messages = []
        is_one_time_match = const.IS_ONE_TIME_MATCH
        for response in self._condition_specific_responses.values():
            if matcher.match(message, response.match_field, response.match_type) and response.enable:
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
            logger.error(f"Error executing method '{method.__name__}': {str(e)}")
            return None


manager = ReplyRegistryManager()
