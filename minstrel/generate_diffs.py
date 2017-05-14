from typing import Iterable
from frozendict import frozendict
import jsonpatch
from .handling import best_default_dict, simplify_dicts


def _unfreeze(dct: frozendict) -> dict:
    if not isinstance(dct, frozendict):
        return dct

    dct = dct._dict
    for key, value in dct.items():
        if isinstance(value, frozendict):
            dct[key] = _unfreeze(value)
        elif isinstance(value, tuple):
            dct[key] = [_unfreeze(item) for item in value]

    return dct


def differ(dicts: Iterable[dict]) -> Iterable[dict]:
    simplified = simplify_dicts(dicts)
    default = _unfreeze(best_default_dict(simplified))

    patches = []
    for dct in simplified:
        if dct == default:
            continue

        dct = _unfreeze(dct)
        patches.append(jsonpatch.make_patch(default, dct))

    return default, patches
