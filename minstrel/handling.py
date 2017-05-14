#!/usr/bin/env python

from typing import Any, Union, Dict, Callable, List, Type
import json
from .types import HandlerDict, Permutations
from .weighted_set import WeightedSet

HandleValues = Callable[[Any, HandlerDict], Permutations]
handle_values: HandleValues = None
from .handlers import handler_map  # noqa


def _any_of_types(value, types):
    return any(isinstance(value, type_) for type_ in types)


def handle_values(
    values: Any, handler_dict: HandlerDict = handler_map
) -> Permutations:
    for types, handler in handler_dict.items():
        nones = [value for value in values if value is None]
        others = [value for value in values if value is not None]

        permutations = WeightedSet()
        for type_ in types:
            if all(_any_of_types(value, types) for value in others):
                permutations = handler(permutations, others)

        if len(permutations) == 0:
            continue

        for none in nones:
            permutations.add(none)

        return permutations

    types = ', '.join(set(type(value).__name__ for value in values))
    raise TypeError('No handler for typeset [{}]'.format(types))
