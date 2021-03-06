from functools import partial
from frozendict import frozendict
from typing import Any, Iterable, Tuple, List
from collections import defaultdict
from .handlers import HandlerMap, get_handler_map
from ..types import Path


def flattenit(pyobj, keytuple=()):
    if hasattr(pyobj, 'items'):
        if len(keytuple) > 0:
            yield keytuple, pyobj
        for key, value in pyobj.items():
            yield from flattenit(value, keytuple + (key,))
    else:
        yield keytuple, pyobj


def _any_of_types(value, types):
    return any(isinstance(value, type_) for type_ in types)


def simplify_value(path: Path, value: Any, handler_map: HandlerMap) -> Any:
    for types, handler in handler_map.items():
        if _any_of_types(value, types):
            return handler.simplify(path, value)

    raise TypeError('Cannot simplify value of type {}'.format(type(value)))


def realify_filler(path: Path, filler: Any, handler_map: HandlerMap) -> Any:
    for types, handler in handler_map.items():
        if _any_of_types(getattr(filler, 'original_value', filler), types):
            return handler.realify(path, filler)

    raise TypeError('Cannot realify value of type {}'
                    .format(type(filler.original_value)))


def best_default_dict(dicts: Iterable[frozendict]) -> frozendict:
    key_counts = defaultdict(int)
    keys_map = {}
    for dct in dicts:
        keys = []
        for key, value in flattenit(dct):
            key_counts[key] += 1
            keys.append(key)

        keys_map[tuple(sorted(keys))] = dct

    best_keys = []
    other_keys = {}
    for key, count in key_counts.items():
        if count > (len(dicts) / 2):
            best_keys.append(key)
        else:
            other_keys[key] = count
        best_keys.sort(key=lambda l: l[0])

    if tuple(best_keys) in keys_map:
        out = keys_map[tuple(best_keys)]
        return out

    sorted_keys = sorted(other_keys.items(), key=lambda l: l[1])
    for key, _ in sorted_keys:
        best_keys.append(key)
        best_keys.sort()

        if tuple(best_keys) in keys_map:
            return keys_map[tuple(best_keys)]

    raise Exception('could not find best default dict')


def handle_dicts(dicts: List[dict]) -> Tuple[dict, List[dict]]:
    handler_map = get_handler_map()

    bound_simplify = partial(simplify_value, handler_map=handler_map)
    bound_realify = partial(realify_filler, handler_map=handler_map)

    for _, handler in handler_map.items():
        handler.simplify_value = bound_simplify
        handler.realify_filler = bound_realify

    simplifieds = set()
    for dct in dicts:
        simple = bound_simplify((), dct)
        simplifieds.add(simple)

    out = []
    for simple in simplifieds:
        out.append(bound_realify((), simple))

    default = best_default_dict(out)
    out.remove(default)

    return default, out
