from ..types import Path
from .base_handler import BaseHandler


class BoolHandler(BaseHandler[bool, bool, bool]):

    def simplify(self, path: Path, value: bool) -> bool:
        return value

    def realify(self, path: Path, value: bool) -> bool:
        return value
