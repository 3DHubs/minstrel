from typing import Any, Dict, Callable, List, TypeVar
from .weighted_set import WeightedSet


T = TypeVar('T')
Permutations = WeightedSet
TypeHandler = Callable[[List[T]], Permutations]
HandlerDict = Dict[Any, TypeHandler]
