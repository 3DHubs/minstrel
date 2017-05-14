#!/usr/bin/env python

from typing import Any, Iterable, Tuple
from collections import defaultdict
from frozendict import frozendict
from .handlers import handler_map


def _any_of_types(value, types):
    return any(isinstance(value, type_) for type_ in types)


def simplify_value(value: Any) -> Any:
    if isinstance(value, dict):
        return simplify_dict(value)
    if isinstance(value, list):
        return simplify_list(value)

    for types, handler in handler_map.items():
        if _any_of_types(value, types):
            return handler(value)

    raise TypeError('Cannot simplify value of type {}'.format(type(value)))


def simplify_list(values: Iterable[Any]) -> Tuple[Any]:
    out = set()
    for value in values:
        out.add(simplify_value(value))
    return tuple(out)


def simplify_dict(dct: dict) -> dict:
    out = {}
    for key, value in dct.items():
        out[key] = simplify_value(value)

    return frozendict(out)


def simplify_dicts(dicts: Iterable[dict]) -> Tuple[dict]:
    output_dicts = set()
    for dct in dicts:
        output_dicts.add(simplify_dict(dct))
    return tuple(output_dicts)


def best_default_dict(dicts: Iterable[dict]) -> dict:
    key_counts = defaultdict(int)
    keys_map = {}
    for dct in dicts:
        for key in dct:
            key_counts[key] += 1

        keys_map[tuple(dct.keys())] = dct

    best_keys = []
    other_keys = {}
    for key, count in key_counts.items():
        if count > (len(dicts) / 2):
            best_keys.append(key)
        else:
            other_keys[key] = count

    if tuple(best_keys) in keys_map:
        return keys_map[tuple(best_keys)]

    for key, _ in sorted(other_keys.items(), key=lambda l: l[1]):
        best_keys.append(key)

        if tuple(best_keys) in keys_map:
            return keys_map[tuple(best_keys)]
