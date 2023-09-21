from typing import Dict

from multilogging import multilogger

from dicergirl.common.response import GenericResponse, ConditionResponse
from dicergirl.reply.parsers.matcher import matcher

logger = multilogger(name="DicerGirl", payload="ReplyData")


class GenericData:
    def __init__(self,
                 group_name: str,
                 version: str,
                 author: str = "",
                 description: str = "",
                 enable: bool = True):
        self.group_name = group_name
        self.items: Dict = {}
        self.version = version
        self.author = author
        self.description = description
        self.enable = enable

    def add(self, *args):
        for data in args:
            if isinstance(data, GenericResponse):
                self.items[data.event_name] = data

    def remove(self, *args):
        for arg in args:
            key = arg.event_name if isinstance(arg, GenericResponse) else str(arg)
            if self.items.get(key) is not None:
                del self.items[key]

    def enable(self, event_name: str = None):
        self.set_event_status(event_name, True)

    def disable(self, event_name: str = None):
        self.set_event_status(event_name, False)

    def toggle(self, event_name: str = None):
        self.set_event_status(event_name)

    def set_event_status(self, event_name: str = None, status: bool = None):
        if event_name is None:
            self.enable = not self.enable if not status else status
        elif self.items.get(event_name):
            self.items[event_name].enable = status if status is not None else not self.items[
                event_name].enable

    def get_response(self, event_name: str) -> GenericResponse:
        for key, value in self.items.items():
            if key == event_name:
                return value

    def is_enable(self, event_name: str = None):
        return self.enable and (not event_name or (self.items.get(event_name) and self.items[event_name].enable))


class ConditionData(GenericData):
    def __init__(self, group_name: str,
                 version: str,
                 author: str = "",
                 description: str = "",
                 enable: bool = True):
        super().__init__(group_name, version, author, description, enable)

    def add(self, *args):
        for data in args:
            if isinstance(data, ConditionResponse):
                self.items[data.event_name] = data

    def get_responses(self, message: str):
        return_dict = {}
        for value in self.items.values():
            if isinstance(value, ConditionResponse):
                if matcher.match(message, value.match_field, value.match_type):
                    return_dict[self] = value
        return return_dict
