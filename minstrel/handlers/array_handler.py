from typing import NamedTuple, Dict, Any
from enum import Enum, auto
from collections import defaultdict
from frozendict import frozendict
from ..types import Path
from .base_handler import BaseHandler, ComplexFiller


class ArrayForms(Enum):
    EMPTY = auto()
    FILLED = auto()


class ArrayFiller(ComplexFiller):
    form: ArrayForms
    path: Path
    original_value: tuple


class ArrayHandler(BaseHandler[tuple, ArrayFiller, ArrayForms]):

    pathed_counter: Dict[tuple, int]
    pathed_types: Dict[tuple, set]

    filler = ArrayFiller

    def __init__(self, *args, **kwargs):
        self.pathed_counter = {}
        self.pathed_types = defaultdict(set)
        super().__init__(*args, **kwargs)

    def simplify(self, path: Path, value: tuple):
        if len(value) == 0:
            return self.create_filler(ArrayForms.EMPTY, path, ())

        items = set()
        for index, item in enumerate(value):
            items.add(self.simplify_value(path, item))
        items = tuple(items)

        self.pathed_counter[path] = 0
        self.pathed_types[path].add(items)

        return self.create_filler(ArrayForms.FILLED, path, items)

    def realify(self, path: Path, filler: ArrayFiller) -> list:
        if filler.form == ArrayForms.EMPTY:
            return []

        options = tuple(self.pathed_types[path])

        out = []
        for i, option in enumerate(options[self.pathed_counter[path]]):
            out.append(self.realify_filler(path, option))

        if self.pathed_counter[path] < len(options) - 1:
            self.pathed_counter[path] += 1
        return out
