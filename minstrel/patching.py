from logging import getLogger
from typing import Iterable

import jsonpatch

logger = getLogger(__name__)


def patch(base: dict, patches: Iterable[dict]):
    return jsonpatch.JsonPatch(patches).apply(base)
