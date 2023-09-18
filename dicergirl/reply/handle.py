from typing import Dict

from dicergirl.reply.parsers.parser import parser
from dicergirl.reply.response import GenericResponse


def generic_handle(event_name: str,
                   response_dict: Dict[str, GenericResponse],
                   *args,
                   **kwargs) -> str | None:
    if event_name in response_dict:
        return parser.replacement(response_dict[event_name].send_text, **kwargs)
    else:
        return None
