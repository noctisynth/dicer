import re
import string
from enum import Enum, unique


@unique
class MatchType(Enum):
    """
    EXACT_MATCH 完全匹配
    PARTIAL_MATCH 部分匹配
    REGEX_MATCH 正则匹配
    FUNCTION_MATCH 方法匹配
    """
    EXACT_MATCH = 0
    PARTIAL_MATCH = 1
    REGEX_MATCH = 2
    FUNCTION_MATCH = 3


class TextMatcher:
    def match(self, send_text, match_field: string, match_type: MatchType) -> bool:
        """
        匹配方法
        """
        if match_type == MatchType.EXACT_MATCH:
            return self.__exact_matcher(send_text, match_field)
        elif match_type == MatchType.PARTIAL_MATCH:
            tmp = match_field.split(";")
            return self.__partial_matcher(send_text, *tmp)
        elif match_type == MatchType.REGEX_MATCH:
            return self.__regex_matcher(send_text, match_field)
        elif match_type == MatchType.FUNCTION_MATCH:
            # TODO
            pass

    @staticmethod
    def __exact_matcher(first, second) -> bool:
        """
         完全匹配器
        """
        return str(first) == str(second)

    @staticmethod
    def __partial_matcher(text, *args) -> bool:
        """
        部分匹配器
        """
        for arg in args:
            if str(arg) in str(text):
                return True
        return False

    @staticmethod
    def __regex_matcher(text, regex) -> bool:
        """
        正则匹配器
        """
        return bool(re.match(regex, str(text)))


matcher = TextMatcher()
