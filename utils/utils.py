from pathlib import Path
from botpy import logging

current_dir = Path(__file__).resolve().parent
_coc_cachepath = current_dir.parent / "data" / "coc_cards.json"
_scp_cachepath = current_dir.parent / "data" / "scp_cards.json"
logger = logging.get_logger()

def get_group_id(message):
    return message.channel_id