from ..types import Path
from .base_handler import BaseHandler


class NoneHandler(BaseHandler[None, None, None]):

    def simplify(self, path: Path, value: None) -> None:
        return None

    def realify(self, path: Path, value: None) -> None:
        return None
