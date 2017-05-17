from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Hashable,
    List,
    NamedTuple,
    Set,
    Type,
    TypeVar,
    Union,
)
from mypy_extensions import Arg
from collections import defaultdict
from ..types import Path

ValueType = TypeVar('ValueType')
Forms = TypeVar('Forms', bound=Hashable)


FillerType = TypeVar('FillerType', bound=Any)


class Filler:
    def __init__(self, form, path, original_value):
        self.form = form
        self.path = path
        self.original_value = original_value

    def __hash__(self):
        return hash((self.form, self.path))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return '<Filler(form={} path={}) original_value={}) [hash {}]>'.format(
            self.form, self.path, self.original_value, hash(self))


class ComplexFiller(Filler):
    def __hash__(self):
        return hash((self.form, self.path, self.original_value))


class BaseHandler(Generic[ValueType, FillerType, Forms]):

    handler_map: Any
    filler: Type[FillerType]
    path_map: Dict[Path, Dict[Forms, Set[FillerType]]]

    simplify_value: Callable[[Path, Any], Any]
    realify_value: Callable[[Path, Any], Any]

    def __init__(self):
        self.path_map = defaultdict(lambda: defaultdict(set))

    def create_filler(self, form: Forms, path: Path, value: ValueType) \
            -> FillerType:
        filler = self.filler(form, path, value)
        self.path_map[path][form].add(filler)
        return filler

    def simplify(self, path: Path, value: ValueType) -> FillerType:
        raise NotImplementedError()

    def realify(self, path: Path, filler: FillerType) -> ValueType:
        return next(iter(self.path_map[path][filler.form])).original_value
