from typing import Dict, NamedTuple
from collections import defaultdict
from enum import Enum, auto
from ...types import Number, Path
from .base_handler import BaseHandler, Filler


class StringForms(Enum):
    EMPTY = auto()
    FILLED = auto()


class StringFiller(Filler):
    form: StringForms
    path: Path
    original_value: str


class StringHandler(BaseHandler[str, StringFiller, StringForms]):

    filler = StringFiller

    def simplify(self, path, value):
        if len(value) == 0:
            return self.create_filler(StringForms.EMPTY, path, value)

        return self.create_filler(StringForms.FILLED, path, value)
