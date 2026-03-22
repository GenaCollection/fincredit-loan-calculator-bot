# callbacks.py

from enum import Enum
from typing import Tuple, List


class CallbackType(str, Enum):
    MAIN_MENU = "main_menu"
    LOAN_DETAILS = "loan_details"
    LOAN_SCHEDULE = "loan_schedule"
    ADD_PAYMENT = "add_payment"
    SETTINGS = "settings"
    HELP = "help"


SEPARATOR = ":"


def make_callback_data(cb_type: CallbackType, *parts: str) -> str:
    return SEPARATOR.join((cb_type.value, *parts))


def parse_callback_data(data: str) -> Tuple[CallbackType, List[str]]:
    head, *rest = data.split(SEPARATOR)
    return CallbackType(head), rest
