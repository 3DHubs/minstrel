from typing import Iterable
import jsonpatch
from .jester.handling import handle_dicts


def differ(dicts: Iterable[dict]) -> Iterable[dict]:
    default, derivatives = handle_dicts(dicts)

    patches = []
    for dct in derivatives:
        patches.append(jsonpatch.make_patch(default, dct))

    return default, patches
