from typing import List, Union, NamedTuple
from collections import defaultdict
from frozendict import frozendict
from .types import Permutations, HandlerDict

Number = Union[int, float]


class CountedValues:

    values: set
    count: int

    def __init__(self):
        self.values = set()
        self.count = 0


def number_handler(
    permutations: Permutations, values: List[Number]
) -> Permutations:
    for value in values:
        if value > 0:
            permutations.add(1)
            permutations.add(1.5)
        elif value < 0:
            permutations.add(-1)
            permutations.add(-1.5)
        elif value == 0:
            permutations.add(0)

    return permutations


def string_handler(
    permutations: Permutations, values: List[str]
) -> Permutations:
    for value in values:
        if len(value) > 0:
            permutations.add('foo')
        elif len(value) == 0:
            permutations.add('')

    return permutations


def dict_handler(
    permutations: Permutations, values: List[dict]
) -> Permutations:
    from .handling import handle_values  # noqa
    key_values_map = defaultdict(CountedValues)

    for value in values:
        for key, value in value.items():
            key_values_map[key].values.add(value)
            key_values_map[key].count += 1

    default_dict = {}
    other_keys = []
    for key, counted_values in key_values_map.items():
        if counted_values.count > (len(values) / 2):
            default_dict[key] = handle_values(counted_values.values)
        else:
            other_keys.append((key, counted_values))

    frozen_default = frozendict(default_dict)

    for key, counted_values in key_values_map.items():
        permutations.add(frozen_default)

        for value in handle_values(counted_values.values):
            permutation = default_dict.copy()
            permutation[key] = value
            permutations.add(frozendict(permutation))

    return permutations


handler_map: HandlerDict = {
    (int, float): number_handler,
    (str,): string_handler,
    (dict,): dict_handler,
}
