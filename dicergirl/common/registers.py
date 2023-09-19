from ..reply.manager import manager
from ..utils.utils import (
    get_name,
    get_group_id,
    get_user_id,
    get_user_card,
    get_mode,
    get_status,
)

def regist_vars():
    manager.register_method(get_name, "BotName")
    manager.register_method(get_group_id, "GroupID")
    manager.register_method(get_user_id, "UserID")
    manager.register_method(get_user_card, "SenderCard")
    manager.register_method(get_mode, "Mode")
    manager.register_method(get_status, "Status")