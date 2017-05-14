from typing import Any, Dict, Callable, TypeVar, Union

Number = Union[int, float]


T = TypeVar('T')
TypeHandler = Callable[[T], T]
HandlerDict = Dict[Any, TypeHandler]
