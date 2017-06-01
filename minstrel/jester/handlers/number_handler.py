from typing import Dict, NamedTuple
from enum import Enum, auto
from ...types import Number, Path
from .base_handler import BaseHandler, Filler


class NumberForms(Enum):
    ZERO = auto()
    POSITIVE = auto()
    POSITIVE_FLOAT = auto()
    NEGATIVE = auto()
    NEGATIVE_FLOAT = auto()


class NumberFiller(Filler):
    form: NumberForms
    path: Path
    original_value: Number


class NumberHandler(BaseHandler[Number, NumberFiller, NumberForms]):

    filler = NumberFiller

    def simplify(self, path, value):
        if value == 0:
            return self.create_filler(NumberForms.ZERO, path, value)

        if value > 0:
            form = NumberForms.POSITIVE
            if value != int(value):
                form = NumberForms.POSITIVE_FLOAT
        else:
            form = NumberForms.NEGATIVE
            if value != int(value):
                form = NumberForms.NEGATIVE_FLOAT

        return self.create_filler(form, path, value)
