from typing import Dict, Tuple, Any
from frozendict import frozendict

HandlerMap = Dict[Tuple[type, ...], Any]

from .array_handler import ArrayHandler
from .bool_handler import BoolHandler
from .none_handler import NoneHandler
from .number_handler import NumberHandler
from .object_handler import ObjectHandler
from .string_handler import StringHandler


def get_handler_map() -> HandlerMap:
    return {
        (type(None),): NoneHandler(),
        (bool,): BoolHandler(),
        (int, float): NumberHandler(),
        (str,): StringHandler(),
        (dict, frozendict): ObjectHandler(),
        (list, tuple): ArrayHandler(),
    }
